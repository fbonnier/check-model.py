import os
import sys
import argparse
from check_model import instance_kgv2 as instance2
from check_model import instance_kgv3 as instance3
from check_model import instance as instance

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate HBP model instance runscript from instance ID or metadata JSON file")

    # parser.add_argument("--id", type=str, metavar="Model Instance ID", nargs=1, dest="id", default=os.environ.get(["HBP_INSTANCE_ID"], ""),\
    # help="ID of the Instance to download")

    # parser.add_argument("--token", type=str, metavar="Authentification Token", nargs=1, dest="token", default=os.environ.get("HBP_AUTH_TOKEN", None),\
    # help="Authentification Token used to log to EBRAINS")

    parser.add_argument("--json", type=argparse.FileType('r'), metavar="JSON Metadata file", nargs=1, dest="json", default="",\
    help="JSON File that contains Metadata of the HBP model to run")

    parser.add_argument("--workdir", type=str, metavar="Working Directory", nargs=1, dest="workdir", default=os.environ.get("WORKDIR", "./"),\
    help="Working directory")

    # parser.add_argument("--kg", type=int, metavar="KG Version", nargs=1, dest="kg", default=int(os.environ.get("KG_VERSION", 2)),\
    # help="Version number of Knowledge Graph to use")

    args = parser.parse_args()


    # Test new KG-v2 instantiation

    ## Define a model to try
    # model_id = args.id[0]
    # if not model_id:
    #     print ("Error: Instance ID not recognized", file=sys.stderr)
    #     exit(1)

    ## Define a working directory
    work_dir = args.workdir[0]

    # auth_token = os.environ.get("HBP_AUTH_TOKEN", None)
    # if args.token:
    # auth_token = args.token[0]
    # if not auth_token:
    #     print ("Error: Authentification Token not recognized", file=sys.stderr)
    #     exit(1)

    # auth_user = os.environ["HBP_USER"]
    # auth_pass = os.environ["HBP_PASSWORD"]

    # kg_version = args.kg
    # if kg_version != 2 and kg_version != 3:
    #     print ("Error: KG_VERSION=" + str(kg_version) + " Unknown", file=sys.stderr)
    #     exit (1)

    json_file = args.json[0]
    if not json_file:
        print ("Fatal Error:  Invalid JSON File, please give a valid JSON file using \"--json myfile\"")
        exit(1)

    model_instance = None
    # if kg_version == 2:
    #     ## Create Instance object
    #     model_instance = instance2.KGV2_Instance(model_id, token=auth_token)
    # if kg_version == 3:
    #     ## Create Instance object
    #     model_instance = instance3.KGV3_Instance(model_id, token=auth_token)
    model_instance = instance.Instance(json_file.name)


    model_instance.create_script_file(work_dir)
    model_instance.write_code_location()
    model_instance.write_code_unzip ()
    model_instance.write_goto_project_folder()
    model_instance.write_download_inputs()
    model_instance.write_pip_installs()
    # model_instance.write_download_results()

    model_instance.write_watchdog()
    model_instance.write_code_run()
    model_instance.write_watchdog_kill()
    model_instance.close_script_file()
    print (model_instance.metadata)
    # Exit Done ?
    print ("Done.\n ----- Exit SUCCESS")
