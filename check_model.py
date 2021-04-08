import os
from hbp_validation_framework import ModelCatalog
import requests
import spur

main_repo = {"github": {"pattern": "https://github.com", "tar_url":"", "source": "", "file": "git-download.txt", "download_command": "git clone "},
             "cscs": {"pattern": "https://object.cscs.ch", "tar_url":"", "source": "", "file": "cscs-download.txt", "download_command": "wget -N "},
             "testing": {"pattern": "http://example.com", "tar_url":"", "source": "", "file": "no-download.txt", "download_command": ""},
             }

WORKDIR = os.environ["HOME"]
archive_format = [".tar.gz", ".tar", ".zip", ".rar"]

def get_password ():

    cmd = "pass show HBP/model-catalog"
    pswd = spur.LocalShell().run(cmd.split(), encoding="utf-8")
    toreturn = pswd.output.strip()
    print (toreturn)
    if (toreturn.startswith("Error:")):
        print (toreturn + "\nTry to log with HBP_PASS environment variable.")
        toreturn = os.environ["HBP_PASS"]
        if not toreturn :
            print ("Error :: HBP_PASS must be set.\n----- Exit FAIL")
            exit(1)

    return toreturn


def find_html_options (var_instance):
    html_options = {}

    # If there are html options in the link
    if "?" in var_instance["source"]:
        list_of_options = var_instance["source"].split("?")[1].split("&")
        var_instance["source"] = var_instance["source"].split("?")[0]
        for i_option in list_of_options:
            html_options [i_option.split("=")[0]] = i_option.split("=")[1]

    var_instance["html_options"] = html_options
    return var_instance


def get_repository_location(var_i_instance):
    # If source is archive, WGET archive file
    is_archive = [var_i_instance["source"].endswith(format) for format in archive_format]
    try:
        # Source is an archive
        idx = is_archive.index(True)
        response = requests.get(var_i_instance["source"], stream=True)
        if (response.ok):
            return ("wget -N --directory-prefix=" + WORKDIR + " " + var_i_instance["source"])
        else :
            print ("Error :: '" + var_i_instance["source"] + "' Response status = " + str(response.status_code))
    except ValueError:
        # Source is not archive
        print ("Error :: " + var_i_instance["source"] + " is not an archive. Let's try something else ...")


    # If source is git repo
    if (var_i_instance["source"].startswith(main_repo["github"]["pattern"])):
        # If model has version number, try to get archive file of version
        if (var_i_instance["version"]):
            # For all archive format, ping the file
            for format in archive_format:
                tar_url = var_i_instance["source"] + "/archive/v" + var_i_instance["version"] + format
                response = requests.get(tar_url, stream=True)
                if(response.ok):
                    return ("wget -N --directory-prefix=" + WORKDIR + " " + tar_url)

            print("Error :: " + var_i_instance["source"] + " does not provide archive release, try to clone git project.")
            return ("git clone " + var_i_instance["source"] + " " + WORKDIR  + "/" + os.environ["HBP_INSTANCE_ID"])
        else :
            # Git clone project
            print("Error :: " + var_i_instance["source"] + " does not have version number, try to clone git project.")
            return ("git clone " + var_i_instance["source"] + " " + WORKDIR + "/" + os.environ["HBP_INSTANCE_ID"])

    # Error :: the source does not exists or source pattern not taken into account
    print("Error :: Source '" + var_i_instance["source"] + " (" + var_i_instance["version"] + ")' does not exist or service not available.\n----- Exit FAIL")
    exit (1)

def get_unzip_instruction(var_download_command):

    is_archive = [var_download_command.endswith(format) for format in archive_format]
    try:
        idx = is_archive.index(True)
        filename = var_download_command.split("/")
        return ("arc -overwrite unarchive " + WORKDIR + "/" + filename[len(filename)-1] + " " + WORKDIR + "/" + os.environ["HBP_INSTANCE_ID"])
    except ValueError:
        return ("")

