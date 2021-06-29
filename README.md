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
**Check-Model.py** uses [hbp-validation-framework](https://github.com/HumanBrainProject/hbp-validation-framework/) to use KnowledgeGraph v2:

- [hbp-validation-client](https://github.com/HumanBrainProject/hbp-validation-client/)
- [Documentation hbp-validation-client](https://hbp-validation-client.readthedocs.io/en/master/)
- [PyPi hbp-validation-framework](https://pypi.org/project/hbp-validation-framework/)

And uses the **KG-Core** to run with new KnowledgeGraph v3:

- [kg-core](https://github.com/HumanBrainProject/kg-core)
- [kg-core Python Client](https://github.com/HumanBrainProject/kg-core-python)

Python package to login to EBRAINS, get model's metadata and download an instance of this model.<br />
hbp-validation-client is supposed to be installed.

**Check-Model.py** requieres some variables the user needs to have access:

- *username*, the username to login to EBRAINS,

- *password*, the password to login to EBRAINS,

- *instance id*, the instance identifier associated to the instance to download and run,

- *workdir*, the location where the scripts are and where the instance will be downloaded.<br />
No default value has been set at this moment, so the user needs to set this variable correctly.

--------------------------------------------------------------------------------

## How Check-Model.py operates
**Check-Model.py** is a script generator.<br />
From *instance id* identifier, the model instance is retrieved and associated
metadata are downloaded. **Check-Model.py** analyses these metadata and computes the
instance's code location and download method. If the code is within an archive,
the file is downloaded and extracted using [Archiver](https://github.com/mholt/archiver).<br />
[Archiver](https://github.com/mholt/archiver) has been chosen in order to normalize the extract instructions, but this method should be updated
to use more native tools.<br />
The extracted model instance is moved into a folder named with the instance identifier.

Finally, **Check-Model.py** calls the model instance's runscript, which
is a script provided by the model custodian that runs the instance correctly.

To be clear, **Check-Model.py** generates a script **WORKDIR/run_me.sh** that

1. download instance's metadata,
2. computes code location,
3. download and extract instance's code into **INSTANCE_ID** subfolder,
4. cd to extracted code subfolder,
5. runs instance runscript

--------------------------------------------------------------------------------

## How to install/run Check-Model.py

There is no install process to install **Check-Model.py** at this time, but there are three dependencies:

1. Python-3.x,
2. [PyPi hbp-validation-framework](https://pypi.org/project/hbp-validation-framework/),
3. [Archiver](https://github.com/mholt/archiver).

These must be first installed.

### Example
A full example is proposed in **check_model-kgv2.py** that gives an example on how to use **Instance** objects using KnowledgeGraph v2. <br />
Another full example would be proveded soon to illustrate KGV3 use.

**It is highly recommended to check and validate the run_me.sh script file before running it.**
