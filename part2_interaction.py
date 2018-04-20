import requests
import json
from bs4 import BeautifulSoup
import sqlite3
import plotly.plotly as py
import plotly.graph_objs as go


DBNAME = 'restaurants.db'

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
		return message

def load_help_text():
	with open('help.txt') as f:
		return f.read()

# Part 3: Implement interactive prompt. We've started for you!
def interactive_prompt():
	help_text = load_help_text()
	response = ''
	response = input('Please enter the command ( search, exit, help):')
	# city=""
	while response != 'exit':
		# response = input('Enter a command: ')

		if response == 'help':
			print(help_text)
			# continue
		if response == 'search':    
			process_command(response)
		else:
			# while 
			print("Command not recognized")
		response = input('Please enter the command ( search, exit, help): ')


def process_command(command):
	command_city=input("Please select a city")
	command_splited=command_city.split(" ")

	if len(command_splited)>=1:
		# pass
		# if command_splited[0]=="NY":
		catalog_query=input("Which catalog(s) (1)all, (2) 3 stars, (3) 2 stars, (4)1 stars, (5)Bib Gourmand, (6)The Plate MICHELIN :")
		while catalog_query != 'back':
			if len(catalog_query)>=1:
				cata_q=catalog_query.split()

				for query in cata_q:
					print(query)
					if query == "1":
						pass
						# show all 
					if query == "2":
						query_result=query_db("3 Stars%", city=command_splited[0])
						# print(query_result[0])
						
						if len(query_result)>0:
							plot_sites_for_city(query_result,command_splited[0])
							restaurant_detail(query_result,command_splited[0])
							# for row in query_result:
							# 	# print(row)
							# 	print(row.title+"["+row.catalog+"] / "+row.cuisine)
							
						else:
							print("No Data")
					elif query == "3":
						query_result=query_db("2 Stars MICHELIN", city=command_splited[0])
						# print(query_result[0])
						
						if len(query_result)>0:
							plot_sites_for_city(query_result,command_splited[0])
							restaurant_detail(query_result,command_splited[0])
							# for row in query_result:
							# 	# print(row)
							# 	print(row.title+"["+row.catalog+"] / "+row.cuisine)
							
								
						else:
							print("No Data")
					elif query == "4":
						query_result=query_db("1%", city=command_splited[0])
						# print(query_result[0])
						
						if len(query_result)>0:
							plot_sites_for_city(query_result,command_splited[0])
							restaurant_detail(query_result,command_splited[0])
							# for row in query_result:
							# 	# print(row)
							# 	print(row.title+"["+row.catalog+"] / "+row.cuisine)
							# plot_sites_for_city(query_result,command_splited[0])
								
						else:
							print("No Data")
					elif query == "5":
						query_result=query_db("Bib Gourmand", city=command_splited[0])
						# print(query_result[0])
						
						if len(query_result)>0:
							plot_sites_for_city(query_result,command_splited[0])
							restaurant_detail(query_result,command_splited[0])
							# for row in query_result:
							# 	# print(row)
							# 	print(row.title+"["+row.catalog+"] / "+row.cuisine)
							# plot_sites_for_city(query_result,command_splited[0])
								
						else:
							print("No Data")
					elif query == "6":
						query_result=query_db("The Plate MICHELIN", city=command_splited[0])
						# print(query_result[0])
						
						if len(query_result)>0:
							plot_sites_for_city(query_result,command_splited[0])
							restaurant_detail(query_result,command_splited[0])
							# for row in query_result:
							# 	# print(row)
							# 	print(row.title+"["+row.catalog+"] / "+row.cuisine)
							# plot_sites_for_city(query_result,command_splited[0])
								# print(row[1]+"["+row[2]+"] / "+row[3])
						else:
							print("No Data")

					elif query == "1":
						query_result=query_db("All", city=command_splited[0])
						if len(query_result)>0:
						
							for row in query_result:
								# print(row)
								print(row.title+"["+row.catalog+"] / "+row.cuisine)
							plot_sites_for_city(query_result,command_splited[0])
							donut_chart(query_result,command_splited[0])
						else:
							print("No Data")

					else:
						print("Command not recognized")


			else:
				print("Command not recognized")

			catalog_query=input("Which catalog(s) (1)all, (2) 3 stars, (3) 2 stars, (4)1 stars, (5)Bib Gourmand, (6)The Plate MICHELIN, or back :")
		# pass
		# elif command_splited[0]=="San-Francisco":
		# 	pass
		# else:
		# 	print("Command not recognized")
	else:
		print("Command not recognized:"+command)

