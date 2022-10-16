import copy
import json
import os
from pathlib import Path
import scripts.release_notes as release_notes

# global release_info_from_file

def main():    
    
    release_info_from_file = read_release_info_file()    

    # Scrape release note page to find new releases
    release_info = copy.deepcopy(release_info_from_file)                                # Required to prevent reference
    release_info_from_web = release_notes.get_latest_versions(release_info)

    for c in release_info_from_web:        
        for k, v in release_info_from_web[c].items():        
            if k not in release_info_from_file[c]:
                print("New Version Available for "+ c +": "+k)
                # Kick off gathering of info
                release_notes.scrape_specific_release_page(c,v["url"])              
    
    write_release_info_to_local_file(release_info_from_web)

# Read local release info file
def read_release_info_file():
    local_release_info_file = Path(__file__).parent/"release_info.json"
    #local_release_info_file = "C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\release_info.json"
    
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
    local_release_info_file = Path(__file__).parent/"release_info.json"
    # local_release_info_file = "C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\release_info.json"
    f = open(local_release_info_file,"w")
    f.write(json.dumps(release_info_from_web, indent=4))
    f.close()


if __name__ == "__main__":
    main()