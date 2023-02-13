# Automate model checking workflow
class: CommandLineTool
cwlVersion: v1.0
id: verification_output_analysis
label: Output comparison verification method
$namespaces:
  sbg: 'https://www.sevenbridges.com/'

requirements: []
baseCommand: ["file_compare"]

inputs:
  runreport:
    type: File
    format: json
    inputBinding:
      position: 1
      prefix: --report

  watchdog_report:
    type: File
    format: txt
    inputBinding:
      position: 2
      prefix: --watchdog
    

outputs: 
  scoredreport:
    type: File
    outputBinding:
      glob: report.json