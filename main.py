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

    # req_components ={}
    # for component,version in components.items():
    #     if component in ['Dynatrace SaaS','Dynatrace Managed','OneAgent','ActiveGate']:
    #         req_components[component]=version

    if len(components) > 0:         # Only proceed if there is a new version 

        # Get latest blogs and save to html file
        blogs_latest.scrape_blogs(components)
        
        # Create newsletter and email    
        newsletter.create_newsletter(components)

        # Write newsletter date to local file
        read_write.write_last_newsletter_date_json(components)

        # Send email
        email.send_email(components)

        # Print email sent message
        print("Email sent")
        read_write.write_to_log_file("Email sent")
        
    
    else:
        print("All up to date")
        read_write.write_to_log_file("All up to date")


if __name__ == "__main__":
    main()