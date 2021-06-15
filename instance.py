import os
#import spur
import requests

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
    def download_instance (self, new_id):
        pass

    def __init__ (self, new_id):
        self.id = new_id
        self.workdir = os.environ.get("WORKDIR", os.environ["HOME"])



class KGV3_Instance (Instance):

    def download_instance (self):
        print ("KGV3:: Download Instance")

    def connect_to_service (self):
        token_handler = SimpleToken(os.environ["HBP_AUTH_TOKEN"])
        return KGv3(host="core.kg.ebrains.eu", token_handler=token_handler)

    def __init__ (self, new_id):
        super().__init__ (self, new_id)
        self.catalog = connect_to_service()

class KGV2_Instance (Instance):

    def download_instance (self, new_id):
        print ("KGV2:: Download Instance")

    def connect_to_service (self, username = None, password = None):
        # Connect to HBP Model Catalog
        # return ModelCatalog(os.environ["HBP_USER"], get_password())
        return ModelCatalog(username=username, password=password)

    def __init__ (self, new_id, username=None, password=None):
        super().__init__ (self, new_id)
        self.catalog = connect_to_service(username=username, password=password)
        os.environ["HBP_AUTH_TOKEN"]=self.catalog.auth.token
        download_instance (new_id)
