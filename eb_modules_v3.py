from binstar_client.utils import get_server_api, parse_specs
import os
import subprocess

while True:
    print("================")
    print("Welcome to Jubail HPC Easybuild")
    print("================")
    print("\n")
    print("1. Create easyconfig from https://anaconda.org with specific custom conda channels (default channels :-  bioconda, conda-forge ).")
    print("2. Local yml conda ( yml file needs to be specified locally using a full path )")
    print("3. Create easyconfig from a local tarball.")
    print("4. Create easyconfig from a remote tarball.")
    print("5. Create a bundle which is a mix of packages already added in easybuild.")
    print("6. 'WORK IN PROGRESS' - Create easyconfig for a manually installed package.")
    print("7. 'WORK IN PROGRESS' - Create easyconfig from a ConfigureCmake compiled package.")
    print("8. To exit this menu, press 8")

    try:
        selection  = int(input("\nEnter the choice number: "))
    except ValueError:
        print("The input is not an integer")
    print("============================")

    if(selection == 1):
        print("Now the module installation begins conda on a specified package available in https://anaconda.org/.")
        print("+++++++++++++++++++++++++++")


        name=input("Enter the conda package name:- ")
        version=input("Optional:- Enter the conda package version, if not specified, it picks latest version:- ")
        channel=input("Enter the channel name:- ")

        package=f"{channel}/{name}/{version}"
        conda_api = get_server_api()
        specs = parse_specs(package)

        default_channels = ['bioconda', 'conda-forge']
        if channel not in default_channels:
            default_channels.append(channel)


        package_data = conda_api.package(specs.user, specs.package)
        latest_version = package_data['latest_version']
        summary = package_data['summary']
        url = package_data['url']
        homepage = f"https://anaconda.org/{specs.user}/{specs.package}"

        if version:
            version_to_use = version
        else:
            version_to_use = latest_version

        eb_conda=f'''##
# This is an easyconfig file for EasyBuild, see https://github.com/easybuilders/easybuild
##

easyblock = 'Conda'

name = "{name}"
version = "{version_to_use}"

homepage = '{homepage}'
description = """{summary}"""

toolchain = SYSTEM

requirements = "%(name)s=%(version)s"
channels = {default_channels}

builddependencies = [('Mamba', '23.11.0-0')]

sanity_check_paths = {{}}

moduleclass = 'tools'
    '''
        eb_config_folder="eb_config"
        output=f"{name}-{version_to_use}.eb"

        file_path=os.path.join(eb_config_folder, output)

        with open(file_path, "w") as file:
            file.write(eb_conda)

        eb_command=f"eb -r {file_path}"
        eb_command_out=subprocess.run(eb_command, shell=True, text=True)

        if eb_command_out.returncode == 0:
            print("+++++++++++++++++++++++++++")
            print("Build executed successfully")
            print("To load module issue below command on a new session")
            print("===========================")
            print("module load all gencore/3")
            print("module load", name + "/" + version_to_use)
            print("+++++++++++++++++++++++++++")
        else:
            print("+++++++++++++++++++++++++++")
            print(f"Build failed with return code {eb_command_out.returncode}, please contact admin.")
            print("+++++++++++++++++++++++++++")
        break

    elif(selection == 2):
        print("Now the module installation begins conda on a local yml")
        print("+++++++++++++++++++++++++++")
        eb_config_folder="eb_config"
        name=input("Enter the package name:- ")
        version=input("Enter the version number for the build:- ")
        yml_file_name=input(f"Specify the conda yml filename (Note: yml should present in {eb_config_folder} directory):- ")
        print("\n")

        eb_conda_local = f'''##
# This is an easyconfig file for conda yml file located locally.
##

easyblock = 'Conda'

name = "{name}"
version = "{version}"

homepage = "homepage"
description = """ description """

toolchain = SYSTEM

sources = ["{yml_file_name}"]
environment_file = sources[0]

builddependencies = [('Mamba', '23.11.0-0')]

sanity_check_paths = {{}}

moduleclass = 'tools'
'''
        output=f"{name}-{version}.eb"
        file_path=os.path.join(eb_config_folder, output)

        with open(file_path, "w") as file:
            file.write(eb_conda_local)
        eb_command = f"cd {eb_config_folder} && eb -r {output}"
        eb_command_out=subprocess.run(eb_command, shell=True, text=True)

        if eb_command_out.returncode == 0:
            print("+++++++++++++++++++++++++++")
            print("Build executed successfully")
            print("To load module issue below command on a new session")
            print("===========================")
            print("module load all gencore/3")
            print("module load", name + "/" + version)
            print("+++++++++++++++++++++++++++")
        else:
            print("+++++++++++++++++++++++++++")
            print(f"Build failed with return code {eb_command_out.returncode}, please contact admin.")
            print("+++++++++++++++++++++++++++")
        break


    elif(selection == 3):
        print("Now the module installation begins on binary on downloaded local package..")
        print("+++++++++++++++++++++++++++")
        eb_config_folder="eb_config"
        name=input("Enter the package name:- ")
        version=input("Enter the version number of the package:- ")
        homepage=input("Enter the URL of the package:- ")
        description=input("Enter short description about package:- ")
        package_name=input(f"Enter the downloaded tar or zip filename (File should present in {eb_config_folder} directory:- ")

        eb_binary_local = f'''##
# This is an easyconfig file for binary based remote installation.
##

easyblock = 'Binary'

name = "{name}"
version = "{version}"

homepage = "{homepage}"
description = """ {description} """

toolchain = SYSTEM

sources = ['{package_name}']

extract_sources = True

install_cmd = "mkdir %(installdir)s/bin/ &&"
install_cmd += "cp -a %(builddir)s/* %(installdir)s/bin/ && "
install_cmd += "touch %(installdir)s/bin/testfile"

sanity_check_paths = {{
    'files': ['bin/testfile'],
    'dirs': [],
}}

moduleclass = 'tools'
'''


        output=f"{name}-{version}.eb"
        file_path=os.path.join(eb_config_folder, output)
        with open(file_path, "w") as file:
            file.write(eb_binary_local)

        eb_command = f"cd {eb_config_folder} && eb -r {output}"
        eb_command_out=subprocess.run(eb_command, shell=True, text=True)

        if eb_command_out.returncode == 0:
            print("+++++++++++++++++++++++++++")
            print("Build executed successfully")
            print("To load module issue below command on a new session")
            print("===========================")
            print("module load all gencore/3")
            print("module load", name + "/" + version)
            print("+++++++++++++++++++++++++++")
        else:
            print("+++++++++++++++++++++++++++")
            print(f"Build failed with return code {eb_command_out.returncode}, please contact admin.")
            print("+++++++++++++++++++++++++++")
        break
        

    elif(selection == 4):
        print("Now the module installation begins on binary on a remote package.")
        print("+++++++++++++++++++++++++++")
        name=input("Enter the package name:- ")
        version=input("Enter the version number of the package:- ")
        homepage=input("Enter the URL of the package:- ")
        description=input("Enter short description about package:- ")
        package_url=input("Specify the full path of download url:- ")

        #Processing the download url.
        source_urls=package_url.rsplit('/', 1)[0]
        sources=package_url.split("/")[-1]
        eb_binary_remote = f'''##
# This is an easyconfig file for binary based remote installation.
##

easyblock = 'Binary'

name = "{name}"
version = "{version}"

homepage = "{homepage}"
description = """ {description} """

toolchain = SYSTEM

source_urls = ['{source_urls}']
sources = ['{sources}']

extract_sources = True

install_cmd = "mkdir %(installdir)s/bin/ &&"
install_cmd += "cp -a %(builddir)s/* %(installdir)s/bin/ && "
install_cmd += "touch %(installdir)s/bin/testfile"

sanity_check_paths = {{
    'files': ['bin/testfile'],
    'dirs': [],
}}

moduleclass = 'tools'
'''

        eb_config_folder="eb_config"
        output=f"{name}-{version}.eb"

        file_path=os.path.join(eb_config_folder, output)

        if os.path.exists(file_path):
            raise ValueError(f"Error: The file '{file_path}' already exists. Please choose a different version or remove the current file.")

        with open(file_path, "w") as file:
            file.write(eb_binary_remote)
        eb_command=f"eb -r {file_path}"
        eb_command_out=subprocess.run(eb_command, shell=True, text=True)

        if eb_command_out.returncode == 0:
            print("+++++++++++++++++++++++++++")
            print("Build executed successfully")
            print("To load module issue below command on a new session")
            print("===========================")
            print("module load all gencore/3")
            print("module load", name + "/" + version)
            print("+++++++++++++++++++++++++++")
        else:
            print("+++++++++++++++++++++++++++")
            print(f"Build failed with return code {eb_command_out.returncode}, please contact admin")
            print("+++++++++++++++++++++++++++")
        break

    elif(selection == 5):
        print("Module installation begins on easyconfig via bundle which is a mix of packages already added.")
        print("+++++++++++++++++++++++++++")
        name=input("Enter the bundle name:- ")
        version=input("Enter the version number of the bundle:- ")
        dependency_list=input("Specify the installed modules by comma seperated. eg:- kaiju/1.10.1,gtotree/1.2.2 :- ")

        dependency = [tuple(i.split('/')) for i in dependency_list.split(',')]

        eb_bundle = f'''##
# This is an easyconfig file for bundle remote installation.
##

easyblock = 'Bundle'

name = "{name}"
version = "{version}"

toolchain = SYSTEM

homepage = "homepage"
description = """ description """

'''

        eb_bundle += "dependencies = [\n"
        for modname, vers in dependency:
            eb_bundle += f"    ('{modname}', '{vers}'),\n"
        eb_bundle += "]\n"

        eb_bundle += '''
moduleclass = 'devel'
'''
        eb_config_folder="eb_config"
        output=f"{name}-{version}.eb"

        file_path=os.path.join(eb_config_folder, output)

        if os.path.exists(file_path):
            raise ValueError(f"Error: The file '{file_path}' already exists. Please choose a different version or remove the current file.")

        with open(file_path, "w") as file:
            file.write(eb_bundle)

        eb_command=f"eb -r {file_path}"
        eb_command_out=subprocess.run(eb_command, shell=True, text=True)

        if eb_command_out.returncode == 0:
            print("+++++++++++++++++++++++++++")
            print("Build executed successfully")
            print("To load module issue below command on a new session")
            print("===========================")
            print("module load all gencore/3")
            print("module load", name + "/" + version)
            print("+++++++++++++++++++++++++++")
        else:
            print("+++++++++++++++++++++++++++")
            print(f"Build failed with return code {eb_command_out.returncode}, please contact admin.")
            print("+++++++++++++++++++++++++++")
        break

    elif(selection == 6):
        print("Selected choice is 7 - WORK IN PROGRESS -Manually build module config.")
        print("\n")
        break


    elif(selection == 7):
        print("Selected choice is 7 - WORK IN PROGRESS --Configuremake.")
        print("\n")
        break

    elif(selection == 8):
        print("============================")
        print("Thank you for choosing this Jubail HPC Easybuild package service")
        print("============================")
        break

    elif(selection > 8):
        print("The selected choice is out of range, please choose the right option.")
        print("\n")

##Procedure ends##
