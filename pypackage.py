"""
A script to download, update and remove software from a set list of links.
Requires urlgrabber (you can get it from pip: pip3 install urlgrabber).
TODO: Eliminate urlgrabber dependency.
"""
import os, json, zipfile, tarfile, shutil
from urlgrabber.grabber import URLGrabber

### stupid config stuff ###
# todo: document. this all conforms with XDG somehow
cache_home = os.environ.get('XDG_CACHE_HOME', os.environ['HOME'] + '/.cache') + '/pypackage/'
config_home = os.environ.get('XDG_CONFIG_HOME', os.environ['HOME'] + '/.config') + '/pypackage/'
try:
    os.mkdir(cache_home)
    os.mkdir(config_home)
except FileExistsError:
    pass
pathcheck = os.path.exists(config_home + 'config.json')
if pathcheck:
    with open(config_home + 'config.json', 'r+') as json_data_file:
        config_file = json.load(json_data_file)
else:
    print("Config file not found, quitting! Automatic configuration file generation coming soon(tm), for now use the config template on the repo.")
    exit(1)
### end of stupid config stuff ###
    
# print banner at top
print("===== PyPackage =====\n")

# option 1. install a package
print("[1] Get (update/install) a package")

# option 2. remove a package
# todo: implement
#print("[2] Remove a package")

# option 3. add a package
# todo: implement
#print("[3] Add a package")

# option 4. quit
print("[0] Quit\n")

try:
    main_menu_option = int(input("What would you like to do? "))
except ValueError:
    print("Valid base10 number not provided, quitting!")
    exit(1)

if main_menu_option == 0:
    print("Quitting!")
    exit(0)

if main_menu_option == 1:
    entry_number = 1
    entries = dict()
    for repo_entry in config_file['repo']:
        print('[' + str(entry_number) + '] ' + config_file['repo'][repo_entry]['name'])
        entries[entry_number] = repo_entry
        entry_number = entry_number + 1
    try:
        get_menu_option = int(input("What package would you like to get? "))
    except ValueError:
        print("Valid base10 number not provided, quitting!")
        exit(1)
        
    if get_menu_option in entries:
        package_temporary_directory = cache_home + entries[get_menu_option]
        print("Making temporary directory " + package_temporary_directory + "...")
        try:
            os.mkdir(package_temporary_directory)
        except FileExistsError:
            print("Temporary directory already exists! This shouldn't happen! Report as a bug!")
        print("Downloading URL " + config_file['repo'][entries[get_menu_option]]['url'] + " as pypackage_" + entries[get_menu_option] + " and placing in temporary directory...")
        package_downloader = URLGrabber(timeout = 10.0)
        package_downloader.urlgrab(config_file['repo'][entries[get_menu_option]]['url'], package_temporary_directory + "/pypackage_" + entries[get_menu_option])
        print("Figuring out library to use... ", end='')
        if tarfile.is_tarfile(package_temporary_directory + "/pypackage_" + entries[get_menu_option]) == True:
            print("Tarfile.")
            print("Extracting...")
            tar_to_open = tarfile.open(package_temporary_directory + "/pypackage_" + entries[get_menu_option], 'r')
            tar_to_open.extractall(package_temporary_directory)
            tar_to_open.close()
            os.remove(package_temporary_directory + "/pypackage_" + entries[get_menu_option])
            print("Moving...")
            if len(os.listdir(package_temporary_directory)) == 1:
                if os.path.isdir(package_temporary_directory + '/' + os.listdir(package_temporary_directory)[0]):
                    if 'dir_to_place' in config_file['repo'][entries[get_menu_option]]:
                        dir_to_place = config_file['repo'][entries[get_menu_option]]['dir_to_place']
                    else:
                        dir_to_place = config_file['dir_to_place']
                    os.rename(package_temporary_directory + '/' + os.listdir(package_temporary_directory)[0], package_temporary_directory + '/' + entries[get_menu_option])
                    shutil.move(package_temporary_directory + '/' + entries[get_menu_option], dir_to_place)
                    os.rmdir(package_temporary_directory)
                else:
                    if 'dir_to_place' in config_file['repo'][entries[get_menu_option]]:
                        dir_to_place = config_file['repo'][entries[get_menu_option]]['dir_to_place']
                    else:
                        dir_to_place = config_file['dir_to_place'] 
                    shutil.move(os.listdir(package_temporary_directory)[0], config_file['repo'][entries[get_menu_option]]['dir_to_place'])
                    os.rmdir(package_temporary_directory)
            elif len(os.listdir(package_temporary_directory)) > 1:
                if 'dir_to_place' in config_file['repo'][entries[get_menu_option]]:
                    dir_to_place = config_file['repo'][entries[get_menu_option]]['dir_to_place']
                else:
                    dir_to_place = config_file['dir_to_place']
                shutil.move(package_temporary_directory, dir_to_place)
                
            print("Done!")
                
        elif zipfile.is_zipfile(package_temporary_directory + "/" + entries[get_menu_option]) == True:
            print("Zipfile.")
            print("Extracting zips is not supported yet, but it is a priority - expect it next update. Cleaning up and quitting!")
            os.remove(package_temporary_directory + "/pypackage_" + entries[get_menu_option])
            os.rmdir(package_temporary_directory)
            exit(1)
        else:
            print("Not supported, cleaning up and quitting!")
            os.remove(package_temporary_directory + "/pypackage_" + entries[get_menu_option])
            os.rmdir(package_temporary_directory)
            exit(1)
            
        
        #file_type = subprocess.run(['file', package_temporary_directory + "/" + entries[get_menu_option]], stdout=subprocess.PIPE).stdout.decode('utf-8')
        #if regsearchmatch("executable", file_type):
        #    print("plain executable.\nNot extracting.")
        #else:
        #    print("File type not an archive!\nCleaning up and quitting...")
        
    else:
        print("Not a valid option, quitting!")
        exit(1)
    
if main_menu_option > 1:
    print("Not a valid option, quitting!")
    exit(1)