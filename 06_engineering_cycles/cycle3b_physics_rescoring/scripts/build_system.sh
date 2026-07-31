#!/bin/bash
# Cycle 3b Stage 1 - build ONE control system end-to-end and benchmark it.
#
# Pipeline: extract co-folded complex -> (optional) install D-Ala2 by mirroring
#   -> orient in membrane normal (memembed) -> pack POPC bilayer + water + 0.15 M NaCl
#   -> parametrize ff14SB/Lipid21 -> minimise -> CHIRALITY GATE -> equilibrate
#   -> CHIRALITY GATE -> short production benchmark to measure ns/day.
#
# Usage: build_system.sh <tag> <dres|none>
#   tag  : e.g. c3b_dtII_DOR   (expects out_<tag>/ from the boltz run)
#   dres : residue index in the PEPTIDE chain to convert to D, or 'none'
set -euo pipefail

TAG="${1:?usage: build_system.sh <tag> [dres|none|auto]}"
# DRES defaults to "auto": read the D-residue position from the design table rather
# than from this argument. Passing an explicit value is still allowed but is CROSS-
# CHECKED against the table and must agree -- see peptide_spec.sh for why (a silent
# "none" default built the all-L analog of deltorphin II on 2026-07-30 and disabled
# the chirality gate that would have caught it).
DRES="${2:-auto}"
# Amidation is ON by default: the free acid is the wrong species for every
# peptide in this panel. Pass --no-amidate only for a deliberate control.
AMIDATE=yes
for a in "$@"; do [ "$a" = "--no-amidate" ] && AMIDATE=no; done

W=/data/users/kzanaj/boltz_dock/cycle3b
E=/data/users/kzanaj/envs/gmxmmpbsa
GMX=/data/users/kzanaj/envs/gmxcuda/bin/gmx
export AMBERHOME=$E
export PATH=$E/bin:$PATH
PY=$E/bin/python

# SYSROOT lets a pre-flight sweep (STAGE=orient) write into an isolated tree so it
# cannot touch systems/ or disturb a build already in flight. Scripts, envs and the
# design table still resolve under $W -- only the OUTPUT location moves.
SYSROOT="${SYSROOT:-$W/systems}"
SYS=$SYSROOT/$TAG
mkdir -p "$SYS"; cd "$SYS"

# ---- STAGE split: keep the CPU-bound hour off the contended GPU node ----------
# pgpu is a SINGLE node with gpu:2 and is usually saturated, so a build that asks
# for a GPU up front waits for the whole packing hour it does not need. Only the
# minimisation (stage 6) actually uses the GPU. Split:
#   STAGE=cpu  stages 1-5 on pshort_el8 (no GPU, 5 idle nodes, 2 h limit) -> BUILD_CPU_OK
#   STAGE=gpu  stage 6 only, on pgpu --gres=gpu:1 (minutes)              -> BUILD_OK
#   STAGE=all  everything in one job (default; unchanged behaviour)
STAGE="${STAGE:-all}"
# STAGE=orient is a PRE-FLIGHT: run stages 1-3b (pose -> chirality -> amide ->
# memembed -> tilt fix/assert) and stop before packing. Costs ~1 min of CPU instead of
# ~40 min, and exercises the IDENTICAL code path the real build uses, so a sweep across
# the panel cannot drift from production behaviour.
case "$STAGE" in all|cpu|gpu|orient) ;; *) echo "FAIL: STAGE must be all|cpu|gpu|orient (got '$STAGE')"; exit 1 ;; esac
echo "stage: $STAGE"

# ---- resolve peptide chemistry from the design table, not the command line ------
. $W/scripts/peptide_spec.sh
load_peptide_spec "$TAG" || exit 1
if [ "$DRES" = "auto" ]; then
  DRES="$SPEC_DRES"
elif [ "$DRES" != "$SPEC_DRES" ]; then
  echo "FAIL: dres='$DRES' on the command line contradicts the design table"
  echo "      ($TAG requires dres=$SPEC_DRES). Fix the caller or the table -- not this check."
  exit 1
fi
echo "  D-residue: $DRES | C-terminus: $SPEC_AMIDE"

