#!/bin/bash

MAIN_DIR=$( dirname -- "$0"; )
MODEL_ID='4efb127d-8393-4c97-b955-90f2c492b526'

python3 $MAIN_DIR/../../hbp_cwl_input_downloader/main.py --id $MODEL_ID --token $HBP_AUTH_TOKEN --run 'waiting for the stars to align'

mv report.json report_metadata.json
python3 $MAIN_DIR/../../hbp_download_data/main.py --json $MAIN_DIR/report_metadata.json
