import re
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import pkg.read_write as read_write


def scrape_blogs(components):

    new_blog_csv_data,blog_list = scrape_and_update_local_blogs_file()

    ############# Write to markdown file ##########
    table_full = write_to_md_file(new_blog_csv_data)
    read_write.write_local_md_file(table_full,"blogs")

    table_latest = write_to_md_file(blog_list)
    read_write.write_local_md_file(table_latest,"blogs_latest")

    # ############# Write to html file ##############
    write_to_html(components)


def scrape_and_update_local_blogs_file():
    # Specify max number of pages to check. At the time of editing the max pages available were 72
    max_pages_to_check = 3
    
    local_blog_csv_data = read_write.read_local_blogs_csv_file()
    
    i=0
    position = 0
    blog_list=[]
    for i in range(max_pages_to_check):
        i+=1
        val="https://www.dynatrace.com/news/page/"+str(i)+"/?post_type=post"    
        page = requests.get(val)
        soup = BeautifulSoup(page.content, 'html.parser')
        regex = re.compile('feeditem js-feeditem hentry h-entry post-.*')        
        blog_data = soup.find_all(True, {"class":regex})

        for item in blog_data:
            if position > 2:                                            # Skip first 3 highlighted blogs
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

                if blog_title == local_blog_csv_data[1][0]: 
                    break
                if any(blog_title in entry for entry in local_blog_csv_data):
                    continue
                elif any(blog_title in entry for entry in blog_list):
                    continue
                else:
                    blog_list.append(blog_entry)
            else:
                position +=1
        # else:            
        #     continue
        break
    
    ############# Write to csv file file ##############
    new_blog_csv_data=[]
    new_blog_csv_data.extend(local_blog_csv_data)
    position = 1
    for i in blog_list:
        new_blog_csv_data.insert(position, i)
        position+=1

    read_write.write_local_blogs_csv_file(new_blog_csv_data)
    read_write.write_latest_blogs_csv_file(blog_list)

    return new_blog_csv_data,blog_list  


############# Write to md file ##############
def write_to_md_file(csv_data):   

    count=0
    hlink=[]
    tags=[]
    table=[]
    table.append("|Blog     |Date   |Author     | Tags    |")
    table.append("|---------|---------|---------|---------|")
    for i in csv_data:
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
    
    return table

def write_to_html(components):
    # file_name = os.path.join(Path(__file__).parent.parent,"data","blogs.html")
    last_newsletter_date_json = read_write.read_last_newsletter_date_json()
    blog_csv_data = read_write.read_local_blogs_csv_file()

    last_newsletter_date = last_newsletter_date_json["Newsletter"]
    last_newsletter_date_component =""
    for component in components:
        last_newsletter_date_component = last_newsletter_date_json[component]        

    parsed_last_newsletter_date = datetime.strptime(last_newsletter_date,"%b %d, %Y")
    parsed_last_newsletter_date_component = datetime.strptime(last_newsletter_date_component,"%b %d, %Y")
    file = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","data","blogs.html"))
    
    position = 0
    with open(file,'w') as f:
        for blog in blog_csv_data:
            if position > 0:
                parsed_blog_date = datetime.strptime(blog[1],"%B %d, %Y")
                # days_since = datetime.now() - parsed_blog_date
                if parsed_blog_date > parsed_last_newsletter_date_component:
                    if parsed_blog_date > parsed_last_newsletter_date:
                        print("<h2 style='text-align:left'>"+"<a href="+blog[3]+">"+blog[0]+"</a>"+"</h2>",file=f)
                        print("<p style='text-align:left'>"+ blog[1] +"</p>",file=f)
                else:
                    break
            position +=1
    f.close()
