# Automate model checking workflow
class: CommandLineTool
cwlVersion: v1.0
id: verification_output_analysis
label: Output comparison verification method
$namespaces:
  sbg: 'https://www.sevenbridges.com/'

baseCommand: ["file_compare"]

inputs:
  report:
    type: File
    # format: json
    inputBinding:
      position: 1
      prefix: --json

  outputs_folder:
    type: Directory
    
  code_folder:
    type: Directory

outputs: 
  report:
    type: File
    outputBinding:
      glob: $(inputs.report.basename)


requirements:
    InitialWorkDirRequirement:
        listing:
            - entry: $(inputs.code_folder)
              writable: true
            - entry: $(inputs.outputs_folder)
              writable: true