import os
#import spur
import requests
import json
# hbp-validation-framework
from hbp_validation_framework import ModelCatalog

# KG-v3, KG-Core Python Interface
from kg_core.oauth import SimpleToken
from kg_core.kg import KGv3
from kg_core.models import Stage
from kg_core.models import Pagination

# Fuzzy String comparisons
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
error_msgs = {"continue":"\n----- Continue", "success":"\n----- Exit SUCCESS", "fail":"\n----- Exit FAIL"}

archive_format = [".tar.gz", ".tar", ".zip", ".rar"]
main_repo = {"github": {"pattern": "https://github.com", "tar_url":"", "source": "", "file": "git-download.txt", "download_command": "git clone "},
             "cscs": {"pattern": "https://object.cscs.ch", "tar_url":"", "source": "", "file": "cscs-download.txt", "download_command": "wget -N "},
             "testing": {"pattern": "http://example.com", "tar_url":"", "source": "", "file": "no-download.txt", "download_command": ""},
             }

def print_error (error_msg, exit_type=None):
    print ((("Error :: ") if exit_type!="success" else "Message :: ") + str (error_msg) + ((" " + error_msgs[exit_type]) if exit_type!=None else ""))

#def get_password ():

#    cmd = "pass show HBP/model-catalog"
#    pswd = spur.LocalShell().run(cmd.split(), encoding="utf-8")
#    toreturn = pswd.output.strip()
#    if (toreturn.startswith("Error:")):
#        print_error (toreturn + "\nTry to log with HBP_PASS environment variable.", "continue")
#        toreturn = os.environ["HBP_PASS"]
#        if not toreturn :
#            print_error ("Error :: HBP_PASS must be set.", "fail")
#            exit(EXIT_FAILURE)
#    return toreturn


