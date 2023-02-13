# Automate model checking workflow
class: CommandLineTool
cwlVersion: v1.0
id: decision_maker
label: Decision Maker TODO
$namespaces:
  sbg: 'https://www.sevenbridges.com/'

requirements: []
  # - class: InitialWorkDirRequirement
  #   listing:
  #     -$(inputs.workdir)

  # 'sbg:license': CeCiLL
  # 'sbg:toolAuthor': Florent Bonnier
baseCommand: ["decision_maker"]

inputs:
  score_output_analysis:
    type: File
    inputBinding:
        position: 1
    

outputs: 
    decision_report:
        type: File
        format: json
        outputBinding:
          glob: decision_report.json