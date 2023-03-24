# Automate model checking workflow
class: CommandLineTool
cwlVersion: v1.0
id: download_data
label: Download Data TODO
$namespaces:
  sbg: 'https://www.sevenbridges.com/'

baseCommand: ["hbp_download_data"]

inputs:
  report:
    type: File
    inputBinding:
      position: 1
      prefix: --json

outputs:
  report:
    type: File
    outputBinding:
      glob: report.json

  outputs_folder:
    type: Directory
    outputBinding:
      glob: "./outputs/"
    
  code_folder:
    type: Directory
    outputBinding:
      glob: "./code/"
  
requirements: []
'sbg:license': CeCiLL
'sbg:toolAuthor': Florent Bonnier