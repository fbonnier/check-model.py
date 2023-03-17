#!/bin/bash

MAIN_DIR=$( dirname -- "$0"; )
MODEL_ID='79561fa3-093d-4d2b-b074-51af888eeb11'

python3 $MAIN_DIR/../../hbp_cwl_input_downloader/main.py --id $MODEL_ID --token $HBP_AUTH_TOKEN --run 'waiting for the stars to align'

mv report.json report_metadata.json
python3 $MAIN_DIR/../../hbp_download_data/main.py --json $MAIN_DIR/report_metadata.json
