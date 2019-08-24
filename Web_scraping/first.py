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

elem = wd.find_element_by_id('imgCaptcha')
location = elem.location
size = elem.size
png = wd.get_screenshot_as_png()


im = Image.open(BytesIO(png)) 


left = location['x']+50
top = location['y']+165
right = left + size['width']+25
bottom = top + size['height']+20


im = im.crop((left, top, right, bottom)) # defines crop points
im.save('./screenshot.png') # saves new cropped image


import pytesseract,cv2
image = cv2.imread('./screenshot.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

text  = pytesseract.image_to_string(gray)

print(text)





# now that we have the preliminary stuff out of the way time to get that image :D




 # uses PIL library to open image in memory



