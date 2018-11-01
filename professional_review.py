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
HEADER_LIST = ["Country", "State", "Store Name", "Address", "Website URL",
"Tel Phone", "Email", "About", "Description"]
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
			COUNTRY_LIST.append({"country":link['href'].split("/")[0].title(), "state": link.text,"link":BASE_URL+link['href']})
		print(COUNTRY_LIST)
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
				print(country)
				header_link = BASE_URL+update.find('strong').find("a")['href']
				print("update request failed {}".format(header_link))
				update_req = requests.get(header_link)
				if update_req.status_code == 200:
					try:
						update_response = update_req.text;
						update_soup = BeautifulSoup(update_response, 'html.parser');
						header_sec = update_soup.find("div", class_="jumbotron")
						store_name = header_sec.find("h1", class_="display-4").text.decode('utf-8','ignore').strip()
						address = header_sec.find("p", class_="lead my-3").text.decode('utf-8','ignore').strip()
						web_url = header_sec.find_all("a")[0]['href'].decode('utf-8','ignore').strip()
						tel_phone = header_sec.find_all("a")[1]['href'].decode('utf-8','ignore').strip()
						email = update_soup.find_all("li", class_="text-info")[0].text
						about_desc = update_soup.find_all("p", class_="mb-0")
						about = about_desc[0].text.replace('\n', ' ')
						description =  ""
						if about_desc[1]:
							description = about_desc[1].text.decode('utf-8','ignore').strip().replace('\n', ' ')

						UPDATE_DATA.append([country['country'],country['state']
						, store_name, address, web_url, tel_phone, email, about, description ])
					except:
						pass
				else:
					print("update request failed {}".format(header_link))
			data.update({"Sheet {}".format(country['country']): UPDATE_DATA})
	else:
		logger.error("#----country {0} find details failed link {1}.----".format(country['country'], country['link']))


def format_file():
	from openpyxl import load_workbook
	from openpyxl.styles import Font, Alignment
	wb = load_workbook(filename=FILE_NAME)
	black_font = Font(size=11, bold=True, color='FF000000')
	count = 1
	
	for ws in wb.worksheets:
		width = 15
		ws.row_dimensions[0].height = 30
		for column in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
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