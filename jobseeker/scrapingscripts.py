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

# path = 'jobseeker\chromedriver.exe'
options = ChromeOptions()
options.add_argument('--disable-dev-shm-usage')

# Specify the version of Chrome you want to use
chrome_version = "122.0.6261.131"

driver = Chrome(chrome_version=chrome_version, options=options)

class ScrapeIndeed:

    def __init__(self, data):
        """Parameter initialization"""
         
        self.email = data['email']
        self.password = data['linkedin_password']
        self.indeedpass = data['linkedin_password']
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
        # Find job elements
        availablejobs = []
        job_elements = driver.find_elements(By.CSS_SELECTOR, '.cardOutline.tapItem')

        # Extract job information
        for job_element in job_elements:
            # Extract job details
            try:
                job = job_element.find_element(By.CSS_SELECTOR, '.jobTitle')
                job_title = job.text.strip()

            except:
                job_title = 'Not Stated'
            try:
                job = job_element.find_element(By.CSS_SELECTOR, '.jobTitle')
                application_url = 'Not Stated'
            except:
                application_url = 'Not Stated'

            try:
                company_name = job_element.find_element(By.CSS_SELECTOR, '.company_location [data-testid="company-name"]').text.strip()
            except:
                company_name= 'Not Stated'

            try:
                location = job_element.find_element(By.CSS_SELECTOR, '.company_location [data-testid="text-location"]').text.strip()
            except:
                location = "Not Stated"

            try:
                job_description = job_element.find_element(By.CSS_SELECTOR, '.css-9446fg').text.strip()  # Adjust CSS selector as needed
            except:
                job_description = 'Not Stated'


            # Inside your loop where you create jobinfo
            jobinfo = {
                'job_title': job_title,
                'company_name': company_name,
                'location': location,
                'job_description': job_description,
                'application_url': application_url
            }
            availablejobs.append(jobinfo)
            # Print or process job information
            print("Job Title:", job_title)
            print("Company:", company_name)
            print("Location:", location)
            print("Description:", job_description)
            print('Application Url:', application_url)
            print("-" * 50)
            
        
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


class ZipRecruiterApp:

    def __init__(self, data):
        """Parameter initialization"""
         
        self.email = data['email']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver = driver


    def job_search(self):
        self.driver.get("https://www.ziprecruiter.co.uk")
        # search based on keywords and location and hit enter
        search_keywords = self.driver.find_element(By.XPATH, '//*[@id="q"]')
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        search_location = self.driver.find_element(By.XPATH, '//*[@id="l"]')
        search_location.clear()
        search_location.send_keys(self.location)
        search_location.send_keys(Keys.RETURN)
        time.sleep(4)

    def extract_jobs(self):
        zipRecruiterJobs = []
        job_elements = driver.find_elements(By.CLASS_NAME, "jobList-introWrap")

        for job_element in job_elements:
            try:
                # Extract job details
                job_title = job_element.find_element(By.CLASS_NAME, "jobList-title").text
            except NoSuchElementException:
                job_title = "Not Stated"

            try:
                company = job_element.find_element(By.CSS_SELECTOR, ".jobList-introMeta li:nth-child(1)").text
            except NoSuchElementException:
                company = "Not Stated"

            try:
                location = job_element.find_element(By.CSS_SELECTOR, ".jobList-introMeta li:nth-child(2)").text
            except NoSuchElementException:
                location = "Not Stated"

            try:
                description = job_element.find_element(By.CLASS_NAME, "jobList-description").text
            except NoSuchElementException:
                description = "Not Stated"
            try:
                # Extract job details
                link_element = job_element.find_element(By.CLASS_NAME, "jobList-title")
                application_url = link_element.get_attribute('href')
            except NoSuchElementException as e:
                print(f"Error finding URL: {e}")
            zipRecruiterJob = {
                'job_title': job_title,
                'company': company,
                'location': location,
                'description': description,
                'application_url': application_url
                }
            zipRecruiterJobs.append(zipRecruiterJob)
            # Display extracted data
            print("Job Title:", job_title)
            print("Company:", company)
            print("Location:", location)
            print("Description:", description)
            return zipRecruiterJobs

# data = {
#      'email': "ekoech.mboya@gmail.com",
#      'password': 'enock2005',
#      'keywords': ['python '],
#      'location': 'Remote'
#      }
# bot = ZipRecruiterApp(data)
# bot.job_search()
# bot.extract_jobs()
 
