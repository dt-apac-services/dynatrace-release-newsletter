import json
import logging
import os
from pathlib import Path


def main():    
    # Setup logger
    logger = logging.getLogger(__name__)
    release_info_from_file = read_release_info_file()
    #print(release_info_from_file["Dynatrace SaaS"])

# Read local release info file
def read_release_info_file():
    #local_release_info_file = Path(__file__).parent/"release_info.json"
    local_release_info_file = "C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\release_info.json"
    
    # Create file if not present
    if not os.path.exists(local_release_info_file):
        new_file = open(local_release_info_file,"w")
        new_file.close()

    # Open local release info file and read content
    # release_info_from_file = []
    f = open(local_release_info_file,"r")
    content = f.read()
    if content != "":
        release_info_from_file= json.loads(content)
    f.close()
    return release_info_from_file


if __name__ == "__main__":
    main()