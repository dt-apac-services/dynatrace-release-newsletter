import re
import json
import requests
from bs4 import BeautifulSoup

## Read Release notes page
URL="https://www.dynatrace.com/support/help/whats-new/release-notes"    
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find_all(title=re.compile("Release notes*"))

json_file = "C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-info\\data\\release_info.json"
# Read from json file
with open(json_file, 'r') as openfile:    
    release_info = json.load(openfile)

for i in results:
    component = re.findall("(Dynatrace\s[\w]+)",i['title'])[0]
    version = re.findall("[version|release]\s*([\d.]+)",i['title'])[0]
    link = "https://dynatrace.com"+i['href']

    if component not in release_info:
        release_info[component]=[]
    if version not in release_info[component]:
        release_info[component].append(version)
        # trigger creation of report
    
json_data = json.dumps(release_info, indent=4)
# Writing to release_info.json
with open(json_file, "w") as outfile:
    outfile.write(json_data)
    
    
    


