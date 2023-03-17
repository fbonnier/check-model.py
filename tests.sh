#!/bin/bash

# Test battery with multiple models
MAIN_DIR=$( dirname -- "$0"; )

# Model n°1: 79561fa3-093d-4d2b-b074-51af888eeb11
echo "START Model 1\n"
MODEL_ID="79561fa3-093d-4d2b-b074-51af888eeb11"
pre_instructions=""
instructions=""

cwltool $MAIN_DIR/main.cwl --hbp_token $HBP_AUTH_TOKEN --instruction 'running instruction' --model_instance_id $MODEL_ID

echo "END Model 1\n\n"

# # Model n°2: c62641c5-5c1d-4a9b-a971-73ab83559a6f
# Controlled Access

# echo "START Model 2\n"
# MODEL_ID="c62641c5-5c1d-4a9b-a971-73ab83559a6f"
# pre_instructions=""
# instructions=""

# cwltool $MAIN_DIR/main.cwl --hbp_token $HBP_AUTH_TOKEN --instruction 'running instruction' --model_instance_id $MODEL_ID

# echo "END Model 2\n\n"

# Model no 3: 5692f99c-cfe3-4d61-85c8-222c171e5ef8
echo "START Model 3\n"
MODEL_ID="5692f99c-cfe3-4d61-85c8-222c171e5ef8"
pre_instructions=""
instructions=""

cwltool $MAIN_DIR/main.cwl --hbp_token $HBP_AUTH_TOKEN --instruction 'running instruction' --model_instance_id $MODEL_ID

echo "END Model 3\n\n"

# # Model no 4: e5cb8fc8-bbcf-49a8-bf45-0f89a321b72a
# Controlled Access

# echo "START Model 4\n"
# MODEL_ID="e5cb8fc8-bbcf-49a8-bf45-0f89a321b72a"
# pre_instructions=""
# instructions=""

# cwltool $MAIN_DIR/main.cwl --hbp_token $HBP_AUTH_TOKEN --instruction 'running instruction' --model_instance_id $MODEL_ID
# echo "END Model 4\n\n"

# # Model no 5: d67c84f4-af71-47a4-952e-446b523a03a2
# Controlled Access
# echo "START Model 5\n"
# MODEL_ID="d67c84f4-af71-47a4-952e-446b523a03a2"
# pre_instructions=""
# instructions=""

# cwltool $MAIN_DIR/main.cwl --hbp_token $HBP_AUTH_TOKEN --instruction 'running instruction' --model_instance_id $MODEL_ID
# echo "END Model 5\n\n"

# Model no 6: efa844cc-3807-4eeb-895d-1d240a35af9f
# Attribute Timeout on None object to investigate
# echo "START Model 6\n"
# MODEL_ID="efa844cc-3807-4eeb-895d-1d240a35af9f"
# pre_instructions=""
# instructions=""

# cwltool $MAIN_DIR/main.cwl --hbp_token $HBP_AUTH_TOKEN --instruction 'running instruction' --model_instance_id $MODEL_ID
# echo "END Model 6\n\n"

# Model no 7: fa393b61-92ab-4925-ad53-d36cde34c5d6
echo "START Model 7\n"
MODEL_ID="fa393b61-92ab-4925-ad53-d36cde34c5d6"
pre_instructions=""
instructions=""

cwltool $MAIN_DIR/main.cwl --hbp_token $HBP_AUTH_TOKEN --instruction 'running instruction' --model_instance_id $MODEL_ID
echo "END Model 7\n\n"


# Model no 8: 45438037-efc0-4f14-a031-d5ff5c346ebd
echo "START Model 8\n"
MODEL_ID="45438037-efc0-4f14-a031-d5ff5c346ebd"
pre_instructions=""
instructions=""

cwltool $MAIN_DIR/main.cwl --hbp_token $HBP_AUTH_TOKEN --instruction 'running instruction' --model_instance_id $MODEL_ID
echo "END Model 8\n\n"


# Model no 9: 9be16ff0-e546-468e-b506-c0540df78005
echo "START Model 9\n"
MODEL_ID="9be16ff0-e546-468e-b506-c0540df78005"
pre_instructions=""
instructions=""

cwltool $MAIN_DIR/main.cwl --hbp_token $HBP_AUTH_TOKEN --instruction 'running instruction' --model_instance_id $MODEL_ID
echo "END Model 9\n\n"


# # Model no 10: 4efb127d-8393-4c97-b955-90f2c492b526
# # Nonetype has no attribute timeout
# echo "START Model 10\n"
# MODEL_ID="4efb127d-8393-4c97-b955-90f2c492b526"
# pre_instructions=""
# instructions=""

# cwltool $MAIN_DIR/main.cwl --hbp_token $HBP_AUTH_TOKEN --instruction 'running instruction' --model_instance_id $MODEL_ID
# echo "END Model 10\n\n"