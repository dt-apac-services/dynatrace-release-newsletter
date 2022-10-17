## This script pulls 'all' blog post details from dynatrace.com
# Run only once!

import re
import requests
from bs4 import BeautifulSoup
import time

# Specify number of pages to retrieve. At the time of editing the max pages available were 72
pages_to_retrieve = 72

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
            blog_list.append(n_list)
    time.sleep(1)
    i+=1


import csv
import os
csv_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","blogs.csv"))
with open(csv_file, 'w', newline='',encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Date", "Author","Link","Tag1","Tag2","Tag3","Tag4","Tag5","Tag6","Tag7"])
    writer.writerows(blog_list)

## Write to md file

import csv
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
file = open(md_file, "w",encoding='utf-8')
for line in table:
    file.write(line)
    file.write('\n')
file.close()
