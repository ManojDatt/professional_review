"""
pip install pyexcel-xlsx
pyexcel-io==0.5.9.1
pyexcel-xlsx==0.5.6
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
FILE_NAME = os.path.join(os.getcwd(),"report/professional-review_{}.xlsx".format(int(time.time())))

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
			
			updates = soup.find_all("div", class_="card flex-md-row mb-4 box-shadow h-md-200")
			for update in updates:
				logo = update.find('img')['src']
				header = update.find('strong').find('a').text
				header_link = BASE_URL+update.find('strong').find("a")['href']
				update_date = update.find('div', class_='text-muted').text.split(" ")[-1]
				message = update.find('p', class_='card-text').text
				# get update data 
				update_req = requests.get(header_link)
				if update_req.status_code == 200:
					update_response = update_req.content;
					update_soup = BeautifulSoup(update_response, 'html.parser');
					latest_updates = soup.find_all("div", class_="card flex-md-row mb-4 box-shadow h-md-200")
					for update_data in latest_updates:
						title = soup.select("h1.display-4")[0].text
						title_desc = soup.find("p", class_="lead my-3").text
						header_links = soup.find_all("a")
					

				UPDATE_DATA.append([country['name'], title, logo, header, header_link, update_date, message ])
			data.update({"Sheet {}".format(country['name']): UPDATE_DATA})
	else:
		logger.error("#----country {0} find details failed link {1}.----".format(country['name'], country['link']))


def format_file():
	from openpyxl import load_workbook
	from openpyxl.styles import Font, Alignment
	wb = load_workbook(filename=FILE_NAME)
	black_font = Font(size=11, bold=True, color='FF000000')
	count = 1
	
	for ws in wb.worksheets:
		width = 15
		ws.row_dimensions[0].height = 30
		for column in ["A", "B", "C", "D", "E", "F", "G"]:
			ws.column_dimensions[column].width = width
			width+=10

		for cell in ws["1:1"]:
			cell.font = black_font
			cell.alignment = Alignment(horizontal='center', vertical='center',wrap_text=True)
			count +=1

	wb.save(filename=FILE_NAME)

if __name__ == "__main__":
	get_details()
	save_data(FILE_NAME, data)
	format_file()
	logger.info("#-------done--------")