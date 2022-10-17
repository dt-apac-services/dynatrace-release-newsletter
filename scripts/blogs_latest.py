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
    blog_csv = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","data","blogs.csv"))
    # blog_csv = "C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\data\\blogs.csv"
    with open(blog_csv, newline='',encoding='utf-8') as f:
        local_data = list(csv.reader(f))
        f.close()

    i=1    
    blog_list=[]
    for i in range(pages_to_retrieve):
        val="https://www.dynatrace.com/news/page/"+str(i)+"/?post_type=post"    
        page = requests.get(val)
        soup = BeautifulSoup(page.content, 'html.parser')
        regex = re.compile('feeditem js-feeditem hentry h-entry post-.*')        
        blog_data = soup.find_all(True, {"class":regex})

        for item in blog_data:            
            blog_url = item['href']
            blog_title = item.find('h2').text.strip()
            blog_date = item.find('time').text.strip()
            blog_author = item.find("span",{"class":"fn p-name"}).text.strip()            
            blog_entry = [blog_title,blog_date,blog_author,blog_url] 
            
            # Get blog post tags
            blog_classes = item['class']
            for c in blog_classes:
                if ("tag-" in c):
                    blog_entry.append(c.split("-",1)[1])                

            if blog_title == local_data[1][0]: 
                break
            elif any(blog_title in entry for entry in local_data):
                print(blog_title)
                continue
            else:
                blog_list.append(blog_entry)
        else:
            continue
        break
    
    ############# Write to csv file file ##############
    new_blog_csv=[]
    new_blog_csv.extend(local_data)
    position = 1
    for i in blog_list:
        new_blog_csv.insert(position, i)
        position+=1

    with open(blog_csv, 'w', newline='',encoding="utf-8") as f:
        writer = csv.writer(f)    
        writer.writerows(new_blog_csv)

    # ############# Write to html file ##############
    # write_to_html(new_blog_csv)

    ############# Write to markdown file ##########
    write_to_md_file()
    

############# Write to md file ##############
def write_to_md_file():
    
    # blog_csv = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","data","blogs.csv"))
    blog_csv = "C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\data\\blogs.csv"
    with open(blog_csv, newline='',encoding='utf-8') as f:
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

    # md_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","blogs.md"))
    md_file = "C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\blogs.md"
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
