#!/bin/bash
set -eo pipefail
GMX=/data/users/kzanaj/envs/gmxcuda/bin.AVX_256/gmx
WD=$1; cd $WD
[ -f prod.gro ] || { echo "SKIP $WD: not finished"; exit 0; }
export GMX_MAXBACKUP=-1
printf '"System" all;\n"DNA" resname DG DC DA DT DT3 DA5;\n"CAT" resname DOTAP MC3T MC3N;\n"LIP" resname DOTAP MC3T MC3N DOPE CHOL;\n' > sel_groups.dat
printf '(resname DOTAP MC3T MC3N DOPE CHOL) and within 0.6 of (resname DG DC DA DT DT3 DA5)\n' > sel_contacts.dat
$GMX select -s prod.tpr -sf sel_groups.dat -on idx.ndx
printf "DNA\nSystem\n" | $GMX trjconv -f prod.xtc -s prod.tpr -n idx.ndx -pbc mol -center -o whole.xtc
$GMX rdf -f whole.xtc -s prod.tpr -ref "resname DG DC DA DT DT3 DA5" -sel "resname DOTAP MC3T MC3N" -bin 0.02 -o rdf_cat_dna.xvg
$GMX select -f whole.xtc -s prod.tpr -sf sel_contacts.dat -os contacts.xvg
printf "DNA\nLIP\n" | $GMX mindist -f whole.xtc -s prod.tpr -n idx.ndx -od mindist.xvg
printf "DNA\n" | $GMX gyrate -f whole.xtc -s prod.tpr -n idx.ndx -o gyrate_dna.xvg
echo "ANALYZED $WD OK"
