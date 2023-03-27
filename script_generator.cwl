# Automate model checking workflow
class: CommandLineTool
cwlVersion: v1.0
id: download_metadata
label: Download Metadata TODO
$namespaces:
  sbg: 'https://www.sevenbridges.com/'

  # - class: InitialWorkDirRequirement
  #   listing:
  #     -$(inputs.workdir)

  # 'sbg:license': CeCiLL
  # 'sbg:toolAuthor': Florent Bonnier
baseCommand: ["script_generator"]

inputs:
  jsonfile:
    type: File
    # format: json
    inputBinding:
        position: 1
        prefix: --json
    

outputs: 
    runscript_bash:
        type: File
        # format: sh
        outputBinding:
          glob: run_me.sh