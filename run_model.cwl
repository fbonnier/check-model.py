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

    workdir:
        type: Directory
        outputBinding:
            glob: "./"



requirements:
    InitialWorkDirRequirement:
        listing:
            - $(inputs.code_folder)
            - $(inputs.outputs_folder)