"""Classify docking trajectories by which peptide domain contacts the receptor first.

The question (after the 2026 preprint on beta-endorphin at the mu receptor): opioid
peptides carry a 'message' domain that drives signalling and an 'address' domain that
drives receptor selection. Does engagement begin with one or the other, and is one
order more PRODUCTIVE, meaning more likely to end in a native-like pose?

Definitions used here, stated because they are choices and not givens:

  message / address split
      deltorphin  YAFEVVG   message = Y1 a2 F3        address = E4 V5 V6 G7
      engPENK     YGGFEVVG  message = Y1 G2 G3 F4     address = E5 V6 V7 G8
      The split is at the conserved aromatic that ends the message motif, so both
      peptides are divided by the same chemical logic rather than by position index.

  first contact
      The first trajectory frame in which ANY heavy atom of a domain comes within
      CONTACT_A of any receptor heavy atom. If both domains cross in the same frame
      the trajectory is 'simultaneous' and is reported separately rather than being
      forced into one class, because assigning it would invent a distinction the
      frame rate cannot resolve.

  productive
      Final-frame ligand RMSD to the crystal pose below NATIVE_A, computed on CA
      atoms after superposing the RECEPTOR (not the peptide), so the number measures
      whether the peptide found the right place rather than the right shape.

Everything returns per-trajectory rows; no aggregation happens in here, so the gate
arithmetic stays visible in the caller.
"""
import os, re, glob, tarfile
import numpy as np

CONTACT_A = 4.5      # heavy-atom contact, the usual interface criterion
NATIVE_A  = 5.0      # the threshold G1 was scored against, kept identical

# What the two molecules are, used to separate them without trusting chain IDs.
MAX_PEPTIDE_RES  = 25   # opioid peptides are 5 to 8 residues; 25 is generous
MIN_RECEPTOR_RES = 40   # a class A GPCR is ~300; 40 admits small test receptors

MESSAGE = {"YAFEVVG": (1, 3), "YGGFEVVG": (1, 4)}   # inclusive 1-based residue ranges
ADDRESS = {"YAFEVVG": (4, 7), "YGGFEVVG": (5, 8)}


def read_models(path):
    """Yield (model_number, atoms) for a multi-MODEL PDB.

    atoms is a structured array with fields name, resi, chain, xyz. CABS writes
    trajectories as MODEL/ENDMDL blocks; a file with no MODEL records is treated as
    a single frame so the same reader serves both trajectories and final poses.
    """
    cur, num, out = [], 0, []
    with open(path, errors="ignore") as fh:
        for ln in fh:
            if ln.startswith("MODEL"):
                try: num = int(ln.split()[1])
                except Exception: num += 1
                cur = []
            elif ln.startswith("ENDMDL"):
                if cur: out.append((num, _pack(cur)))
                cur = []
            elif ln.startswith(("ATOM  ", "HETATM")):
                cur.append(ln)
    if cur:
        out.append((num or 1, _pack(cur)))
    return out


def _pack(lines):
    rec = np.zeros(len(lines), dtype=[("name", "U4"), ("resi", "i4"),
                                      ("chain", "U1"), ("xyz", "f4", 3)])
    for i, ln in enumerate(lines):
        rec[i] = (ln[12:16].strip(), int(ln[22:26]), ln[21],
                  (float(ln[30:38]), float(ln[38:46]), float(ln[46:54])))
    return rec


def split_chains(atoms, pep_len=None):
    """Separate receptor from peptide. STRICT: raises rather than guessing.

    An earlier version fell back to 'the trailing residue block of the expected
    length' when no chain matched pep_len. On the crystal reference that fallback
    silently returned the last seven RECEPTOR residues as the peptide, because the
    reference peptide is EIGHT residues (deltorphin plus its NH2 amide cap, which is
    modelled as its own residue) while the simulated peptide is seven (CABS cannot
    represent the cap). Every RMSD computed against it was meaningless, and nothing
    in the output looked wrong.

    So: the peptide is the SMALLEST chain, the receptor the largest, and the split is
    accepted only if the two are unambiguous by a wide margin. pep_len, if given, is
    checked and reported but is NOT used to go hunting for a matching block.
    """
    nres = {ch: len(np.unique(atoms["resi"][atoms["chain"] == ch]))
            for ch in np.unique(atoms["chain"])}
    if len(nres) < 2:
        raise ValueError("only one chain present (%s); cannot separate receptor from peptide"
                         % nres)
    order = sorted(nres.items(), key=lambda kv: kv[1])
    small, large = order[0], order[-1]
    # The criterion states what the two molecules ARE rather than imposing an
    # arbitrary size ratio: a GPCR is a few hundred residues, an opioid peptide is
    # under twenty. A ratio rule rejected legitimate small test cases.
    if small[1] > MAX_PEPTIDE_RES or large[1] < MIN_RECEPTOR_RES:
        raise ValueError("chains %s do not look like receptor plus peptide "
                         "(peptide must be <=%d residues, receptor >=%d)"
                         % (nres, MAX_PEPTIDE_RES, MIN_RECEPTOR_RES))
    m = atoms["chain"] == small[0]
    rec, pep = atoms[~m], atoms[m]
    n_res = len(np.unique(pep["resi"]))
    if pep_len is not None and n_res != pep_len:
        raise PeptideLengthMismatch(n_res, pep_len, small[0])
    return rec, pep


class PeptideLengthMismatch(ValueError):
    """Raised when the peptide chain is not the expected length.

    Carries the observed length so a caller that knows WHY they differ (an amide cap
    present in a crystal structure and absent from a coarse-grained model) can handle
    it deliberately instead of a fallback papering over it.
    """
    def __init__(self, found, expected, chain):
        self.found, self.expected, self.chain = found, expected, chain
        super().__init__("peptide chain %s has %d residues, expected %d"
                         % (chain, found, expected))


