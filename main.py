from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

EMAIL = "YOUR_LINKEDIN_EMAIL_HERE"
PWD = "YOUR_LINKEDIN_PWD_HERE"
LINKEDIN_JOB_URL = "YOUR_SAVED_JOB_SEARCH_URL_HERE"

chrome_driver_path = "C:\Development\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get(LINKEDIN_JOB_URL)
driver.find_element_by_link_text("Sign in").click()

time.sleep(5)

email = driver.find_element_by_id("username")
pwd = driver.find_element_by_id("password")
email.send_keys(EMAIL)
pwd.send_keys(PWD)
pwd.send_keys(Keys.ENTER)

job_listings = driver.find_elements_by_css_selector(".job-card-container")
print(job_listings)

for job_listing in job_listings:
    print("called")
    job_listing.click()
    time.sleep(2)

    try:
        apply_button = driver.find_element_by_css_selector(".jobs-s-apply button")
        apply_button.click()
        time.sleep(5)
        submit_button = driver.find_element_by_css_selector("footer button")

        # If the submit_button is a "Next" button, then this is a multi-step application, so skip.
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            close_button = driver.find_element_by_class_name("artdeco-modal__dismiss").click()
            time.sleep(3)
            discard_button = driver.find_elements_by_class_name("artdeco-modal__confirm-dialog-btn")[1]
            discard_button.click()
            print("Complex application, skipped.")
            continue
        else:
            submit_button = driver.find_element_by_css_selector("footer button")
            submit_button.click()

            # Once application completed, close the pop-up window.
        time.sleep(2)
        close_button = driver.find_element_by_class_name("artdeco-modal__dismiss")
        close_button.click()

    # If already applied to job or job is no longer accepting applications, then skip.
    except NoSuchElementException:
        print("No application button, skipped.")
        continue

    time.sleep(5)
    driver.quit()

driver.close()
