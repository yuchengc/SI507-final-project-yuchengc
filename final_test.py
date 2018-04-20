import unittest
from part1_crawl import *
from part2_interaction import *
# from part1_crawl import *

class TestDatabase(unittest.TestCase):
	def test_restaurant_table(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()

		sql = 'SELECT Title FROM SF_restaurants'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertIn(('Aster',), result_list)
		self.assertEqual(len(result_list), 150)

		sql = 'SELECT Catalog FROM SF_restaurants'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertIn(('3 Stars MICHELIN',), result_list)


		sql = '''
			SELECT *
			FROM SF_restaurants
			WHERE [Catalog] like "1 Star MICHELIN"
		'''
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertEqual(len(result_list), 23)
		# self.assertEqual(results.rowcount,23)

		sql = 'SELECT Title FROM NY_restaurants'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertIn(('Danji',), result_list)
		self.assertEqual(len(result_list), 150)

		sql = 'SELECT Catalog FROM NY_restaurants'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertIn(('3 Stars MICHELIN',), result_list)


		sql = '''
			SELECT *
			FROM SF_restaurants
			WHERE [Catalog]="2 Stars MICHELIN"
			
		'''
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertEqual(len(result_list), 6)
		conn.close()

	def test_US_table(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()

		sql = '''
			SELECT Total
			FROM US_Michelin

		'''
		results = cur.execute(sql)
		count = results.fetchone()[0]
		self.assertEqual(count, 150)

		sql = '''
			SELECT BibGourmand
			FROM US_Michelin

		'''
		results = cur.execute(sql)
		count = results.fetchone()[0]
		self.assertEqual(count, 35)

		conn.close()
	def test_restaurant_class(self):
		# pass
		test_rest=Restaurant("Luce","1 Star MICHELIN","Contemporary","SoMa","+1 415-616-6566","888 Howard St., CA 94103","50 - 75 USD","/us/san-francisco/luce/restaurant")
		self.assertEqual(test_rest.title, "Luce")
		self.assertEqual(test_rest.cuisine, "Contemporary")
		self.assertEqual(test_rest.phone, "+1 415-616-6566")
		# "141"	"Luce"	"1 Star MICHELIN"	"Contemporary"	"SoMa"	"50 - 75 USD"	"888 Howard St., CA 94103"	"1"	"37.7819400"	"-122.4049800"	"+1 415-616-6566"	"/us/san-francisco/luce/restaurant"
	def test_restaurant_db_query(self):
		# test_rest=Restaurant("Luce","1 Star MICHELIN","Contemporary","SoMa","+1 415-616-6566","888 Howard St., CA 94103","50 - 75 USD","/us/san-francisco/luce/restaurant")
		# get_gps(test_rest)
		test_rest=query_db("2 Stars MICHELIN","SF")
		self.assertEqual(test_rest[0].title, "Acquerello")
		self.assertEqual(test_rest[0].cuisine, "Italian")


		test_rest=query_db("The Plate MICHELIN","NY")
		self.assertEqual(test_rest[0].title, "15 East")
		self.assertEqual(test_rest[0].cuisine, "Japanese")
		
unittest.main()
