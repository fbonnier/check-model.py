#!/bin/bash

MAIN_DIR=$( dirname -- "$0"; )
MODEL_ID='efa844cc-3807-4eeb-895d-1d240a35af9f'

python3 $MAIN_DIR/../../hbp_cwl_input_downloader/main.py --id $MODEL_ID --token $HBP_AUTH_TOKEN --run 'waiting for the stars to align'

mv report.json report_metadata.json
python3 $MAIN_DIR/../../hbp_download_data/main.py --json $MAIN_DIR/report_metadata.json
