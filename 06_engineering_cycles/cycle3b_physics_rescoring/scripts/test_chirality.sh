#!/usr/bin/env bash
# Self-test for chirality.py. Run before deploying any change to it, because this
# assertion is the ONLY thing that can detect an inverted D-centre: the ff14SB
# topology is enantiomer-blind by construction (no improper term references the
# sp3 alpha-carbon type), so a silent inversion during MD is otherwise invisible.
#
# Ground-truth anchor: the real all-L Boltz-2 pose of deltorphin II gave
# V = +2.504 for residue 2, and after mirroring V = -2.504. So V > 0 is L,
# V < 0 is D, and the magnitude must be preserved by a correct inversion.
set -u
cd "$(dirname "$0")"
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT

cat > "$T/L.pdb" <<'EOF'
ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00  0.00           N
ATOM      2  CA  ALA A   1       1.458   0.000   0.000  1.00  0.00           C
ATOM      3  C   ALA A   1       2.009   1.420   0.000  1.00  0.00           C
ATOM      4  CB  ALA A   1       1.988  -0.773  -1.199  1.00  0.00           C
ATOM      5  N   ALA A   2       5.000   0.000   0.000  1.00  0.00           N
ATOM      6  CA  ALA A   2       6.458   0.000   0.000  1.00  0.00           C
ATOM      7  C   ALA A   2       7.009   1.420   0.000  1.00  0.00           C
ATOM      8  CB  ALA A   2       6.988  -0.773  -1.199  1.00  0.00           C
ATOM      9  N   GLY A   3      10.000   0.000   0.000  1.00  0.00           N
ATOM     10  CA  GLY A   3      11.458   0.000   0.000  1.00  0.00           C
ATOM     11  C   GLY A   3      12.009   1.420   0.000  1.00  0.00           C
EOF

PY=${PY:-python3}
pass=0; fail=0
chk () { local desc="$1" exp="$2"; shift 2
  local out; out=$("$@" 2>&1); local got=$?
  if [ "$got" = "$exp" ]; then pass=$((pass+1)); printf "  PASS  %-44s exit=%s\n" "$desc" "$got"
  else fail=$((fail+1)); printf "  FAIL  %-44s exit=%s want=%s\n        %s\n" "$desc" "$got" "$exp" "$(echo "$out"|tail -2|tr '\n' ' ')"; fi; }

echo "=== chirality.py self-test ==="
chk "L residue REJECTED by D assertion"       2 $PY chirality.py assert "$T/L.pdb" 2 --by-position
chk "L->D inversion succeeds"                 0 $PY chirality.py invert "$T/L.pdb" 2 --by-position "$T/D.pdb"
chk "inverted residue PASSES D assertion"     0 $PY chirality.py assert "$T/D.pdb" 2 --by-position
chk "Gly (achiral) fails loudly"              1 $PY chirality.py assert "$T/D.pdb" 3 --by-position
chk "neighbour res1 untouched (still L)"      2 $PY chirality.py assert "$T/D.pdb" 1 --by-position
chk "out-of-range position fails"             1 $PY chirality.py assert "$T/D.pdb" 99 --by-position
chk "refuses to invert an already-D centre"   1 $PY chirality.py invert "$T/D.pdb" 2 --by-position "$T/X.pdb"
chk "missing file fails"                      1 $PY chirality.py assert "$T/nope.pdb" 1 --by-position

echo
echo "--- signed volumes (must be equal magnitude, opposite sign) ---"
$PY chirality.py assert "$T/L.pdb" 2 --by-position 2>&1 | head -1
$PY chirality.py assert "$T/D.pdb" 2 --by-position 2>&1 | head -1
NMOVED=$(diff "$T/L.pdb" "$T/D.pdb" | grep -c "^>")
echo "--- atoms moved by inversion: $NMOVED (expect 1: the CB only) ---"
[ "$NMOVED" = 1 ] || { echo "  FAIL: inversion moved $NMOVED atoms, not 1"; fail=$((fail+1)); }

echo
echo "RESULT: $pass passed, $fail failed"
[ "$fail" = 0 ] && { echo "chirality.py VERIFIED"; exit 0; } || exit 1
