#!/bin/bash
#SBATCH --partition=pgpu
#SBATCH --account=kzanaj
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --job-name=enk_cofold4
#SBATCH --output=/data/users/kzanaj/boltz_dock/enk_cofold/cofold_%j.log
set -uo pipefail
export PATH=/data/users/kzanaj/envs/boltz2/bin:$PATH
cd /data/users/kzanaj/boltz_dock/enk_cofold
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
for tag in DOR_Metenk DOR_Leuenk MOR_Metenk MOR_Leuenk; do
  echo "=== $tag  $(date +%H:%M:%S) ==="
  boltz predict ./${tag}.yaml --out_dir ./out --cache /data/users/kzanaj/boltz_dock/cache \
    --use_msa_server --diffusion_samples 15 --recycling_steps 3 --output_format pdb 2>&1 | tail -6
done
echo "=== collecting ==="
for tag in DOR_Metenk DOR_Leuenk MOR_Metenk MOR_Leuenk; do
  for f in ./out/boltz_results_$tag/predictions/$tag/*.pdb ./out/boltz_results_$tag/predictions/$tag/confidence*.json; do
    [ -f "$f" ] && cp "$f" "./${tag}_$(basename $f)"
  done
done
ls -lh ./*_*model_0.pdb ./*confidence*.json 2>&1 | head -20
echo "DONE $(date +%H:%M:%S)"
