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
. $SYS/pepmeta.txt   # exports PEP_* variables, which the caller can use for AMIDE/DRES

# Defaults: assume all controls are amidated (NHE) and all-L (no D-residue)
AMIDE="${3:-yes}"
DRES_REL="${4:-none}"

bash "$SCRIPT" "$TAG" "$REP" "$AMIDE" "$DRES_REL"
JOB_EXIT=$?
echo "JOB_EXIT=$JOB_EXIT"
exit $JOB_EXIT
