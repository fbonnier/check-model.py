# Automate model checking workflow
class: Workflow
cwlVersion: v1.0
id: model_verification
label: Model Verification TODO
$namespaces:
  sbg: 'https://www.sevenbridges.com/'

# hints:
#   DockerRequirement:
#     dockerPull: docker-registry.ebrains.eu/hbp-model-validation/docker-ebrains-base
#     # dockerImageId: docker-registry.ebrains.eu/hbp-model-validation/docker-ebrains-base
#     dockerOutputDirectory: "/tmp/cwl-test" 

inputs:
  hbp_token: string

  model_instance_id: string

  instruction: string

  pre_instructions: string

  # code_folder:
  #   type:
  #     type: array
  #     items: [Directory, File]

  # outputs_folder:
  #   type:
  #     type: array
  #     items: [Directory, File]
  # workdir: Directory
  # workdir: string

  # hbp_pass: string
    
  # hbp_user: string

  # jsonfile: File

    
requirements:
  - class: DockerRequirement
    dockerPull: docker-registry.ebrains.eu/hbp-model-validation/docker-ebrains-base
    dockerOutputDirectory: "/tmp/cwl-test" 
  # - class: InitialWorkDirRequirement
  #   listing:
  #     - $(inputs.code_folder)
  #     - $(inputs.outputs_folder)
  - class: InlineJavascriptRequirement
  # InitialWorkDirRequirement:
  #   listing:
  #     - $(inputs.workdir)
  # 'sbg:license': CeCiLL
  # 'sbg:toolAuthor': Florent Bonnier

outputs:  []
  # metareport:
  #   type: File
  #   outputBinding: 
  #     glob: report.json



steps:

  # # Get Credentials.
  # # USELESS ?
  # step0_get_credentials:
  #   run: get_credentials.cwl
  
  #   in:
  #     hbp_token: hbp_token

  #   out: []
  #   label: Get Credentials



# Download workflow and meta
# JSON File contains metadata and is localized in {workdir}, a.k.a {self.path/..}
  download_metadata: 
    run: download_metadata.cwl
    in:
      hbp_token: hbp_token
      model_instance_id: model_instance_id
      instruction: instruction
      pre_instructions: pre_instructions
      
    out: [report]

    label: Download Metadata

# Download data
# Download code, inputs, documentation
  download_data: 
    run: download_data.cwl
    in:
      report: download_metadata/report
      
    out: [report, code_folder, outputs_folder]

    label: Download Data

  script_generator:
    run: script_generator.cwl
    in:
      jsonfile: download_data/report

    out: [runscript_bash]
    label: Generates runscript

  run_model:
    run: run_model.cwl
    in:
      runscript: script_generator/runscript_bash
      code_folder: download_data/code_folder
      outputs_folder: download_data/outputs_folder
      
    out: [watchdog_report, outputs_folder, code_folder]

    label: Run model

  extract_watchdog:
    run: extract_watchdog.cwl
    in:
      watchdog_report: run_model/watchdog_report
      report: download_data/report
      code_folder: run_model/code_folder
      outputs_folder: run_model/outputs_folder
      
    out: [report]
    label: Extract Watchdog

  verification_output_analysis:
    run: verification_output_analysis.cwl
    in:
      report: extract_watchdog/report
      outputs_folder: run_model/outputs_folder
      code_folder: run_model/code_folder

    out: [report]

    label: Verification output comparison

  # verification_documentation_analysis:
  # # TODO
  #   run: verification_documentation_analysis.cwl
  #   in:
  #     report: download_data/report

  #   out: [scoredreport]

  #   label: Verification documentation analysis

  # decision_maker:
  # # TODO
  #   run: decision_maker.cwl
  #   in:
  #     report_list:
  #       source: [verification_output_analysis/report, verification_documentation_analysis/scoredreport]
  #       linkMerge: merge_flattened
      
  #   # out: [decision_report]
  #   out: []
  #   label: Decision Maker

# Testing Step for debugging
# Print JSON File using 'cat'
  # step_print_JSON_metadata:
  #   run: print_file.cwl
  #   in:
  #     file: download_metadata/report
  #   out: []

  #   label: Print JSON file after download metadata
  

# # Testing Step for debugging
# # Print JSON File using 'cat'
#   step_print_JSON_data:
#     run: print_file.cwl
#     in:
#       file: download_data/report
#     out: []

#     label: Print JSON file after download data

# # Testing Step for debugging
# # Print JSON File using 'cat'
#   step_print_runscript:
#     run: print_file.cwl
#     in:
#       file: script_generator/runscript_bash
#     out: []
#     label: Print runscript

# # Testing Step for debugging
# # Print Ls 
#   step_ls_download_data:
#     run: 
#       class: CommandLineTool
#       cwlVersion: v1.0
#       baseCommand: ls
#       stdout: ./output.txt
#       inputs:
#         outputs_folder:
#           type:
#             type: array
#             items: [Directory, File]
#           inputBinding:
#             position: 1

#         code_folder:
#           type:
#             type: array
#             items: [Directory, File]
#           inputBinding:
#             position: 1
#       outputs: 
#         out: stdout  
#     in:
#       outputs_folder: download_data/outputs_folder
#       code_folder: download_data/code_folder
#     out: [out]
#     label: Print runscript



# # Testing Step for debugging
# # Print Watchdog Log File using 'cat'
#   step_print_watchdog_report:
#     run: print_file.cwl
#     in:
#       file: run_model/watchdog_report
#     out: []

#     label: Print Watchdog file