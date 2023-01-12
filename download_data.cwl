# Automate model checking workflow
class: CommandLineTool
cwlVersion: v1.0
id: download_data
label: Download Data TODO
$namespaces:
  sbg: 'https://www.sevenbridges.com/'

baseCommand: ["python3"]

inputs:
  jsonfile:
    type: File
    # dirname: workdir
    # basename: "hbp_cwl_input_downloader/main.py"
    




outputs:
    jsonfile:
        type: File
  

 
  #     inputs: {}
  #     #   instance_id: string
  #     #   workdir: string
  #     #   hbp_user: string
  #     #   hbp_pass: string
  #     #   hbp_token: string

  #     # out: [credentials]

  #     outputs:
  #       credentials:
  #         type: stdout
  #       # token: 

  #     stdout: credentials.yml
    
  #   in: {}
  #     # instance_id: model_instance_id
  #     # workdir: workdir
  #     # hbp_user: hbp_user
  #     # hbp_pass: hbp_pass
  #     # hbp_token: hbp_token
  #   out: [credentials]
  
  # step_test:
  #   run:
  #     class: ExpressionTool
  #     requirements:
  #       InlineJavascriptRequirement: {}

  #     inputs: {}

  #     outputs:
  #       message:
  #         type: string
  #     expression: |
  #       ${ return {"message": process.env.HBP_TOKEN}; }
    
  #   in: {}
  #   out: [message]

#   step_echo:
#     run:
#       class: CommandLineTool
#       baseCommand: echo
#       # requirements: 
#       #   StepInputExpressionRequirement: {}

#       inputs:
#         hbp_token:
#           type: string
#           default: "TG2"
      
#       outputs: 
#         type: stdout

#     in:
#       hbp_token: hbp_token
#         # source: step_test/message
#         # valueFrom: $(outputs.message)
#     out: []



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