# Minimisation, factored out so the split and combined paths run IDENTICAL code.
do_minimise() {
  $GMX grompp -f $W/scripts/min.mdp -c system.gro -p system.top -o min.tpr -n index.ndx -maxwarn 5 >grompp_min.log 2>&1 \
    || { echo "FAIL: grompp min"; tail -25 grompp_min.log; exit 1; }
  $GMX mdrun -deffnm min -nb gpu >md_min.log 2>&1 \
    || { echo "FAIL: mdrun min"; tail -20 md_min.log; exit 1; }
  echo "min: $(grep -E 'Potential Energy|Maximum force' md_min.log | tail -2 | tr '\n' ' ')"
  [ -f min.gro ] || { echo "FAIL: min.gro not produced"; exit 1; }

  # Interface gate. Potential energy above is a whole-system number over ~155k atoms of
  # lipid and water -- a single 1.7 A clash at the receptor-peptide interface is far
  # inside its noise, so it cannot tell us whether minimisation did the one job we need
  # it to do here. Measure the interface directly against the pre-min baseline.
  $PY $W/scripts/contacts.py check system.top min.gro pepmeta.txt contacts_pre.txt \
    || { echo "FAIL: receptor-peptide clash survived minimisation"; exit 1; }
}

# STAGE=gpu resumes from the CPU stage's output: verify it, minimise, done.
if [ "$STAGE" = "gpu" ]; then
  # contacts_pre.txt included: do_minimise's post-min gate compares against it, so a
  # missing baseline must fail HERE with a clear cause, not 20 min later inside the gate.
  for f in system.top system.gro index.ndx pepmeta.txt contacts_pre.txt; do
    [ -f "$f" ] || { echo "FAIL: STAGE=gpu needs $f from the CPU stage; not found in $SYS"; exit 1; }
  done
  echo "resuming from CPU stage output in $SYS"
  do_minimise
  echo "BUILD_OK $TAG"
  exit 0
fi

# --resume: skip straight to the post-packing steps if a parametrized topology
# already exists. Packing costs ~30 min of CPU per system and the topology on disk
# is already the correct (amidated) species, so there is nothing to gain by redoing
# it after a downstream scripting failure.
RESUME=no
for a in "$@"; do [ "$a" = "--resume" ] && RESUME=yes; done
if [ "$RESUME" = "yes" ] && [ -n "$(echo *_lipid.top)" ] && [ -e "$(echo *_lipid.top | cut -d" " -f1)" ]; then
  echo "resuming from existing packed topology in $SYS"
  SKIP_PACK=yes
fi

POSE=$(find $W/out_${TAG} -name "*model_0.pdb" | head -1)
[ -n "$POSE" ] || { echo "FAIL: no pose for $TAG"; exit 1; }
echo "pose: $POSE"

# ---- 1. split complex; strip Boltz artefacts -------------------------------
grep "^ATOM" "$POSE" | awk 'substr($0,22,1)=="A"' > rec_raw.pdb
grep "^ATOM" "$POSE" | awk 'substr($0,22,1)=="B"' > pep_raw.pdb
echo "receptor atoms: $(wc -l < rec_raw.pdb) | peptide atoms: $(wc -l < pep_raw.pdb)"

# ---- 2. install D-residue by geometric mirroring ---------------------------
if [ "$DRES" != "none" ]; then
  $PY $W/scripts/chirality.py invert pep_raw.pdb "$DRES" - pep_D.pdb
  $PY $W/scripts/chirality.py assert pep_D.pdb "$DRES" || { echo "FAIL: inversion did not take"; exit 1; }
  mv pep_D.pdb pep_chir.pdb
else
  cp pep_raw.pdb pep_chir.pdb
fi

# ---- 2b. install the C-terminal primary amide ------------------------------
# MANDATORY, and the reason Cycle 3b exists. The bioactive species of every control
# and of our payload is C-terminally AMIDATED (PAM recognises the terminal Gly).
# Boltz-2 cannot represent an amide, and packmol-memgen --parametrize just runs
# tleap, which defaults a bare C-terminus to the CHARGED FREE ACID. Skipping this
# step silently simulates the wrong chemical species -- an extra -1 charge sitting
# exactly on the pharmacophore that sets delta-selectivity -- and the run still
# completes looking healthy. Verified: NHE gives net charge 0.000 vs -1 free acid,
# tleap Errors=0 Warnings=0, and the D-centre survives (V = -2.504).
if [ "$AMIDATE" = "yes" ]; then
  $PY $W/scripts/amidate.py pep_chir.pdb pep_amide.pdb || { echo "FAIL: amidation"; exit 1; }
  $PY $W/scripts/amidate.py pep_amide.pdb /dev/null --check \
    || { echo "FAIL: amide cap not present after amidation"; exit 1; }
  mv pep_amide.pdb pep_chir.pdb
  echo "  C-terminus: primary amide (NHE)"
else
  echo "  C-terminus: FREE ACID (--no-amidate given)"
fi

