# Gencore-modules
This is the documentation for gencore module build on a HPC system. 
This solution works not only with the HPC, even cloud, virtual machines, containers etc. 

Prerequisites for running this script 
- Easybuild==4.9.2
- tcl==8.6.14
- Modules==5.4.0
- gcc
- python=3.11



To install Easy
export LD_LIBRARY_PATH=/scratch/jr5241/Gencoremodules_v3/easybuild/tcl_local/lib:$LD_LIBRARY_PATH
#module 5.4.0
export PATH=/scratch/jr5241/Gencoremodules_v3/easybuild/env_modules/bin:$PATH
source /scratch/jr5241/Gencoremodules_v3/easybuild/env_modules/init/bash

#Below 4 steps needs during the inital setup of easybuild, now we have install eb inside eb
#export EB_TMPDIR=/scratch/jr5241/Gencoremodules_v3/easybuild/eb_tmp_dir
#python3 -m pip install --ignore-installed --prefix $EB_TMPDIR easybuild
#export PATH=$EB_TMPDIR/bin:$PATH
#export PYTHONPATH=$(/bin/ls -rtd -1 $EB_TMPDIR/lib*/python*/site-packages | tail -1):$PYTHONPATH
#export EB_PYTHON=python3
export EASYBUILD_PREFIX=/scratch/jr5241/Gencoremodules_v3/easybuild/.eb/3.0
export EASYBUILD_CONFIGFILES=/scratch/jr5241/Gencoremodules_v3/easybuild/.eb/3.0/config.cfg

unset MODULEPATH
export MODULEPATH=/scratch/jr5241/Gencoremodules_v3/easybuild/.eb/3.0/modules/all
 module load EasyBuild/4.9.2