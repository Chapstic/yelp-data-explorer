"""
	This script grabs data from the Yelp API based on 
"""


import csv
import datetime
from datetime import timedelta
import json
import os
import pandas as pd
import requests
import sys


_URL_BASE = 'https://api.yelp.com/v3/businesses/'
_API_KEY = None

def get_credentials():
	global _API_KEY
	with open('credentials.json') as cred_file:
		data = json.load(cred_file)
	_API_KEY = data['api_key']
	

def get_data():	
	headers = {
		'Authorization':'Bearer {0}'.format(_API_KEY)
	}
	params = {
		'term': 'restaurants', # optional
		'location': 'San Francisco', # required if latiude or longitude not provided
		# 'latitude' # required if location not provided
		# 'longitude' # required if location not provided
		'radius': 40000, # optional(25 mile max)
		'limit': 50, # number of results, max is 50
		# 'categories': None, # optional, supported list: https://www.yelp.com/developers/documentation/v3/all_category_list
		# 'price': '1,2', # optional, 1=$, 2=$$, etc
	}
	url = _URL_BASE + 'search'
	response = requests.get(url, headers=headers, params=params)
	data = response.json()
	# print(data)

	dst_csv = 'data.csv'
	count = 0
	with open(dst_csv, mode='w', newline='') as write_file:
		csvwriter = csv.writer(write_file)
		businesses = data['businesses']
		for packet in businesses:
			if count == 0:
				header = packet.keys()
				csvwriter.writerow(header)
				count +=1
			else:
				csvwriter.writerow(packet.values())
				count += 1
	return dst_csv
	
			
def main():	
	get_credentials()
	dst_csv = get_data()

	
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print('Interrupted')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)