def restaurant_detail(restaurant_list,city):
	index=1
	for row in restaurant_list:
		# print(row)
		print('('+str(index)+')'+row.title+"["+row.catalog+"] / "+row.cuisine)
		index+=1

	restaurant_query=input("please select a restaurant number or back:")
	while restaurant_query != 'back':
		print('('+restaurant_query+')'+restaurant_list[int(restaurant_query)-1].title)
		print("Catalog: "+restaurant_list[int(restaurant_query)-1].catalog)
		print("Cuisine: "+restaurant_list[int(restaurant_query)-1].cuisine)
		print("Price range: "+restaurant_list[int(restaurant_query)-1].price)
		print("Phone: "+restaurant_list[int(restaurant_query)-1].phone)
		print("District: "+restaurant_list[int(restaurant_query)-1].district)
		print("Address: "+restaurant_list[int(restaurant_query)-1].address)
		print("Website: "+restaurant_list[int(restaurant_query)-1].web)


		plot_sites_for_city([restaurant_list[int(restaurant_query)-1]],city)
		restaurant_query=input("please select a restaurant number or back:")


def query_db(catalog,city):
	return_list=[]
	try:
		conn=sqlite3.connect(DBNAME)
		cur=conn.cursor()
		print("connected to db")
	except:
		print("error for connecting to db")

	# table_name=city+"_restaurants"
	insertion = [catalog]
	if city == "NY":
		if catalog=="All":
			db_statement="""
			 SELECT * FROM NY_restaurants;
			"""
			result=cur.execute(db_statement)
			conn.commit()
		else:
			db_statement="""
			 SELECT * FROM NY_restaurants WHERE [Catalog] LIKE ? ;
			"""

			result=cur.execute(db_statement, insertion)
			conn.commit()

	if city == "SF":
		if catalog=="All":
			db_statement="""
			 SELECT * FROM SF_restaurants;
			"""
			result=cur.execute(db_statement)
			conn.commit()
		else:
			db_statement="""
			 SELECT * FROM SF_restaurants WHERE [Catalog] LIKE ? ;
			"""

			result=cur.execute(db_statement, insertion)
			conn.commit()


	for row in result:
		# print(row)
		# print(row[1]+"["+row[2]+"] / "+row[3])
		return_list.append(Restaurant(row[1],row[2],row[3],row[4],row[10],row[6],row[5],row[11]))
		return_list[-1].gps_latitude=row[8]
		return_list[-1].gps_longitude=row[9]
		return_list[-1].web=row[12]
		# title,catalog,cuisine,district,phone_temp,address,price_s,link=None

	return return_list


