# Github repositories functions

import os

# PyGitub
from github import Github
import check_model.errors as errors
import check_model.archive as archive
import requests

def github_commit (id, workdir, metadata):
    if os.environ["GIT_TOKEN"]:
        gitbase = Github(os.environ["GIT_TOKEN"])
        try:
            repo = gitbase.get_repo(metadata["source"])
            commit = repo.get_commit(sha=metadata["version"])
            cmd_to_return = "git clone " + metadata["source"] + " " + workdir  + "/" + id\
            + "\n cd " + workdir + "/" + id\
            + "\n git checkout " + metadata["version"]\
            + "\n cd " + workdir
            return cmd_to_return

        except Exception as e:
            print (e)
            errors.print_error ("Get commited version ... FAIL. Try to clone source code", "continue")
            return ("")
    else :
        errors.print_error ("The version number does not correspond to a commit-ID, try to clone the project", "continue")
        return ("")

def github_release (id, workdir, metadata):
    for format in archive.archive_format:
        tar_url = metadata["source"] + "/archive/v" + metadata["version"] + format
        response = requests.get(tar_url, stream=True)
        if(response.ok):
            cmd_to_return = "wget -N --directory-prefix=" + workdir + " " + tar_url
            metadata["archive_name"] = tar_url.split("/")[-1]
            print("Try to get release archive from version number ... SUCCESS")
            print ("get_code_location ==> END")
            return cmd_to_return

def github_clone (id, workdir, metadata):
    metadata["archive_name"] = metadata["source"].split("/")[-1]
    return ("git clone " + metadata["source"] + " " + workdir  + "/" + id)
