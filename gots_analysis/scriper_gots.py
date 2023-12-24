from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import pandas as pd
from functions import *

url = 'https://global-standard.org/find-suppliers-shops-and-inputs/certified-suppliers/database/search'
path = '/Users/chaim/Downloads/chromedriver/chromedriver.exe'
path_to_brave = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'

# Set up the Chrome options
chrome_options = webdriver.ChromeOptions()

# Specify the path to the ChromeDriver executable using the executable_path in ChromeOptions
chrome_options.binary_location = path_to_brave

# Create the WebDriver
driver = webdriver.Chrome(options=chrome_options)
print("Opening the page...")
# Open the initial page
driver.get(url)
print("Page opened successfully.")

# Perform your initial actions (e.g., clicking, waiting, etc.)
try:
    # Wait for the element to be clickable  
    
    wait = WebDriverWait(driver, 10)

    # Wait for overlay to disappear
    # wait.until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="row-fluid"]')))

    # search_result = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="xFormForm-0-submit"]')))
    # search_result.click()
    # print("it clicked succesfully")
    # time.sleep(2)
    search_result = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@id="xFormForm-0-submit"]')))
    driver.execute_script("arguments[0].click();", search_result)
    print("it clicked succesfully")
    time.sleep(2)

except Exception as e:
    print(f"An error occurred in clicking: {e}")

# def scrape_details(row):
        
#                 details_link = WebDriverWait(row, 10).until(
#                     EC.presence_of_element_located((By.XPATH, './/td[@class="col-5"]//a[@title="details"]'))
#                 )
#                 driver.execute_script("arguments[0].click();", details_link)
#                 # details_link.click()
#                 print("clicked on details successfully")

#                 # Wait for the details to load 
#                 time.sleep(2)
#                 contact_data = driver.find_element(By.ID, 'xFormTable-1')
#                 license_data = driver.find_element(By.ID, 'xFormTable-2')
#                 other_data = driver.find_element(By.ID, 'xFormTable-3')

#                 get_details(contact_data, contact_name, 'xFormTd-4')
#                 get_details(contact_data, email_address, 'xFormTd-7')
#                 get_details(contact_data, address, 'xFormTd-8')
#                 get_details(license_data, license_number, 'xFormTd-15')
#                 get_details(other_data, certification_body, 'xFormTd-18')
#                 get_details(other_data, expiry_date, 'xFormTd-20')
#                 get_details(other_data, product_details, 'xFormTd-17')

#                 # Go back to the main page
#                 driver.back()

#                 # Refresh the rows to avoid stale element reference
#                 rows = WebDriverWait(driver, 10).until(
#                     EC.presence_of_all_elements_located((By.XPATH, '//table[@class="ui-table search-result-list"]//tr'))
#                 )
#                 time.sleep(1)



