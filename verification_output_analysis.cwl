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
      prefix: --report

  watchdog_report:
    type: File
    # format: txt
    inputBinding:
      position: 2
      prefix: --watchdog

  workdir:
    type: Directory

outputs: 
  report:
    type: File
    outputBinding:
      glob: report.json


requirements:
    InitialWorkDirRequirement:
        listing:
            - entry: $(inputs.workdir)
              writable: true
            # - entry: $(inputs.outputs_folder)
              # writable: true