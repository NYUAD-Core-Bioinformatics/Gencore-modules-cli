## Gencore Modules v3
This is the documentation for gencore module v3  build system on a HPC system. 
This solution works not only with the HPC, even cloud, virtual machines, containers etc. 

### Prerequisites for running this script 
- Easybuild==4.9.2
- tcl==8.6.14
- Modules==5.4.0
- gcc
- python>=3.8
- anaconda-client
- urllib3==1.26.5



### Easybuild install Instructions


```
export EB_TMPDIR=eb_tmp_dir
python3 -m pip install --ignore-installed --prefix $EB_TMPDIR easybuild
export PATH=$EB_TMPDIR/bin:$PATH
export PYTHONPATH=$(/bin/ls -rtd -1 $EB_TMPDIR/lib*/python*/site-packages | tail -1):$PYTHONPATH
export EB_PYTHON=python3
```

Create easybuild ```config``` under the install-dir.
```
[config]
module-syntax = Tcl
modules-tool = EnvironmentModules
```

To install Easybuild as a module 
```
eb --install-latest-eb-release --prefix <path-to-install>
```

### Excecute build script

```
cd /scratch/gencore/Gencoremodules_v3/
python eb_modules_v3.py
```

As of now it consist of different methods to install a package and convert it as a module in HPC.

```
1. Create easyconfig from anaconda with specific custom conda channels (default channels :-  bioconda, conda-forge ).
2. Local yml conda ( yml file needs to be specified locally using a full path )
3. Create easyconfig from a local tarball.
4. Create easyconfig from a remote tarball.
5. Create a bundle which is a mix of packages already added in easybuild.
```

### Key Benefits


1. Loaded with mamba for conda based installation and this helps the dependency resolving smootly and reduced the excecution time compared to native conda method. 
2. Ability to supply/pass new conda channels.
3. Supports local and remote tarball based installations. 
4. Module bundle based integration to club multiple modules.  

### Future Enhancement requests


1. Create easyconfig for a manually installed package.
2. Create easyconfig from a ConfigureCmake compiled package.



### Known Issues


Issues with integrating this setup on HPC system 

1. Module build dependency doesn't recognize due to incorrect regex patter matching. 
To fix, added "re.search" and commented the other line containing re.match in the modules.py script.
```
                 res = bool(re.search(mod_exists_regex, line))
                #res = bool(re.match(mod_exists_regex, line))
```

2. Special characters in the module show output causing already installed module cannot receognize.
To fix, add a new regex pattern as below in the modules.py script. 
```
   	        (stdout, stderr) = proc.communicate()
   	        ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')
   
   	        stdout = ansi_escape.sub('', stdout)
   	        stderr = ansi_escape.sub('', stderr)
   	        self.log.debug("Output of module command '%s': stdout: %s; stderr: %s" % (full_cmd, stdout, stderr))
```