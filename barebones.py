import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

def set_up_base(mode, w_time=30):
    file_name = '{}_{}_{}_{}_{}_{}.csv'.format(mode, time.gmtime()[0], time.gmtime()[1], time.gmtime()[2], time.gmtime()[3],
                                              time.gmtime()[4])
    driver = webdriver.Firefox()
    driver.get('https://m.huobi.io/market/chart/?s=btc_usdt')
    time.sleep(5)
    if mode == 'DAY':
        button_1 = driver.find_element_by_xpath('//span[@data-period="1day"]')
        button_1.click()
    if mode == 'HOUR':
        button_1 = driver.find_element_by_xpath('//span[@data-period="1hour"]')
        button_1.click()
    time.sleep(5)
    while True:
        source = driver.page_source
        soup = BeautifulSoup(source)
        current_time = time.ctime()
        entries = {'TIME': current_time,
                    'MA5': soup.findAll('span', {"style": "color:#F6DC93"})[0].text,
                    'MA10': soup.findAll('span', {"style": "color:#61D1C0"})[0].text,
                    'MA30': soup.findAll('span', {"style": "color:#CB92FE"})[0].text}
        write_to_csv(entries, file_name)
        time.sleep(5)
        print(entries)

def write_to_csv(entry_dict, file_name):
    with open(file_name, 'a') as f:
        fieldnames = list(entry_dict.keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(entry_dict)

set_up_base('DAY')