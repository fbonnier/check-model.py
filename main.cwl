# Automate model checking workflow
class: Workflow
cwlVersion: v1.0
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

  hbp_pass:
    type: string
    default: ""
    
  hbp_user:
    type: string
    default: ""


outputs:
  credentials:
    type: File
    outputSource: step0_get_credentials/credentials
  # jsonfile:
  #   type: File
  #   outputSource: step1_download_metadata/jsonfile
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

  step0_get_credentials:
    run:
      class: CommandLineTool
      baseCommand: echo
      requirements:
        EnvVarRequirement:
          envDef:
            HBP_INSTANCE_ID: $(inputs.instance_id)
            WORKDIR: $(inputs.workdir)
            HBP_USER: $(inputs.hbp_user)
            HBP_PASSWORD: $(inputs.hbp_pass)
            HBP_TOKEN: $(inputs.hbp_token)

      inputs:
        instance_id: string
        workdir: string
        hbp_user: string
        hbp_pass: string
        hbp_token: string

      # out: [credentials]

      outputs:
        credentials:
          type: stdout

      stdout: credentials.yml
    
    in:
      instance_id: model_instance_id
      workdir: workdir
      hbp_user: hbp_user
      hbp_pass: hbp_pass
      hbp_token: hbp_token
    out: [credentials]


# Download workflow and meta
  # step1_download_metadata:
  #   in:
  #     instance_id: model_instance_id
  #     token: hbp_token

  #   out: [jsonfile, download_metadata_log_err, download_metadata_log]

  #   run: ./download-metadata.cwl
  #   label: Download Metadata

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