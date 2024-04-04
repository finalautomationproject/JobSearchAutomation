from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from undetected_chromedriver import Chrome, ChromeOptions
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

options = ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Specify the version of Chrome you want to use
chrome_version = "122.0.6261.131"

driver = Chrome(chrome_version=chrome_version, options=options)

class DiceApp:

    def __init__(self, data):
        """Parameter initialization"""
        
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver = driver

    def login(self):
        self.driver.get("https://www.dice.com/dashboard/login")
        # Find the email field and enter the email address
        email_field = driver.find_element(By.ID, "email")
        email_field.clear()  # Clear any existing value in the field
        email_field.send_keys(self.email)

        # Find the password field and enter the password
        password_field = driver.find_element(By.ID, "password")
        password_field.clear()  # Clear any existing value in the field
        password_field.send_keys(self.password)

        # Submit the form
        password_field.send_keys(Keys.RETURN)
        time.sleep(3)
        try:
            close_sms = driver.find_element(By.ID, "sms-remind-me")
            close_sms.click()
        except:
            print("no sms found")

    def upload_resume(self):
        dropdown_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dropdown-menu"))
        )

        # Find the profile link and click it
        profile_link = dropdown_menu.find_element(By.XPATH, "//a[contains(@href, '/dashboard/profiles')]")
        profile_link.click()

        try:
            time.sleep(10)
            not_now = driver.find_element(By.ID, "not-now-link")
            not_now.click()
        except:
            print("Not know button passed")
        resume_filename = 'resume.docx'
        resume_path = os.path.abspath(resume_filename)

        try:
            # Locate the dhi-candidates-card element
            card = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sc-dhi-candidates-candidate-profile-resume')))

            # Locate the input element within the card
            input_element = card.find_element(By.CSS_SELECTOR, 'input[type="file"]')

            # Upload the file by sending the file path to the input element
            input_element.send_keys(resume_path)
            
            print("Resume uploaded successfully!")

        except Exception as e:
            print(f"Failed to upload resume: {e}")
        try:
            # Find the dialog box
            dialog = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dhi-candidates-card_0Y_W6rXMDi"]')))
        except Exception as e:
            print("Failed to locate the dialog box:", e)

        
        try:
            # Find the upload input element
            upload_input = dialog.find_element(By.CSS_SELECTOR, 'input[type="file"]')

            # Upload the file
            upload_input.send_keys(resume_path)
        except Exception as e:
            print("Failed to upload the file:", e)
        resume_upload = driver.find_element(By.CLASS_NAME, 'sc-dhi-candidates-file-upload-button')
        resume_upload.send_keys(resume_path)


    def job_search(self):
        self.driver.get("https://www.dice.com/")
        # search based on keywords and location and hit enter
        search_keywords = self.driver.find_element(By.XPATH,'//*[@id="typeaheadInput"]')
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        search_location = self.driver.find_element(By.XPATH,  '//*[@id="google-location-search"]')
        search_location.clear()
        search_location.send_keys(self.location)
        time.sleep(5)
        search_button = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.ID, "submitSearch-button"))
        )
        search_button.click()
        
    def extract_jobs(self):
        # Find all search cards
        time.sleep(5)
        search_cards = driver.find_elements(By.CSS_SELECTOR, "dhi-search-card")
        diceJobInfo = []
        # Iterate over each search card and extract the desired information
        for search_card in search_cards:
            # Extracting job title
            
            try:
                title_element = search_card.find_element(By.CSS_SELECTOR, "a.card-title-link")
                title = title_element.text
            except:
                title = "Not stated"
            
            # Extracting company name
            try:
                company_element = search_card.find_element(By.CSS_SELECTOR, "a.search-result-company-name")
                company = company_element.text
            except:
                company = "Not stated"

            
            # Extracting job location
            try:
                location_element = search_card.find_element(By.CSS_SELECTOR, "span.search-result-location")
                location = location_element.text
            except:
                location = "Not stated"

            
            # Extracting job description
            try:
                description_element = search_card.find_element(By.CSS_SELECTOR, "div.card-description")
                description = description_element.text
            except:
                description = "Not stated"

            
            # Extracting employment type
            try:
                employment_type_element = search_card.find_element(By.CSS_SELECTOR, "span[data-cy='search-result-employment-type']")
                employment_type = employment_type_element.text
            except:
                employment_type = "Not stated"

            
            # Extracting posted date
            try:
                posted_date_element = search_card.find_element(By.CSS_SELECTOR, "span.posted-date")
                posted_date = posted_date_element.text
            except:
                posted_date = "Not stated"

            try:
                title_element = search_card.find_element(By.CSS_SELECTOR, "a.card-title-link")

                link_id = title_element.get_attribute("id")
                # Generate the URL using the extracted ID
                application_url = f"https://www.dice.com/job-details/{link_id}"

            except:
                application_url = "Not stated"
            diceJob = {
                'title': title,
                'company': company,
                'location': location,
                'description': description,
                'employment_type': employment_type,
                'posted_date': posted_date,
                'application_url': application_url
            }
            diceJobInfo.append(diceJob)
            
            # Printing or storing the extracted information
            print("Title:", title)
            print("Company:", company)
            print("Location:", location)
            print("Description:", description)
            print("Employment Type:", employment_type)
            print("Posted Date:", posted_date)
            print("\n")

        return diceJobInfo  
        
    def quit(self):
        self.driver.quit()

        
data = {
     'email': "ekoech.mboya@gmail.com",
     'password': 'enock2005',
     'keywords': ['python '],
     'location': 'Remote'
     }
bot = DiceApp(data)
bot.job_search()
bot.extract_jobs()
# bot.login()
# bot.job_search()
# bot.extract_jobs()
