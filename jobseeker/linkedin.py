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
options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
import os


class EasyApplyLinkedin:

    def __init__(self, data):
        """Parameter initialization"""
         
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver = driver


    def login_linkedin(self):
       """This function logs into your personal LinkedIn profile"""

       # go to the LinkedIn login url
       self.driver.get("https://www.linkedin.com/login")

        # introduce email and password and hit enter
       login_email = self.driver.find_element(By.NAME, 'session_key')
       login_email.clear()
       login_email.send_keys(self.email)
       login_pass = self.driver.find_element(By.NAME, 'session_password')
       login_pass.clear()
       login_pass.send_keys(self.password)
       login_pass.send_keys(Keys.RETURN)

    
    def job_page(self):
        """This function goes to the 'Jobs' section and looks for all the jobs that match the keywords and location"""
        # go to Jobs
        jobs_link = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span[title="Jobs"]'))
        )
        jobs_link.click()
    
    def job_search(self):
        # search based on keywords and location and hit enter
        search_keywords = self.driver.find_element(By.CLASS_NAME, 'jobs-search-box__text-input')
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        search_location = self.driver.find_element(By.CLASS_NAME, 'jobs-search-box__text-input')
        search_location.clear()
        search_location.send_keys(self.location)
        search_location.send_keys(Keys.RETURN)
   

    def filter(self):
        """This function filters all the job results by 'Easy Apply'"""
        #self.driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3802046228&f_AL=true&geoId=100710459&keywords=python%20developer&location=Kenya&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R")

        # select all filters, click on Easy Apply and apply the filter
        easy_filters_button = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Easy Apply filter."]'))
        )
        easy_filters_button.click()
       # class="artdeco-toggle artdeco-toggle--32dp artdeco-toggle--default ember-view"

#        easy_apply_button = WebDriverWait(self.driver, 70).until(
#        EC.presence_of_element_located((By.CLASS_NAME, 'artdeco-toggle--32dp'))
#        )
#        easy_apply_button.click()
#
#        apply_filter_button = WebDriverWait(self.driver, 70).until(
#        EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Apply current filters to show results"]'))
#       )
#        apply_filter_button.click()


    def find_offers(self):
        """This function finds all the offers through all the pages result of the search and filter"""



    def scrape_offers(self):
        # Find all elements with the specified class name
        elements = WebDriverWait(self.driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card-container"))
        )
        jobresults = []
        # Iterate over each element
        for element in elements:
            # Extract data from each element
            title = element.find_element(By.CLASS_NAME, "job-card-list__title").text
            company = element.find_element(By.CLASS_NAME, "job-card-container__primary-description").text
            location = element.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text
    
            # Print the extracted data
            print("Title:", title)
            print("Company:", company)
            print("Location:", location)
            print("-" * 50)

            jobresult = {title, company, location}
            jobresults.append(jobresult)
            return jobresults



    # pagination = WebDriverWait(driver, 70).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "artdeco-pagination__pages--number"))
    # )
    # buttons = pagination.find_elements(By.TAG_NAME, "button")
    # for button in buttons:
    #     driver.execute_script("arguments[0].scrollIntoView(true);", button)
    #     button.click()
            


    def appply_to_job(self):
        time.sleep(10)
        job_apply_button = WebDriverWait(self.driver, 70).until(
    
        EC.presence_of_element_located((By.CLASS_NAME, 'jobs-apply-button'))
        )
        job_apply_button.click()

        phone_number_field = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id$="phoneNumber-nationalNumber"]'))
        )
        phone_number_field.clear()  # Clear any existing content in the field
        phone_number_field.send_keys("1234567890")

        next_button = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Continue to next step"]'))
        )
        next_button.click()
        
        resume_filename = 'resume.docx'
        resume_path = os.path.abspath(resume_filename)

        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id^="jobs-document-upload-file-input-upload-resume-"]'))
        )