# ---- 3. orient the COMPLEX along the membrane normal -----------------------
# IMPORTANT: orient receptor+peptide together as one rigid body. Orienting the
# receptor alone and re-appending the peptide would destroy the docked pose,
# because memembed applies a rotation+translation that the peptide must share.
cat rec_raw.pdb > complex_raw.pdb
echo "TER" >> complex_raw.pdb
cat pep_chir.pdb >> complex_raw.pdb
echo "END" >> complex_raw.pdb

# NOTE ON FILENAMES: packmol-memgen builds its MEMEMBED output name as
#   pdb[:-4] + n_ter + "_EMBED.pdb"   (main.py:774)  with n_ter defaulting to "in".
# An input whose name ENDS IN "_in" (e.g. complex_in.pdb) becomes "complex_inin_EMBED.pdb", which
# collides with the path its shutil.move writes, and memgen dies with
# FileNotFoundError. The build input is named complex_start.pdb to avoid this.
ORIENT=""
if command -v memembed >/dev/null 2>&1; then
  if memembed -o complex_oriented.pdb complex_raw.pdb >memembed.log 2>&1; then
    # Verify the peptide survived: atom count preserved and the peptide is still
    # in contact with the receptor. A silent chain drop is the failure mode here.
    if $PY - <<PYEOF
import sys, numpy as np
# MEMEMBED appends DUM pseudo-atoms marking the two bilayer planes (~4400 of them).
# Strip those, then verify the real solute was moved as ONE RIGID BODY.
def rd(f, drop_dum=False):
    A=[l for l in open(f) if l.startswith(("ATOM","HETATM"))]
    if drop_dum: A=[l for l in A if l[17:20].strip()!="DUM"]
    xyz=lambda l: np.array([float(l[30:38]),float(l[38:46]),float(l[46:54])])
    return A, {c: np.array([xyz(l) for l in A if l[21]==c]) for c in {l[21] for l in A}}
Ai,ci = rd("complex_raw.pdb")
Ao,co = rd("complex_oriented.pdb", drop_dum=True)
ndum = sum(1 for l in open("complex_oriented.pdb")
           if l.startswith(("ATOM","HETATM")) and l[17:20].strip()=="DUM")
print(f"  memembed: {ndum} DUM bilayer-marker atoms stripped")
if len(Ai)!=len(Ao):
    print(f"  REJECT: solute atom count changed {len(Ai)}->{len(Ao)}"); sys.exit(1)
if set(ci)!=set(co):
    print(f"  REJECT: chain set changed {sorted(ci)}->{sorted(co)}"); sys.exit(1)
def mind(d):
    a,b=d["A"],d["B"]
    return float(np.sqrt(((a[:,None,:]-b[None,:,:])**2).sum(-1)).min())
d0,d1 = mind(ci), mind(co)
# a rigid-body move preserves ALL internal distances, so also check the radius of gyration
rg=lambda d: float(np.sqrt(((np.vstack(list(d.values()))-np.vstack(list(d.values())).mean(0))**2).sum(1).mean()))
g0,g1 = rg(ci), rg(co)
print(f"  min receptor-peptide dist: {d0:.2f} -> {d1:.2f} A | Rg: {g0:.2f} -> {g1:.2f} A")
ok = abs(d0-d1) < 0.05 and abs(g0-g1) < 0.05
if not ok: print("  REJECT: pose was NOT moved as a rigid body")
sys.exit(0 if ok else 1)
PYEOF
    then grep -vE "^(ATOM|HETATM).{9}DUM" complex_oriented.pdb > complex_start.pdb; ORIENT="--preoriented"
    else echo "  memembed output rejected; letting memgen orient"; cp complex_raw.pdb complex_start.pdb
    fi
  else
    echo "  memembed failed; letting memgen orient"; cp complex_raw.pdb complex_start.pdb
  fi
else
  cp complex_raw.pdb complex_start.pdb
fi
echo "orientation: ${ORIENT:-memgen internal}"

