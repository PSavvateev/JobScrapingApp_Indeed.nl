# Indeed.nl Jobs Scraping App

## Overview
Program to scrape and store posted jobs in the Netherlands from  www.indeed.nl

Gets the next information from the website:
- original id generated by Indeed;
- job title (`job_title`)
- posting date (`job_date`)
- location  (`job_loc`)
- short description (`job_summary`)
- salary (or salary range) in a list format (`job_salary`)
- url of the job (`job_url`)
- company name (`company_name`)
- company type: recruiter or direct employer (`company_type`)

## Getting Started
1. Install all required packages from requirements.txt.<br/>
`$ pip install -r requirements.txt`
<br/><br/>
2. Save credentials for your POSTGRESQL database in the **`.env`** file:<br/>
`POSTGRESQL_USER = '<username>'`<br/>
`POSTGRESQL_PASSWORD = '<password>'`<br/>
`POSTGRESQL_HOST = '<host>'`<br/>
`POSTGRESQL_PORT = '<port>>'`<br/>
`POSTGRESQL_NAME = '<db name>'`
<br/><br/>
3. Set up the tables in the database
First option: run the **`db_scheme.py`**<br/>
`$ python3 db_scheme.py`
<br/>
Second option: create tables manually in the POSTGRESQL admin tool using sql scripts from the **`db_scheme.sql`** 
Then, add the data to the *`cities`* table from **`/data/cities_nl.csv`**

## How to use
1. Assign search parameters in the **`parameters.py`**: <br/>
- `positions` should be a list of strings with all positions names or key-words for search. Even if there is one word,
keep it in the list: `positions = ["auditor"]`
- `company_types` by default `company_types = ["employer", "recruiter"]`. it helps to differentiate companies,
which posted vacancies. Can be also chosen only one of the types.
- `education_level` has two options 'master' for a positions required a master degree or 'any' for all positions. 
- `red_flags` is a list of key-words. It doesn't impact the scraping, but then adds extra parameter for each found job
as 'qualified' / 'not qualified'. The principle is: if a key word appears in the job title or job description, this job will
be marked as 'not qualified'. Can be also set as an empty list: `red_flags = []`
2. Run the **`app.py`**<br>
`$ python3 app.py`


## Functionality:
1. Scraping jobs by the key parameters: search key-words, company type: direct employer or agency and education level.
2. Cleaning / formatting data.
3. Qualifying correctness of the search by the words-combinations in the job description. Adds a mark 'qualified' / 
' non qualified' to each found position based on the found red_flags in the title or the job summary.
4. Connects each found job with a city in the Netherlands, which helps to define precise geolocation (city name, 
province, longitude and latitude)
5. Each scraping session saves the results as a csv data dump to the *`data_dumps/`* folder.
6. Data Dump is saved into the POSTGRESQL database, preliminary excluding already existent in the database records. 
8. Each step of the scraping is logged into the **`log.txt`** with printing the outcomes in the console.


## Architecture:
1. **`app.py`** - enter point
2. **`main.py`** - the main workflow of the program
3. **`indeed_nl_scraper.py`** - scraping functionality module
4. **`dumping.py`** -  data cleaning / formatting module + saving data dumps
5. **`logger.py`** - logging functionality
6. **`database`** - connection and communication with the POSTGRESQL database.
7. **`.env`** - POSTGRESQL database engine credentials
8. **`parameters.py`** - keeping scraping parameters in separate module for easy access.

Additional:
1. **`db_scheme.py`** or **`db_scheme.sql`** for initial database setup.
2. **`requirements.txt`** required python packages.


## Requirements:
`python 3`
`postgresql engine`
<br><br>
Packages:
- `pandas 1.4.2`
- `requests 2.28.0`
- `beautifulsoup4 4.11.1`
- `python-dotenv 0.20.0`
- `SQLAlchemy 1.4.37`







