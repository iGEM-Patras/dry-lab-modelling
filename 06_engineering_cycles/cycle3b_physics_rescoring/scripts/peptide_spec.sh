#!/bin/bash
# Authoritative per-tag peptide chemistry lookup.  source this; do not execute.
#
# WHY THIS EXISTS
# --------------
# build_system.sh and run_prod_job.sh both took DRES as a POSITIONAL argument that
# silently defaulted to "none". On 2026-07-30 that default cost a full build: the
# c3b_dtII_DOR pilot was launched with dres=none, so the D-Ala2 inversion never ran
# and the 155k-atom system that came out was the ALL-L analog of deltorphin II. It
# looked perfect -- tilt 0.00 deg, tleap Errors=0, groups partitioning exactly -- and
# nothing downstream would have flagged it, because run_prod.sh's chirality gate is
# itself SKIPPED when DRES_REL=none. A silent default in the argument feeding a
# safety gate disables the gate. Deltorphin II's entire delta-selectivity rests on
# that D-Ala2, so the run would have measured the wrong molecule.
#
# The fix is to stop trusting the command line for chemistry. prod_all.txt is the
# design table of record ("tag rep amide dres"); this helper reads DRES and AMIDE
# from it and hard-FAILS on an unknown tag instead of assuming a safe-looking value.
#
# Usage:  . "$W/scripts/peptide_spec.sh"; load_peptide_spec "$TAG"
#         -> sets SPEC_DRES ("none" or an integer) and SPEC_AMIDE ("yes"/"no")

load_peptide_spec() {
  local tag="${1:?load_peptide_spec needs a tag}"
  local table="${PROD_TABLE:-$W/prod_all.txt}"

  [ -f "$table" ] || { echo "FAIL: design table $table not found -- refusing to guess peptide chemistry"; return 1; }

  # Columns: tag rep amide dres.  Chemistry must be consistent across replicates of
  # a tag; if it is not, the table itself is wrong and we must not pick a winner.
  local combos
  combos=$(awk -v t="$tag" '$1==t {print $3" "$4}' "$table" | sort -u)

  if [ -z "$combos" ]; then
    echo "FAIL: tag '$tag' not in $table -- refusing to default to all-L."
    echo "      Known tags: $(awk '{print $1}' "$table" | sort -u | tr '\n' ' ')"
    return 1
  fi
  if [ "$(printf '%s\n' "$combos" | wc -l)" -ne 1 ]; then
    echo "FAIL: inconsistent chemistry for '$tag' in $table:"
    printf '        amide=%s dres=%s\n' $combos
    return 1
  fi

  SPEC_AMIDE=$(printf '%s' "$combos" | awk '{print $1}')
  SPEC_DRES=$(printf  '%s' "$combos" | awk '{print $2}')

  case "$SPEC_AMIDE" in yes|no) ;; *) echo "FAIL: bad amide flag '$SPEC_AMIDE' for $tag"; return 1 ;; esac
  case "$SPEC_DRES" in
    none) ;;
    ''|*[!0-9]*) echo "FAIL: bad dres value '$SPEC_DRES' for $tag (want integer or 'none')"; return 1 ;;
  esac

  echo "  spec[$tag]: dres=$SPEC_DRES amide=$SPEC_AMIDE  (from $(basename "$table"))"
  return 0
}