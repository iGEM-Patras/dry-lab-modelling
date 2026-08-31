#!/bin/bash
#SBATCH --job-name=fclass
#SBATCH --partition=pshort_el8
#SBATCH --time=00:40:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --array=1-40%20
#SBATCH --output=/data/users/kzanaj/boltz_dock/cycle3b/logs/fclass_%A_%a.out
set -uo pipefail
C=/data/users/kzanaj/boltz_dock/cycle3b
G=/data/users/kzanaj/envs/gmxcuda/bin/gmx

# mount guard (carried forward from the MD campaign)
for i in $(seq 1 30); do [ -d "$C/systems" ] && break; sleep 10; done
[ -d "$C/systems" ] || { echo "FATAL: /data not mounted"; exit 90; }

mapfile -t JOBS < <(for s in c3b_menk_DOR c3b_menk_MOR c3b_em1_DOR c3b_em1_MOR \
                             c3b_dtI_DOR c3b_dtI_MOR c3b_dtII_DOR c3b_dtII_MOR; do
                      for r in 1 2 3 4 5; do echo "$s $r"; done; done)
set -- ${JOBS[$((SLURM_ARRAY_TASK_ID-1))]}
SYS=$1; REP=$2
R=$C/systems/$SYS/rep$REP
cd $R || { echo "FATAL: no $R"; exit 91; }
export GMX_MAXBACKUP=-1

# Concatenated index: System0 Protein1 MEMB2 SOLV3 Receptor4 Ligand5.
# Referenced BY NUMBER because both files may contain like-named groups.
cat index.ndx mmgbsa.ndx > comb.ndx
NG=$(grep -c "^\[" comb.ndx)
[ "$NG" -eq 6 ] || { echo "FATAL: expected 6 groups in comb.ndx, got $NG"; exit 92; }

# (a) ligand <-> membrane minimum distance, every frame of the FULL trajectory
printf '5\n2\n' | $G mindist -s prod.tpr -f prod.xtc -n comb.ndx \
    -od $C/frameclass/${SYS}_r${REP}_memb.xvg -tu ns >/dev/null 2>&1 \
    || { echo "FATAL: mindist failed"; exit 93; }

# (b) ligand RMSD from the docked pose after superposing the receptor:
#     directly measures "has the peptide left the pose it started in"
printf '4\n5\n' | $G rms -s prod.tpr -f prod.xtc -n comb.ndx \
    -o $C/frameclass/${SYS}_r${REP}_ligrmsd.xvg -tu ns -fit rot+trans >/dev/null 2>&1 \
    || { echo "FATAL: rms failed"; exit 94; }

NM=$(grep -vc "^[#@]" $C/frameclass/${SYS}_r${REP}_memb.xvg)
NR=$(grep -vc "^[#@]" $C/frameclass/${SYS}_r${REP}_ligrmsd.xvg)
echo "FCLASS_OK $SYS rep$REP memb_frames=$NM rmsd_frames=$NR"
rm -f comb.ndx