class NaukriApp:

    def __init__(self, data):
        """Parameter initialization"""
         
        self.email = data['email']
        self.linkedin_password = data['linkedin_password']            
        self.dice_password = data['dice_password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver = driver


    def job_search(self):
        self.driver.get("https://www.naukri.com/")
        # search based on keywords and location and hit enter
        search_keywords = self.driver.find_element(By.XPATH,"//input[@placeholder='Enter skills / designations / companies']")
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        search_location = self.driver.find_element(By.XPATH,  "//input[@placeholder='Enter location']")
        search_location.clear()
        search_location.send_keys(self.location)

        search_button = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[7]/div/div[1]/div[6]'))
        )
        search_button.click()


    def extract_jobs(self):
        naukriJobInfo = []
        job_tuples = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.CLASS_NAME, "srp-jobtuple-wrapper"))
        )
        if job_tuples:
            job_tuples = driver.find_elements(By.CLASS_NAME, "srp-jobtuple-wrapper")


        # Iterate over each job tuple and extract the desired information
        for job_tuple in job_tuples:
            # Extracting job title
            try: 
                title = job_tuple.find_element(By.CLASS_NAME, "title").text
            except:
                title = "Not Stated"
            # Extracting company name
            try: 
                company = job_tuple.find_element(By.CLASS_NAME, "comp-name").text
            except:
                company = "Not Stated"            
            
            # Extracting job experience
            
            try: 
                experience = job_tuple.find_element(By.CLASS_NAME, "expwdth").get_attribute("title")
            except:
                experience = "Not Stated"            
            # Extracting job description
            
            try: 
                description = job_tuple.find_element(By.CLASS_NAME, "job-desc").text
            except:
                description = "Not Stated"            
            # Extracting job tags
            try: 
                tags = job_tuple.find_elements(By.CLASS_NAME, "tag-li")
                tags_list = [tag.text for tag in tags]
            except:
                tags_list = "Not Stated"            
            # Extracting job posting date
            posting_date = job_tuple.find_element(By.CLASS_NAME, "job-post-day").text
            try: 
                posting_date = job_tuple.find_element(By.CLASS_NAME, "job-post-day").text
            except:
                posting_date = "Not Stated"  
            try:
                # Extract job details
                link_element = job_tuple.find_element(By.CLASS_NAME, "title")
                application_url = link_element.get_attribute('href')
            except NoSuchElementException as e:
                print(f"Error finding URL: {e}")

            naukriJob = {
                'title': title,
                'company': company,
                'experience': experience,
                'description': description,
                'tags_list': tags_list,
                'posting_date': posting_date,
                'application_url': application_url
            }
            naukriJobInfo.append(naukriJob)        
            # Printing or storing the extracted information
            print("Title:", title)
            print("Company:", company)
            print("Experience:", experience)
            print("Description:", description)
            print("Tags:", tags_list)
            print("Posting Date:", posting_date)
            print("\n")
        return naukriJobInfo

class DiceApp:

    def __init__(self, data):
        """Parameter initialization"""
        
        self.email = data['email']
        self.linkedin_password = data['linkedin_password']            
        self.dice_password = data['dice_password']
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
        password_field.send_keys(self.dice_password)

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
                application_url = f"https://www.dice.com/job-detail/{link_id}"

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
            print('application_url:', application_url)
            print("\n")

        return diceJobInfo  
    
    def easyApply(self, application_url):
        self.driver.get(f"{application_url}")
        try:
            time.sleep(5)
            apply = driver.find_element(By.ID, 'applyButton')
            apply.click()
        except Exception as e:
            print(e)
        next_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/span/div/main/div[4]/button[2]')
        next_button.click()
        apply = driver.find_element(By.XPATH, '//*[@id="app"]/div/span/div/main/div[3]/button[2]')
        apply.click()
        print("Successfully applied to a job")
        
    def quit(self):
        self.driver.quit()


class EasyApplyLinkedin:

    def __init__(self, data):
        """Parameter initialization"""
         
        self.email = data['email']
        self.linkedin_password = data['linkedin_password']            
        self.dice_password = data['dice_password']
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
       login_pass.send_keys(self.linkedin_password)
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
        easy_filters_button = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Easy Apply filter."]'))
        )
        easy_filters_button.click()


    def find_offers(self):
        """This function finds all the offers through all the pages result of the search and filter"""



    def scrape_offers(self):
        scraped_offers= []
        # Find the container element
        container_element = driver.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')

        # Find all elements with the specified class name
        job_elements = container_element.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')

        # Extract job details from each job element
        for job_element in job_elements:
            try:
                # Extract job title
                job_title = job_element.find_element(By.CSS_SELECTOR, '.job-card-list__title strong').text.strip()
            except:
                job_title = "Not Stated"

            try:
                # Extract company name
                company_name = job_element.find_element(By.CSS_SELECTOR, '.job-card-container__subtitle').text.strip()
            except:
                company_name = "Not Stated"

            try:
                # Extract location
                location = job_element.find_element(By.CSS_SELECTOR, '.job-card-container__primary-description').text.strip()
            except:
                location = "Not Stated"

            try:
                # Extract background image URL
                background_image_url = job_element.find_element(By.CSS_SELECTOR, '.job-card-list__logo img').get_attribute('src')
            except:
                background_image_url = "Not Stated"
            try:
                anchor_element = job_element.find_element(By.CSS_SELECTOR, '.job-card-container__link')
                
                # Extract the URL
                url = anchor_element.get_attribute('href')
            except:
                url = "Not available"
            jobinfo = {
                'job_title': job_title,
                'company_name': company_name,
                'location': location,
                'url': url
            }
            scraped_offers.append(jobinfo)
            # Print or process job information
            print("Job Title:", job_title)
            print("Company:", company_name)
            print("Location:", location)
            print("Background Image URL:", background_image_url)
            print("Application URL:", url)
            print("-" * 50)

        return scraped_offers

    def apply_to_job(resume_path ,phone_number, self):
        time.sleep(10)
        job_apply_button = WebDriverWait(self.driver, 70).until(
    
        EC.presence_of_element_located((By.CLASS_NAME, 'jobs-apply-button'))
        )
        job_apply_button.click()

        phone_number_field = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id$="phoneNumber-nationalNumber"]'))
        )
        phone_number_field.clear()  # Clear any existing content in the field
        phone_number_field.send_keys(f"{phone_number}")

        next_button = WebDriverWait(self.driver, 70).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Continue to next step"]'))
        )
        next_button.click()
        


        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id^="jobs-document-upload-file-input-upload-resume-"]'))
        )

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




