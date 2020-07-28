from selenium import webdriver
import time
import csv
import configparser
from config import Config
import key 
import os
import random

Config().set_driver_path()

# load ini file
#prop = configparser.ConfigParser()
#prop.read(os.environ['config_file_path'])
#application_env = prop['atg.env']['env']

#chromedriver = os.environ['chrome_driver_path']
#os.environ["webdriver.chrome.driver"] = chromedriver
prefs = {"profile.default_content_setting_values.notifications": 2}
options = webdriver.ChromeOptions()
#options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
# options.add_argument('headless')
#options.add_experimental_option("prefs", prefs)

def writeToCsv(name, phone, email, link, csvname):
    with open('%s.csv' %csvname, 'a') as csvfile:
        fieldnames = ['name', 'phone','email','link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #if not exists(name):
        writer.writerow({'name': name, 'phone': phone, 'email': email, 'link': link})


a_dict = key.grp

def search(groups,no_searches):
    group_value = random.choice(list(groups.keys()))
    loc = key.locs
    loc_value = random.choice(loc)
    
    #for key in group_value:
    group = group_value
    group = group.replace(' ','+')
    location = loc_value
    location = location.replace(' ','+')
    driver = webdriver.Chrome(executable_path='/Users/harshjasani/Downloads/chromedriver')
    driver.maximize_window()
    driver.get("https://www.google.com/maps/search/"+location+" "+group+"/")
    time.sleep(1)
    content = driver.find_elements_by_class_name("section-result-content")
    counter = no_searches + 1
    for _k in range((no_searches//20 +1)):
        for i in range(0,20):
            counter-=1
            if(counter ==0):
                break
            time.sleep(4)
            while True:
                try:
                    searches = driver.find_elements_by_class_name("section-result-content")
                    title = searches[i].find_element_by_class_name("section-result-title")
                except IndexError:
                    continue
                break

            name=(title.text)
            xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "section-info-line", " " ))]'
            searches[i].click()
            time.sleep(2)
            info_sections = driver.find_elements_by_xpath(xpath)
            eorw=[]

            phone =''
            for j in info_sections:
               try:
                    phone = int((j.text).replace(' ', ''))
               except ValueError:
                    k = j.text
                    if (
                         k.endswith('.net') or k.endswith('.biz') or k.endswith('.name') or
                         k.endswith('.com') or k.endswith('.com') or k.endswith('.pro') or 
                         k.endswith('.in') or k.endswith('.university') or k.endswith('.info') or
                         k.endswith('.gov') or k.endswith('.travel') or k.endswith('.aero') or
                         k.endswith('.org') or k.endswith('.gov') or k.endswith('.edu') or
                         k.endswith('.me')):
                         eorw.append(j.text)
                         
            #driver.execute_script(script="window.history.back(-1);")
            driver.get("https://www.google.com/maps/search/"+location+" "+group+"/")
            time.sleep(3)
            mail =''
            site = ''
            for l in eorw:
                if '@' in l:
                    mail = l
                else:
                    site = l
                    site.replace('Menu\n','')
            #writeToCsv(name,phone,mail,site,key)
            print(name,phone,mail,site)
        time.sleep(2)
        #next = driver.find_element_by_xpath('//*[@aria-label=" Next page "]')
        next = driver.find_element_by_class_name('n7lv7yjyC35__button-next-icon')
        next.click()
    driver.quit()

search(a_dict,20)
