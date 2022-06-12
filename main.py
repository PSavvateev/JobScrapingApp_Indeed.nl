from parameters import positions, company_types, red_flags
from engine import ScrapingSession

session = ScrapingSession(positions, company_types, red_flags)

if __name__ == "__main__":
    session.run()
