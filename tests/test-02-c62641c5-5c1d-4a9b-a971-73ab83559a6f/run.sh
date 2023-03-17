#!/bin/bash

MAIN_DIR=$( dirname -- "$0"; )
MODEL_ID='c62641c5-5c1d-4a9b-a971-73ab83559a6f'

python3 $MAIN_DIR/../../hbp_cwl_input_downloader/main.py --id $MODEL_ID --token $HBP_AUTH_TOKEN --run 'waiting for the stars to align'

mv report.json report_metadata.json
python3 $MAIN_DIR/../../hbp_download_data/main.py --json $MAIN_DIR/report_metadata.json