class Instance:
    def get_id (self):
        return None
    def get_source (self):
        return None
    def get_version (self):
        return None
    def get_authors (self):
        return [None]
    def get_custodians (self):
        return [None]
    def connect_to_service (self):
        return None

    id = None
    catalog = None
    workdir = ""
    watchdog_pid = None

    metadata = dict()
    # Additional data in Metadata:
    ##  html_options
    ##  archive_name
    script_file_ptr = None

    def get_watchdog (self):
        # Get watchdog/watchmedo instructions
        print ("get_watchdog ==> START")
        print ("get_watchdog ==> END")
        return ("watchmedo shell-command --patterns='*' --recursive --command='echo ${watch_src_path}' . & WATCHDOG_PID=$!\n")

    def write_watchdog (self):
        # Write watchdog/watchmedo instructions
        print ("write_watchdog ==> START")
        assert (self.script_file_ptr != None)
        self.script_file_ptr.write(self.get_watchdog ())
        print ("write_watchdog ==> END")

    def write_watchdog_kill (self):
        # Write instruction to kill Watchdog from PID
        print ("write_watchdog_kill ==> START")
        assert (self.script_file_ptr != None)
        self.script_file_ptr.write("kill -15 $WATCHDOG_PID\n\n")
        print ("write_watchdog_kill ==> END")



    def download_instance_metadata (self):
        pass

    def create_script_file (self, work_dir):
        print ("create_script_file ==> START")
        # Error if metadata empty
        if (not self.metadata):
            print_error ("create_script_file :: meta_data empty", exit_type="fail")
            exit(EXIT_FAILURE)

        # Metadata not empty
        print ("WORKDIR  = " + work_dir)
        self.script_file_ptr = open (work_dir + "/run_me.sh", "w")
        # f = open (WORKDIR + "/run_me.sh", "a")
        self.script_file_ptr.write("#!/bin/bash\n\n")
        runscript_file = work_dir + self.id + ".sh"
        self.workdir = work_dir
        print ("create_script_file ==> END")

    def parse_html_options (self):
        print ("parse_html_options ==> START")
        html_options = {}

        # If there are html options in the link
        if "?" in self.metadata["source"]:
            list_of_options = self.metadata["source"].split("?")[1].split("&")
            self.metadata["source"] = self.metadata["source"].split("?")[0]
            for i_option in list_of_options:
                html_options [i_option.split("=")[0]] = i_option.split("=")[1]

        self.metadata["html_options"] = html_options
        print ("parse_html_options ==> END")

    def get_code_location (self):
        print ("get_code_location ==> START")
        cmd_to_return = ""

        # If source is archive, WGET archive file
        is_archive = [self.metadata["source"].endswith(format) for format in archive_format]
        try:
            # Source is an archive
            idx = is_archive.index(True)
            response = requests.get(self.metadata["source"], stream=True)
            if (response.ok):
                cmd_to_return = "wget -N --directory-prefix=" + self.workdir + " " + self.metadata["source"]
                self.metadata["archive_name"] = self.metadata["source"].split("/")[-1]
                print ("get_code_location ==> END")
                return cmd_to_return
            else :
                print_error (self.metadata["source"] + "' Response status = " + str(response.status_code), "fail")
                exit(EXIT_FAILURE)
        except ValueError:
            # Source is not archive
            print_error (self.metadata["source"] + " is not an archive. Let's try something else ...", "continue")

        # If source is git repo
        if (self.metadata["source"].startswith(main_repo["github"]["pattern"])):
            # If model has version number, try to get archive file of version
            print ("Source is GIT repository")
            if (self.metadata["version"]):
                # For all archive format, ping the file
                print("Try to get release archive from version number ...")
                for format in archive_format:
                    tar_url = self.metadata["source"] + "/archive/v" + self.metadata["version"] + format
                    response = requests.get(tar_url, stream=True)
                    if(response.ok):
                        cmd_to_return = "wget -N --directory-prefix=" + self.workdir + " " + tar_url
                        self.metadata["archive_name"] = tar_url.split("/")[-1]
                        print("Try to get release archive from version number ... SUCCESS")
                        print ("get_code_location ==> END")
                        return cmd_to_return

                print("Try to get release archive from version number ... FAIL")
                print_error (self.metadata["source"] + " does not provide archive release, try to clone GIT project.", "continue")
                cmd_to_return = "git clone " + self.metadata["source"] + " " + self.workdir  + "/" + self.id
                print ("get_code_location ==> END")
                self.metadata["archive_name"] = self.metadata["source"].split("/")[-1]
                return cmd_to_return
            else :
                # Git clone project
                print_error (self.metadata["source"] + " does not have version number, try to clone GIT project.", "continue")
                cmd_to_return = "git clone " + self.metadata["source"] + " " + self.workdir + "/" + self.id
                self.metadata["archive_name"] = self.metadata["source"].split("/")[-1]
                print ("get_code_location ==> END")
                return cmd_to_return

        # Error :: the source does not exists or source pattern not taken into account
        print_error (self.metadata["source"] + " (" + self.metadata["version"] + ")' does not exist or service not available.", "fail")
        exit (EXIT_FAILURE)

    def write_code_location (self):
        print ("write_code_location ==> START")
        # If file pointer is Null, exit fail
        if not self.script_file_ptr:
            print_error("write_code_location:: Null file pointer", exit_type="fail")

        self.script_file_ptr.write ("# Download Instance Code\n")

        # Else get code location
        # If source is archive, WGET archive file
        is_archive = [self.metadata["source"].endswith(format) for format in archive_format]
        try:
            # Source is an archive
            idx = is_archive.index(True)
            response = requests.get(self.metadata["source"], stream=True)
            if (response.ok):
                self.script_file_ptr.write ("wget -N --directory-prefix=" + self.workdir + " " + self.metadata["source"] + "\n")
                self.metadata["archive_name"] = self.metadata["source"].split("/")[-1]
                print ("write_code_location ==> END")
                self.script_file_ptr.write ("\n")
                return
            else :
                print_error (self.metadata["source"] + "' Response status = " + str(response.status_code), "fail")
                self.script_file_ptr.close()
                exit(EXIT_FAILURE)
        except ValueError:
            # Source is not archive
            print_error (self.metadata["source"] + " is not an archive. Let's try something else ...", "continue")


        # If source is git repo
        if (self.metadata["source"].startswith(main_repo["github"]["pattern"])):
            # If model has version number, try to get archive file of version
            print ("Source is GIT repository")
            if (self.metadata["version"]):
                # For all archive format, ping the file
                print("Try to get release archive from version number ...")
                for format in archive_format:
                    tar_url = self.metadata["source"] + "/archive/v" + self.metadata["version"] + format
                    response = requests.get(tar_url, stream=True)
                    if(response.ok):
                        self.script_file_ptr.write ("wget -N --directory-prefix=" + self.workdir + " " + tar_url + "\n")
                        self.metadata["archive_name"] = tar_url.split("/")[-1]
                        print("Try to get release archive from version number ... SUCCESS")
                        print ("write_code_location ==> END")
                        self.script_file_ptr.write ("\n")
                        return

                print("Try to get release archive from version number ... FAIL")
                print_error (self.metadata["source"] + " does not provide archive release, try to clone GIT project.", "continue")
                self.script_file_ptr.write ("git clone " + self.metadata["source"] + " " + self.workdir  + "/" + self.id + "\n")
                print ("write_code_location ==> END")
                self.metadata["archive_name"] = self.metadata["source"].split("/")[-1]
                self.script_file_ptr.write ("\n")
                return
            else :
                # Git clone project
                print_error (self.metadata["source"] + " does not have version number, try to clone GIT project.", "continue")
                self.script_file_ptr.write ("git clone " + self.metadata["source"] + " " + self.workdir + "/" + self.id + "\n")
                self.metadata["archive_name"] = self.metadata["source"].split("/")[-1]
                print ("write_code_location ==> END")
                self.script_file_ptr.write ("\n")
                return

        # Error :: the source does not exists or source pattern not taken into account
        print_error (self.metadata["source"] + " (" + self.metadata["version"] + ")' does not exist or service not available.", "fail")
        self.script_file_ptr.close()
        exit (EXIT_FAILURE)

    def write_code_unzip (self):
        print ("write_code_unzip ==> START")
        is_archive = [self.metadata["archive_name"].endswith(format) for format in archive_format]
        try:
            idx = is_archive.index(True)
            # filename = var_download_command.split("/")
            self.script_file_ptr.write ("arc -overwrite unarchive " + self.workdir + "/" + self.metadata["archive_name"] + " " + self.workdir + "/" + self.id + "\n")
        except ValueError as e:
            print_error ("write_code_unzip :: " + self.metadata["archive_name"] + " is not a recognized archive format", "fail")
            # print (e)
            # self.script_file_ptr.close()
            # exit (EXIT_FAILURE)
        print ("write_code_unzip ==> END")


    def write_goto_project_folder(self):
        print ("write_goto_project_folder ==> START")
        # CD to project base folder
        print ("Go to project root folder")
        self.script_file_ptr.write("# Go to Instance's root repository\n")
        self.script_file_ptr.write("cd " + self.workdir + "/" + self.id + "\n")
        self.script_file_ptr.write("while [ $(ls -l | grep -v ^d | wc -l) -lt 2 ]\ndo\nif [ -d $(ls) ]; then \ncd $(ls);\nfi\ndone" + "\n\n")
        print ("write_goto_project_folder ==> END")

    def write_pip_installs (self):
        print ("write_pip_installs ==> START")
        self.script_file_ptr.write ("# Additional PIP packages\n")
        # TODO : try-catch to catch missing pip_install parameter
        try :
            if self.metadata["parameters"]["pip_installs"]:
                print ("Installing additional PIP packages")
                for ipackage in self.metadata["parameters"]["pip_installs"]:
                    self.script_file_ptr.write ("pip3 install " + ipackage + "\n")
                self.script_file_ptr.write ("\n")
            else:
                print ("No additional PIP package to install")
                self.script_file_ptr.write ("# No additional packages to install\n\n")
        except ValueError as e:
            print_error ("write_pip_installs", "fail")
            print (e)
            self.script_file_ptr.close()
            exit (EXIT_FAILURE)
        print ("write_pip_installs ==> END")

    def close_script_file (self):
        print ("close_script_file ==> START")
        self.script_file_ptr.close()
        print ("close_script_file ==> END")

    def __init__ (self, new_id):
        self.id = new_id
        self.workdir = os.environ.get("WORKDIR", os.environ["HOME"])
