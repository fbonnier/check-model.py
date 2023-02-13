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
  download_metadata: 
    run: download_metadata.cwl
    in:
      hbp_token: hbp_token
      model_instance_id: model_instance_id
      instruction: instruction
      
    out: [report]

    label: Download Metadata

# Download data
# Download code, inputs, documentation
  download_data: 
    run: download_data.cwl
    in:
      report: download_metadata/report
      
    out: [report]

    label: Download Data

  script_generator:
    run: script_generator.cwl
    in:
      jsonfile: download_data/report

    out: [runscript_bash]
    label: Generates runscript to run the model

  run_model:
  # TODO
    run: run_model.cwl
    in:
      runscript: script_generator/runscript_bash
      jsonfile: download_metadata/report

    out: [runreport]

    label: Run model

  verification_output_analysis:
  # TODO
    run: verification_output_analysis.cwl
    in:
      runreport: run_model/runreport

    out: [scoredreport]

    label: Verification output comparison

  verification_documentation_analysis:
  # TODO
    run: verification_documentation_analysis.cwl
    in:
      report: download_data/report

    out: [scoredreport]

    label: Verification documentation analysis

  decision_maker:
  # TODO
    run: decision_maker.cwl
    in:
      score_output_analysis: verification_output_analysis/scoredreport
      score_documentation_analysis: verification_documentation_analysis/scoredreport

    out: [decision_report]

# Testing Step for debugging
# Print JSON File using 'cat'
  step_print_JSON:
    run: print_json_file.cwl
    in:
      jsonfile: download_metadata/report
    out: []

    label: Print JSON file
  
  
# Testing Step for debugging
# Print JSON File using 'cat'
  step_print_runscript:
    in:
      runscript_bash: script_generator/runscript_bash
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