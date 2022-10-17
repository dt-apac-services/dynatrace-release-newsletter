import copy
import json
import os
from pathlib import Path
import scripts.release_notes as release_notes
import scripts.newsletter as newsletter
import pkg.read_write as read_write
import scripts.blogs_latest as blogs_latest

# global release_info_from_file

def main():    
    
    release_info_from_file = read_write.read_release_info_file()    

    # Scrape release note page to find new releases
    release_info = copy.deepcopy(release_info_from_file)                                # Required to prevent reference
    release_info_from_web = release_notes.get_latest_versions(release_info)

    components = {}
    

    for c in release_info_from_web:        
        for k, v in release_info_from_web[c].items():        
            if k not in release_info_from_file[c]:
                print("New Version Available for "+ c +": "+k)                
                components[c] = k                
                read_write.write_release_info_to_local_file(release_info_from_web)

                # Kick off gathering of info
                release_notes.scrape_specific_release_page(c,k)
    
    blogs_list = blogs_latest.scrape_latest_blogs()
    
    newsletter.create_newsletter(components,blogs_list)

if __name__ == "__main__":
    main()