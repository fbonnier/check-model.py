#!/bin/bash

MAIN_DIR=$( dirname -- "$0"; )
MODEL_ID='fa393b61-92ab-4925-ad53-d36cde34c5d6'

python3 $MAIN_DIR/../../hbp_cwl_input_downloader/main.py --id $MODEL_ID --token $HBP_AUTH_TOKEN --run 'waiting for the stars to align'

mv report.json report_metadata.json
python3 $MAIN_DIR/../../hbp_download_data/main.py --json $MAIN_DIR/report_metadata.json
