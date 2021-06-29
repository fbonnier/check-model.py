import os
# from hbp_validation_framework import ModelCatalog
# import requests
# import spur
from check_model import instance


if __name__ == "__main__":

    # Test new KG-v2 instantiation

    ## Define a model to try
    model_id = "803c92ff-16f5-4fea-8827-d8416fd65745" # SpiNNCer

    ## Define a working directory
    work_dir = "."

    ## Create Instance object
    model_instance = instance.KGV2_Instance(model_id, username="hplovecraft", password="TheColourOutOfSpace")
    model_instance.create_script_file(work_dir)
    model_instance.write_code_location()
    model_instance.write_goto_project_folder()
    model_instance.write_pip_installs()
    model_instance.write_download_inputs()
    model_instance.write_download_results()

    model_instance.write_code_run()
    model_instance.close_script_file()
    print (model_instance.metadata)
    # Exit Done ?
    print ("Done.\n ----- Exit SUCCESS")
