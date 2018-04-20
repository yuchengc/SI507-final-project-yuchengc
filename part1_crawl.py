# 507/206 Homework 7 Part 1
import requests
import json
from bs4 import BeautifulSoup
import sqlite3

DBNAME = 'restaurants.db'
CACHE_GOOGLE_GPS = 'google_nearby_cache_data.json'
CACHE_FNAME = 'michelin_cache_data.json'

try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()

# if there was no file, no worries. There will be soon!
except:
	CACHE_DICTION = {}

try:
	gp_cache_file = open(CACHE_GOOGLE_GPS, 'r')
	gp_cache_contents = gp_cache_file.read()
	GPS_CACHE_DICTION = json.loads(gp_cache_contents)
	gp_cache_file_state.close()
except:
	GPS_CACHE_DICTION={}

#### Your Part 1 solution goes here ####
class Restaurant():
	def __init__(self,title,catalog,cuisine,district,phone_temp,address,price_s,link=None):
		self.title=title
		self.catalog=catalog
		self.cuisine=cuisine
		self.district=district
		self.phone=phone_temp
		self.address=address
		self.price=price_s
		self.link=link

		self.web=''
		self.gps_latitude=None
		self.gps_longitude=None

	def __str__(self):
		message=self.title+'('+self.catalog+')'+' : '+self.cuisine+','+self.district+','+self.price+'/n'+'Contact info: '+self.address+'('+self.phone+')'

def get_web_data(page,city,restaurant_list):
	#  crawl [and scraping] multiple pages in the Michelin Guide website
	

	data=[]
	print(page)
	baseurl = 'https://guide.michelin.com/us/'+city+'/restaurants/page/'+str(page)+'?max=30&sort=relevance&order=desc'
	extendedurl = baseurl #+ '/page/'+str(page)
	# params={'max':'30','sort':'relevance','order': 'desc'}
	params={}
	header = {'User-Agent': 'SI_CLASS'}
	print(baseurl)

	page_text_cache=make_request_using_cache(CACHE_DICTION,CACHE_FNAME,baseurl,params,header)
	page_soup = BeautifulSoup(page_text_cache,'html.parser')


	michelin_catalog={"=":"Bib Gourmand","‹":"The Plate MICHELIN","m":"1 Star MICHELIN","n":"2 Stars MICHELIN","o":"3 Stars MICHELIN"}


	name = page_soup.find_all(class_='grid-restaurants__item__body')



	title_all= page_soup.find_all(class_='resto-inner-title')
	# print(title_all)
	for link_i in range(len(title_all)):
		title=title_all[link_i].a.text
		title=title.strip()
		catalog=michelin_catalog[title[-1:]]
		title=title[:-2].strip()
		link= title_all[link_i].a['href']


# crawl the restaurant single page by using the link from main page.
		sub_baseurl = 'https://guide.michelin.com'
		sub_extendedurl = sub_baseurl+link 
		params={}
		header = {'User-Agent': 'SI_CLASS'}

		restaurant_page_text_cache=make_request_using_cache(CACHE_DICTION,CACHE_FNAME,sub_extendedurl,params,header)
		restaurant_page_soup = BeautifulSoup(restaurant_page_text_cache, 'html.parser')
		try:
			cuisine_temp=restaurant_page_soup.find(class_="content-header-desc__cuisine")
			cuisine=cuisine_temp.a.string
		except:
			cuisine=''
		
		try:
			district_temp=restaurant_page_soup.find(class_="content-header-desc__area")
			district=district_temp.a.string
			print(district)
		except:
			district=''

		try:
			price_temp=restaurant_page_soup.find_all(class_="restaurant-criteria__desc")
			price=price_temp[-1].string
			price_s=price.strip()
			# print("price")
			print(price_s)
		except:
			price_s=''
		# print(restaurant_page_soup)

		try:
			address_temp=restaurant_page_soup.find_all(class_="location-item__desc")
			# print(len(address_temp))
			p_address=address_temp[0].find_all('p')

			address=p_address[1].string
			address=address.strip().replace("\n", "")
			address=address.replace("  ","")
		except:
			address=''

		try:
			web_temp=restaurant_page_soup.find_all(class_="o-link")
			# print(len(address_temp))
			web=web_temp[1]["href"]

			# address=p_address[1].string
			# address=address.strip().replace("\n", "")
			# address=address.replace("  ","")
		except:
			web=''

		# print(p_address)
		try:
			phone_temp=address_temp[3].p.string

		except:
			phone_temp=''

		# try:
		gps_tag=restaurant_page_soup.find(class_="v-location-map")
		gps_lat=gps_tag.div["data-lat"]
		gps_lon=gps_tag.div["data-lon"]
		
		print(title+"("+catalog+")"+" : "+link)
		print(address)
		print(phone_temp)

		data.append([title,catalog,cuisine,district,phone_temp,address,price_s,link])
		restaurant_list.append(Restaurant(title,catalog,cuisine,district,phone_temp,address,price_s,link))
		restaurant_list[-1].gps_latitude=gps_lat
		restaurant_list[-1].gps_longitude=gps_lon
		restaurant_list[-1].web=web
		
	return restaurant_list

	# return umsi_titles





