from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import pytesseract,cv2
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
for k in range(2010,2020):
	try:
		s3= Select(wd.find_element_by_id('ddlFromYear'))
		s3.select_by_visible_text(str(k))
		print('Found element with that year!')
	except:
		print('Was not able to find an element with that name.')
	District=['मुंबई जिल्हा','मुंबई उपनगर जिल्हा']
	for d in District:
		select = Select(wd.find_element_by_id('ddlDistrict'))
		select.select_by_visible_text(d)
		
		time.sleep(2)

		from selenium import webdriver
		for i in range(97,123):
			try:
				village_name = wd.find_element_by_id('txtAreaName')


				ii=chr(i)
				village_name.send_keys(Keys.BACKSPACE)
				village_name.send_keys(Keys.BACKSPACE)
				village_name.send_keys(Keys.BACKSPACE)
				village_name.send_keys(ii)
				village_name.send_keys(Keys.ENTER)
				time.sleep(4)

				select_village = wd.find_element_by_id('ddlareaname')
				select_village.click()
				time.sleep(2)
				select_village = wd.find_element_by_id('ddlareaname')
				j=0
				for option in select_village.find_elements_by_tag_name('option'):
					try:
						if(j==0):
							print ('0')
							j=j+1
						else:
							s3= Select(wd.find_element_by_id('ddlareaname'))
							s3.select_by_visible_text(option.text)
							j=j+1
							temp_option=option.text
							time.sleep(1)
							for i in range(1,10000):
								property_num = wd.find_element_by_id('txtAttributeValue')
								property_num.send_keys(Keys.BACKSPACE)
								property_num.send_keys(Keys.BACKSPACE)
								property_num.send_keys(i)
								#property_num.send_keys(Keys.ENTER)
								time.sleep(1)

								try:
									wd.execute_script("window.scrollTo(0, 0);")
									time.sleep(0.5)
									wd.execute_script("window.scrollTo(0, 0);")
									wd.execute_script("window.scrollTo(0, 0);")
									elem = wd.find_element_by_id('imgCaptcha')
									location = elem.location
									size = elem.size
									png = wd.get_screenshot_as_png()


									im = Image.open(BytesIO(png)) 


									left = location['x']+80
									top = location['y']+165
									right = left + size['width']
									bottom = top + size['height']+20


									im = im.crop((left, top, right, bottom)) # defines crop points
									 # saves new cropped image

									im.save('./screenshot.png') 
									elem2 = wd.find_element_by_id('txtImg')
									image = cv2.imread('./screenshot.png')
									gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

									text  = pytesseract.image_to_string(gray)
									elem2.send_keys(Keys.BACKSPACE)
									elem2.send_keys(Keys.BACKSPACE)
									elem2.send_keys(Keys.BACKSPACE)
									elem2.send_keys(Keys.BACKSPACE)
									elem2.send_keys(Keys.BACKSPACE)
									elem2.send_keys(text)
									apply = wd.find_element_by_id('btnSearch')
									apply.click()
									time.sleep(5)
									element = wd.find_element_by_xpath("//*[@id='RegistrationGrid']/tbody")
									all_options = element.find_elements_by_tag_name("tr")
									lenofpg=len(all_options)
									pgnum=1
									try:
										while(1):
											bottom_nav=wd.find_element_by_xpath('//*[@id="RegistrationGrid"]/tbody/tr[12]')
											all_nav = bottom_nav.find_elements_by_tag_name("td")
											len_bottom=len(all_nav)
											print(len_bottom)
											if(len_bottom==12):
												if(pgnum==11):
													butn=wd.find_element_by_xpath('//*[@id="RegistrationGrid"]/tbody/tr[12]/td/table/tbody/tr/td[11]/a')
													butn.click()
													time.sleep(3)
													print('... Clicked')
													pgnum=1
												else:
													butn=wd.find_element_by_xpath('//*[@id="RegistrationGrid"]/tbody/tr[12]/td/table/tbody/tr/td[{}]'.format(pgnum))
													butn.click()
													print("{} clicked".format(pgnum))
													pgnum=pgnum+1
													time.sleep(2)
											if(len_bottom==13):
												pgnum=pgnum+1
												if(pgnum==12):
													butn=wd.find_element_by_xpath('//*[@id="RegistrationGrid"]/tbody/tr[12]/td/table/tbody/tr/td[12]/a')
													butn.click()
													print('... Clicked')
													time.sleep(3)
													pgnum=1
												else:
													
													butn=wd.find_element_by_xpath('//*[@id="RegistrationGrid"]/tbody/tr[12]/td/table/tbody/tr/td[{}]'.format(pgnum))
													butn.click()
													print("{} clicked".format(pgnum))
													time.sleep(2)
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
									except:
										print('end of property records')


								except:
									print('error detecting captcha')
									village_name.send_keys(Keys.BACKSPACE)
								s3= Select(wd.find_element_by_id('ddlFromYear'))
								s3.select_by_visible_text(str(k))
								select = Select(wd.find_element_by_id('ddlDistrict'))
								select.select_by_visible_text(d)
								time.sleep(2)
								village_name = wd.find_element_by_id('txtAreaName')
								
								village_name.send_keys(ii)
								village_name.send_keys(Keys.ENTER)
								time.sleep(3)

								select_village = wd.find_element_by_id('ddlareaname')
								select_village.click()

								select_village = wd.find_element_by_id('ddlareaname')
								s3= Select(wd.find_element_by_id('ddlareaname'))
								s3.select_by_visible_text(temp_option)


								property_num = wd.find_element_by_id('txtAttributeValue')
								property_num.send_keys(Keys.BACKSPACE)
								property_num.send_keys(Keys.BACKSPACE)
								property_num.send_keys(Keys.BACKSPACE)
								property_num.send_keys(Keys.BACKSPACE)


					except:
						print('Not Found')
						property_num.send_keys(Keys.BACKSPACE)
						property_num.send_keys(Keys.BACKSPACE)


					
				time.sleep(1)
				village_name = wd.find_element_by_id('txtAreaName')
				village_name.send_keys(Keys.BACKSPACE)

			except:
				print('Crashed')