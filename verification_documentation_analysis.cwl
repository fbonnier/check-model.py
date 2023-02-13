# Automate model checking workflow
class: CommandLineTool
cwlVersion: v1.0
id: verification_documentation_analysis
label: Documentation analysis
$namespaces:
  sbg: 'https://www.sevenbridges.com/'

requirements: []
baseCommand: ["documentation_check"]

inputs:
  runreport:
    type: File
    format: json
    inputBinding:
      position: 1
      prefix: --json

outputs: 
  scoredreport:
    type: File
    outputBinding:
      glob: documentation_report.json