def plot_sites_for_city(restaurant_list,city):

	ctlg_1star_lat_vals=[]
	ctlg_1star_lon_vals=[]
	ctlg_1star_text_vals=[]

	ctlg_2star_lat_vals=[]
	ctlg_2star_lon_vals=[]
	ctlg_2star_text_vals=[]

	ctlg_3star_lat_vals=[]
	ctlg_3star_lon_vals=[]
	ctlg_3star_text_vals=[]

	ctlg_bg_lat_vals=[]
	ctlg_bg_lon_vals=[]
	ctlg_bg_text_vals=[]

	ctlg_plate_lat_vals=[]
	ctlg_plate_lon_vals=[]
	ctlg_plate_text_vals=[]

	lat_vals = []
	lon_vals = []
	text_vals = []

	for restaurant in restaurant_list:
		if restaurant.gps_latitude != None:
			if restaurant.gps_longitude != None:
				lon_vals.append(restaurant.gps_longitude)			
				lat_vals.append(restaurant.gps_latitude)
				text_vals.append(restaurant.title)

				if restaurant.catalog=="1 Star MICHELIN":
					ctlg_1star_lat_vals.append(restaurant.gps_longitude)
					ctlg_1star_lon_vals.append(restaurant.gps_latitude)
					ctlg_1star_text_vals.append(restaurant.title)

				if restaurant.catalog=="2 Stars MICHELIN":
					ctlg_2star_lat_vals.append(restaurant.gps_longitude)
					ctlg_2star_lon_vals.append(restaurant.gps_latitude)
					ctlg_2star_text_vals.append(restaurant.title)

				if restaurant.catalog=="3 Stars MICHELIN":

					ctlg_3star_lat_vals.append(restaurant.gps_longitude)
					ctlg_3star_lon_vals.append(restaurant.gps_latitude)
					ctlg_3star_text_vals.append(restaurant.title)

				if restaurant.catalog=="Bib Gourmand":
					ctlg_bg_lat_vals.append(restaurant.gps_longitude)
					ctlg_bg_lon_vals.append(restaurant.gps_latitude)
					ctlg_bg_text_vals.append(restaurant.title)

				if restaurant.catalog=="The Plate MICHELIN":
					ctlg_plate_lat_vals.append(restaurant.gps_longitude)
					ctlg_plate_lon_vals.append(restaurant.gps_latitude)
					ctlg_plate_text_vals.append(restaurant.title)
	
	# print(lon_vals)	
		
	min_lat = 10000
	max_lat = -10000
	min_lon = 10000
	max_lon = -10000
	# print(type(lat_vals[0]))
	for str_v in lat_vals:
		v = float(str_v)
		if v < min_lat:
			min_lat = v
		if v > max_lat:
			max_lat = v
	for str_v in lon_vals:
		v = float(str_v)
		if v < min_lon:
			min_lon = v
		if v > max_lon:
			max_lon = v


	lat_axis = [min_lat, max_lat]
	lon_axis = [min_lon, max_lon]

	center_lat = (max_lat+min_lat) / 2
	center_lon = (max_lon+min_lon) / 2

	data_all =  dict(
		type = 'scattergeo',
		locationmode = 'USA-states',
		lon = lat_vals,
		lat = lon_vals,
		text = text_vals,
		mode = 'markers',
		marker = dict(
		size = 20,
		symbol = 'star',
		color = 'red'
		# title = '1 Star'
		))

	data_1star =  dict(
		type = 'scattergeo',
		locationmode = 'USA-states',
		lon = ctlg_1star_lat_vals,
		lat = ctlg_1star_lon_vals,
		text = ctlg_1star_text_vals,
		mode = 'markers',
		name = '1 Star',
		marker = dict(
		size = 12,
		symbol = 'star',
		color = 'yellow'
		
		))

	data_2star =  dict(
		type = 'scattergeo',
		locationmode = 'USA-states',
		lon = ctlg_2star_lat_vals,
		lat = ctlg_2star_lon_vals,
		text = ctlg_2star_text_vals,
		mode = 'markers',
		name = '2 Star',
		marker = dict(
		size = 16,
		symbol = 'star',
		color = 'orange',
		
		))
	data_3star =  dict(
		type = 'scattergeo',
		locationmode = 'USA-states',
		lon = ctlg_3star_lat_vals,
		lat = ctlg_3star_lon_vals,
		text = ctlg_3star_text_vals,
		mode = 'markers',
		name = '3 Star',
		marker = dict(
		size = 20,
		symbol = 'star',
		color = 'red',
		
		))
	data_gb =  dict(
		type = 'scattergeo',
		locationmode = 'USA-states',
		lon = ctlg_bg_lat_vals,
		lat = ctlg_bg_lon_vals,
		text = ctlg_bg_text_vals,
		mode = 'markers',
		name = 'Bib Gourmand',
		marker = dict(
		size = 10,
		symbol = 'circle',
		color = 'blue',
		
		))
	data_plate =  dict(
		type = 'scattergeo',
		locationmode = 'USA-states',
		lon = ctlg_plate_lat_vals,
		lat = ctlg_plate_lon_vals,
		text = ctlg_plate_text_vals,
		mode = 'markers',
		name = 'The Plate',
		marker = dict(
		size = 10,
		symbol = 'circle',
		color='black',
		
		))

	data = [data_1star, data_2star, data_3star, data_gb, data_plate]

	layout = dict(
			title = 'Restaurant in '+str(city),
			geo = dict(
				scope='usa',
				projection=dict( type='albers usa' ),
				showland = True,
				landcolor = "rgb(250, 250, 250)",
				subunitcolor = "rgb(100, 217, 217)",
				countrycolor = "rgb(217, 100, 217)",
				
				lataxis = {'range': lat_axis},
				lonaxis = {'range': lon_axis},
				center= {'lat': center_lat, 'lon': center_lon },
				countrywidth = 3,
				subunitwidth = 3
			),
		)


	fig = dict(data=data, layout=layout )
	# py.plot( fig, validate=False, filename='Nearby sites in '+str(text_vals))
	py.plot( fig, validate=False, filename='Restaurants in '+str(city) )
	# plot_nearby_for_site(state_park[0])
	# pass
