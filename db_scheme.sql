CREATE TABLE IF NOT EXISTS jobs (
    job_id TEXT PRIMARY KEY,
    job_title TEXT,
    job_date DATE,
    job_loc TEXT,
    city_id INTEGER,
    job_summary TEXT,
    job_salary integer[],
    job_education TEXT,
    job_url TEXT,
    company_name TEXT,
    company_type TEXT,
    search_time TIMESTAMP,
    search_position TEXT,
    source TEXT,
    search_qualified TEXT,
    FOREIGN KEY(city_id) REFERENCES cities(id)

    );

CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    city TEXT,
    lat NUMERIC,
    lng NUMERIC,
    country TEXT,
    iso2 TEXT,
    admin_name TEXT,
    capital TEXT,
    population INTEGER,
    population_proper INTEGER
    );
