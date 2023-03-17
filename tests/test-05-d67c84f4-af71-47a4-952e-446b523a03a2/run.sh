#!/bin/bash

MAIN_DIR=$( dirname -- "$0"; )
MODEL_ID='d67c84f4-af71-47a4-952e-446b523a03a2'

python3 $MAIN_DIR/../../hbp_cwl_input_downloader/main.py --id $MODEL_ID --token $HBP_AUTH_TOKEN --run 'waiting for the stars to align'

mv report.json report_metadata.json
python3 $MAIN_DIR/../../hbp_download_data/main.py --json $MAIN_DIR/report_metadata.json
