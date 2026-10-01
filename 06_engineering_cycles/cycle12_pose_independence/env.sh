# source before any ADFR/ADCP command.
# ADFRsuite 1.0 BUILD 5 (Oct 2019) ships openbabel 2.4.1 plugins linked against
# libpng12 / libSM / libICE, none of which are in the sandbox base image. Without
# these on LD_LIBRARY_PATH *every* openbabel format plugin fails to load -- including
# pdbformat and pdbqtformat -- and agfr exits 1. The conda python env carries all three.
export ADFR="/home/kay/.claude-science/orgs/6cf41134-f542-4332-8c2d-8b7df40cdb61/workspaces/26811836-f929-4728-a6f6-a5c8fb1dc9c2/adcp/ADFR"
export LD_LIBRARY_PATH="/home/kay/.claude-science/conda/envs/python/lib:$LD_LIBRARY_PATH"
export PATH="$ADFR/bin:$PATH"
