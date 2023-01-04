# Automate model checking workflow
class: Workflow
cwlVersion: v1.2
id: model_verification
label: Model Verification TODO
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
inputs:
  hbp_token:
    type: string
    default: ""

  model_instance_id:
    type: string
    default: ""

  workdir:
    type: string
    default: "."

outputs:
  jsonfile:
    type: File
    outputSource: step1_download_metadata/jsonfile
  download_metadata_log_err:
    type: File
    outputSource: step1_download_metadata/download_metadata_log_err
  download_metadata_log:
    type: File
    outputSource: step1_download_metadata/download_metadata_log
  generate_runscript_log_err:
    type: File
    outputSource: step3_generate_runscript/generate_runscript_log_err
  generate_runscript_log:
    type: File
    outputSource: step3_generate_runscript/generate_runscript_log
#  code_directory:
#    type: Directory
#    outputSource: step2_download_code/code_directory
#  code_archive:
#    type: File
#    outputSource: step2_download_code/code_archive

steps:
  step1_download_metadata:
    in:
      instance_id: model_instance_id
      token: hbp_token

    out: [jsonfile, download_metadata_log_err, download_metadata_log]

    run: ./download-metadata.cwl
    label: Download Metadata

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