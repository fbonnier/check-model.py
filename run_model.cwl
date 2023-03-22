# Automate model checking workflow
class: CommandLineTool
cwlVersion: v1.0
id: download_metadata
label: Run Model
$namespaces:
  sbg: 'https://www.sevenbridges.com/'

requirements: []
baseCommand: [sh]

inputs:
    runscript:
        type: File
        inputBinding:
            position: 1

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