# Send the file path to the file input element
        file_input.send_keys(resume_path)

        review_button = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Review your application"]'))
        )
        review_button.click()

        submit_button = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Submit applicationn"]'))
        )
        submit_button.click()

        # find the total amount of results (if the results are above 24-more than one page-, we will scroll trhough all available pages)
        total_results = self.driver.find_element(By.CLASS_NAME, "display-flex.t-12.t-black--light.t-normal")
        total_results_int = int(total_results.text.split(' ',1)[0].replace(",",""))
        print("total results: ", total_results_int)

        time.sleep(2)
        # get results for the first page
        current_page = self.driver.current_url
        results = self.driver.find_elements(By.CLASS_NAME, "occludable-update.artdeco-list__item--offset-4.artdeco-list__item.p0.ember-view")

        # for each job add, submits application if no questions asked
        for result in results:
            hover = ActionChains(self.driver).move_to_element(result)
            hover.perform()
            titles = result.find_elements(By.CLASS_NAME, 'job-card-search__title.artdeco-entity-lockup__title.ember-view')
            for title in titles:
                self.submit_apply(title)

        # if there is more than one page, find the pages and apply to the results of each page
        if total_results_int > 24:
            time.sleep(2)

            # find the last page and construct url of each page based on the total amount of pages
            find_pages = self.driver.find_elements(By.CLASS_NAME, "artdeco-pagination__indicator.artdeco-pagination__indicator--number")

# Check if find_pages is not empty before accessing its elements
        if find_pages:
            total_pages = find_pages[len(find_pages) - 1].text
            total_pages_int = int(re.sub(r"[^\d.]", "", total_pages))
            
            # Rest of your code here...
            
            get_last_page = self.driver.find_element(By.XPATH, "//button[@aria-label='Page " + str(total_pages_int) + "']")
            get_last_page.send_keys(Keys.RETURN)
            time.sleep(2)
            last_page = self.driver.current_url

            try:
                total_jobs = int(last_page.split('start=', 1)[1])
            except IndexError:
                # Handle the case where 'start=' is not found
                total_jobs = 0  # or any other default value you want

            # Rest of your code...
        else:
            print("No pagination elements found.")


            # go through all available pages and job offers and apply
            for page_number in range(25,total_jobs+25,25):
                self.driver.get(current_page+'&start='+str(page_number))
                time.sleep(2)
                results_ext = self.driver.find_elements(By.CLASS_NAME, "occludable-update.artdeco-list__item--offset-4.artdeco-list__item.p0.ember-view")
                for result_ext in results_ext:
                    hover_ext = ActionChains(self.driver).move_to_element(result_ext)
                    hover_ext.perform()
                    titles_ext = result_ext.find_elements(By.CLASS_NAME, 'job-card-search__title.artdeco-entity-lockup__title.ember-view')
                    for title_ext in titles_ext:
                        self.submit_apply(title_ext)
            else:
                self.close_session()

    def submit_apply(self,job_add):
        """This function submits the application for the job add found"""

        print('You are applying to the position of: ', job_add.text)
        job_add.click()
        time.sleep(2)
        
        # click on the easy apply button, skip if already applied to the position
        try:
            in_apply = self.driver.find_element(By.XPATH, "//button[@data-control-name='jobdetails_topcard_inapply']")
            in_apply.click()
        except NoSuchElementException:
            print('You already applied to this job, go to next...')
            pass
        time.sleep(1)

        # try to submit if submit application is available...
        try:
            submit = self.driver.find_element(By.XPATH, "//button[@data-control-name='submit_unify']")
            submit.send_keys(Keys.RETURN)
        
        # ... if not available, discard application and go to next
        except NoSuchElementException:
            print('Not direct application, going to next...')
            try:
                discard = self.driver.find_element(By.XPATH, "//button[@data-test-modal-close-btn]")
                discard.send_keys(Keys.RETURN)
                time.sleep(1)
                discard_confirm = self.driver.find_element(By.XPATH, "//button[@data-test-dialog-primary-btn]")
                discard_confirm.send_keys(Keys.RETURN)
                time.sleep(1)
            except NoSuchElementException:
                pass

        time.sleep(1)

    def close_session(self):
        """This function closes the actual session"""
        
        print('End of the session, see you later!')
        self.driver.close()

    def apply(self):
        """Apply to job offers"""

        self.driver.maximize_window()
        self.login_linkedin()
        time.sleep(5)
        self.job_page()
        time.sleep(5)
        self.job_search()
        time.sleep(5)
        self.filter()
        time.sleep(2)


# data = {
#     'email': "ekoech.mboya@gmail.com",
#     'password': 'enock2005',
#     'keywords': ['python ', 'django ', 'automation'],
#     'location': 'Kenya'
#     }


#             # Initialize your automation script with user data
# bot = EasyApplyLinkedin(data)
# bot.apply()

