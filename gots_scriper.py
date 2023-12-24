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
chrome_options.binary_location = path

# Specify the path to the ChromeDriver executable using the executable_path in ChromeOptions
chrome_options.binary_location = path_to_brave

# Create the WebDriver
driver = webdriver.Chrome(options=chrome_options)
# driver.implicitly_wait(3)
print("Opening the page...")

driver.get(url)

print("Page opened successfully.")

try:
    # Wait for the element to be clickable  
    wait = WebDriverWait(driver, 10)

    search_result = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="xFormForm-0-submit"]')))
    search_result.click()
    print("it clicked succesfully")
    time.sleep(2)

    

except Exception as e:
    print(f"An error occurred in clicking: {e}")

# data = []
company = []
Country	= []
product_category = []
brand_name = []
contact_name = []
email_address = []
address = []
license_number = []
pdf = []
certification_body = []
expiry_date = []
product_details = []


try:

# ---------------------------50 rows -------------------------- START
    try:

        show50link = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[@class="xforms-limiter-limit" and @limit="50"]'))
        )

        # Click on the "50" link
        show50link.click()
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
            show50link.click()
            print("Show 50 clicked successfully after navigating back")

            # Wait for the page to load after clicking "50"
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//table[@class="ui-table search-result-list"]//tr'))
            )

        except Exception as e:
            print(f"Error clicking '50' after navigating back: {e}")

# ---------------------------50 rows -------------------------- END

    rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//table[@class="ui-table search-result-list"]//tr')))

    for row in rows:
        try:

            get_column(row, './/td[@class="col-1"]', company)
            get_column(row, './/td[@class="col-2"]', Country)
            get_column(row, './/td[@class="col-3"]', product_category)
            get_column(row, './/td[@class="col-4"]', brand_name)
 
        except Exception as row_error:
            # print(f"Error processing row: {row_error}")
            print(f"Error processing row")
            # company.append(None)


        try:
            details_link = WebDriverWait(row, 10).until(
                EC.element_to_be_clickable((By.XPATH, './/td[@class="col-5"]//a[@title="details"]'))
            )
            details_link.click()

            # Wait for the details to load (adjust the wait time as needed)
            time.sleep(2)
            contact_data = driver.find_element(By.ID,  'xFormTable-1')
            license_data = driver.find_element(By.ID,  'xFormTable-2')
            other_data = driver.find_element(By.ID,  'xFormTable-3')

            # contact name
            get_details(contact_data, contact_name, 'xFormTd-4')
           
            # email address
            get_details(contact_data, email_address, 'xFormTd-7')

            # address
            get_details(contact_data, address, 'xFormTd-8')

            # license number
            get_details(license_data, license_number, 'xFormTd-15')

            # certification_body
            get_details(other_data, certification_body, 'xFormTd-18')

            # license number
            get_details(other_data, expiry_date, 'xFormTd-20')

            # license number
            get_details(other_data, product_details, 'xFormTd-17')
            

            # Go back to the main page
            driver.back()

            # Refresh the rows to avoid stale element reference
            rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//table[@class="ui-table search-result-list"]//tr')))

            
        except Exception as details_error:
            print(f"An error occurred while processing details: {details_error}") 





except Exception as e:
    print(f"An error occurred in scraping rows: {e}")

# print("company: ",company)


df = pd.DataFrame({
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
    'product_details': product_details})

df.to_csv('gots_test_fun.csv', index= False)



# def row_element(row, text_html):
#     element = row.find_element(By.XPATH, text_html).text.encode('utf-8', errors='ignore').decode('utf-8')
#     return element




# df = pd.DataFrame({
#     'company': company, 
#     'country': Country, 
#     'product_category': product_category,
#     'brand_name': brand_name,
#     'contact_name': contact_name, 
#     'email_address': email_address, 
#     'address': address,
#     'license_number': license_number,
#     'certification_body': certification_body,
#     'expiry_date': expiry_date,
#     'product_details': product_details})

#---------------------------------other rows------------------------- Start
            # company_element = row.find_element(By.XPATH, './/td[@class="col-1"]').text.encode('utf-8', errors='ignore').decode('utf-8')
            # country_element = row.find_element(By.XPATH, './/td[@class="col-2"]').text.encode('utf-8', errors='ignore').decode('utf-8')
            # category_element = row.find_element(By.XPATH, './/td[@class="col-3"]').text.encode('utf-8', errors='ignore').decode('utf-8')
            # brand_element = row.find_element(By.XPATH, './/td[@class="col-4"]').text.encode('utf-8', errors='ignore').decode('utf-8')
            # Country.append(country_element)
            # product_category.append(category_element)
            # brand_name.append(brand_element)
#---------------------------------other rows------------------------- END


