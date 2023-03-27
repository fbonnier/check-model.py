# Automate model checking workflow
class: CommandLineTool
cwlVersion: v1.0
id: download_metadata
label: Run Model
$namespaces:
  sbg: 'https://www.sevenbridges.com/'

baseCommand: [sh]

inputs:
    runscript:
        type: File
        inputBinding:
            position: 1

    code_folder:
        type: Directory
            # inputBinding:
            #     position: 2

    outputs_folder:
        type: Directory
            # inputBinding:
            #     position: 3

    # jsonfile:
    #     type: File
    #     inputBinding:
    #         position: 2
    

outputs: 
    # runreport:
    #     type: File
    #     outputBinding:
    #       glob: runreport.json

    watchdog_report:
        type: File
        outputBinding:
            glob: watchdog_log.txt

    outputs_folder:
        type: Directory
        outputBinding:
            glob: "./outputs/"

    code_folder:
        type: Directory
        outputBinding:
            glob: "./code/"


requirements:
    InitialWorkDirRequirement:
        listing:
            - entry: $(inputs.code_folder)
              writable: true
            - entry: $(inputs.outputs_folder)
              writable: true