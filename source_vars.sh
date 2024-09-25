export LD_LIBRARY_PATH=<path-to-tcl>/lib:$LD_LIBRARY_PATH
export PATH=<path-to-modules>/bin:$PATH
source <path-to-modules>/init/bash
export EASYBUILD_PREFIX=/<path-to-eb-install-dir>/easybuild/.eb/3.0
export EASYBUILD_CONFIGFILES=/<path-to-eb-install-dir>/easybuild/.eb/3.0/config.cfg
unset MODULEPATH
export MODULEPATH=/<path-to-eb-install-dir>/easybuild/.eb/3.0/modules/all

