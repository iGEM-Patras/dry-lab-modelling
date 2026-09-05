#!/bin/bash
#SBATCH --job-name=c3b_e2e_cpu
#SBATCH --partition=pibu_el8
#SBATCH --account=kzanaj
#SBATCH --cpus-per-task=32
#SBATCH --mem=32G
#SBATCH --time=24:00:00
#SBATCH --output=/data/users/kzanaj/boltz_dock/cycle3b/e2e_cpu_%j.log
set -uo pipefail
W=/data/users/kzanaj/boltz_dock/cycle3b
cd "$W" || { echo "FATAL: cannot cd $W"; exit 1; }
REP=99   # own replicate dir: runs CONCURRENTLY with the GPU twin (rep1), no collision

echo "############ END-TO-END PIPELINE VALIDATION - CPU ############"
echo "CPU twin of run_pipeline_validate.sh. Uses scripts/run_prod_cpu.sh:"
echo "run_prod.sh with the 3 mdrun lines changed from '-nb gpu -ntmpi 1 -ntomp 8'"
echo "to '-nb cpu -ntmpi \$GMX_NTMPI -ntomp \$GMX_NTOMP'. Nothing else differs;"
echo "physics, seeds and all three chirality gates are identical."
echo
echo "Runs as rep$REP so it does NOT touch the GPU job's rep1."
echo "Production truncated to 200 ps. NOT a production replicate (those are 20 ns)."
echo "NVT (200 ps) + NPT (1 ns) run FULL LENGTH -- hence 24 h on CPU."
echo

# ---- chemistry from the design table, never from a positional default -------
# run_pipeline_validate.sh calls run_prod.sh with 2 args, so DRES_REL defaults to
# 'none' -- and gate() returns early when DRES_REL=none. The GPU twin therefore
# validates the pipeline with all three chirality gates SKIPPED. Same class of
# defect that cost the 2026-07-30 build (see scripts/peptide_spec.sh). Fixed here.
. "$W/scripts/peptide_spec.sh"
load_peptide_spec c3b_dtII_DOR || exit 1
[ -f systems/c3b_dtII_DOR/chem.txt ] || { echo "FAIL: chem.txt missing -- rebuild"; exit 1; }
. systems/c3b_dtII_DOR/chem.txt
if [ "$BUILT_DRES" != "$SPEC_DRES" ] || [ "$BUILT_AMIDE" != "$SPEC_AMIDE" ]; then
  echo "FAIL: build/run chemistry mismatch (built dres=$BUILT_DRES amide=$BUILT_AMIDE;"
  echo "      table dres=$SPEC_DRES amide=$SPEC_AMIDE). Wrong molecule -- rebuild."
  exit 1
fi
echo "  build/run chemistry agree: dres=$SPEC_DRES amide=$SPEC_AMIDE"
[ "$SPEC_DRES" = "none" ] && { echo "FAIL: dres=none would disarm the gates"; exit 1; }
echo "  chirality gates ARMED on D-residue $SPEC_DRES"
echo

export GMX_NTMPI=4 GMX_NTOMP=8   # 4 x 8 = 32 cores
echo "Threading: -ntmpi $GMX_NTMPI -ntomp $GMX_NTOMP | node $(hostname) | $(date -Is)"
echo

PROD_NSTEPS=100000 bash scripts/run_prod_cpu.sh c3b_dtII_DOR "$REP" "$SPEC_AMIDE" "$SPEC_DRES"
RC=$?
echo "RUN_PROD_EXIT=$RC"
[ $RC -ne 0 ] && { echo "ABORT: run_prod_cpu.sh failed"; exit $RC; }
echo

echo "############ GUARD TEST: rescore must REFUSE a truncated run ############"
bash scripts/rescore.sh c3b_dtII_DOR "$REP"
GRC=$?
echo "RESCORE_EXIT=$GRC (expected 3 = correctly refused)"
[ $GRC -eq 3 ] && echo "GUARD_OK" || echo "GUARD_FAILED: truncated run was not refused"
echo

echo "############ RESCORE THE TRUNCATED RUN ANYWAY (path test only) ############"
rm -f systems/c3b_dtII_DOR/rep$REP/TRUNCATED_NOT_FOR_ANALYSIS
bash scripts/rescore.sh c3b_dtII_DOR "$REP"
echo "RESCORE_PATHTEST_EXIT=$?"
echo "E2E_DONE $(date -Is)"
