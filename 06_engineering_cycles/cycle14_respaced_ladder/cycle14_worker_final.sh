#!/bin/bash
#SBATCH --partition=pibu_el8
#SBATCH --account=kzanaj
#SBATCH --time=71:00:00
#SBATCH --cpus-per-task=48
#SBATCH --mem=64G
#SBATCH --requeue
# Cycle 14 production worker. 48 cores rank-heavy per the provider notes: the 8-core
# configuration carried over from the GPU partition is substantially suboptimal here.
JOBDIR="$PWD"
exec >"$JOBDIR/w14_${SLURM_JOB_ID}.txt" 2>&1
set +e
D=/data/users/kzanaj; G=$D/envs/gmxcuda/bin/gmx; W=$D/cycle14
LK=$W/locks14; mkdir -p $LK
BUDGET=$((69*3600))
T0=$SECONDS
LEGS="prod_c3b_menk_DOR_r1 prod_c3b_menk_MOR_r1 prod_c3b_menk_DOR_r2 prod_c3b_menk_MOR_r2"

echo "worker $SLURM_JOB_ID on $(hostname) start=$(date)"

# guard 1: the shared filesystem must be mounted before anything is claimed
for i in $(seq 1 60); do [ -x "$G" ] && { echo "gpfs ready ${i}0s"; break; }; sleep 10; done
[ -x "$G" ] || { echo "FATAL: /data not mounted on $(hostname)"; exit 90; }

# guard 2: refuse to start without room for trajectories
avail=$(df -Pk "$W" | tail -1 | awk '{print int($4/1024)}')
echo "disk available: ${avail} MB"
[ "$avail" -lt 400 ] && { echo "FATAL: under 400 MB free, refusing to start"; exit 91; }

done_count=0
pass=0
while :; do
  pass=$((pass+1))
  claimed_any=0
  for LEG in $LEGS; do
    O=$W/$LEG
    [ -d "$O" ] || { echo "no directory $LEG"; continue; }
    # a leg is only eligible if all 57 inputs exist: a partial window set is how an
    # earlier campaign spread sampling across windows it could never finish
    ntpr=$(ls -1 $O/w*.tpr 2>/dev/null | wc -l)
    if [ "$ntpr" -ne 57 ]; then
      echo "SKIP $LEG: $ntpr/57 tpr present, not launchable"
      continue
    fi
    for i in $(seq -w 0 56); do
      w="w$i"
      elapsed=$((SECONDS-T0))
      [ "$elapsed" -gt "$BUDGET" ] && { echo "budget spent after ${elapsed}s"; break 3; }

      # completion test: reached step, not a status file
      last=$(for f in $O/${w}_run.part*.log $O/${w}_run.log; do
               [ -s "$f" ] && grep -oE "^ *Step +[0-9]+" "$f" 2>/dev/null | tail -1 | awk '{print $2}'
             done 2>/dev/null | sort -n | tail -1)
      [ -n "$last" ] && [ "$last" -ge 1500000 ] && continue

      # atomic claim: mkdir succeeds for exactly one worker
      mkdir "$LK/${LEG}_${w}" 2>/dev/null || continue
      claimed_any=1
      echo "=== claim $LEG $w  (pass $pass, t=$((SECONDS-T0))s)"

      before="${last:-0}"
      CPI=""
      ls $O/${w}_run.cpt >/dev/null 2>&1 && CPI="-cpi ${w}_run.cpt"
      cd $O || { rmdir "$LK/${LEG}_${w}"; continue; }

      $G mdrun -s $w.tpr -deffnm ${w}_run $CPI -noappend \
               -ntmpi 1 -ntomp 48 -nb cpu -pme cpu \
               -maxh 11.5 >/dev/null 2>${w}_mdrun.log

      after=$(for f in $O/${w}_run.part*.log $O/${w}_run.log; do
                [ -s "$f" ] && grep -oE "^ *Step +[0-9]+" "$f" 2>/dev/null | tail -1 | awk '{print $2}'
              done 2>/dev/null | sort -n | tail -1)
      after="${after:-0}"

      # progress gate: a window that advanced NO simulated time is a deterministic
      # failure, not a transient one. Abort rather than loop on it.
      if [ "$after" -le "$before" ]; then
        echo "PROGRESS GATE: $LEG $w advanced no time ($before -> $after). Aborting."
        tail -12 ${w}_mdrun.log | sed 's/^/    /'
        rmdir "$LK/${LEG}_${w}" 2>/dev/null
        exit 95
      fi
      echo "    $w: $before -> $after steps"

      if [ "$after" -ge 1500000 ]; then
        echo "    $w COMPLETE"
        done_count=$((done_count+1))
        echo "$LEG $w $SLURM_JOB_ID cpu $(date +%s)" >> $W/hardware_map14.txt
      else
        # released unfinished so another worker can resume it from the checkpoint
        rmdir "$LK/${LEG}_${w}" 2>/dev/null
      fi
    done
  done
  [ "$claimed_any" -eq 0 ] && { echo "nothing left to claim after pass $pass"; break; }
done

echo "worker $SLURM_JOB_ID finished $done_count window(s), t=$((SECONDS-T0))s, $(date)"
