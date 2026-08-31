#!/bin/bash
#SBATCH --job-name=c3b_rescore_smoke
#SBATCH --partition=pshort_el8
#SBATCH --time=01:50:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --no-requeue
#SBATCH --output=/data/users/kzanaj/boltz_dock/cycle3b/logs/rescore_%j.out

set -uo pipefail
W=/data/users/kzanaj/boltz_dock/cycle3b

# GPFS mount-wait guard (nodes resuming from POWERED_DOWN see /data absent)
for i in $(seq 1 60); do [ -s "$W/prod_all.txt" ] && break; sleep 5; done
[ -s "$W/prod_all.txt" ] || { echo "FAIL: /data not mounted after 300s"; exit 90; }

# disk guard: MM-GBSA writes temp trajectories; refuse to start if space is tight
TAG=${1:?TAG}; REP=${2:?REP}
probe="$W/systems/$TAG/rep$REP/.diskprobe"
if ! dd if=/dev/zero of="$probe" bs=1M count=2048 status=none 2>/dev/null; then
  rm -f "$probe"; echo "FAIL: cannot write 2 GB probe -- disk/quota problem"; exit 91
fi
rm -f "$probe"
echo "disk guard OK (2 GB writable)"

echo "=== rescore $TAG rep$REP starting $(date -Is) on $(hostname) ==="
t0=$(date +%s)
bash "$W/scripts/rescore.sh" "$TAG" "$REP"
rc=$?
t1=$(date +%s)
echo "=== exit $rc after $(( (t1-t0)/60 )) min ==="
exit $rc
