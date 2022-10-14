# Dynatrace Release Newsletter

A script to scrape latest Dynatrace release notes, blogs & lab notes and create an HTML newsletter that can be shared via email.

Work in progress.. 

## Design

1. Synthetic test or Script checks Release notes page once a day
2. On new release of SaaS/Managed/OneAgent/ActiveGate - Scipt goes to step 3, else exits.
3. Update local release_info.json file with new version
4. Navigate to new version page
    - Scrape all h1, h2, h3 & p
    - Prepare HTML
5. Get public blogs (since last update)
    - Scrape heading & some content
    - Prepare HTML
6. Get lab notes (since last update)
    - Scrape heading & some content
    - Prepare HTML
7. Combine HTML and send out notification