def min_dist(a, b):
    if len(a) == 0 or len(b) == 0:
        return np.inf
    d = np.linalg.norm(a["xyz"][:, None, :] - b["xyz"][None, :, :], axis=-1)
    return float(d.min())


def classify_trajectory(path, peptide, ref_rec=None, ref_pep=None, stride=1):
    """Engagement class plus the BEST pose the trajectory ever reaches.

    Productivity is the MINIMUM peptide RMSD over all frames, not the RMSD of the last
    frame. The last frame is the wrong quantity: CABS runs replica-exchange Monte
    Carlo and derives its reported poses by CLUSTERING the trajectory, so a replica's
    final frame is simply wherever that replica happened to be when sampling stopped,
    frequently a high-temperature replica far from any bound state. Scoring final
    frames gave 28 to 46 A for every one of forty trajectories while the clustered
    models from the same run reached 3.41 A, which is how the error announced itself.
    """
    pep_len = len(peptide)
    mlo, mhi = MESSAGE[peptide]
    alo, ahi = ADDRESS[peptide]
    frames = read_models(path)
    if not frames:
        return None

    first_msg = first_adr = None
    best_rmsd, best_frame = np.inf, None
    for k, (num, atoms) in enumerate(frames):
        if stride > 1 and k % stride and first_msg is not None and first_adr is not None:
            continue
        rec, pep = split_chains(atoms, pep_len)
        base = pep["resi"].min() - 1                       # map to 1-based peptide index
        idx = pep["resi"] - base
        msg = pep[(idx >= mlo) & (idx <= mhi)]
        adr = pep[(idx >= alo) & (idx <= ahi)]
        if first_msg is None and min_dist(msg, rec) <= CONTACT_A:
            first_msg = k
        if first_adr is None and min_dist(adr, rec) <= CONTACT_A:
            first_adr = k
        if ref_rec is not None:
            r = ligand_rmsd(atoms, pep_len, ref_rec, ref_pep)
            if r == r and r < best_rmsd:
                best_rmsd, best_frame = r, k

    if first_msg is None and first_adr is None:
        cls = "no_contact"
    elif first_adr is None:
        cls = "message_first"
    elif first_msg is None:
        cls = "address_first"
    elif first_msg < first_adr:
        cls = "message_first"
    elif first_adr < first_msg:
        cls = "address_first"
    else:
        cls = "simultaneous"

    return {"file": os.path.basename(path), "frames": len(frames), "class": cls,
            "first_message_frame": first_msg, "first_address_frame": first_adr,
            "best_rmsd": (best_rmsd if best_rmsd < np.inf else np.nan),
            "best_rmsd_frame": best_frame}


def _ca(atoms):
    return atoms[atoms["name"] == "CA"]


def kabsch(P, Q):
    """Rotation aligning P onto Q, both already centred."""
    V, S, Wt = np.linalg.svd(P.T @ Q)
    d = np.sign(np.linalg.det(V @ Wt))
    D = np.diag([1.0, 1.0, d])
    return V @ D @ Wt


def ligand_rmsd(atoms, pep_len, ref_rec, ref_pep):
    """Peptide CA RMSD after superposing the RECEPTOR onto the reference receptor.

    Receptor-frame superposition is the point: it asks whether the peptide sits where
    the crystal puts it, not merely whether it has a similar internal conformation.
    """
    rec, pep = split_chains(atoms, pep_len)
    r_ca, p_ca = _ca(rec), _ca(pep)
    rr_ca, rp_ca = _ca(ref_rec), _ca(ref_pep)
    common = np.intersect1d(r_ca["resi"], rr_ca["resi"])
    if len(common) < 50 or len(p_ca) == 0 or len(rp_ca) == 0:
        return np.nan
    A = r_ca["xyz"][np.isin(r_ca["resi"], common)]
    B = rr_ca["xyz"][np.isin(rr_ca["resi"], common)]
    n = min(len(A), len(B)); A, B = A[:n], B[:n]
    cA, cB = A.mean(0), B.mean(0)
    R = kabsch(A - cA, B - cB)
    moved = (pep["xyz"][pep["name"] == "CA"] - cA) @ R + cB
    m = min(len(moved), len(rp_ca))
    if m == 0:
        return np.nan
    return float(np.sqrt(((moved[:m] - rp_ca["xyz"][:m]) ** 2).sum(axis=1).mean()))


def load_reference(path, pep_len):
    """Load the crystal reference, trimming a terminal cap if the structure has one.

    8F7S models deltorphin as TYR1 DAL2 PHE3 GLU4 VAL5 VAL6 GLY7 NH2, so the chain is
    EIGHT residues while CABS simulates seven (it represents neither the D-alanine
    stereocentre nor the amide cap, both declared deviations). The extra residue is
    dropped explicitly here, with the reason recorded, rather than being absorbed by a
    length-matching fallback.
    """
    atoms = read_models(path)[0][1]
    try:
        rec, pep = split_chains(atoms, pep_len)
    except PeptideLengthMismatch as e:
        if e.found != pep_len + 1:
            raise
        rec, pep = split_chains(atoms, None)
        keep = np.unique(pep["resi"])[:pep_len]            # drop the trailing cap
        pep = pep[np.isin(pep["resi"], keep)]
    return rec, pep


def extract(archive, dest):
    with tarfile.open(archive) as t:
        t.extractall(dest)
    return sorted(glob.glob(os.path.join(dest, "**", "replica_*.pdb"), recursive=True))
