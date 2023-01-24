# Automate model checking workflow
class: Workflow
cwlVersion: v1.0
id: model_verification
label: Model Verification TODO
$namespaces:
  sbg: 'https://www.sevenbridges.com/'

hints:
  DockerRequirement:
    dockerPull: docker-registry.ebrains.eu/hbp-model-validation/docker-ebrains-base@sha256:98457aec67f83325b3d2e177c82067fc420c07110dfa11e7ca6a1ab7cbaef2e5

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

outputs:  
  jsonfile:
    type: File

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



    out: [jsonfile]

    label: Download Metadata



# Testing Step for debugging
  # step_debug:
  #   run:
  #     class: CommandLineTool
  #     baseCommand: cat
  #     # requirements: 
  #     #   StepInputExpressionRequirement: {}

  #     inputs:
  #       jsonfile: 
  #         type: File
  #         inputBinding:
  #           position: 1
      
  #     outputs: []
  #     stdout: stdout
  #   in:
  #     jsonfile: step1_download_metadata/jsonfile
  #   out: []