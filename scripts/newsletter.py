

import os
from pathlib import Path
from re import Pattern
import re
import shutil
import pkg.read_write as read_write


def create_newsletter(components, blogs_list):
    position = 1    
    master_file_template = os.path.join(Path(__file__).parent.parent,"templates","release_notes_template.html")
    release_block = os.path.join(Path(__file__).parent.parent,"templates","release_block.html")
    master_file = os.path.join(Path(__file__).parent.parent,"release_notes.html")                
    
    # copy template to root folder
    shutil.copyfile(master_file_template,master_file)
    
    release_info_from_file=read_write.read_release_info_file()

    for k in components:
        
        update_file = os.path.join(Path(__file__).parent.parent,"data",k+"_release_notes.html")
        
        # update_file="C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\data\\"+k+"_release_notes.html"
        # master_file_template="C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\templates\\release_notes_template.html"
        # release_block="C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\templates\\release_block.html"
        # master_file="C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\release_note.html"                
        
        url = release_info_from_file[k][components[k]]["url"]
        # url="https://www.dynatrace.com/support/help/whats-new/release-notes/saas/sprint-252"        

        # add block and then replace value in block        
        f = open(release_block,"r")        
        block = f.read()
        f.close()

        f = open(master_file,"r")
        master = f.read()
        f.close()

        master = re.sub("<!--REPLACE_WITH_RELEASE_NOTES_BLOCK_"+str(position)+"-->",block,master)

        f = open(update_file,"r")
        content = f.read()
        f.close()

        master = re.sub("<!--REPLACE_WITH_RELEASE_NOTES-->",content,master)
        master = re.sub("REPLACE_WITH_RELEASE_NOTES_URL",url,master)

        f = open(master_file,"w")
        f.write(master)
        f.close()

        position+=1

        

        
    