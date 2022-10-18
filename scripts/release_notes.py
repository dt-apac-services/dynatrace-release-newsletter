import copy
import os
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup
import pkg.read_write as read_write


def scrape_release_page():
    release_info_from_file = read_write.read_release_info_file()
    
    # Scrape release note page and get all available components and versions
    release_info = copy.deepcopy(release_info_from_file)                                # Required to prevent reference
    release_info_from_web = get_component_and_versions(release_info)

    # Get the new release - component & version - and create html file(s)
    components = {}
    for component in release_info_from_web:        
        for version in release_info_from_web[component]:        
            if version not in release_info_from_file[component]:
                print("New Version Available for "+ component +": "+version)                
                components[component] = version     

                # Kick off gathering of specific component release info
                page_url = release_info_from_web[component][version]["url"]
                rollout_start = release_info_from_web[component][version]["rollout"]
                scrape_specific_release_page_and_save_html(component, page_url,rollout_start)
    
    # Write new info into local file
    read_write.write_release_info_to_local_file(release_info_from_web)
    return components

def get_component_and_versions(release_info):
    
    ## Read Release notes page
    URL="https://www.dynatrace.com/support/help/whats-new/release-notes"    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    tags = ['h2','td']
    regex = "((?:Changelog )?[Vv]ersion\s.*|\w*\s\d{1,2},\s\d{4}|^Dynatrace\s\S*\w$|^OneAgent$|^ActiveGate$|^Cloud Automation$)"
    results = soup.find_all(tags,string=re.compile(regex))
    ver_regex = "(?:Changelog )?[Vv]ersion\s(.*)"
    component = ""
    version = ""  
    for i in results:
        val = i.text.strip()
        if i.name == "h2":
            component = val
            if component not in release_info:
                release_info[component]={}            
        else:            
            a = i.find('a')
            if a:
                if "github" in a.get('href'):
                    url = a.get('href')
                else:
                    url = "https://dynatrace.com"+a.get('href')                        
                version = re.match(ver_regex,val).group(1)
                release_info[component][version]={}
                release_info[component][version]["url"] = url                 
            else:
                release_info[component][version]["rollout"] = val                

    return release_info


def scrape_specific_release_page_and_save_html(component, page_url, rollout_start):    
    
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    exclude_list = ['Dynatrace API','Resolved issues','Operating systems support','Operating system support','Operating systems','Other support changes','OneAgent for Android resolved issues','OneAgent for iOS resolved issues','OneAgent for JavaScript resolved issues']    
    
    file_name = os.path.join(Path(__file__).parent.parent,"data",component+"_release_notes.html")
    line_skip = False # Used to skip default "Rollout start" line in OneAgent & ActiveGate release notes.

    with open(file_name,'w') as f:
        
    # creating a list of all common heading tags
        tags = ["h1", "h2", "h3","h4","p","li"]
        position = 0   
        for tag in soup.find_all(tags):
            # print(tags.name + ' -> ' + tags.text.strip())        
            val = tag.text.strip()
            if tag.name == "h1":
                val= tag.text.replace("release notes", "")
                print("<h1 style='text-align:left'>"+val+"</h1>",file=f)
                print("<p style='text-align:left'>"+"Rollout start: "+rollout_start+"</p>",file=f)
                if component in ['OneAgent','ActiveGate']:
                    line_skip = True
                position += 1         
            if tag.name == "h2":
                if component in ['OneAgent','ActiveGate']:  # Remove skip as soon as h2 is encountered
                    line_skip = False         
                print("  ",file=f)
                if val not in exclude_list:
                    print("<h2 style='text-align:left'>"+val+"</h2>",file=f)
                else:
                    break
                position += 1
            if tag.name == "h3":
                print("<h3 style='text-align:left;margin-left: 25px;'>"+val+"</h3>",file=f)
                position += 1
            if tag.name == "h4":
                print("<h4 style='text-align:left;margin-left: 25px;'>"+val+"</h4>",file=f)
                position += 1
            if tag.name == "p":
                if not line_skip:
                    if "|" not in val:                                        
                        print("<p style='text-align:left;margin-left: 25px;'>"+val+"</p>",file=f)
                    position += 1
            if tag.name == "li":
                if position > 0:                    
                    print("<p style='text-align:left;margin-left: 25px;'>"+"- "+val+"</p>",file=f)                
    f.close()
























    # for tags in soup.find_all(heading_tags):
    #     print(tags.name + ' -> ' + tags.text.strip())        
    #     if tags.name == "h2":            
    #         h2_text = tags.text.strip()
    #         if h2_text not in page_dict:
    #             page_dict[h2_text]={}
    #     if tags.name == "h3":
    #         none_set = False
    #         h3_text = tags.text.strip()
    #         if h3_text not in page_dict[h2_text]:
    #             page_dict[h2_text][h3_text]=[]

    #     if (tags.name == "p") and (last_tag == "h2"):
    #         if not none_set:
    #             page_dict[h2_text]["none"]=[]
    #             none_set = True

    #     if tags.name == "p":
    #         p_text = tags.text.strip()
    #         if last_tag == "h3":
    #             page_dict[h2_text][h3_text].append(p_text)
    #         if last_tag == "h2":
    #             if none_set:
    #                 page_dict[h2_text]["none"].append(p_text)
    #     last_tag = tags.name
    
    # print(json.dumps(page_dict,indent=4))

    
    
    
    


