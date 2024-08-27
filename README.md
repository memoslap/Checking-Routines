# Checking-Routines
This repository is related to scripts we use to check for data completeness on XNAT, and for equal entries in different files meant to be uploaded on XNAT

# How to use...
MeMoSLAP_PythonScript_CheckroutinesXNATData.py
- to check if the data structure contains folder for behavioral files, tDCS logfiles, phenotype files (.tsv/.json) and MR protocols
- so far, it only allows to check if the respective folders are created on XNAT. IT DOES NOT check whether the respective files are actually uploaded.
- works best with the following folder structure:

  - XXXXX           (folder with the script)
      - XMLdata     (contains XML files downloaded from XNAT)
      - Output      (contains output files)

   
MeMoSLAP_RScript_CheckroutinesXNATData.RMD
- to check if the excel file containing demographic and neuropsych data include show gaps
