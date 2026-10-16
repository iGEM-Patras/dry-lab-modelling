# source before any ADFR/ADCP command.
# ADFRsuite 1.0 BUILD 5 (Oct 2019) ships openbabel 2.4.1 plugins linked against
# libpng12 / libSM / libICE, none of which are in the sandbox base image. Without
# these on LD_LIBRARY_PATH *every* openbabel format plugin fails to load -- including
# pdbformat and pdbqtformat -- and agfr exits 1. The conda python env carries all three.
# ADFR location, relative to this script so the path does not depend on one machine.
export ADFR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/adcp/ADFR"
# Resolve the active interpreter's lib directory rather than hardcoding one machine's
# path, so this script is portable. Falls back to leaving LD_LIBRARY_PATH untouched.
_PYLIB="$(python3 -c 'import sys,os;print(os.path.join(sys.prefix,"lib"))' 2>/dev/null)"
[ -d "$_PYLIB" ] && export LD_LIBRARY_PATH="$_PYLIB:$LD_LIBRARY_PATH"
export PATH="$ADFR/bin:$PATH"
