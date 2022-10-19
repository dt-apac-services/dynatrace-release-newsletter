# Read local release info file
import csv
import json
import os
from pathlib import Path
from datetime import datetime


def read_release_info_file():
    local_release_info_file = Path(__file__).parent.parent/"release_info.json"    
    
    # Create file if not present
    if not os.path.exists(local_release_info_file):
        dict = {"Dynatrace SaaS":{},"Dynatrace Managed":{},"OneAgent":{},"ActiveGate":{},"Dynatrace API":{},"Cloud Automation":{},"Dynatrace Operator":{}}
        new_file = open(local_release_info_file,"w")        
        new_file.write(json.dumps(dict, indent=4))    
        new_file.close()

    # Open local release info file and read content
    f = open(local_release_info_file,"r")
    content = f.read()
    if content != "":
        release_info_from_file= json.loads(content)
    f.close()
    return release_info_from_file


# Write into local release info file
def write_release_info_to_local_file(release_info_from_web):
    local_release_info_file = Path(__file__).parent.parent/"release_info.json"
    f = open(local_release_info_file,"w")
    f.write(json.dumps(release_info_from_web, indent=4))
    f.close()


def read_local_blogs_csv_file():
    blog_csv = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","data","blogs.csv"))

    with open(blog_csv, newline='',encoding='utf-8') as f:
        local_blog_csv_data = list(csv.reader(f))
        f.close()

    return local_blog_csv_data

def write_local_blogs_csv_file(new_blog_csv_data):
    blog_csv = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","data","blogs.csv"))
    
    with open(blog_csv, 'w', newline='',encoding="utf-8") as f:
        writer = csv.writer(f)    
        writer.writerows(new_blog_csv_data)

def write_latest_blogs_csv_file(blogs_list):
    blog_csv = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","data","blogs_latest.csv"))    
    with open(blog_csv, 'w', newline='',encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date", "Author","Link","Tag1","Tag2","Tag3","Tag4","Tag5","Tag6","Tag7"])
        writer.writerows(blogs_list)

def write_local_md_file(table,file_name):
    md_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..",file_name+".md"))    
    file = open(md_file, "w",encoding='utf-8')
    for line in table:
        file.write(line)
        file.write('\n')
    file.close()

def read_last_newsletter_date_json():
    file_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","data","last_newsletter_date.json"))
    
    f = open(file_path,"r")
    content = f.read()
    if content != "":
        last_newsletter_date= json.loads(content)
    f.close()

    return last_newsletter_date

def write_last_newsletter_date_json(components):
    file_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","data","last_newsletter_date.json"))
    script_run_date = datetime.today().strftime('%b %d, %Y')
    
    f = open(file_path,"r")
    content = json.loads(f.read())
    f.close()

    release_info_from_file = read_release_info_file()

    for component,version in components.items():
        content[component] = release_info_from_file[component][version]["rollout"]
    content["Newsletter"] = script_run_date
    
    f = open(file_path,"w")
    f.write(json.dumps(content, indent=4))
    f.close()

def read_email_creds():
    file_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","data","email_creds.json"))
    
    f = open(file_path,"r")
    content = f.read()
    if content != "":
        email_creds= json.loads(content)
    f.close()

    return email_creds

def read_release_notes_html():
    file_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","release_notes.html"))
    
    f = open(file_path,"r")
    content = f.read()
    if content != "":
        release_notes = content
    f.close()

    return release_notes