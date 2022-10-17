from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup
import time
import csv
import os
from datetime import datetime, timedelta
import time
# Specify number of pages to retrieve. At the time of editing the max pages available were 72

def scrape_latest_blogs():

    pages_to_retrieve = 3

    # read existing csv file

    # csv_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","data","blogs.csv"))
    csv_file = "C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\data\\blogs.csv"
    with open(csv_file, newline='',encoding='utf-8') as f:
        existing_data = list(csv.reader(f))
        f.close()

    i=1
    blog_titles=[]
    links_with_text = []
    blog_list=[]
    while i < pages_to_retrieve:
        val="https://www.dynatrace.com/news/page/"+str(i)+"/?post_type=post"    
        page = requests.get(val)
        soup = BeautifulSoup(page.content, 'html.parser')
        section = soup.find(class_ = re.compile("feed--grid feed--grid--3cols * js-feed"))    
        for a in section.find_all('a', href=True): 
            if a.text:
                link=(a['href'])            
                cl=(a['class']) 
                n_list=list(filter(None, a.text.replace("\n","").split('  ')))
                n_list.append(link)            
                for txt in cl:
                    if txt.startswith("tag-"):
                        n_list.append(txt.split("-",1)[1])  
                if (n_list[0] == existing_data[1][0]):         
                    break
                else:
                    blog_list.append(n_list)
            else:
                continue
        else:
            continue
        break      
        time.sleep(1)
        i+=1
    


    ############# Write to csv file file ##############
    new_csv=[]
    new_csv.extend(existing_data)
    position = 1
    for i in blog_list:
        new_csv.insert(position, i)
        position+=1

    with open(csv_file, 'w', newline='',encoding="utf-8") as f:
        writer = csv.writer(f)    
        writer.writerows(new_csv)

    write_to_html(new_csv)

    write_to_md_file()

    return blog_list


############# Write to md file ##############
def write_to_md_file():
    
    csv_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","data","blogs.csv"))
    with open(csv_file, newline='',encoding='utf-8') as f:
        data = list(csv.reader(f))

    count=0
    hlink=[]
    tags=[]
    table=[]
    table.append("|Blog     |Date   |Author     | Tags    |")
    table.append("|---------|---------|---------|---------|")
    for i in data:
        if (i[0] != "Show more") and (i[0] != "Name"):
            hlink.append("["+i[0]+"]("+i[3]+")")
            tag_column=4
            tags_line=""
            while tag_column < 11:
                try:
                    if len(i[tag_column])!=0:
                        tags_line += "["+str(i[tag_column])+ "]"+ "(https://www.dynatrace.com/news/tag/"+str(i[tag_column])+")" +", "          
                except:            
                    pass         
                tag_column+=1
            tags.append(tags_line[:-2])    
            table_line = "| " + hlink[count] + " | "+ i[1] + " | " + i[2] +" | " + tags[count] + " | "
            table.append(table_line)
            count+=1

    md_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","blogs.md"))
    # md_file = "C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\blogs.md"
    file = open(md_file, "w",encoding='utf-8')
    for line in table:
        file.write(line)
        file.write('\n')
    file.close()



def write_to_html(blogs_list):

    # file_name = os.path.join(Path(__file__).parent.parent,"data","blogs.html")
    file_name = "C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\data\\blogs.html"
    position = 0
    with open(file_name,'w') as f:
        for blog in blogs_list:
            if position > 0:
                parsed_blog_date = datetime.strptime(blog[1],"%B %d, %Y")
                days_since = datetime.now() - parsed_blog_date
                if days_since.days < 30:
                    print("<h2 style='text-align:left'>"+"<a href="+blog[3]+">"+blog[0]+"</a>"+"</h2>",file=f)
                    print("<p style='text-align:left'>"+ blog[1] +"</p>",file=f)
                else:
                    break
            position +=1
    f.close()
