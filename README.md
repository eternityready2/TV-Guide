# SSH command to start the TV Guide

sudo systemctl restart tvguide
or.. sudo systemctl restart tv.service

# SSH command to start scrappers

CD to home/manager/chg, Run bash do_scrape.sh

# Guide for Dev Ops to understand how code posts scrapped data 

1. Overview

This document provides a comprehensive guide to scraping TV channel schedules using dedicated scrapers encapsulated within individual classes. It outlines the scraping logic, systematic execution process, and the handling of additional arguments ('extra args') within the execution script.



2. Scraping Logic

Each TV channel schedule is scraped using a dedicated scrapper class. These classes utilize BeautifulSoup (bs4) predominantly for parsing HTML or JSON responses, except for channels with dynamic content, which require Selenium like channel 50.

The scraping logic within each scrapper class retrieves schedule information from the respective channel's website or API endpoints. BeautifulSoup facilitates efficient parsing of HTML or JSON data structures, allowing for streamlined data extraction.

Selenium is employed for channels with dynamic content or JavaScript-rendered pages, enabling interaction with the webpage to retrieve schedule information.

Each scrapper class inherits common functionality from the base class Trawler and provides a method "get_info_for_days" for retrieving schedule information for a given set of days. By implementing the "get_data" function within each scrapper class, schedule data can be efficiently retrieved and processed for further analysis or integration.



3. Execution of Scrapers

Importing Scraper Classes: The execution script (do_scrape.py) imports all scrapper classes from the trawlers module, ensuring accessibility to each channel's scraping logic.

Initializing Logging: Logging is configured within the execution script to provide informative messages throughout the scraping process. These messages include the initiation of scraping, successful data retrieval, encountered errors, and any additional details deemed relevant.

Initializing Days: The execution script initializes a list of days for which schedule information needs to be retrieved. This ensures that the scraping process covers the desired timeframe for schedule data.

Updating Schedules: For each TV channel, the execution script triggers the respective scrapper class to retrieve schedule information. This involves iterating through the list of days and invoking the appropriate method within each scrapper class to retrieve schedule data for each day.

Handling Additional Arguments ('Extra Args'): Some channels may require additional arguments to retrieve specific schedule data. These 'extra args' are handled within the execution script by passing them to the appropriate scrapper class method. This ensures flexibility and customization in retrieving schedule data tailored to the requirements of each channel.

Data Saving: Upon successful retrieval of schedule information for all channels, the data is saved into pickle files for future reference. This includes saving both the schedule data and the list of days into separate pickle files, ensuring easy access to the scraped information.

Handling Errors: In the event of errors encountered during the scraping process, the execution script includes error handling mechanisms. This ensures that errors are logged appropriately, and the scraping process can continue seamlessly, maintaining robustness and reliability.



4. Conclusion

This document serves as a comprehensive guide to scraping TV channel schedules, covering the scraping logic, systematic execution process, and the handling of additional arguments within the execution script. By following this structured approach, TV channel schedules can be efficiently scraped, facilitating further analysis or integration into other systems.