def donut_chart(restaurant_list,city):
	star_1=0
	star_2=0
	star_3=0
	db=0
	plate=0

	try:
		conn=sqlite3.connect(DBNAME)
		cur=conn.cursor()
		print("connected to db")
	except:
		print("error for connecting to db")

	# table_name=city+"_restaurants"
	# insertion = [catalog]
	if city == "NY":
		# if catalog=="All":
		db_statement="""
		 SELECT * FROM US_Michelin WHERE City like"New-York";
		"""
		# result=cur.execute(db_statement)
		# conn.commit()

	if city == "SF":
		db_statement="""
		 SELECT * FROM US_Michelin WHERE City like"San-Francisco";
		"""

	result=cur.execute(db_statement)
	conn.commit()

	for row in result:
		tar_1=row[5]
		star_2=row[4]
		star_3=row[3]
		db=row[6]
		plate=row[7]
	# for restaurant in restaurant_list:	
	# 	if restaurant.catalog=="1 Star MICHELIN":
	# 		star_1+=1
	# 	if restaurant.catalog=="2 Stars MICHELIN":
	# 		star_2+=1
	# 	if restaurant.catalog=="3 Stars MICHELIN":
	# 		star_3+=1
	# 	if restaurant.catalog=="Bib Gourmand":
	# 		db+=1
	# 	if restaurant.catalog=="The Plate MICHELIN":
	# 		plate+=1


	fig = {
	  "data": [
	    {
	      "values": [star_1, star_2, star_3, db, plate],
	      "labels": [
	        "1 Star MICHELIN",
	        "2 Stars MICHELIN",
	        "3 Stars MICHELIN",
	        "Bib Gourmand",
	        "The Plate MICHELIN"
	      ],
	      "domain": {"x": [0, .48]},
	      "name": "Restaurant distribution ",
	      "hoverinfo":"label+percent+name",
	      "hole": .4,
	      "type": "pie"
	    }],
	  "layout": {
	        "title":'Restaurants in '+str(city),
	        "annotations": [
	            {
	                "font": {
	                    "size": 20
	                },
	                "showarrow": False,
	                "text": str(city),
	                "x": 0.20,
	                "y": 0.5
	            }
	        ]
	    }
	}
	py.plot(fig, filename='donut')


if __name__=="__main__":
	# interactive_prompt()
	process_command("response")
