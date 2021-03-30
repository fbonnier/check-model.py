# Check-Model.py

**Check-Model.py** is a Python3.x script that generates scriptfiles able to download,
run and validate an instance of a model from the **EBRAINS Model-Catalog**.

**EBRAINS Model-Catalog** gives access to models developped and maintained by
scientists.

A model can be implemented with multiple instances defined with a version number.<br />
**Check-Model.py** downloads a single instance and runs the associated scriptfile to produce
expected results.

--------------------------------------------------------------------------------

## How to use Check-Model.py
**Check-Model.py** uses [hbp-validation-framework](https://github.com/HumanBrainProject/hbp-validation-framework/)

- [hbp-validation-client](https://github.com/HumanBrainProject/hbp-validation-client/)
- [Documentation hbp-validation-client](https://hbp-validation-client.readthedocs.io/en/master/)
- [PyPi hbp-validation-framework](https://pypi.org/project/hbp-validation-framework/)

Python package to login to EBRAINS, get model's metadata and download an instance of this model.<br />
hbp-validation-client is supposed to be installed.

**Check-Model.py** uses some environment variables to get user's informations:

- *$HBP_USER*, the username to login to EBRAINS,

- *$HBP_PASS*, the password to login to EBRAINS,

- *$HBP_INSTANCE_ID*, the instance identifier associated to the instance to download and run,

- *$WORKDIR*, the location where the scripts are and where the instance will be downloaded.<br />
This variable is optional as the default value is *$HOME*.

--------------------------------------------------------------------------------

## How Check-Model.py operates
**Check-Model.py** is a script generator.<br />
From *$HBP_INSTANCE_ID* identifier, the model instance is retrieved and associated
metadata are downloaded. **Check-Model.py** analyses these metadata and computes the
instance's code location and download method. If the code is within an archive,
the file is downloaded and extracted using [Archiver](https://github.com/mholt/archiver).

Finally, **Check-Model.py** calls the user's runscript named **$HBP_INSTANCE_ID.sh**, which
is a script written by the user (or the model's provider) that runs the instance correctly.
This script is supposed to be in *$WORKDIR* location.

To be clear, **Check-Model.py** generates a script **WORKDIR/run_me.sh** that

1. download instance's metadata,
2. computes code location,
3. download and extract instance's code,
4. cd to extracted code subfolder,
5. runs **$WORKDIR/$HBP_INSTANCE_ID.sh** runscript

--------------------------------------------------------------------------------

## How to install/run Check-Model.py

There is no install process to install **Check-Model.py** at this time, but there are three dependencies:

1. Python-3.x,
2. [PyPi hbp-validation-framework](https://pypi.org/project/hbp-validation-framework/),
3. [Archiver](https://github.com/mholt/archiver).

These must be first installed.

### Example

    export HBP_USER='hplovecraft' HBP_PASS='atthemountainsofmadness' HBP_INSTANCE_ID='20-08-1890-15-03-1937' WORKDIR=$HOME
    mv ./20-08-1890-15-03-1937.sh $WORKDIR
    python3 check-model.py
    cd $WORKDIR
    chmod +x ./run_me.sh
    ./run_me.sh

Where HBP_USER value is replaced with user's HBP username, HBP_PASS with user's HBP password and HBP_INSTANCE_ID with model instance identifier.<br />
**It is highly recommended to check and validate the run_me.sh script file before running it.**

--------------------------------------------------------------------------------
## Check-Model.py and Containers

**Check-Model.py** is compatible with containers as far as environment variables are exported to container and as *$WORKDIR*
corresponds to a valid location mounted and available within the container.

For example [Singularity](https://singularity.lbl.gov/) mounts *$HOME* folder and gives access to it within container and
[Docker](https://docs.docker.com/get-started/) mounts *$PWD* folder. Please ensure *$WORKDIR* corresponds to a valid emplacement.
