# PyMOL, same three shots
load DOR_engPENK_complex_annotated.pdb, cplx
bg_color black
hide everything; show cartoon, cplx
# AlphaFold pLDDT palette, on the 0-100 B-factor column
set_color af_vhigh, [0.00,0.33,0.84]
set_color af_conf,  [0.40,0.80,0.95]
set_color af_low,   [1.00,0.86,0.07]
set_color af_vlow,  [1.00,0.49,0.27]
color af_vlow, cplx
color af_low,  cplx and b > 50
color af_conf, cplx and b > 70
color af_vhigh,cplx and b > 90
set ray_opaque_background, 0
set cartoon_transparency, 0.65, cplx and chain A
show sticks, cplx and chain B
distance pharm, cplx and chain B and resi 1 and name OH, cplx and chain B and resi 4 and name CZ
color yellow, pharm
orient cplx and chain B
# spin 360 frames:  mset 1 x360 ; util.mroll(1,360,1) ; movie.produce engPENK.mp4
