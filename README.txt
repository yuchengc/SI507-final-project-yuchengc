Goal:
I crawl [and scraping] multiple pages in the Michelin Guide website. Michelin Guide website list all recommended restaurants and sites in that city. I will focus on the restaurants part and crawl the detail information of each restaurant. For the restaurant, the website shows a list of all recommended restaurants. it also provides the filter to classify the distinction of each restaurant. I crawl all restaurants information and save it into database.

File:
(1)part1_crawl.py : crawl the information in the websites and store it into database.
(2)part2_interaction.py : provide interactive control (command line) for user to query the restaurant infomation.
(3)final_test.py: unittest. test the database query and class.
(4)michelin_cache_data.json: cache file
(5)help.txt: short instruction

How to use:
City:
	Which city do you want to explore? (1) SF (=San-Francisco) (2) NY (=New York)

Catalog:
	(1)all, (2) 3 stars, (3) 2 stars, (4)1 stars, (5)Bib Gourmand, (6)The Plate MICHELIN

Restaurant detail:
	Show detail information for user.

	if you select (1) all, the system will shows all restaurants at that city and also draw a plotly map which includes types of restaurants for you and a donut chart to show the distribution of types. 

	if you select (2)-(6), the system will shows a list of restaurant (that catalog) and the plotly map. User can further query a specific restaurant and view its detail information and it's map.

