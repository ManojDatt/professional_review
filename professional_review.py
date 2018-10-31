"""
pip install pyexcel-xlsx
python professional-review.py
"""
import re
import os
import time
import requests
from bs4 import BeautifulSoup
import json
import logging
from pyexcel_xlsx import save_data
from collections import OrderedDict
logging.basicConfig(filename="job-logs.log",
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='w',
                    level=logging.DEBUG)
logger=logging.getLogger()

BASE_URL = "http://professional-review.com/"
COUNTRY_LIST=[]
HEADER_LIST = ["Country", "Title", "Update Logo", "Update Header", "Update Link", "Update Date", "Update Content"]
data = OrderedDict()
__program__ = ""
__version__ = "0.0.1"
def get_country():
	logger.info("#----start to find all country----") 
	req = requests.get(BASE_URL)
	if req.status_code == 200:
		response = req.content;
		soup = BeautifulSoup(response, 'html.parser');
		links = soup.find_all("a", class_="p-2 text-muted")
		for link in links:
			COUNTRY_LIST.append({"name":link.text,"link":BASE_URL+link['href']})
		logger.info("#----country find success----")
	else:
		logger.error("#----country find request failed.----")


def get_details():
	get_country()
	for country in COUNTRY_LIST:
		req = requests.get(country['link'])
		if req.status_code == 200:
			UPDATE_DATA = [HEADER_LIST]
			response = req.content;
			soup = BeautifulSoup(response, 'html.parser');
			title = soup.select("h1.display-4")[0].text
			latest_updates = soup.find_all("div", class_="card flex-md-row mb-4 box-shadow h-md-200")
			for update in latest_updates:
				logo = update.find('img')['src']
				header = update.find('strong').find('a').text
				header_link = update.find('strong').find("a")['href']
				update_date = update.find('div', class_='text-muted').text.split(" ")[-1]
				message = update.find('p', class_='card-text').text
				UPDATE_DATA.append([country['name'], title, logo, header, header_link, update_date, message ])
			data.update({"Sheet {}".format(country['name']): UPDATE_DATA})
	else:
		logger.error("#----country {0} find details failed link {1}.----".format(country['name'], country['link']))


if __name__ == "__main__":
	get_details()
	save_data("profession-review_{}.xlsx".format(int(time.time()), data)
	logger.info("#-------done--------")