#!/usr/bin/env python3
"""Write a rescoring topology containing ONLY the MM-GBSA solute (receptor + ligand).

WHY THIS EXISTS
  These are POPC-embedded GPCRs. gmx_MMPBSA's cleantop() strips water and ions from
  [ molecules ] but keeps everything else -- so the 274 lipid copies stay in the
  topology while being absent from mmgbsa.ndx, and it aborts with
    "The complex index has fewer atoms than the topology."

WHY REMOVING THE MEMBRANE IS DEFENSIBLE (not a workaround)
  Implicit-solvent GB has no lipid phase; keeping the bilayer would have it treated as
  water regardless. The measured justification is that the peptide never touches the
  bilayer: over the rescoring window the ligand-to-MEMB minimum distance stays >= 0.488 nm
  with ZERO contacts within 0.4 nm in 1001/1001 frames (see mindist_ligand_memb.txt in
  each run directory). The receptor's lipid-facing surface is therefore essentially
  identical in the complex and in the free receptor, so its (wrong) GB solvation term
  cancels in dG = G_com - G_rec - G_lig, and cancels again in the ddG comparisons this
  pipeline actually consumes. Absolute values remain non-affinities, as the design states.

  This does NOT hold for a ligand that contacts lipid. rescore.sh re-measures the
  distance per run and refuses to proceed if contacts appear.

Usage: strip_membrane_top.py <in.top> <mmgbsa.ndx> <out.top>
"""
import re, sys

def main():
    intop, ndxf, outtop = sys.argv[1:4]

    # --- atom count per moleculetype -----------------------------------------
    counts, order = {}, []
    name, sec, seen_name = None, None, False
    for line in open(intop):
        s = line.split(';', 1)[0].strip()
        m = re.match(r'^\[\s*(\S+)\s*\]$', s)
        if m:
            sec = m.group(1).lower()
            if sec == 'moleculetype':
                name, seen_name = None, False
            continue
        if not s:
            continue
        if sec == 'moleculetype' and not seen_name:
            name, seen_name = s.split()[0], True
            counts.setdefault(name, 0); order.append(name)
        elif sec == 'atoms' and name and re.match(r'^\d+\s', s):
            counts[name] += 1
    if not counts:
        sys.exit("FAIL: parsed no moleculetypes from %s" % intop)

    # --- [ molecules ] in order ----------------------------------------------
    mols, insec = [], False
    for line in open(intop):
        s = line.split(';', 1)[0].strip()
        if re.match(r'^\[\s*molecules\s*\]$', s, re.I):
            insec = True; continue
        if insec:
            if s.startswith('['): break
            if not s: continue
            f = s.split()
            if len(f) >= 2:
                mols.append((f[0], int(f[1])))
    if not mols:
        sys.exit("FAIL: no [ molecules ] section in %s" % intop)

    # --- solute atom set from the index --------------------------------------
    solute, cur = set(), None
    for line in open(ndxf):
        s = line.strip()
        m = re.match(r'^\[\s*(.+?)\s*\]$', s)
        if m:
            cur = m.group(1).lower(); continue
        if cur in ('receptor', 'ligand'):
            solute.update(int(x) for x in s.split())
    if not solute:
        sys.exit("FAIL: no Receptor/Ligand atoms found in %s" % ndxf)

    # --- decide, per molecule instance, whether it is solute ----------------
    keep, at, kept_atoms = [], 1, 0
    for mname, n in mols:
        per = counts.get(mname)
        if per is None:
            sys.exit("FAIL: [ molecules ] names %r but no moleculetype defines it" % mname)
        k = 0
        for _ in range(n):
            rng = range(at, at + per)
            hit = sum(1 for i in rng if i in solute)
            if hit == per:
                k += 1
            elif hit:
                sys.exit("FAIL: molecule %s spanning atoms %d-%d is only PARTIALLY in the "
                         "solute index (%d/%d). Refusing to guess." % (mname, at, at+per-1, hit, per))
            at += per
        if k:
            keep.append((mname, k)); kept_atoms += k * per

    # --- the kept set must be exactly the solute, contiguous from atom 1 -----
    if kept_atoms != len(solute):
        sys.exit("FAIL: kept %d atoms but the solute index has %d" % (kept_atoms, len(solute)))
    if set(range(1, kept_atoms + 1)) != solute:
        sys.exit("FAIL: solute atoms are not contiguous starting at 1 (min=%d max=%d n=%d). "
                 "A reduced topology would misalign with the index; refusing."
                 % (min(solute), max(solute), len(solute)))

    # --- emit -----------------------------------------------------------------
    out, insec = [], False
    for line in open(intop):
        if re.match(r'^\s*\[\s*molecules\s*\]\s*$', line, re.I):
            out.append(line); insec = True
            out.append('; reduced by strip_membrane_top.py -- solute only (see module docstring)\n')
            out.append('; Compound        #mols\n')
            for mname, k in keep:
                out.append('%-16s %d\n' % (mname, k))
            continue
        if insec:
            s = line.split(';', 1)[0].strip()
            if s.startswith('['):
                insec = False
            else:
                continue
        out.append(line)
    open(outtop, 'w').writelines(out)

    print("  reduced topology: %s" % outtop)
    print("  kept: %s  = %d atoms (solute index has %d)"
          % (", ".join("%s x%d" % kv for kv in keep), kept_atoms, len(solute)))
    dropped = [(m, n) for m, n in mols if m not in dict(keep)]
    print("  dropped: %s" % (", ".join("%s x%d" % kv for kv in dropped) or "(nothing)"))

if __name__ == "__main__":
    main()
