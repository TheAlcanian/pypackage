"""
A script to download, update and remove software from a set list of links.
Requires urlgrabber (you can get it from pip: pip3 install urlgrabber).
"""
import os
import json
import zipfile
import tarfile
import shutil
from sys import exit as sysexit
from urlgrabber.grabber import URLGrabber

### stupid config stuff ###
cache_home = os.environ.get("XDG_CACHE_HOME", os.environ["HOME"] + "/.cache") + "/pypackage/"
config_home = os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config") + "/pypackage/"
try:
    os.mkdir(cache_home)
    os.mkdir(config_home)
except FileExistsError:
    pass
pathcheck = os.path.exists(config_home + "config.json")
if pathcheck:
    with open(config_home + "config.json", "r+") as json_data_file:
        config_file = json.load(json_data_file)
else:
    print(
        "Config file not found, quitting! Automatic configuration file generation coming soon(tm), for now use the config template on the repo."
    )
    sysexit(1)
### end of stupid config stuff ###

# print banner at top
print("===== PyPackage =====\n")

# option 1. install a package
print("[1] Get (update/install) a package")

# option 2. remove a package
# print("[2] Remove a package")

# option 3. add a package
# print("[3] Add a package")

# option 4. quit
print("[0] Quit\n")

try:
    # get input, store as int
    main_menu_option = int(input("What would you like to do? "))
except ValueError:
    # if not a base10 num, die
    print("Valid base10 number not provided, quitting!")
    sysexit(1)

if main_menu_option == 0:
    # quit
    print("Quitting!")
    sysexit(0)

if main_menu_option == 1:
    # get a package
    # we are on entry number 1
    entry_number = 1
    # entries is an empty dict
    entries = dict()
    # for each package added to repos
    for repo_entry in config_file["repo"]:
        # print it out
        print("[" + str(entry_number) + "] " + config_file["repo"][repo_entry]["name"])
        # add it to entries dict
        entries[entry_number] = repo_entry
        # bump entry number
        entry_number = entry_number + 1
    try:
        # get input, store as int
        get_menu_option = int(input("What package would you like to get? "))
    except ValueError:
        # if not base 10 num, die
        print("Valid base10 number not provided, quitting!")
        sysexit(1)

    if get_menu_option in entries:
        # if input int is in entries
        # make a new var package, set it to the current repo package's name
        package = entries[get_menu_option]
        # package temp dir, xdg cache home + repo package name
        package_temp_dir = cache_home + package
        # package url, repo package url
        package_url = config_file["repo"][package]["url"]
        # package "name", misleading, actually the pretty name with spaces n things
        package_name = config_file["repo"][package]["name"]
        # if we have special instructions on where to put the files
        if "dir_to_place" in config_file["repo"][package]:
            # follow those
            dir_to_place = config_file["repo"][package]["dir_to_place"]
        else:
            # otherwise use the global instructions
            dir_to_place = config_file["dir_to_place"]
        print("Making temporary directory " + package_temp_dir + "...")
        # make temporary directory; where we will put package files
        try:
            os.mkdir(package_temp_dir)
        except FileExistsError:
            # if temp directory exists, barf at the user but don't die
            print("Temporary directory already exists! This shouldn't happen! Report as a bug!")
        print(
            "Downloading URL "
            + package_url
            + " as pypackage_"
            + package
            + " and placing in temporary directory..."
        )
        # set up urlgrabber timeout; all good programs should have one
        package_downloader = URLGrabber(timeout=10.0)
        # download a file from package's url; store in the temp directory
        package_downloader.urlgrab(
            config_file["repo"][package]["url"], package_temp_dir + "/pypackage_" + package
        )
        print("Figuring out library to use... ", end="")
        # figure out python library to use on the file we just downloaded
        if tarfile.is_tarfile(package_temp_dir + "/pypackage_" + package):
            print("Tarfile.")
            print("Extracting...")
            # tar to open; tells tarfile to open the file we downloaded as read only
            tar_to_open = tarfile.open(package_temp_dir + "/pypackage_" + package, "r")
            # extract everything in file
            tar_to_open.extractall(package_temp_dir)
            # close file
            tar_to_open.close()
            # remove original archive
            os.remove(package_temp_dir + "/pypackage_" + package)
            print("Moving...")
            # if there's only one file in the extracted remains of the file we downloaded
            if len(os.listdir(package_temp_dir)) == 1:
                # is it a dir?
                if os.path.isdir(package_temp_dir + "/" + os.listdir(package_temp_dir)[0]):
                    # if it is, just rename it and throw it in the place we're told to
                    os.rename(
                        package_temp_dir + "/" + os.listdir(package_temp_dir)[0],
                        package_temp_dir + "/" + package,
                    )
                    shutil.move(package_temp_dir + "/" + package, dir_to_place)
                    # remove temporary dir
                    os.rmdir(package_temp_dir)
                else:
                    # if its not a dir
                    # move it to where we're told to
                    shutil.move(os.listdir(package_temp_dir)[0], config_file["repo"][package]["dir_to_place"])
                    # remove temp dir
                    os.rmdir(package_temp_dir)
            elif len(os.listdir(package_temp_dir)) > 1:
                # if there's more than one file
                # move the temporary directory to where we were told
                shutil.move(package_temp_dir, dir_to_place)

            print("Done!")

        elif zipfile.is_zipfile(package_temp_dir + "/" + package):
            # if file is zip, clean up, print special message and die
            print("Zipfile.")
            print(
                "Extracting zips is not supported yet, but it is a priority - expect it next update. Cleaning up and quitting!"
            )
            os.remove(package_temp_dir + "/pypackage_" + package)
            os.rmdir(package_temp_dir)
            sysexit(1)
        else:
            # if the file isnt a tar or a zip, clean up and die
            print("Not supported, cleaning up and quitting!")
            os.remove(package_temp_dir + "/pypackage_" + package)
            os.rmdir(package_temp_dir)
            sysexit(1)
    else:
        print("Not a valid option, quitting!")
        sysexit(1)

if main_menu_option > 1:
    print("Not a valid option, quitting!")
    sysexit(1)
