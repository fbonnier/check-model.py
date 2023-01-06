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

  # message:
  #   type: string
  #   default: ""
    


outputs:
  credentials:
    type: File
    outputSource: step0_get_credentials/credentials

  message:
    type: string
    outputSource: step_test/message

  # hbp_token:
  #   type: string
  #   outputSource: step0_get_credentials/token
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
      baseCommand: ["sh", "get_credentials.sh"]
      requirements:
        InitialWorkDirRequirement:
          listing:
            - entryname: get_credentials.sh
              entry: |-
                MSG="hbp_instance_id: \${HBP_INSTANCE_ID}\\n"
                MSG="\${MSG}hbp_user: \${HBP_USER}\\n"
                MSG="\${MSG}hbp_pass: \${HBP_PASSWORD}\\n"
                MSG="\${MSG}hbp_token: \${HBP_TOKEN}\\n"
                MSG="\${MSG}hbp_workdir: \${WORKDIR}"
                echo "\${MSG}"

      # requirements:

      inputs: {}
      #   instance_id: string
      #   workdir: string
      #   hbp_user: string
      #   hbp_pass: string
      #   hbp_token: string

      # out: [credentials]

      outputs:
        credentials:
          type: stdout
        # token: 

      stdout: credentials.yml
    
    in: {}
      # instance_id: model_instance_id
      # workdir: workdir
      # hbp_user: hbp_user
      # hbp_pass: hbp_pass
      # hbp_token: hbp_token
    out: [credentials]
  
  step_test:
    run:
      class: ExpressionTool
      requirements:
        InlineJavascriptRequirement: {}

      inputs: {}

      outputs:
        message:
          type: string
      expression: |
        ${ return {"message": process.env.HBP_TOKEN}; }
    
    in: {}
    out: [message]

  step_echo:
    run:
      class: CommandLineTool
      baseCommand: echo
      requirements: 
        StepInputExpressionRequirement: {}

      inputs:
        message:
          type: string
        

      
      outputs:
        myout:
          type: stdout

      stdout: out.yml

    in:
      message:
        valueFrom: $(outputs.message)
    out: [myout]



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