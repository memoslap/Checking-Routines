# ##########################################################################
#
# Author: Steffen Riemann, Sven Passmann
# created: 09.08.2024
# changed: 
#
# checks downloaded XML files (from XNAT) for completeness of uploaded 
# files (logfiles from behavioral tasks, MRprotocols, tDCS logfiles and 
# neuropsych files
#
#
# works best with the following folder structure:
#
#    - XXXXX (folder with the script)
#        - XMLdata (contains XML files downloaded from XNAT)
#        - Output (contains output files)
#
# 
###########################################################################

import xml.etree.ElementTree as ET
import os
import csv


# Set the new working directory
os.chdir('Y:/01_Studien/00_FOR5429_MeMoSLAP/RU_IT/Server/02_Checking_Routines')
#os.chdir('C:/Users/svenp/Desktop/HGW/02_Checking_Routines')


# Verify the new working directory
print(os.getcwd())


#__________________________________________________________________________________________________________________________
# read in data

file_path = r'Y:/01_Studien/00_FOR5429_MeMoSLAP/RU_IT/Server/02_Checking_Routines/XMLdata' 
#file_path = r'C:/Users/svenp/Desktop/HGW/02_Checking_Routines/XMLdata' 
files = [entry.name for entry in os.scandir(file_path) if entry.is_file()]
print(files)

#__________________________________________________________________________________________________________________________
# creating dictionaries and variables the code refers to at later stages{"keys": [values]}

# list of (sub-)nodes in the XML-file
data = {
    "overall": "sets", 
    "sub_ses": "entrySet",
    "resources": ["sets", "entrySet"], # level for files
    "files": ["entries", "entry"], # stored jsons, tsv's, log files 
}

# list of files to be expected 
expectedfiles = {
    "baseline" : ["MRprotocol"],
    "session1" : ["phenotype", "MRprotocol", "tDCS"],
    "session2" : ["phenotype", "MRprotocol", "tDCS"],
    "session3" : ["beh", "phenotype", "MRprotocol", "tDCS"],
    "session4" : ["beh", "phenotype", "MRprotocol", "tDCS"],
}


prefix = "{http://nrg.wustl.edu/catalog}" # replace the "cat:..."-part of the xml-file in the following code

#__________________________________________________________________________________________________________________________


# Parse the XML file
for file in files:
    tree = ET.parse('XMLData/' + file)
    root = tree.getroot()
    print(root)

    missing = {} # creates empty dictionary to print the subjects matching with the aim to find subujects witout uploaded files

    root = root.find(prefix + data["overall"]) # erase the first root level --> let the code start to count from second entry (cat:sets)

    for child in root.findall(prefix + data["sub_ses"]): # loops through the level of "entryset"

        existingfiles = {} # creating empty list for the files which should exist

        description = child.get('description')
        project = description.split(", ")[0].split(": ")[1]  # extracts the projectID
        project = str(project)[-1]                           # extracts the projectID
        subject = description.split(", ")[2].split(": ")[1]  # extracts the subjectID


        missing[subject] = {} # creating empty dictionary, separately for subject ID
        
        
        resources_0 = child.find(prefix + data["resources"][0]) # access the first level of the resources
        if resources_0 is None:
           missing[subject]["allfiles"] = True # if no resources level exist, no file is uploaded at all, and subjectID will be added to dictionary
           continue                            # if it exists, go to next loop...


        # otherwise access the level below
        resources_1 = resources_0.find(prefix + data["resources"][1]) # access the second level of the resources
        
        if resources_1 is None: # checking if the second level of resources exists
           continue             # if not, go to next loop; otherwise...


        # extracting the respective name of the session from the second level of resources; 
        # checks what session exist at this level
        description = resources_1.get('description') 
        if "_base" in description:
            print("baseline")
            ses = "baseline"
            
        elif "_1" in description:
            print("session 1")
            ses = "session1" 
            
        elif "_2" in description:
            print("session 2")
            ses = "session2"
            
        elif "_3" in description:
            print("session 3")
            ses = "session3"
            
        elif "_4" in description:
            print("session 4")
            ses = "session4"
            
            
        print(expectedfiles[ses])
                

        
        existingfiles = [] # creating empty list for the files which should exist
        missing[subject][ses] = [] # creating empty list for the missing files, separately for subject ID and session number 

           
        resources_2 = resources_1.find(prefix + data["files"][0]) # access the first level of the files
        resources_3 = resources_2.findall(prefix + data["files"][1]) # access the second level of the  
        
        for resource_3 in resources_3: # loops through the level of interest            
            name = resource_3.get('name') # extracting the name of the file which is there
            existingfile = name.split("/")[1]
            existingfiles.append(existingfile) # append the existing files on this level
        
        for expectedfile in expectedfiles[ses]: # loops through the expectedfiles, and check, if they match with the existingfiles
            
            if expectedfile in existingfiles: # if yes, go to next loop
                continue
           
            missing[subject][ses].append(expectedfile) # otherwise append what file is missing in which session for which subject
            missing_sorted = dict(sorted(missing.items())) # sort the dictionary "missing" by keys ()

    #______________________________________________________________________________________
    # export file as tsv and json

    # tsv
    with open('Output/missingfiles_P' + project + '.tsv', 'w', newline='') as f_output:
        writer = csv.writer(f_output, delimiter='\t')

        # Write each key-value pair in a separate row
        for key, value in missing_sorted.items():
            writer.writerow([f"{key}: {value}"])
            
            print(missing)         