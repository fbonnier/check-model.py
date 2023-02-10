# Automate model checking workflow
class: Workflow
cwlVersion: v1.0
id: model_verification
label: Model Verification TODO
$namespaces:
  sbg: 'https://www.sevenbridges.com/'

hints:
  DockerRequirement:
    dockerPull: docker-registry.ebrains.eu/hbp-model-validation/docker-ebrains-base

inputs:
  hbp_token: string

  model_instance_id: string

  instruction: string

  # workdir: Directory
  # workdir: string

  # hbp_pass: string
    
  # hbp_user: string

  # jsonfile: File

    
requirements:
  InlineJavascriptRequirement: {}
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
      # workdir: workdir



    out: [metareport]

    label: Download Metadata


  step2_script_generator:
    run: script_generator.cwl
    in:
      jsonfile: step1_download_metadata/metareport

    out: [runscript_bash]
    label: Generates runscript to run the model



# Testing Step for debugging
# Print JSON File using 'cat'
  step_print_JSON:
    run: print_json_file.cwl
    in:
      jsonfile: step1_download_metadata/metareport
    out: []

    label: Print JSON file
  
  
# Testing Step for debugging
# Print JSON File using 'cat'
  step_print_runscript:
    in:
      runscript_bash: step2_script_generator/runscript_bash
    out: []
    label: Print runscript
    run:
      class: CommandLineTool
      baseCommand: cat
      inputs:
        runscript_bash: 
          type: File
          inputBinding:
            position: 1
      outputs: []
      
  #     outputs: []
  #     stdout: stdout
  #   in:
  #     jsonfile: step1_download_metadata/jsonfile
  #   out: []