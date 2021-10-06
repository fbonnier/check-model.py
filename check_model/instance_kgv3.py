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

# Source server from which the ALREADY KG-v3 instances are downloaded
# Default is Official KG-v3 server
SOURCE_SERVER = "https://core.kg.ebrains.eu"


class KGV3_Instance (instance.Instance):

    def download_instance_metadata (self):
        print ("KGV3:: Download Instance")
        print ("KGV3 :: Get model instance metadata ==> START")
        kgv3_instance_metadata = self.catalog.get_instance(stage=Stage.IN_PROGRESS, instance_id=self.id).data()
        print (kgv3_instance_metadata)
        print ("\n\n")
        # Get source repo
        self.metadata["source"] = self.catalog.get_instance(stage=Stage.IN_PROGRESS, instance_id=kgv3_instance_metadata["https://openminds.ebrains.eu/vocab/repository"][0]["@id"].split("/")[-1]).data()["https://openminds.ebrains.eu/vocab/name"]
        # self.metadata["inputs"] = self.catalog.get_instance(stage=Stage.IN_PROGRESS, instance_id=kgv3_instance_metadata["https://openminds.ebrains.eu/vocab/repository"][0]["@id"].split("/")[-1]).data()

        # Try to get outputs
        try:
            self.metadata["outputs"] = [self.catalog.get_instance(stage=Stage.IN_PROGRESS, instance_id=item["@id"].split("/")[-1]).data()["https://openminds.ebrains.eu/vocab/IRI"] for item in kgv3_instance_metadata["https://openminds.ebrains.eu/vocab/outputData"]]
        except KeyError as e:
            print (e)
            print_error("No ouputs, please choose of a model instance that provides outputs", "fail")
            exit(EXIT_FAILURE)
        print (self.metadata)
        ## self.metadata = self.catalog.get_model_instance(instance_id=self.id)
        ## self.metadata["parameters"] = json.loads(self.metadata["parameters"])
        # self.parse_html_options ()

        # Get parameters
        # TODO


        print ("KGV3 :: Get model instance metadata ==> END")

    def create_script_file (self, work_dir):
        super().create_script_file(work_dir)

    def parse_html_options (self):
        super().parse_html_options()

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


    def connect_to_service (self, token):
        token_handler = SimpleToken(token)
        return KGv3(host=SOURCE_SERVER, token_handler=token_handler)

    def __init__ (self, new_id, token):
        super().__init__ (new_id)
        self.catalog = self.connect_to_service(token)
        self.download_instance_metadata ()
