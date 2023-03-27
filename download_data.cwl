# Automate model checking workflow
class: CommandLineTool
cwlVersion: v1.0
id: download_data
label: Download Data TODO
$namespaces:
  sbg: 'https://www.sevenbridges.com/'

baseCommand: ["hbp_download_data"]

requirements:                                                                   
  InitialWorkDirRequirement: 
    listing:
      - entry: $(inputs.report)
        writable: True

inputs:
  report:
    type: File
    # format: json
    inputBinding:
      position: 1
      prefix: --json

outputs:
  report:
    type: File
    # format: json
    outputBinding:
      glob: $(inputs.report.basename)

  outputs_folder:
    type: Directory
    outputBinding:
      glob: "./outputs/"
    
  code_folder:
    type: Directory
    outputBinding:
      glob: "./code/"
  

'sbg:license': CeCiLL
'sbg:toolAuthor': Florent Bonnier