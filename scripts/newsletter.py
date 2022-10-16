

import os
from pathlib import Path
from re import Pattern
import re
import shutil


def update_newsletter(components,blogs):
    position = 1
    for c in components:
        # update_file_name = os.path.join(Path(__file__).parent.parent,"data",c+"_release_notes.html")
        # master_file_template = os.path.join(Path(__file__).parent.parent,"template","release_notes_template.html")
        # master_file = os.path.join(Path(__file__).parent.parent,"release_notes.html")
        # block_blue_file = os.path.join(Path(__file__).parent.parent,"template","block_blue.html")
        # block_white_file = os.path.join(Path(__file__).parent.parent,"template","block_white.html")

        c = "Dynatrace SaaS"
        update_file="C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\data\\Dynatrace SaaS_release_notes.html"
        master_file_template="C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\template\\release_notes_template.html"
        master_file="C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\release_note.html"
        block_blue_file="C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\template\\block_blue.html"
        block_white_file="C:\\Users\\arun.krishnan\\OneDrive - Dynatrace\\Projects\\github\\dynatrace-release-newsletter\\template\\block_white.html"
        url="https://www.dynatrace.com/support/help/whats-new/release-notes/saas/sprint-252"

        # copy template to root folder
        shutil.copyfile(master_file_template,master_file)

        # add block and then replace value in block
        if (position%2)!=0:
            f = open(block_white_file,"r")
        else:
            f = open(block_blue_file,"r")
        block = f.read()
        f.close()

        f = open(master_file,"r")
        master = f.read()
        f.close()

        master = re.sub("<!--INSERT BLOCK HERE "+str(position)+"-->",block,master)

        f = open(update_file,"r")
        content = f.read()
        f.close()

        master = re.sub("<!--REPLACE WITH CONTENT-->",content,master)
        master = re.sub("REPLACE_WITH_LINK",url,master)

        f = open(master_file,"w")
        f.write(master)
        f.close()

        position+=1
        

        
    