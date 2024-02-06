from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import json
import os


options = Options()
#options.add_argument('--headless')
# options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

class ScrapeIndeed:

    def __init__(self, data):
        """Parameter initialization"""
         
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver = driver

    def search_jobs(self):
        self.driver.get("https://www.indeed.com")



        search_keywords = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="search: Job title, keywords, or company"]'))
        )
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        search_location = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Edit location"]'))
        )
        search_location.clear()
        search_location.send_keys(self.location)
        search_location.send_keys(Keys.RETURN)
        submit_button = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="jobsearch"]/div/div[2]/button'))
        )
        submit_button.click()
        time.sleep(10)

    def job_results(self):
        jobs = driver.find_elements(By.CSS_SELECTOR, ".css-zu9cdh.eu4oa1w0 li")
        availablejobs = []
        for job in jobs:
            driver.execute_script("arguments[0].scrollIntoView(true);", job)

            jobinfo = job.text.strip()
            print(jobinfo)
            availablejobs.append(jobinfo)
        
        return availablejobs   





    def sign_in(self):
        upload_resume = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="resumeTextPromo"]/a'))
        )
        upload_resume.click()


        enter_email = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ifl-InputFormField-ihl-useId-passport-webapp-1"]'))
        )
        enter_email.send_keys(self.email)

        continue_button = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="emailform"]/button'))
        )
        continue_button.click()



# data = {
#     'email': "ekoech.mboya@gmail.com",
#     'password': 'Enock2005',
#     'keywords': ['python, ', 'django, ', 'automation'],
#     'location': 'Remote'
#     }
# bot = ScrapeIndeed(data=data)
# bot.search_jobs()
# bot.job_results()