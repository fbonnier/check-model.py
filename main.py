import os
from check_model import instance_kgv2 as instance2
from check_model import instance_kgv3 as instance3

if __name__ == "__main__":

    # Test new KG-v2 instantiation

    ## Define a model to try
    model_id = os.environ["HBP_INSTANCE_ID"] # SpiNNCer

    ## Define a working directory
    work_dir = os.environ.get("WORKDIR", os.environ["HOME"])
    auth_token = os.environ.get("HBP_AUTH_TOKEN", None)
    auth_user = os.environ["HBP_USER"]
    auth_pass = os.environ["HBP_PASSWORD"]
    kg_version = int(os.environ["KG_VERSION"])
    if kg_version != 2 and kg_version != 3:
        print ("Error :: KG_VERSION=" + str(kg_version) + " Unknown")
        exit (1)

    model_instance = None
    if kg_version == 2:
        ## Create Instance object
        model_instance = instance2.KGV2_Instance(model_id, username=auth_user, password=auth_pass, token=auth_token)
    if kg_version == 3:
        ## Create Instance object
        print ("HBP_AUTH_TOKEN = " + str(auth_token))
        model_instance = instance3.KGV3_Instance(model_id, token=auth_token)

    print ("Authentification Success")

    model_instance.create_script_file(work_dir)
    model_instance.write_code_location()
    model_instance.write_code_unzip ()
    model_instance.write_goto_project_folder()
    model_instance.write_pip_installs()
    model_instance.write_download_inputs()
    model_instance.write_download_results()

    model_instance.write_watchdog()
    model_instance.write_code_run()
    model_instance.write_watchdog_kill()
    model_instance.close_script_file()
    print (model_instance.metadata)
    # Exit Done ?
    print ("Done.\n ----- Exit SUCCESS")
