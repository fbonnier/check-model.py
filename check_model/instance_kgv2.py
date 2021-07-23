import os
#import spur
import requests
import json
# hbp-validation-framework
from hbp_validation_framework import ModelCatalog
import instance

# KG-v3, KG-Core Python Interface
from kg_core.oauth import SimpleToken
from kg_core.kg import KGv3
from kg_core.models import Stage
from kg_core.models import Pagination

class KGV2_Instance (Instance):

    def download_instance_metadata (self):
        print ("KGV2:: Download Instance")
        print ("KGV2 :: Get model instance metadata ==> START")
        self.metadata = self.catalog.get_model_instance(instance_id=self.id)
        self.metadata["parameters"] = json.loads(self.metadata["parameters"])
        self.parse_html_options ()
        print ("KGV2 :: Get model instance metadata ==> END")

    def create_script_file (self, work_dir):
        super().create_script_file(work_dir)

    def parse_html_options (self):
        super().parse_html_options()

    def write_code_location (self):
        print ("KGV2 :: write_code_location ==> START")
        # If file pointer is Null, exit fail
        if not self.script_file_ptr:
            print_error("KGV2::write_code_location:: Null file pointer", exit_type="fail")

        print (self.metadata["source"])

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
                print ("KGV2 :: write_code_location ==> END")
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
                        print ("KGV2 :: write_code_location ==> END")
                        return

                print("Try to get release archive from version number ... FAIL")
                print_error (self.metadata["source"] + " does not provide archive release, try to clone GIT project.", "continue")
                self.script_file_ptr.write ("git clone " + self.metadata["source"] + " " + self.workdir  + "/" + self.id + "\n")
                print ("KGV2 :: write_code_location ==> END")
                self.metadata["archive_name"] = self.metadata["source"].split("/")[-1]
                return
            else :
                # Git clone project
                print_error (self.metadata["source"] + " does not have version number, try to clone GIT project.", "continue")
                self.script_file_ptr.write ("git clone " + self.metadata["source"] + " " + self.workdir + "/" + self.id + "\n")
                self.metadata["archive_name"] = self.metadata["source"].split("/")[-1]
                print ("KGV2 :: write_code_location ==> END")
                return

        # Error :: the source does not exists or source pattern not taken into account
        print_error (self.metadata["source"] + " (" + self.metadata["version"] + ")' does not exist or service not available.", "fail")
        self.script_file_ptr.close()
        exit (EXIT_FAILURE)

    def write_code_unzip (self):
        super().write_code_unzip()

    def write_goto_project_folder(self):
        super().write_goto_project_folder()

    def write_pip_installs (self):
        print ("KGV2 :: write_pip_installs ==> START")
        self.script_file_ptr.write ("# Additional PIP packages\n")
        # TODO : try-catch to catch missing pip_install parameter
        try :
            if self.metadata["parameters"]["pip_installs"]:
                print ("Installing additional PIP packages")
                for ipackage in self.metadata["parameters"]["pip_installs"]:
                    self.script_file_ptr.write ("pip install " + ipackage + "\n")
                self.script_file_ptr.write ("\n")
            else:
                print ("No additional PIP package to install")
                self.script_file_ptr.write ("# No additional packages to install\n\n")
        except ValueError as e:
            print_error ("KGV2::write_pip_installs", "fail")
            print (e)
            self.script_file_ptr.close()
            exit (EXIT_FAILURE)
        print ("KGV2 :: write_pip_installs ==> END")

    def write_download_results (self):
        print ("KGV2 :: write_download_results ==> START")
        self.script_file_ptr.write ("# Download and place expected results\n")
        self.script_file_ptr.write ("# TODO\n")
        self.script_file_ptr.write ("\n")
        print ("----- TODO -----")
        print ("KGV2 :: write_download_results ==> END")

    def write_download_inputs (self):
        print ("KGV2 :: write_download_inputs ==> START")
        self.script_file_ptr.write ("# Download and place inputs\n")
        self.script_file_ptr.write ("# TODO\n")
        self.script_file_ptr.write ("\n")
        print ("----- TODO -----")
        print ("KGV2 :: write_download_inputs ==> END")

    def write_code_run (self):
        print ("KGV2 :: write_code_run ==> START")
        # runscript_file = self.id + ".sh"
        # self.script_file_ptr.write("cp " + self.workdir + "/" + runscript_file + " ." + "\n")
        # self.script_file_ptr.write("pwd; ls -alh;" + "\n")
        # self.script_file_ptr.write("chmod +x ./" + runscript_file + "\n")
        # self.script_file_ptr.write("echo \"TODO : Get INPUT and RESULTS\"" + "\n")
        # self.script_file_ptr.write("./" + runscript_file + "\n")
        self.script_file_ptr.write ("# Run instruction\n")
        if self.metadata["parameters"]["run"]:
            self.script_file_ptr.write(self.metadata["parameters"]["run"] + "\n")
        else:
            print_error ("No run script specified", "fail")
            self.script_file_ptr.close()
            exit(EXIT_FAILURE)
        print ("KGV2 :: write_code_run ==> END")

    def close_script_file (self):
        super().close_script_file()

    def connect_to_service (self, username = None, password = None):
        # Connect to HBP Model Catalog
        # return ModelCatalog(os.environ["HBP_USER"], get_password())
        return ModelCatalog(username=username, password=password)

    def __init__ (self, new_id, username=None, password=None):
        super().__init__ (new_id)
        self.catalog = self.connect_to_service(username=username, password=password)
        os.environ["HBP_AUTH_TOKEN"]=self.catalog.auth.token
        self.download_instance_metadata ()