def get_gps(restaurant):
	# use google place to get GPS

	GOOGLE_PLACE_KEY="AIzaSyBoCZBzpt1ZfEh37nrBDO1CkoaQMxUULNg"
	# google_nearby_baseurl='https://maps.googleapis.com/maps/api/place/nearbysearch/'
	google_textsearch_url='https://maps.googleapis.com/maps/api/place/textsearch/json'


	textsearch_params={"key":GOOGLE_PLACE_KEY,'query':restaurant.title}
	# ,'name':national_site.name,'type':national_site.type
	# google_gps = requests.get(google_textsearch_url, textsearch_params).text
	google_gps=make_request_using_cache(GPS_CACHE_DICTION,CACHE_GOOGLE_GPS,google_textsearch_url, textsearch_params,header={})
	gps_result=json.loads(google_gps)
	# print(google_gps)
	# print(gps_result["results"][0]['geometry']['location'])
	# print(gps_result)
	if gps_result["status"] != 'ZERO_RESULTS':
		# if gps_result["results"][0]['geometry']['location']['lat']!= None:
		restaurant.gps_latitude=gps_result["results"][0]['geometry']['location']['lat']
		print(restaurant.gps_latitude)
		# else:
		# 	national_site.gps_latitude=None
		
		# if gps_result["results"][0]['geometry']['location']['lng'] != None:
		restaurant.gps_longitude=gps_result["results"][0]['geometry']['location']['lng']
		print(restaurant.gps_longitude)
		


def params_unique_combination(baseurl, params):
	alphabetized_keys = sorted(params.keys())
	res = []
	for k in alphabetized_keys:
		res.append("{}-{}".format(k, params[k]))
	return baseurl + "_".join(res)


