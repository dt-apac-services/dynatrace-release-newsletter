import requests
import regex as re
from bs4 import BeautifulSoup
import csv
import os

with open('blog_list.csv', newline='',encoding='utf-8') as f:
    data = list(csv.reader(f))
    f.close()

page_number=1
last_page=2
blog_list=[]
count=0
while page_number < last_page:
    val="https://www.dynatrace.com/news/page/"+str(page_number)+"/?post_type=post"    
    page = requests.get(val)
    soup = BeautifulSoup(page.content, 'html.parser')
    section = soup.find(class_ = re.compile("feed--grid feed--grid--3cols * js-feed"))
    hyperlinks_in_section=section.find_all('a', href=True)
    for a in hyperlinks_in_section:
        count+=1        
        if a.text:
            link=(a['href'])            
            cl=(a['class'])
            name=list(filter(None, a.text.replace("\n","").split('  ')))
            if name[0] != 'Show more':                
                single_line=list(name)
                single_line.append(link)                      
                for txt in cl:
                    if txt.startswith("tag-"):
                        single_line.append(txt.split("-",1)[1])
                if single_line[0] == data[1][0]:                                 
                    break
                else:                    
                    blog_list.append(single_line)                

            if(count==len(hyperlinks_in_section)):                    
                    count=0
                    last_page+=1
                    print("next page :"+ str(last_page))
    page_number+=1

############# Write to csv file file ##############
new_data=[]
new_data.extend(blog_list)
new_data.extend(data)

with open('blog_list.csv', 'w', newline='',encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Date", "Author","Link","Tag1","Tag2","Tag3","Tag4","Tag5","Tag6","Tag7"])
    writer.writerows(new_data)
    

############# Write to .md file ##############

tags=[]
table=[]
table.append("|---------|---------|---------|---------|")
for blog in blog_list:
    hlink="["+blog[0]+"]("+blog[3]+")"
    tag_column_postion=4
    column_count=len(blog)
    tags_line=""
    while tag_column_postion < column_count:
        if len(blog[tag_column_postion])!=0:
            tag=str(blog[tag_column_postion])
            tags_line += "["+tag+ "]" + "(https://www.dynatrace.com/news/tag/"+tag+")" +", "
        tag_column_postion+=1    
    author_name=blog[2].split()[0]+"-"+blog[2].split()[1]
    author="["+ blog[2] +"]"+"(https://www.dynatrace.com/news/blog/author/"+  author_name +")"          
    table_line = "| " + hlink + " | "+ blog[1] + " | " + author +" | " + tags_line[:-2] + " | "
    table.append(table_line)

write_string=""
for line in table:
    write_string+=line+'\n'
    write_string[:-1]

table_start="|---------|---------|---------|---------|"
file_path="D:\\OneDrive\\Projects\\Website\\SREngineer\\content\\dynatrace\\other\\dynatrace-blogs.md"
with open(file_path, 'r+', encoding='utf-8') as f:
        content = f.read().replace(table_start,write_string[:-1])
        f.seek(0)
        f.truncate
        f.write(content)
        f.close()

