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

def scrape_specific_release_page(component, page_url):
    component="Dynatrace Managed" #temp replacement for testing
    page_url = "https://www.dynatrace.com/support/help/whats-new/release-notes/managed/sprint-250" #temp replacement for testing
    
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # exclude_list = ['Home','What\'s new','Release notes','SaaS','Managed']
    exclude_list = ['Dynatrace API','Resolved issues','Operating systems support','Operating systems','Other support changes','OneAgent for Android resolved issues','OneAgent for iOS resolved issues','OneAgent for JavaScript resolved issues']
    # include_list = ['Announcements','New features and enhancements']
    
    file_name = component+"_release_notes.html"

    with open(file_name,'w') as f:
        print("<!DOCTYPE html>",file=f)
        print("<html>",file=f)
        print("<body>",file=f)
    # creating a list of all common heading tags
        tags = ["h1", "h2", "h3","p","li"]
        position = 0   
        for tag in soup.find_all(tags):
            # print(tags.name + ' -> ' + tags.text.strip())        
            val = tag.text.strip()
            if tag.name == "h1":
                print("<h1 style='text-align:left'>"+val+"</h1>",file=f)
                position += 1         
            if tag.name == "h2":          
                print("  ",file=f)
                if val not in exclude_list:
                    print("<h2 style='text-align:left'>"+val+"</h2>",file=f)
                else:
                    break
                position += 1
            if tag.name == "h3":
                print("<h3 style='text-align:left;margin-left: 25px;'>"+"  "+val+"</h3>",file=f)
                position += 1
            if tag.name == "p":
                if "|" not in val:
                    # info = (val[:150] + '...<a href='+page_url+'>Read more</a>') if len(val) > 150 else val
                    # print("<p style='text-align:left;margin-left: 25px;'>"+"    "+info+"</p>",file=f)
                    print("<p style='text-align:left;margin-left: 25px;'>"+"  "+val+"</p>",file=f)
                position += 1
            if tag.name == "li":
                if position > 0:
                    # info = (val[:150] + '...<a href='+page_url+'>Read more</a>') if len(val) > 150 else val
                    # print("<p style='text-align:left;margin-left: 30px;'>"+"     - "+info+"</p>",file=f)
                    print("<li style='text-align:left;margin-left: 25px;'>"+"    "+val+"</li>",file=f)
        print("</body>",file=f)
        print("</html>",file=f)
        
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

    
    
    
    


