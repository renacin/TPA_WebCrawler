# Name:                                            Renacin Matadeen
# Date:                                               11/29/2020
# Title                       Toronto Police Auctions - Website Parsing - Additional Fuunctions
#
# ----------------------------------------------------------------------------------------------------------------------
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# ----------------------------------------------------------------------------------------------------------------------


# Function To Grab Data From Website Either With HTML Or Xpath Scrape
def collect_item_info(raw_html, cdriver_object):


            # Find Name, SKU_ID, Current Price, Upbid Increase | Use Regular Expression, Quicker?
            try:
                re_name = r'title">(.*)<img src'
                re_name_data = re.findall(re_name, raw_html)
                item_name = re_name_data[0]

                re_TPA_ID = r'\(([0-9]{1,7}.)\)'
                re_TPA_ID_data = re.findall(re_TPA_ID, item_name)
                item_TPA_ID = re_TPA_ID_data[0]

                full_TPA_ID = "(" + str(item_TPA_ID) + ")"

                # Clean Name
                item_name = item_name.replace("&amp;", "")
                for clean_x in [full_TPA_ID, "  ", "   ", "    "]:
                    item_name = item_name.replace(clean_x, "")

                re_cur_price = r'Part">(.{1,10})</span>'
                re_cur_price_data = re.findall(re_cur_price, raw_html)
                parsed_prices = re_cur_price_data

                cur_price = re_cur_price_data[0]
                min_upbid = re_cur_price_data[1]
                upbid_increase = round(float(min_upbid) - float(cur_price), 2)


            except ValueError:
                item_name = "N/A"
                item_TPA_ID = "N/A"

                cur_price = "N/A"
                min_upbid = "N/A"
                upbid_increase = "N/A"



            # Find Minutes Left Remaining | Use Selenium Select By Xpath
            try:
                time_remaining_raw = cdriver_object.find_element_by_xpath('/html/body/main/div/div[2]/div/div[3]/div[3]/div[1]/span/span')
                rem_time_raw = time_remaining_raw.get_attribute('innerHTML')

                for rep_chr in ["Days", "Day"]:
                    rem_time_raw = rem_time_raw.replace(rep_chr, "")
                rem_time_data = rem_time_raw.split("  ")

                days_ = rem_time_data[0 ].replace("\n", "")
                days_in_minutes_left = int(days_) * 1440

                time_split = rem_time_data[1].split(":")
                total_minutes_left = days_in_minutes_left + (int(time_split[0]) * 60) + int(time_split[1])

            except ValueError:
                total_minutes_left = "N/A"



            # Find Bidding End & Start Date | Use Selenium Select By Xpath
            try:
                months = {"December": 12, "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11}

                start_date_raw = cdriver_object.find_element_by_xpath('/html/body/main/div/div[2]/div/div[4]/div[4]/table/tbody/tr[7]/td[2]')
                start_date_str = start_date_raw.get_attribute('innerHTML')
                start_date_str_split = start_date_str.split(" ")
                date_ = start_date_str_split[2].replace(" ", "")
                date_ = start_date_str_split[2].replace(",", "")
                start_date = "{}/{}/{}".format(months[start_date_str_split[1]], date_, start_date_str_split[3])

                end_date_raw = cdriver_object.find_element_by_xpath('/html/body/main/div/div[2]/div/div[4]/div[4]/table/tbody/tr[4]/td[2]/span[1]')
                end_date_raw_str = end_date_raw.get_attribute('innerHTML')
                end_date_raw_str_split = end_date_raw_str.split(" ")
                date_ = end_date_raw_str_split[2].replace(" ", "")
                date_ = end_date_raw_str_split[2].replace(",", "")
                end_date = "{}/{}/{}".format(months[end_date_raw_str_split[1]], date_, end_date_raw_str_split[3])

            except ValueError:
                start_date = "00/00/00"
                end_date = "00/00/00"


            # Find Number Of Bids | Use Selenium Select By Xpath
            try:
                # Find Total Number Of Bids
                num_bids_raw = cdriver_object.find_element_by_xpath('/html/body/main/div/div[2]/div/div[4]/div[4]/table/tbody/tr[5]')
                num_bids_str = num_bids_raw.get_attribute('innerHTML')
                num_bids_re = r'="([0-9]{1,3})">'
                num_bids_list = re.findall(num_bids_re, num_bids_str)

                try:
                    num_bids = int(num_bids_list[0])

                except IndexError:
                    num_bids = 0

            except ValueError:
                num_bids = 0


            # Find Highest Bidder | Use Selenium Select By Xpath
            try:
                # Find Highest Bidder Info
                high_bidder_raw = cdriver_object.find_element_by_xpath('/html/body/main/div/div[2]/div/div[4]/div[4]/table/tbody/tr[6]/td[2]/span')
                highest_bidder = high_bidder_raw.get_attribute('innerHTML')

            except ValueError:
                highest_bidder = "N/A"


            return [item_name, item_TPA_ID, cur_price, min_upbid, upbid_increase, total_minutes_left, start_date, end_date, num_bids, highest_bidder]
