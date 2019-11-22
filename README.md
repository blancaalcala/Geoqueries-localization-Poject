# Study on the potential localization of tech company:

This project is focused on the study of different parameters in order to find the optimal location to set an emerging tech company.
After asking all the employees about their preferences on where to place this new office, different factors were studied:
-  Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.
- 30% of the company have at least 1 child.
- Developers like to be near successful tech startups that have raised at least 1 Million dollars.
- Executives like Starbucks A LOT. Ensure there's a starbucks not to far.
- Account managers need to travel a lot
- All people in the company have between 25 and 40 years, give them some place to go to party.
- Nobody in the company likes to have companies with more than 10 years in a radius of 2 KM.
- The CEO is Vegan

Using spatial geoqueries, scraping different websites and using APIs have provided enough information to locate all the different parameters needed to rank the different positions available for setting the company

# Input

- companies.json : file used to obtain information about different companies (obtained from crunchbase)
- public_scools.csv : file obtained from Kaggle database with information regarding public schools in Boston
- startups.csv :  file obtained from angel.io with information regarding different startups in Boston with a minimum revenue of 2M

# Src

- old_companies.ipynb : filters companies founded before 2009 and creates a new attribute in mongo db called location in GEOJSON format
- schools.ipynb : obtains the location of the schools from the csv file and creates a new attribute in the collection in mongo db called location in GEOJSON format
- startups.ipynb: obtains the location of the startups using google places API and creates a new attribute in the collection in mongo db called location in GEOJSON format
- starbucks_nights_vegan.ipynb : creates 3 new collections in mongo db with information about starbucks and their locations in Boston, night bars and their locations in Boston and vegan restaurants in Boston and their locations
- offices.ipynb : performs web scraping of a website focused on office rentals in Boston and stores the obtained variables (office adress, size, coordinates and reference)
- airport_city.ipynb : obtains the coordinates of the city centre and the airport in Boston using google places API
- results.ipynb : Results of the localized categories are mapped (old companies, schools, startups, starbucks, night bars, offices for rent, airport and vegan restaurants).
After ranking each possible office in terms of the rest of the categories depending on the chosen weight of each one of them, a csv table containing information about these offices is saved, and the chosen office (chosen by index) is mapped  in order to visualize its location.

# Output

- csv file containing information about all the potential offices the company could rent
- Two maps saved in html format in order to be able to visualize them outside jupyter notebook