def generate_scriptfile (var_instance):

    f = open (WORKDIR + "/run_me.sh", "a")
    f.write("#!/bin/bash\n")
    runscript_file = os.environ["HBP_INSTANCE_ID"] + ".sh"

    # Parse HTML options
    var_instance = find_html_options(var_instance)
    print (var_instance)

    # write download link into script file
    download_command = get_repository_location(var_instance)
    f.write(download_command + "\n")

    # write extract command into script file
    instruction = get_unzip_instruction(download_command)
    f.write(instruction + "\n")

    # CD to project base folder
    f.write("cd " + WORKDIR + "/" + os.environ["HBP_INSTANCE_ID"] + "\n")
    f.write("while [ $(ls -l | grep -v ^d | wc -l) -lt 2 ]\ndo\nif [ -d $(ls) ]; then \ncd $(ls);\nfi\ndone" + "\n")


    f.write("cp " + WORKDIR + "/" + runscript_file + " ." + "\n")
    f.write("pwd; ls -alh;" + "\n")
    f.write("chmod +x ./" + runscript_file + "\n")
    f.write("echo \"TODO : Get INPUT and RESULTS\"" + "\n")
    f.write("./" + runscript_file + "\n")

    f.close()

def check_1_model_instance (var_mc, var_instance_id):

    # Error if model-instance-id does not exist
    i_instance = var_mc.get_model_instance(instance_id=var_instance_id)
    if (len(i_instance)>0):
        # Write script that download model
        generate_scriptfile (i_instance)

    else :# Error :: the instance does not exist
        print("Error :: Instance '" + var_instance_id + "' does not exists.\n----- Exit FAIL")
        exit (1)



def check_1_model (var_mc, var_model_id):

    # Error when the model does not exists
    # TODO
    var_list_model_instance = var_mc.list_model_instances(model_id=var_model_id)

    # Error when the model does not have any instance
    if (len(var_list_model_instance) == 0):
        print ("Error :: Model '" + var_model_id + "' does not have any instance.\n----- Exit FAIL")
        exit (1)

    for i_instance in var_list_model_instance:
        check_1_model_instance (var_mc, i_instance["id"])


if __name__ == "__main__":


    # Check Environment variables exist
    if (not os.environ.get("HBP_INSTANCE_ID")):
        print ("Error :: HBP_INSTANCE_ID must be set.\n----- Exit FAIL")
        exit (1)
    if (not os.environ.get("HBP_USER")):
        print ("Error :: HBP_USER must be set.\n----- Exit FAIL")
        exit (1)

    # Connect to HBP Model Catalog
    mc = ModelCatalog(os.environ["HBP_USER"], get_password())
    os.environ["HBP_AUTH_TOKEN"]=mc.auth.token

    open ("run_me.sh", "w").close()

    # Check if WORKDIR environment variable exists and set WORKDIR
    WORKDIR = os.environ.get("WORKDIR", os.environ["HOME"])

    # Error if 'HBP_INSTANCE_ID' final folder exists
    # (it should not exists due to git clone fatal error)
    if (os.path.isdir(WORKDIR + "/" + os.environ["HBP_INSTANCE_ID"])):
        print("Error :: " + WORKDIR + "/" + os.environ["HBP_INSTANCE_ID"] + " already exists. You should remove this folder to prevent fatal error from Git clone.\n----- Exit FAIL")
        exit(1)

    # Error if 'HBP_INSTANCE_ID.sh' does not exists
    if (not os.path.isfile(WORKDIR + "/" + os.environ["HBP_INSTANCE_ID"] + ".sh")):
        print("Error :: " + WORKDIR + "/" + os.environ["HBP_INSTANCE_ID"] + ".sh" + " does not exist.\n----- Exit FAIL")
        exit(1)

    # check_1_model (mc, os.environ["HBP_MODEL_ID"])
    check_1_model_instance (mc, os.environ["HBP_INSTANCE_ID"])

    # Exit Done ?
    print ("Done.\n ----- Exit SUCCESS")
