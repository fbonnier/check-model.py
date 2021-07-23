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


class KGV3_Instance (Instance):

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
        pass

    def write_code_unzip (self):
        pass

    def write_goto_project_folder(self):
        pass

    def write_pip_installs (self):
        pass

    def write_download_results (self):
        pass

    def write_download_inputs (self):
        pass

    def write_code_run (self):
        pass

    def close_script_file (self):
        pass


    def connect_to_service (self):
        token_handler = SimpleToken(os.environ["HBP_AUTH_TOKEN"])
        return KGv3(host="core.kg.ebrains.eu", token_handler=token_handler)

    def __init__ (self, new_id):
        super().__init__ (self, new_id)
        self.catalog = connect_to_service()