def scrape_page():

    print(f"Scraping page...")

    company = []
    Country = []
    product_category = []
    brand_name = []
    contact_name = []
    email_address = []
    address = []
    license_number = []
    certification_body = []
    expiry_date = []
    product_details = []
    pdf =[]

    try:
        
        current_row = 1
        
        rows = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//table[@class="ui-table search-result-list"]//tr'))
        )

        
        for row in rows:
            try:
                print(f"------------------------------------ROW {current_row} -------------------------------")

                get_column(row, './/td[@class="col-1"]', company)
                get_column(row, './/td[@class="col-2"]', Country)
                get_column(row, './/td[@class="col-3"]', product_category)
                get_column(row, './/td[@class="col-4"]', brand_name)
            except Exception as row_error:
                print(f"Error processing row")

            try:
                details_link = WebDriverWait(row, 10).until(
                    EC.presence_of_element_located((By.XPATH, './/td[@class="col-5"]//a[@title="details"]'))
                )
                driver.execute_script("arguments[0].click();", details_link)
                # details_link.click()
                print("clicked on details successfully")

                # Wait for the details to load 
                time.sleep(2)
                contact_data = driver.find_element(By.ID, 'xFormTable-1')
                license_data = driver.find_element(By.ID, 'xFormTable-2')
                other_data = driver.find_element(By.ID, 'xFormTable-3')

                get_details(contact_data, contact_name, 'xFormTd-4')
                get_details(contact_data, email_address, 'xFormTd-7')
                get_details(contact_data, address, 'xFormTd-8')
                get_details(license_data, license_number, 'xFormTd-15')
                get_details(other_data, certification_body, 'xFormTd-18')
                get_details(other_data, expiry_date, 'xFormTd-20')
                get_details(other_data, product_details, 'xFormTd-17')

                
                try: 
                    pdf_element = table.find_element(By.XPATH, './/td[@class="col-2"]//a[contains(@title, "view the scope certificate")]').get_attribute("href")
                    pfd.append(pdf_element)

                except NoSuchElementException:
                    print(f"Pdf link with not found.")
                    pdf.append(None)
                # Go back to the main page
                driver.back()

                # Refresh the rows to avoid stale element reference
                rows = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//table[@class="ui-table search-result-list"]//tr'))
                )

                # scrape_details(row)

            except Exception as details_error:
                print(f"An error occurred while processing details: {details_error}")


                # Retry details processing
                for i in range(3):  # Retry up to 3 times
                    try:
                        # scrape_details(row)
                        # Code for processing details
                        details_link = WebDriverWait(row, 10).until(
                            EC.presence_of_element_located((By.XPATH, './/td[@class="col-5"]//a[@title="details"]'))
                        )
                        driver.execute_script("arguments[0].click();", details_link)
                        # details_link.click()
                        print("clicked on details successfully")

                        # Wait for the details to load (adjust the wait time as needed)
                        time.sleep(2)
                        contact_data = driver.find_element(By.ID, 'xFormTable-1')
                        license_data = driver.find_element(By.ID, 'xFormTable-2')
                        other_data = driver.find_element(By.ID, 'xFormTable-3')

                        get_details(contact_data, contact_name, 'xFormTd-4')
                        get_details(contact_data, email_address, 'xFormTd-7')
                        get_details(contact_data, address, 'xFormTd-8')
                        get_details(license_data, license_number, 'xFormTd-15')
                        get_details(other_data, certification_body, 'xFormTd-18')
                        get_details(other_data, expiry_date, 'xFormTd-20')
                        get_details(other_data, product_details, 'xFormTd-17')

                        # Go back to the main page
                        driver.back()

                        # Refresh the rows to avoid stale element reference
                        rows = WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.XPATH, '//table[@class="ui-table search-result-list"]//tr'))
                        )
                        break  # Break out of the loop if successful
                    except Exception as retry_error:
                        print(f"Retry failed. Retrying details {i} processing: {retry_error}")
                        time.sleep(2)  
            
            current_row += 1

    except Exception as e:
        print(f"An error occurred in scraping rows: {e}")

    print("Scraping complete.")

    return pd.DataFrame({
        'company': company,
        'country': Country,
        'product_category': product_category,
        'brand_name': brand_name,
        'contact_name': contact_name,
        'email_address': email_address,
        'address': address,
        'license_number': license_number,
        'certification_body': certification_body,
        'expiry_date': expiry_date,
        'product_details': product_details
    })



try:

        show50link = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[@class="xforms-limiter-limit" and @limit="50"]'))
        )

        # Click on the "50" link
        driver.execute_script("arguments[0].click();", show50link)
        # show50link.click()
        print("Show 50 clicked successfully")
        time.sleep(10)
except Exception as e:
        print(f"An error occurred in 50 clicking: {e}")

  
        try:
            # Re-find the "50" link after navigating back
            show50link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@class="xforms-limiter-limit" and @limit="50"]'))
            )

            # Click on the "50" link again
            driver.execute_script("arguments[0].click();", show50link)
            # show50link.click()
            print("Show 50 clicked successfully after navigating back")

            # Wait for the page to load after clicking "50"
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//table[@class="ui-table search-result-list"]//tr'))
            )

        except Exception as e:
            print(f"Error clicking '50' after navigating back: {e}")

# Call the scrape_page function to scrape the first page
df = scrape_page()

# Set a counter for the number of pages to scrape
pages_to_scrape =  19
# current_page = 2




for i in range(pages_to_scrape):
    try:
        next_page_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[@class="xforms-pager-next"]'))
        )
        driver.execute_script("arguments[0].click();", next_page_link)
        # next_page_link.click()
        print(f"############################################################# Scraping page {i+2}...")
        
        # Reinitialize rows after navigating to the next page
        rows = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//table[@class="ui-table search-result-list"]//tr'))
        )
        time.sleep(3)

        next_page = scrape_page()

        df = pd.concat([df, next_page], ignore_index=True)
        # current_page += 1
    except StaleElementReferenceException:
        print("Stale Element Reference Exception. Retrying...")
    except Exception as e:
        print(f"An error occurred while navigating to the next page: {e}")
        break  # Break out of the loop if there is an error or no next page link is found


df.to_csv('gots_data_1000.csv', index=False)