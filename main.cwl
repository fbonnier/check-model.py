# Automate model checking workflow
class: Workflow
cwlVersion: v1.0
id: model_verification
label: Model Verification TODO
$namespaces:
  sbg: 'https://www.sevenbridges.com/'

inputs:
  hbp_token: string

  model_instance_id: string

  instruction: string

  workdir: File

  # hbp_pass: string
    
  # hbp_user: string

  jsonfile: File

    
# requirements:
  # SubworkflowFeatureRequirement: {}
  # InlineJavascriptRequirement: {}
  # StepInputExpressionRequirement: {}
  # SchemaDefRequirement:
  #   types:
  #     - name: test_record
  #       type: record
  #       fields:
  #         - name: hbp_token
  #           type: string

outputs: 
  jsonfile:
    type: File
  # credentials:
  #   type: File
  #   outputSource: step0_get_credentials/credentials

  # message:
  #   type: string
  #   outputSource: step_test/message

  # hbp_token:
  #   type: string
  #   outputSource: step0_get_credentials/token
  
  # download_metadata_log_err:
  #   type: File
  #   outputSource: step1_download_metadata/download_metadata_log_err
  # download_metadata_log:
  #   type: File
  #   outputSource: step1_download_metadata/download_metadata_log
  # generate_runscript_log_err:
  #   type: File
  #   outputSource: step3_generate_runscript/generate_runscript_log_err
  # generate_runscript_log:
  #   type: File
  #   outputSource: step3_generate_runscript/generate_runscript_log
#  code_directory:
#    type: Directory
#    outputSource: step2_download_code/code_directory
#  code_archive:
#    type: File
#    outputSource: step2_download_code/code_archive

steps:

  # Get Credentials.
  # USELESS ?
  step0_get_credentials:
    run: get_credentials.cwl
  
    in:
      hbp_token: hbp_token

    out: []
    label: Get Credentials



# Download workflow and meta
# JSON File contains metadata and is localized in {workdir}, a.k.a {self.path/..}
  step1_download_metadata: 
    run: download_metadata.cwl
    in:
      hbp_token: hbp_token
      model_instance_id: model_instance_id
      instruction: instruction
      workdir: workdir



    out: 
      jsonfile: jsonfile

    label: Download Metadata

  # Download input data, code, environement from JSON file descriptor
  # step2_download_data: 
  #   run: download_data.cwl
  #   in:
  #     jsonfile: 
  #       valueFrom: step1_download_metadata/jsonfile

  #   out:
  #     jsonfile: jsonfile

  #   label: Download Metadata

  # step3_run_model:
  #   run: download_data.cwl
  #   in: 
  #     jsonfile: jsonfile


  #   out: 
  #     jsonfile: jsonfile

  #   label: Run model


# Testing Step for debugging
  step_debug:
    run:
      class: CommandLineTool
      baseCommand: cat
      # requirements: 
      #   StepInputExpressionRequirement: {}

      inputs:
        jsonfile:
          type: File
          inputBinding:
            position: 1
            valueFrom: step1_download_metadata/jsonfile
      
      outputs: []

    in:
      jsonfile: jsonfile
    out: []


#  cat:
#    in:
#      file: step1_download_metadata/jsonfile
#    out: []
#    run: ./cat.cwl

#  step2_download_code:
#    in:
#      instance_id: model_instance_id
#      token: hbp_token
#    out: [code_directory, code_archive]
#    run: ./download-code.cwl

  # step3_generate_runscript:
  #   in:
  #     jsonfile: step1_download_metadata/jsonfile
  #     instance_id: model_instance_id
  #     token: hbp_token
  #   out: [runscript, generate_runscript_log, generate_runscript_log_err]
  #   run: ./generate_runscript.cwl

#  step4_run_me:
#    in:
#      runscript: step3_generate_runscript/runscript
#    out: [expected_result_list, produced_result_list, code_directory]
#    run: ./run_me.cwl


requirements: []
'sbg:license': CeCiLL
'sbg:toolAuthor': Florent Bonnier