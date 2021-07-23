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

    metadata = None
    # Additional data in Metadata:
    ##  html_options
    ##  archive_name
    script_file_ptr = None



    def download_instance_metadata (self):
        pass

    def create_script_file (self, work_dir):
        print ("create_script_file ==> START")
        # Error if metadata empty
        if (not self.metadata):
            print_error ("create_script_file :: meta_data empty", exit_type="fail")
            exit(EXIT_FAILURE)

        # Metadata not empty
        self.script_file_ptr = open ("run_me.sh", "a")
        # f = open (WORKDIR + "/run_me.sh", "a")
        self.script_file_ptr.write("#!/bin/bash\n")
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

    def write_code_unzip (self):
        print ("write_code_unzip ==> START")
        is_archive = [self.metadata["archive_name"].endswith(format) for format in archive_format]
        try:
            idx = is_archive.index(True)
            # filename = var_download_command.split("/")
            self.script_file_ptr.write ("arc -overwrite unarchive " + self.workdir + "/" + self.metadata["archive_name"] + " " + self.workdir + "/" + self.id + "\n")
        except ValueError as e:
            print_error ("write_code_unzip", "fail")
            print (e)
            self.script_file_ptr.close()
            exit (EXIT_FAILURE)
        print ("write_code_unzip ==> END")


    def write_goto_project_folder(self):
        print ("write_goto_project_folder ==> START")
        # CD to project base folder
        print ("Go to project root folder")
        self.script_file_ptr.write("cd " + self.workdir + "/" + self.id + "\n")
        self.script_file_ptr.write("while [ $(ls -l | grep -v ^d | wc -l) -lt 2 ]\ndo\nif [ -d $(ls) ]; then \ncd $(ls);\nfi\ndone" + "\n\n")
        print ("write_goto_project_folder ==> END")

    def close_script_file (self):
        print ("close_script_file ==> START")
        self.script_file_ptr.close()
        print ("close_script_file ==> END")

    def __init__ (self, new_id):
        self.id = new_id
        self.workdir = os.environ.get("WORKDIR", os.environ["HOME"])
