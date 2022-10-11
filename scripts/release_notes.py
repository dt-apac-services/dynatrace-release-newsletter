import re
import json
import requests
from bs4 import BeautifulSoup


def get_latest_versions(release_info):

    ## Read Release notes page
    URL="https://www.dynatrace.com/support/help/whats-new/release-notes"    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find_all(title=re.compile("Release notes*"))

    for i in results:
        component = re.findall("(Dynatrace\s[\w]+)",i['title'])[0]
        version = re.findall("[version|release]\s*([\d.]+)",i['title'])[0]
        link = "https://dynatrace.com"+i['href']        
    
        if component not in release_info:
            release_info[component]={}
        if version not in release_info[component]:            
            release_info[component][version] = link        
    
    return release_info

def scrape_specific_release_page():
    URL="x"
    
    
    
    


