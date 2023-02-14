# Automate model checking workflow
class: CommandLineTool
cwlVersion: v1.0
id: print_json
label: Print JSON file 

requirements: []
'sbg:license': CeCiLL
'sbg:toolAuthor': Florent Bonnier

$namespaces:
  sbg: 'https://www.sevenbridges.com/'

baseCommand: cat 

inputs:
  file:
    type: File
    inputBinding:
        position: 1

outputs: []
