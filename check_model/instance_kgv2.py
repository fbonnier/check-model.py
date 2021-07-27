import os
#import spur
import requests
import json
# hbp-validation-framework
from hbp_validation_framework import ModelCatalog
import check_model.instance as instance

# KG-v3, KG-Core Python Interface
from kg_core.oauth import SimpleToken
from kg_core.kg import KGv3
from kg_core.models import Stage
from kg_core.models import Pagination

class KGV2_Instance (instance.Instance):

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

    def get_code_location (self):
        return super().get_code_location()

    def write_code_location (self):
        super().write_code_location()

    def write_code_unzip (self):
        super().write_code_unzip()

    def write_goto_project_folder(self):
        super().write_goto_project_folder()

    def write_pip_installs (self):
        super().write_pip_installs()
        
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

    def connect_to_service (self, username = None, password = None, token = None):
        # Connect to HBP Model Catalog
        # return ModelCatalog(os.environ["HBP_USER"], get_password())
        return ModelCatalog(username=username, password=password, token=token)
        # return ModelCatalog()

    def __init__ (self, new_id, username=None, password=None, token=None):
        super().__init__ (new_id)
        self.catalog = self.connect_to_service(username=username, password=password, token=token)
        # os.environ["HBP_AUTH_TOKEN"]=self.catalog.auth.token
        self.download_instance_metadata ()
