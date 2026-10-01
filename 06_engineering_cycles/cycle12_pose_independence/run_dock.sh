#!/bin/bash
# Cycle 12: independent ADCP pose for YGGFEVVG in DOR and MOR.
#
# Design notes that matter for interpreting the result:
#  * the docking box is defined from RECEPTOR residues, never from the co-folded
#    peptide position -- centring on the pose under test would partly build in the
#    agreement we are trying to measure.
#  * the receptor conformation comes from the co-fold complex, so the pocket is
#    already shaped by the predicted peptide (induced fit). That biases TOWARD
#    reproducing the co-folded pose, which makes a disagreement strong evidence
#    and an agreement only weak evidence. Stated, not hidden.
#  * alternate-location atoms are stripped before prepare_receptor: it misaligns
#    the residue-name column when adding H to altloc residues, emitting 80-char
#    lines that prody rejects with "invalid or missing coordinate(s)".
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/env.sh"
POSES="$HERE/poses"
WORK="$HERE/dock"; mkdir -p "$WORK"

# canonical orthosteric anchor Asp3.32 -- verified below, not assumed
declare -A D332=( [DOR]=128 [MOR]=147 )
declare -A POCKET=( [DOR]="128,129,132,274,277,308" [MOR]="147,148,151,293,296,327" )

for R in DOR MOR; do
  SRC="$POSES/cofold_engPENK_${R}.pdb"
  [ -f "$SRC" ] || { echo "[$R] MISSING $SRC"; continue; }
  echo "######## $R"

  # --- split receptor (chain A) and the 8-residue payload (chain B) ---
  awk '/^ATOM/ && substr($0,22,1)=="A" {
        alt=substr($0,17,1); if (alt!=" " && alt!="A") next;
        print substr($0,1,16) " " substr($0,18) }' "$SRC" > "$WORK/${R}_rec.pdb"
  echo "END" >> "$WORK/${R}_rec.pdb"
  awk '/^ATOM/ && substr($0,22,1)=="B"' "$SRC" > "$WORK/${R}_pep_cofold.pdb"
  nrec=$(awk '/^ATOM/{r=substr($0,23,4)+0; if(!(r in s)){s[r]=1;n++}} END{print n+0}' "$WORK/${R}_rec.pdb")
  npep=$(awk '/^ATOM/{r=substr($0,23,4)+0; if(!(r in s)){s[r]=1;n++}} END{print n+0}' "$WORK/${R}_pep_cofold.pdb")
  echo "  receptor $nrec residues | co-folded peptide $npep residues"
  [ "$npep" -eq 8 ] || { echo "  ABORT: payload is not 8 residues"; continue; }

  # --- verify the anchor residue is where we think, do not assume ---
  anum=${D332[$R]}
  aname=$(awk -v A="$anum" '/^ATOM/ && substr($0,23,4)+0==A {print substr($0,18,3); exit}' "$WORK/${R}_rec.pdb")
  echo "  Asp3.32 check: residue $anum is '$aname'"
  [ "$aname" = "ASP" ] || { echo "  ABORT: residue $anum is not ASP; numbering differs, box would be wrong"; continue; }

  # --- build the selection string with real residue names ---
  SEL="A:"
  for r in ${POCKET[$R]//,/ }; do
    nm=$(awk -v R="$r" '/^ATOM/ && substr($0,23,4)+0==R {print substr($0,18,3); exit}' "$WORK/${R}_rec.pdb")
    [ -z "$nm" ] && { echo "  WARN residue $r absent, skipping"; continue; }
    SEL="${SEL}${nm}${r},"
  done
  SEL="${SEL%,}"
  echo "  box selection: $SEL"

  # --- receptor -> pdbqt, asserting the alignment bug did not recur ---
  prepare_receptor -r "$WORK/${R}_rec.pdb" -o "$WORK/${R}_rec.pdbqt" -A hydrogens >"$WORK/${R}_prep.log" 2>&1
  [ -s "$WORK/${R}_rec.pdbqt" ] || { echo "  ABORT: prepare_receptor produced nothing"; tail -3 "$WORK/${R}_prep.log"; continue; }
  nbad=$(awk 'length($0)>79 && /^ATOM/' "$WORK/${R}_rec.pdbqt" | wc -l)
  [ "$nbad" -eq 0 ] || { echo "  ABORT: $nbad malformed PDBQT lines"; continue; }

  # --- target maps ---
  ( cd "$WORK" && agfr -r "${R}_rec.pdbqt" -b residues "$SEL" -P 8.0 -o "${R}_tgt" >"${R}_agfr.log" 2>&1 )
  [ -s "$WORK/${R}_tgt.trg" ] || { echo "  ABORT: no target file"; tail -6 "$WORK/${R}_agfr.log"; continue; }
  echo "  target built: $(stat -c%s "$WORK/${R}_tgt.trg") bytes"

  # --- dock: 50 replicas, lowercase sequence = start from coil ---
  ( cd "$WORK" && adcp -t "${R}_tgt.trg" -s ygGFEVVG -N 50 -n 500000 -c 4 \
        -o "${R}_adcp" -O >"${R}_adcp.log" 2>&1 )
  echo "  ADCP exit $? ; top solutions:"
  ls -1 "$WORK/${R}_adcp"*.pdb 2>/dev/null | head -4 | sed 's|.*/|      |'
  grep -iE "^ *[0-9]+ +-?[0-9]+\.[0-9]+" "$WORK/${R}_adcp.log" 2>/dev/null | head -5 | sed 's/^/      /'
done
echo "ALL DONE"
