# Gencore-modules
This is the documentation for gencore module build on a HPC system. 
This solution works not only with the HPC, even cloud, virtual machines, containers etc. 

Prerequisites for running this script 
- Easybuild==4.9.2
- tcl==8.6.14
- Modules==5.4.0
- gcc
- python=3.11



To install Easybuild refer below steps:- 

```
export EB_TMPDIR=eb_tmp_dir
python3 -m pip install --ignore-installed --prefix $EB_TMPDIR easybuild
export PATH=$EB_TMPDIR/bin:$PATH
export PYTHONPATH=$(/bin/ls -rtd -1 $EB_TMPDIR/lib*/python*/site-packages | tail -1):$PYTHONPATH
export EB_PYTHON=python3
```

Create easybuild config under the install-dir ```config```
```
[config]
module-syntax = Tcl
modules-tool = EnvironmentModules
```

To install Easybuild as a module 
```
eb --install-latest-eb-release --prefix <path-to-install>
```

To excecute the 