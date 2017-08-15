from selenium import webdriver
import os
import urllib
import time
from configuration import CONFIG


chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": os.path.dirname(os.path.abspath(__file__)),
    "directory_upgrade": True
}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(CONFIG['DOWNLOAD_PAGE_WEBSITE_LINK'])

numberOfImages = 100

for index in range (numberOfImages):
    captchaImage = driver.find_element_by_xpath(CONFIG['CAPTCHA_IMAGE_XPATH'])
    src = captchaImage.get_attribute('src')
    urllib.urlretrieve(src, 'captcha-{0}.png'.format(index))
    time.sleep(3)
    driver.execute_script("location.reload()")

