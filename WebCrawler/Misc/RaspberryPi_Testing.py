# Name:                                            Renacin Matadeen
# Date:                                               11/29/2020
# Title                                 Toronto Police Auctions - Website Parsing
#
# ----------------------------------------------------------------------------------------------------------------------
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# ----------------------------------------------------------------------------------------------------------------------


# Create A WebCrawler Class


path = r"/usr/lib/chromium-browser/chromedriver"
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# 'javascript': 2,
prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2,
                            'plugins': 2, 'popups': 2, 'geolocation': 2,
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
                            'durable_storage': 2}}
chrome_options.add_experimental_option('prefs', prefs)

chrome_driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=path)
chrome_driver.get("https://google.com")


