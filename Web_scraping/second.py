from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import pdfkit
import pytesseract
import cv2
import time
import csv
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client


from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
from PIL import Image
from selenium import webdriver
from PIL import Image
from io import BytesIO
wd = webdriver.Chrome()
wd.get("https://freesearchigrservice.maharashtra.gov.in/")
order = ['DocNo', 'DName', 'RDate', 'SROName', 'Seller Name',
		 'Purchaser Name', 'Property Description', 'SROCode', 'Status', 'IndexII']
with open('./output.csv', 'a+') as f:
	writer = csv.DictWriter(f, fieldnames=order)
	writer.writeheader()
try:
	elem = wd.find_element_by_id('ddlFromYear')
	print('Found <%s> element with that class name!' % (elem.tag_name))
except:
	print('Was not able to find an element with that name.')
select = Select(wd.find_element_by_id('ddlDistrict'))
select.select_by_visible_text('मुंबई उपनगर जिल्हा')

time.sleep(2)


village_name = wd.find_element_by_id('txtAreaName')


village_name.send_keys('kole')
village_name.send_keys(Keys.ENTER)
time.sleep(4)

select_village = wd.find_element_by_id('ddlareaname')
select_village.click()

select_village = wd.find_element_by_id('ddlareaname')
j = 0
for option in select_village.find_elements_by_tag_name('option'):
	if(j == 0):
		print('0')
	else:
		s3 = Select(wd.find_element_by_id('ddlareaname'))
		s3.select_by_visible_text(option.text)
		property_num = wd.find_element_by_id('txtAttributeValue')
		property_num.send_keys('4207')
		time.sleep(1)

		elem = wd.find_element_by_id('imgCaptcha')
		location = elem.location
		size = elem.size
		png = wd.get_screenshot_as_png()

		im = Image.open(BytesIO(png))

		left = location['x']+80
		top = location['y']+165
		right = left + size['width']
		bottom = top + size['height']+20

		im = im.crop((left, top, right, bottom))  # defines crop points
		# saves new cropped image

		im.save('./screenshot.png')
		elem2 = wd.find_element_by_id('txtImg')
		image = cv2.imread('./screenshot.png')
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		text = pytesseract.image_to_string(gray)
		elem2.send_keys(text)
		apply = wd.find_element_by_id('btnSearch')
		apply.click()
		time.sleep(8)

		currentUrl = wd.current_url

		
		element = wd.find_element_by_xpath("//*[@id='RegistrationGrid']/tbody")
		all_options = element.find_elements_by_tag_name("tr")
		lenofpg=len(all_options)
		print(lenofpg)
		for start in range(1,lenofpg-2):
			element = wd.find_element_by_xpath("//*[@id='RegistrationGrid']/tbody")
			all_options = element.find_elements_by_tag_name("tr")
			option = all_options[start]
			text_ext='NILNILNIL'
			all_fields = option.find_elements_by_tag_name("td")
			time.sleep(2)
			d = {
				'DocNo': all_fields[0].text,
				'DName': all_fields[1].text,
				'RDate': all_fields[2].text,
				'SROName':all_fields[3].text,
				'Seller Name': all_fields[4].text,
				'Purchaser Name':all_fields[5].text,
				'Property Description': all_fields[6].text,
				'SROCode': all_fields[7].text,
				'Status': all_fields[8].text,
				'IndexII': text_ext
			}
			wd0 = wd.window_handles[0]
			try:
				all_fields[9].click()
				time.sleep(3)
				wd1 = wd.window_handles[1]
				wd.switch_to.window(wd1)
				elem = wd.find_element_by_tag_name("body")
				text_ext=elem.text
			except:
				print("no external Link")
			wd.switch_to.window(wd0)
			data = []
			for key, val in d.items():
				val = val.replace('\n', '')
				val = val.replace(',', '')
				val = val.replace('NILNILNIL', text_ext)
				d[key] = val
			data.append(d)

			with open('./output.csv', 'a+') as f:
				writer = csv.DictWriter(f, fieldnames=order)
				writer.writerows(data)
				print('written')

	j = j+1