def make_request_using_cache(cache_dict, cache_file, baseurl, params, header):
	unique_ident = params_unique_combination(baseurl,params)
	# print("unique_ident:"+unique_ident)

	## first, look in the cache to see if we already have this data
	if unique_ident in cache_dict:
		print("Getting cached data...")
		return cache_dict[unique_ident]


	else:
		print("Making a request for new data...")

		page_text = requests.get(baseurl, params, headers=header).text
		# page_soup = BeautifulSoup(page_text, 'html.parser')
		cache_dict[unique_ident] = page_text
		dumped_json_cache = json.dumps(cache_dict)
		fw = open(cache_file,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
		return cache_dict[unique_ident]



def create_db(city):
	try:
		conn=sqlite3.connect(DBNAME)
		cur=conn.cursor()
		print("connected to db")
	except:
		print("error for connecting to db")

	if city == "san-francisco":
		statement = '''
			DROP TABLE IF EXISTS 'SF_restaurants';
		'''
		cur.execute(statement)
		conn.commit()
		try:
			statement='''
				CREATE  TABLE 'SF_restaurants'(
					'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
					'Title' TEXT ,
					'Catalog' TEXT,
					'Cuisine' TEXT,
					'District' TEXT,
					'Price' TEXT,
					'Address' TEXT ,
					'City' TEXT,
					'GPSlatitude' TEXT ,
					'GPSlongitude' TEXT ,
					'Phone' TEXT ,
					'InternalLink' TEXT ,
					'Website' TEXT 
					);
				'''
			# insertion=table_name
			cur.execute(statement)
			conn.commit()
			print("created SF restaurants table")
		except:
			print("fail to create restaurants table")

	
	if city == "new-york":
		statement = '''
			DROP TABLE IF EXISTS 'NY_restaurants';
		'''
		cur.execute(statement)
		conn.commit()
		table_name="NY_restaurants"
		try:
			statement='''
				CREATE  TABLE 'NY_restaurants'(
					'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
					'Title' TEXT ,
					'Catalog' TEXT,
					'Cuisine' TEXT,
					'District' TEXT,
					'Price' TEXT,
					'Address' TEXT ,
					'City' TEXT,
					'GPSlatitude' TEXT ,
					'GPSlongitude' TEXT ,
					'Phone' TEXT ,
					'InternalLink' TEXT ,
					'Website' TEXT 
					);
				'''
			# insertion=table_name
			cur.execute(statement)
			conn.commit()
			print("created NY restaurants table")
		except:
			print("fail to create restaurants table")


def import_restaurant_data(data, city):
	#import crawled data into database 

	try:
		conn=sqlite3.connect(DBNAME)
		cur=conn.cursor()
		print("connected to db")
	except:
		print("error for connecting to db")


	for restaurant in data:
		# print(country.keys())
		insertion = (restaurant.title, restaurant.catalog, restaurant.cuisine, restaurant.district, restaurant.price, restaurant.address, restaurant.gps_latitude, restaurant.gps_longitude, restaurant.phone, restaurant.link, restaurant.web)
		if city == "san-francisco":
			db_statement="""
			INSERT INTO SF_restaurants (Title, Catalog, Cuisine, District, Price, Address, GPSlatitude, GPSlongitude, Phone, InternalLink,City, Website)
			VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?);
			"""
		if city == "new-york":
			db_statement="""
			INSERT INTO NY_restaurants (Title, Catalog, Cuisine, District, Price, Address, GPSlatitude, GPSlongitude, Phone, InternalLink, City, Website)
			VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 2, ?);
			"""
		cur.execute(db_statement, insertion)
		conn.commit()
	print("import restaurant data")

def create_US_Michelin_summary():
	try:
		conn=sqlite3.connect(DBNAME)
		cur=conn.cursor()
		print("connected to db")
	except:
		print("error for connecting to db")

	statement = '''
		DROP TABLE IF EXISTS 'US_Michelin';
	'''
	cur.execute(statement)
	conn.commit()

	# try:
	statement='''
		CREATE  TABLE 'US_Michelin'(
			'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
			'City' TEXT ,
			'Total' INT ,
			'ThreeStar' INT,
			'TwoStar' INT,
			'OneStar' INT,
			'BibGourmand' INT,
			'Plate' INT 
			);
		'''
	# insertion=table_name
	cur.execute(statement)
	conn.commit()
	print("created NY US_Michelin table")
	# except:
	# 	print("fail to create restaurants table")

def update_US_Michelin():
	try:
		conn=sqlite3.connect(DBNAME)
		cur=conn.cursor()
		print("connected to db")
	except:
		print("error for connecting to db")
	

	db_statement="""
			INSERT INTO US_Michelin (City, Total, ThreeStar, TwoStar, OneStar, BibGourmand, Plate)
			VALUES ( "San-Francisco", 
			(SELECT COUNT(*) FROM SF_restaurants), 
			(SELECT COUNT(*) FROM SF_restaurants WHERE [Catalog] like "3 Stars MICHELIN"), 
			(SELECT COUNT(*) FROM SF_restaurants WHERE [Catalog] like "2 Stars MICHELIN"),
			(SELECT COUNT(*) FROM SF_restaurants WHERE [Catalog] like "1 Star MICHELIN"),
			(SELECT COUNT(*) FROM SF_restaurants WHERE [Catalog] like "Bib Gourmand"),
			(SELECT COUNT(*) FROM SF_restaurants WHERE [Catalog] like "The Plate MICHELIN"));
			"""
	cur.execute(db_statement)
	conn.commit()

	db_statement="""
			INSERT INTO US_Michelin (City, Total, ThreeStar, TwoStar, OneStar, BibGourmand, Plate)
			VALUES ( "New-York", 
			(SELECT COUNT(*) FROM NY_restaurants), 
			(SELECT COUNT(*) FROM NY_restaurants WHERE [Catalog] like "3 Stars MICHELIN"), 
			(SELECT COUNT(*) FROM NY_restaurants WHERE [Catalog] like "2 Stars MICHELIN"),
			(SELECT COUNT(*) FROM NY_restaurants WHERE [Catalog] like "1 Star MICHELIN"),
			(SELECT COUNT(*) FROM NY_restaurants WHERE [Catalog] like "Bib Gourmand"),
			(SELECT COUNT(*) FROM NY_restaurants WHERE [Catalog] like "The Plate MICHELIN"));
			"""
	cur.execute(db_statement)
	conn.commit()

if __name__=="__main__":
	total_dict={}
	create_db("san-francisco")
	restaurant_list=[]
	for i in range(5):
		page_dict=get_web_data(i+1,"san-francisco",restaurant_list)
		# total_dict.update(page_dict)

	
	import_restaurant_data(page_dict,"san-francisco")
	# print(total_dict)
	# create_US_Michelin_summary()
	# update_US_Michelin()
# san-francisco
# umsiW = open("directory_dict.json","w")
# dumped_UMSI_json_cache = json.dumps(total_dict)
# umsiW.write(dumped_UMSI_json_cache)
# umsiW.close() # Close the open file

