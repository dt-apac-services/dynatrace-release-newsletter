# Read local release info file
import json
import os
from pathlib import Path


def read_release_info_file():
    local_release_info_file = Path(__file__).parent.parent/"release_info.json"
    # local_release_info_file = "C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\release_info.json"
    
    # Create file if not present
    if not os.path.exists(local_release_info_file):
        dict = {"Dynatrace SaaS":{},"Dynatrace Managed":{},"OneAgent":{},"ActiveGate":{},"Dynatrace API":{},"Cloud Automation":{},"Dynatrace Operator":{}}
        new_file = open(local_release_info_file,"w")        
        new_file.write(json.dumps(dict, indent=4))    
        new_file.close()

    # Open local release info file and read content
    # release_info_from_file = []
    f = open(local_release_info_file,"r")
    content = f.read()
    if content != "":
        release_info_from_file= json.loads(content)
    f.close()
    return release_info_from_file


# Write into local release info file
def write_release_info_to_local_file(release_info_from_web):
    local_release_info_file = Path(__file__).parent.parent/"release_info.json"
    # local_release_info_file = "C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\release_info.json"
    f = open(local_release_info_file,"w")
    f.write(json.dumps(release_info_from_web, indent=4))
    f.close()