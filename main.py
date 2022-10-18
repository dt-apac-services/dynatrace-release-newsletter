import copy
from pathlib import Path
import scripts.release_notes as release_notes
import scripts.newsletter as newsletter
import pkg.read_write as read_write
import scripts.blogs_latest as blogs_latest

# global release_info_from_file

def main():

    # Get latest release notes and save to html file
    components = release_notes.scrape_release_page()

    # Get latest blogs and save to html file
    blogs_latest.scrape_blogs(components)
    
    # Create newsletter and email    
    newsletter.create_newsletter(components)

    # Write newsletter date to local file
    read_write.write_last_newsletter_date_json(components)

if __name__ == "__main__":
    main()