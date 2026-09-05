#!/bin/bash
#SBATCH --partition=pgpu
#SBATCH --account=kzanaj
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --job-name=c3b_mmgbsa_smoke
#SBATCH --time=02:00:00
#SBATCH --output=smoke_%j.log

# ---- Cycle 3b: MM-GBSA reachability smoke test -------------------------------
# The e2e validation (jobs 17985511/17985540) proved NVT->NPT->prod->3 chirality
# gates and the truncation guard, but could NEVER reach gmx_MMPBSA: prod.mdp emits
# one frame per 10 ps, so a 200 ps run yields 21 frames against rescore.sh's >=90
# frame gate. This run is the cheapest one that clears that gate: 1 ns production
# = 500000 steps at dt=0.002 -> ~101 frames.
#
# rep777 is a SCRATCH slot. prod_all.txt plans reps 1-3; 777 cannot collide.
# Results go to results_smoke_rep777.csv via scripts/rescore_smoke.sh, which is
# byte-identical to rescore.sh except that one target -- collect_dg.py records no
# run-length field, so a smoke row in results_stage1.csv would be indistinguishable
# from production.
set -uo pipefail
W=/data/users/kzanaj/boltz_dock/cycle3b
cd $W

# chemistry from the design table, never a positional default (same as the patch)
. $W/scripts/peptide_spec.sh
load_peptide_spec c3b_dtII_DOR || exit 1
[ -f systems/c3b_dtII_DOR/chem.txt ] || { echo "FAIL: chem.txt missing"; exit 1; }
. systems/c3b_dtII_DOR/chem.txt
[ "$BUILT_DRES" = "$SPEC_DRES" ] && [ "$BUILT_AMIDE" = "$SPEC_AMIDE" ] || {
  echo "FAIL: build/run chemistry disagree (built dres=$BUILT_DRES amide=$BUILT_AMIDE"
  echo "      vs spec dres=$SPEC_DRES amide=$SPEC_AMIDE)"; exit 1; }
echo "  chirality gates ARMED on D-residue $SPEC_DRES"

echo "############ 1 ns production, scratch rep777 ############"
PROD_NSTEPS=500000 bash scripts/run_prod.sh c3b_dtII_DOR 777 "$SPEC_AMIDE" "$SPEC_DRES"
echo "RUN_PROD_EXIT=$?"

echo "############ frame count actually produced ############"
/data/users/kzanaj/envs/gmxcuda/bin/gmx check \
  -f systems/c3b_dtII_DOR/rep777/prod.xtc 2>&1 | awk '/^Step/{print "prod.xtc frames: "$2}'

echo "############ guard must still refuse (marker written by PROD_NSTEPS) ############"
bash scripts/rescore_smoke.sh c3b_dtII_DOR 777
echo "GUARD_EXIT=$? (expect 3)"

echo "############ clear marker on the SCRATCH rep only, then rescore for real ############"
rm -f systems/c3b_dtII_DOR/rep777/TRUNCATED_NOT_FOR_ANALYSIS
bash scripts/rescore_smoke.sh c3b_dtII_DOR 777
echo "RESCORE_EXIT=$? (expect 0 = gmx_MMPBSA reached and completed)"

echo "############ did the collector emit a row? ############"
cat $W/results_smoke_rep777.csv 2>/dev/null || echo "no results file written"
echo "SMOKE_DONE $(date -Is)"
