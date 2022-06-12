
Overview:
Program to scrape and store posted jobs from Dutch version of the www.Indeed.com - www.Indeed.nl
Gets the next information from the website:
- original id generated by Indeed;
- job title (job_title)
- posting date (job_date)
- location  (job_loc)
- short description (job_summary)
- salary (or salary range) in a list format (job_salary)
- url of the job (job_url)
- company name (company_name)
- company type: recruiter or direct employer (company_type)

Functionality:
1. Scraping jobs by the key parameters: search key-words and company type: direct employer or agency.
2. Cleaning / formatting data.
3. Qualifying correctness of the search by the words-combinations in the job description.'
Parameter "red_flags" helps to disqualify jobs, where any of the red-flag words is found in the job summary field
4. Adding precise geo-location (job_lng, job_lat, job_city) comparing job_loc with external database of the cities in the Netherlands
   (file data/nl.csv)
5. Each scraping session saves the results as a csv data dump to the data_dumps/ folder.
6. Saving as a data dump to the SQL DB in the cloud. - > TBD
7. User interface to initiate scraping and define parameters -> TBD
8. Extra: logging each step of the scraping.


Architecture:
1. main.py - enter point
2. engine.py - main workflow of the app within a 'ScrapingSession' class
3. indeed_nl_scraper.py - scraping functionality module
4. dumping.py -  data cleaning /formatting module + saving data dumps ('DataDump' class)
5. logger.py - logging functionality ('Logger' class)
6. search_parameters.py - keeping scraping parameters in separate module for easy access.







