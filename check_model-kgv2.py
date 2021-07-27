import os
from check_model import instance_kgv2 as instance

if __name__ == "__main__":

    # Test new KG-v2 instantiation

    ## Define a model to try
    model_id = os.environ["HBP_INSTANCE_ID"] # SpiNNCer

    ## Define a working directory
    work_dir = "."
    auth_token = os.environ.get("HBP_AUTH_TOKEN", None)
    auth_user = os.environ["HBP_USER"]
    auth_pass = os.environ["HBP_PASSWORD"]

    ## Create Instance object
    model_instance = instance.KGV2_Instance(model_id, username=auth_user, password=auth_pass, token=auth_token)
    model_instance.create_script_file(work_dir)
    model_instance.write_code_location()
    model_instance.write_code_unzip ()
    model_instance.write_goto_project_folder()
    model_instance.write_pip_installs()
    model_instance.write_download_inputs()
    model_instance.write_download_results()

    model_instance.write_watchdog() 
    model_instance.write_code_run()
    model_instance.close_script_file()
    print (model_instance.metadata)
    # Exit Done ?
    print ("Done.\n ----- Exit SUCCESS")