# ---- 3b. correct, then assert, the membrane-normal alignment -----------------
# MANDATORY after memembed/memgen: a tilted bundle will rotate during equilibration,
# so production would measure reorientation, not binding. memembed occasionally fails
# silently while logging success -- observed 19.65 deg on c3b_dtII_DOR while reporting
# a clean exit and "--preoriented". Tilt is orientation-only (sign-agnostic); upright
# and inverted are both acceptable.
#
# Gate the file that is actually PACKED (complex_start.pdb, DUM stripped), NOT
# complex_oriented.pdb. The tilt value is identical either way because DUM atoms are
# not CAs and never enter the measurement, but asserting on a file that packing does
# not consume is how a gate silently goes stale.
#
# tilt.py fix rigid-body rotates EVERY atom about the receptor CA centroid, so the
# docked peptide pose is carried along; it asserts Rg and an interatomic distance are
# preserved, then re-measures from the written file. Rotating about the centroid also
# leaves the solute's z-centre where memembed put it, which is what packmol-memgen
# --preoriented uses to place the bilayer.
if [ -n "$ORIENT" ]; then
  echo "  pre-fix tilt:"
  $PY $W/scripts/tilt.py measure complex_start.pdb --rec-chain A
  $PY $W/scripts/tilt.py fix complex_start.pdb complex_upright.pdb --rec-chain A \
    || { echo "FAIL: tilt fix could not re-orient the complex"; exit 1; }
  mv complex_upright.pdb complex_start.pdb
  # Independent re-assert on the moved file: fix already self-checks, but the gate
  # must hold on the exact bytes that go into packing.
  $PY $W/scripts/tilt.py assert complex_start.pdb --max-deg 10 --rec-chain A \
    || { echo "FAIL: post-fix tilt gate"; exit 1; }
  # The rigid-body rotation must not have broken the docked pose.
  $PY - <<'PYEOF' || { echo "FAIL: pose not preserved through tilt fix"; exit 1; }
import sys, numpy as np
def rd(f):
    A=[l for l in open(f) if l.startswith(("ATOM","HETATM")) and l[17:20].strip()!="DUM"]
    xyz=lambda l: np.array([float(l[30:38]),float(l[38:46]),float(l[46:54])])
    return {c: np.array([xyz(l) for l in A if l[21]==c]) for c in {l[21] for l in A}}
def mind(d):
    a,b=d["A"],d["B"]
    return float(np.sqrt(((a[:,None,:]-b[None,:,:])**2).sum(-1)).min())
o,n = rd("complex_oriented.pdb"), rd("complex_start.pdb")
if set(o)!=set(n): print(f"  REJECT: chains changed {sorted(o)}->{sorted(n)}"); sys.exit(1)
d0,d1 = mind(o), mind(n)
print(f"  pose through fix: min rec-pep dist {d0:.2f} -> {d1:.2f} A")
sys.exit(0 if abs(d0-d1) < 0.05 else 1)
PYEOF
fi

# STAGE=orient stops HERE -- everything chemistry- and orientation-related has run and
# been gated; packing adds 40 min of CPU and tests nothing new about the input pose.
# Distinct marker (not BUILD_OK/BUILD_CPU_OK) so a pre-flight can never be mistaken for
# a usable system: there is no topology, no min.gro, nothing runnable in this directory.
if [ "$STAGE" = "orient" ]; then
  # Report the D-centre only where one is expected; for all-L tags (em1) there is no
  # residue index to assert on and calling chirality.py with 'none' is meaningless.
  if [ "$DRES" != "none" ]; then
    $PY $W/scripts/chirality.py assert pep_chir.pdb "$DRES" \
      || { echo "FAIL: D-centre absent or inverted at res $DRES"; exit 1; }
  else
    echo "  all-L peptide by design (dres=none); no chirality assertion applicable"
  fi
  echo "ORIENT_OK $TAG"
  exit 0
fi

# ---- 4. pack bilayer ------------------------------------------------------
if [ "${SKIP_PACK:-no}" != "yes" ]; then
packmol-memgen --pdb complex_start.pdb --lipids POPC --ratio 1 \
  --dist 15 --dist_wat 20 --salt --salt_c Na+ --saltcon 0.15 \
  --ffprot ff14SB --ffwat tip3p --parametrize --notprotonate \
  $ORIENT --overwrite --log memgen.log > memgen.out 2>&1 || {
    echo "FAIL: packmol-memgen"; tail -25 memgen.out; exit 1; }
fi

# packmol-memgen --parametrize names its Amber output <input>_lipid.top/.crd, NOT
# .prmtop/.rst7. Globbing only for .prmtop made a SUCCESSFUL build report EXIT=2.
# NOTE: do NOT write this as $(ls A B C | head -1). `ls` exits 2 when ANY operand
# does not exist, and with `set -o pipefail` that 2 propagates out of the command
# substitution, so `set -e` kills the script with EXIT=2 and NO error message --
# even though the topology is sitting right there. That is the real cause of the
# exit-2 I previously misdiagnosed as a wrong glob pattern: adding *_lipid.top to
# the list did not help, because *.prmtop still failed to match. Use bash globbing,
# which simply yields nothing.
pick () { local f; for f in "$@"; do [ -e "$f" ] && { printf '%s' "$f"; return 0; }; done; return 0; }
shopt -s nullglob
PRM=$(pick *_lipid.top *.prmtop *.parm7)
CRD=$(pick *_lipid.crd *.rst7 *.inpcrd)
shopt -u nullglob
[ -n "$PRM" ] && [ -n "$CRD" ] || { echo "FAIL: no topology produced"; tail -25 memgen.out; exit 1; }
echo "topology: $PRM | coords: $CRD"
# Assert the amide survived into the FINAL topology. This is the last point at
# which the wrong-species error is catchable; after this the trajectory looks fine.
if [ "$AMIDATE" = "yes" ]; then
  $PY - "$PRM" <<'PYEOF'
