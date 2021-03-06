from parameters import positions, company_types, education_level, red_flags
from main import ScrapingSession

session = ScrapingSession(positions, company_types, education_level, red_flags)

if __name__ == "__main__":
    session.run()
