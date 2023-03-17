#!/bin/bash

MAIN_DIR=$( dirname -- "$0"; )
MODEL_ID='9be16ff0-e546-468e-b506-c0540df78005'

python3 $MAIN_DIR/../../hbp_cwl_input_downloader/main.py --id $MODEL_ID --token $HBP_AUTH_TOKEN --run 'waiting for the stars to align'

mv report.json report_metadata.json
python3 $MAIN_DIR/../../hbp_download_data/main.py --json $MAIN_DIR/report_metadata.json