import sys, parmed as pmd
p = pmd.load_file(sys.argv[1])
names = [r.name for r in p.residues]
if "NHE" not in names:
    sys.exit("FAIL: no NHE in the final topology - the system is a FREE ACID, "
             "which is the wrong chemical species for this panel")
print(f"  amide verified in final topology: {names.count('NHE')} NHE residue(s)")
PYEOF
  [ $? -eq 0 ] || exit 1
fi
# tleap emits ~2 warnings per lipid because Lipid21 SPLITS each POPC into PC/OL/PA
# residues by design. Warnings are therefore not a failure signal here; Errors are.
if [ -f leap_.log ]; then
  LE=$(grep -oE "Errors = [0-9]+" leap_.log | tail -1 | grep -oE "[0-9]+")
  LW=$(grep -oE "Warnings = [0-9]+" leap_.log | tail -1 | grep -oE "[0-9]+")
  echo "tleap: Errors=${LE:-?} Warnings=${LW:-?} (lipid-splitting warnings are expected)"
  [ "${LE:-1}" = "0" ] || { echo "FAIL: tleap reported errors"; grep -iE "error|fatal" leap_.log | head -10; exit 1; }
fi
$PY -c "
import parmed as pmd
p = pmd.load_file('$PRM', xyz='$CRD')
print(f'SYSTEM: {len(p.atoms)} atoms, {len(p.residues)} residues')
import collections
c = collections.Counter(r.name for r in p.residues)
print('  lipids POPC-units:', sum(v for k,v in c.items() if k in ('PC','OL','PA')))
print('  waters:', c.get('WAT',0), '| Na+:', c.get('Na+',0), '| Cl-:', c.get('Cl-',0))
print(f'  box: {p.box}')
p.save('system.top', overwrite=True); p.save('system.gro', overwrite=True)
print('  wrote GROMACS system.top + system.gro')
"

# ---- 5. generate index groups and peptide metadata ---------------------------
# MANDATORY: run_prod.sh consumes index.ndx, pepmeta.txt, and min.gro. Without this,
# every production replicate fails at the pre-flight check. This stage locates the
# peptide, writes thermostat groups, and emits metadata (first/last residue, sequence).
$PY $W/scripts/make_index.py system.top system.gro index.ndx pepmeta.txt \
  || { echo "FAIL: make_index.py"; exit 1; }
[ -f index.ndx ] && [ -f pepmeta.txt ] || { echo "FAIL: index/peptide metadata not produced"; exit 1; }

# Baseline the receptor-peptide interface BEFORE minimisation, so the post-min gate has
# something to compare against. Written by the CPU stage; consumed by the GPU stage.
$PY $W/scripts/contacts.py record system.top system.gro pepmeta.txt contacts_pre.txt \
  || { echo "FAIL: could not baseline receptor-peptide contacts"; exit 1; }

# ---- 6. minimize to get min.gro (input for first equilibration) ---------------
# STAGE=cpu stops HERE: minimisation is the only GPU work, so it is handed to a
# separate short pgpu job. Emitting a DISTINCT marker (BUILD_CPU_OK, not BUILD_OK)
# matters -- BUILD_OK asserts min.gro exists, and run_prod.sh pre-flights on it.
if [ "$STAGE" = "cpu" ]; then
  for f in system.top system.gro index.ndx pepmeta.txt contacts_pre.txt; do
    [ -f "$f" ] || { echo "FAIL: CPU stage did not produce $f"; exit 1; }
  done
  # Record the chemistry this system was ACTUALLY built with, so the production
  # stage can verify the coordinates it inherits match the peptide it thinks it is
  # running. Without this, a mismatched build/run pair is undetectable downstream.
  printf 'BUILT_DRES=%s\nBUILT_AMIDE=%s\n' "$DRES" "$SPEC_AMIDE" > chem.txt
  echo "  recorded chem.txt: dres=$DRES amide=$SPEC_AMIDE"
  echo "BUILD_CPU_OK $TAG"
  echo "next: STAGE=gpu build_system.sh $TAG (needs --gres=gpu:1)"
  exit 0
fi

do_minimise

echo "BUILD_OK $TAG"
