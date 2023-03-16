#!/bin/bash

# Test battery with multiple models

# Model n°1: 79561fa3-093d-4d2b-b074-51af888eeb11

MODEL_ID="79561fa3-093d-4d2b-b074-51af888eeb11"
MAIN_DIR=$( dirname -- "$0"; )

cwltool $MAIN_DIR/main.cwl --hbp_token $HBP_AUTH_TOKEN --instruction 'running instruction' --model_instance_id '79561fa3-093d-4d2b-b074-51af888eeb11'

# Model n°2: 