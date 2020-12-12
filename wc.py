# Name:                                            Renacin Matadeen
# Date:                                               11/29/2020
# Title                                 Toronto Police Auctions - Website Parsing
#
# ----------------------------------------------------------------------------------------------------------------------
import time
import re

from wc_funcs import *

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# ----------------------------------------------------------------------------------------------------------------------


# Create A WebCrawler Class
class WebCrawler():


    # Initial Function, Run When A WebCrawler Object Is Created
    def __init__(self):
        self.raw_html = ""
        path = r"C:\Users\renac\Documents\Programming\Python\Selenium\chromedriver.exe"

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

        self.chrome_driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=path)


    # Navigate To Url | Get Newest HTML Data
    def navigate_url(self, url):
        self.chrome_driver.get(url)
        self.raw_html = self.chrome_driver.page_source
        time.sleep(2)


    # Scrape Number Of Pages On Website
    def scrape_pages(self):
        if self.raw_html != "":

            # Find The Pagination At The Bottom Of The Page Within The Raw HTML
            pagination_pattern = r'">([0-9]{1,2})</a>'
            page_html = re.findall(pagination_pattern, self.raw_html)
            return int(page_html[-1])

        else:
            print("No HTML Data To Scape Pages")


    # Scrape Listing IDs On A Given Webpage
    def scrape_ids(self):
        if self.raw_html != "":

            # Find All Instances Of Listings With Regular Expression Pattern
            listing_pattern = r'/Listing/Details/(.*)" class="btn btn-primary'
            instances = re.findall(listing_pattern, self.raw_html)
            return instances

        else:
            print("No HTML Data To Collect IDs")


    # Scrape Data On Individual Item
    def scrape_data(self):
        if self.raw_html != "":
            item_data = collect_item_info(self.raw_html, self.chrome_driver)
            return item_data

        else:
            print("No HTML Data To Data Mine")



    # Ask The WebCrawler To Set-Up A Connection To A Database; Create One If Not Present
    def connect_to_db(self):
        pass


    # Close WebCrawler
    def self_destruct(self):
        self.chrome_driver.quit()
