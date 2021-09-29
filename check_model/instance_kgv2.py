import os

import requests
import json
import hashlib

#HBP-Validation-Framework
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

        # Check if 'parameters' exist
        # If 'parameters' does not exist, the model will not run as the run instruction is unknown
        if "parameters" not in self.metadata or not self.metadata["parameters"]:
            instance.print_error ("No parameters specidied in the model, the run instruction is Unkown", "fail")
            exit (instance.EXIT_FAILURE)
        self.metadata["parameters"] = json.loads(self.metadata["parameters"])

        # Check if 'run' instruction exists in 'parameters'
        if "run" not in self.metadata["parameters"]:
            instance.print_error ("The run instruction is Unkown", "fail")
            exit (instance.EXIT_FAILURE)

        #Initialize metadata parameters
        if "pip_installs" not in self.metadata["parameters"]:
            self.metadata["parameters"]["pip_installs"] = ""
        if "inputs" not in self.metadata["parameters"]:
            self.metadata["parameters"]["inputs"] = {}
        if "results" not in self.metadata["parameters"]:
            self.metadata["parameters"]["results"] = {}

        self.parse_html_options ()
        print ("KGV2 :: Get model instance metadata ==> END")

    def write_download_results (self):
        print ("KGV2 :: write_download_results ==> START")
        self.script_file_ptr.write ("# Download and place expected results in WORKDIR/expected_results/\n")
        self.script_file_ptr.write ("mkdir " + self.workdir + "expected_results/\n")
        with open (self.workdir + "/list_results.txt", "w") as result_list:
            result_data = []
            if self.metadata["parameters"]["results"]:
                for iresult in self.metadata["parameters"]["results"]:
                    # print ("I-Result filename : " + str(iresult.split("/")[-1]))
                    result_hash = hashlib.md5(b'iresult').hexdigest()
                    result_data.append({"url": iresult, "hash": result_hash})
                    # result_list.write (iresult.split("/")[-1])
                    # result_list.write("\n")
                    # print ("I-Result hash : " + str(result_hash.digest()) + "\n")
                    # self.script_file_ptr.write ("wget -N " + iresult + " -O " + self.workdir + "expected_results/" + iresult.replace("/", ".") + "\n")
                    self.script_file_ptr.write ("wget -N " + iresult + " -O " + self.workdir + "expected_results/" + str(result_hash) + "\n")
            self.script_file_ptr.write ("\n")
            json.dump(result_data, result_list)
        result_list.close()
        print ("KGV2 :: write_download_results ==> END")

    def write_download_inputs (self):
        print ("KGV2 :: write_download_inputs ==> START")
        self.script_file_ptr.write ("# Download and place inputs\n")
        if self.metadata["parameters"]["inputs"]:
            for iinput in self.metadata["parameters"]["inputs"]:
                if iinput["url"] and iinput["destination"]:
                    self.script_file_ptr.write ("wget -N " + iinput["url"] + " --directory-prefix=./" + iinput["destination"] + "\n")

        self.script_file_ptr.write ("\n")
        print ("KGV2 :: write_download_inputs ==> END")

    def write_code_run (self):
        print ("KGV2 :: write_code_run ==> START")
        self.script_file_ptr.write ("# Run instruction\n")
        if self.metadata["parameters"]["run"]:
            self.script_file_ptr.write(self.metadata["parameters"]["run"] + "\n")
        else:
            instance.print_error ("No run script specified", "fail")
            self.script_file_ptr.close()
            exit(instance.EXIT_FAILURE)
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
