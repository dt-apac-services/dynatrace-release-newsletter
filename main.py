import copy
from pathlib import Path
import scripts.release_notes as release_notes
import scripts.newsletter as newsletter
import pkg.read_write as read_write
import scripts.blogs_latest as blogs_latest
import scripts.email as email

# global release_info_from_file

def main():

    # Get latest release notes and save to html file
    components = release_notes.scrape_release_page()

    req_components ={}
    for component,version in components.items():
        if component in ['Dynatrace SaaS','Dynatrace Managed','OneAgent','ActiveGate']:
            req_components[component]=version

    if len(req_components) > 0:         # Only proceed if there is a new version 

        # Get latest blogs and save to html file
        blogs_latest.scrape_blogs(req_components)
        
        # Create newsletter and email    
        newsletter.create_newsletter(req_components)

        # Write newsletter date to local file
        read_write.write_last_newsletter_date_json(req_components)

        # Send email
        email.send_email(req_components)
    
    else:
        print("All up to date")

if __name__ == "__main__":
    main()