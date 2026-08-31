#!/bin/bash
#SBATCH --job-name=c3b_rescore
#SBATCH --partition=pibu_el8
#SBATCH --time=04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --no-requeue
#SBATCH --output=/data/users/kzanaj/boltz_dock/cycle3b/logs/rescore_%A_%a.out

set -uo pipefail
W=/data/users/kzanaj/boltz_dock/cycle3b

for i in $(seq 1 60); do [ -s "$W/prod_all.txt" ] && break; sleep 5; done
[ -s "$W/prod_all.txt" ] || { echo "FAIL: /data not mounted after 300s"; exit 90; }

LINE=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "$W/prod_all.txt")
[ -n "$LINE" ] || { echo "FAIL: no line ${SLURM_ARRAY_TASK_ID} in prod_all.txt"; exit 2; }
TAG=$(echo "$LINE" | awk '{print $1}')
REP=$(echo "$LINE" | awk '{print $2}')
[ -n "$TAG" ] && [ -n "$REP" ] || { echo "FAIL: could not parse '$LINE'"; exit 2; }

probe="$W/systems/$TAG/rep$REP/.diskprobe"
if ! dd if=/dev/zero of="$probe" bs=1M count=3072 status=none 2>/dev/null; then
  rm -f "$probe"; echo "FAIL: cannot write 3 GB probe -- disk/quota problem"; exit 91
fi
rm -f "$probe"

# per-task results file: no concurrent appends to one CSV
export STAGE1_CSV="$W/results_parts/${TAG}_r${REP}.csv"
: > "$STAGE1_CSV"

echo "=== rescore $TAG rep$REP  task ${SLURM_ARRAY_TASK_ID}  $(date -Is) on $(hostname) ==="
t0=$(date +%s)
bash "$W/scripts/rescore.sh" "$TAG" "$REP"; rc=$?
t1=$(date +%s)
echo "=== exit $rc after $(( (t1-t0)/60 )) min ==="

# free the 112 MB window trajectory; prod.xtc is the archival copy
rm -f "$W/systems/$TAG/rep$REP/rescore_window.xtc"
exit $rc
