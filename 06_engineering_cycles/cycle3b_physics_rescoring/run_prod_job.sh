#!/bin/bash
# Cycle 3b Stage 1 - production replicate SLURM wrapper.
# Submitted with --dependency=afterok:<build_job> so run_prod.sh errors propagate
# and halt dependent jobs. This wrapper explicitly exits with the script's code.
set -euo pipefail

TAG="${1:?usage: run_prod_job.sh <tag> <rep>}"
REP="${2:?}"

W=/data/users/kzanaj/boltz_dock/cycle3b
SCRIPT=$W/scripts/run_prod.sh

# run_prod.sh takes 4 positional args: tag, rep, amide_flag, dres_rel
# Caller provides TAG and REP; the other two are read from the build's pepmeta.txt
SYS=$W/systems/$TAG
[ -d "$SYS" ] || { echo "FAIL: $SYS does not exist"; exit 1; }
. $SYS/pepmeta.txt   # exports PEP_* variables

# Peptide chemistry comes from the design table, NEVER from a positional default.
# The previous version used AMIDE="${3:-yes}" / DRES_REL="${4:-none}", which is the
# defect that matters most here: run_prod.sh SKIPS its chirality gate when
# DRES_REL=none, so a defaulted argument silently disarmed the one check designed to
# catch stereochemical corruption. See scripts/peptide_spec.sh.
. $W/scripts/peptide_spec.sh
load_peptide_spec "$TAG" || exit 1
AMIDE="$SPEC_AMIDE"
DRES_REL="$SPEC_DRES"

# Cross-check against what the build actually produced. A build/run mismatch here
# means the coordinates are not the molecule this job thinks it is running.
if [ -f "$SYS/chem.txt" ]; then
  . "$SYS/chem.txt"
  if [ "$BUILT_DRES" != "$DRES_REL" ] || [ "$BUILT_AMIDE" != "$AMIDE" ]; then
    echo "FAIL: build/run chemistry mismatch for $TAG"
    echo "      built with dres=$BUILT_DRES amide=$BUILT_AMIDE"
    echo "      table says dres=$DRES_REL amide=$AMIDE"
    echo "      The system in $SYS is the wrong molecule -- rebuild, do not run."
    exit 1
  fi
  echo "  build/run chemistry agree: dres=$DRES_REL amide=$AMIDE"
else
  echo "FAIL: $SYS/chem.txt missing -- built by an older build_system.sh that did not"
  echo "      record its chemistry. Rebuild rather than assume; a dres=none build is"
  echo "      indistinguishable from a correct one by inspection of the coordinates."
  exit 1
fi

bash "$SCRIPT" "$TAG" "$REP" "$AMIDE" "$DRES_REL"
JOB_EXIT=$?
echo "JOB_EXIT=$JOB_EXIT"
exit $JOB_EXIT
