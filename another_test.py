from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import pandas as pd

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


    rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//table[@class="ui-table search-result-list"]//tr')))

    for row in rows:
        try:

            company_element = row.find_element(By.XPATH, './/td[@class="col-1"]').text.encode('utf-8', errors='ignore').decode('utf-8')
            country_element = row.find_element(By.XPATH, './/td[@class="col-2"]').text.encode('utf-8', errors='ignore').decode('utf-8')
            category_element = row.find_element(By.XPATH, './/td[@class="col-3"]').text.encode('utf-8', errors='ignore').decode('utf-8')
            brand_element = row.find_element(By.XPATH, './/td[@class="col-4"]').text.encode('utf-8', errors='ignore').decode('utf-8')


            company.append(company_element)
            Country.append(country_element)
            product_category.append(category_element)
            brand_name.append(brand_element)

    
       

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

            try:            
                contact_name_element = contact_data.find_element(By.ID, 'xFormTd-4').text.strip()
                # print("Contact Name:", contact_name_element)
                contact_name.append(contact_name_element)

            except  Exception as contact_error:
                print(f"contact name not found")
                contact_name.append(None)
                # email_address.append(None)
                # address.append(None)

            try: 
                email_address_element = contact_data.find_element(By.ID, 'xFormTd-7').text.strip()
                email_address.append(email_address_element)

            except Exception as email_address_error:
                print(f"An error occurred while processing email address")
                email_address.append(None)
            
            try: 
                address_element = contact_data.find_element(By.ID, 'xFormTd-8').text.strip()
                address.append(address_element)

            except Exception as email_address_error:
                print(f"An error occurred while processing address")
                address.append(None)
            
            try: 
                license_number_element = license_data.find_element(By.ID, 'xFormTd-15').text.strip()
                license_number.append(license_number_element)

            except Exception as license_number_error:
                print(f"An error occurred while processing license number")
                license_number.append(None)

            try: 
                certification_body_element = other_data.find_element(By.ID, 'xFormTd-18').text.strip()
                certification_body.append(certification_body_element)

            except Exception as certification_body_error:
                print(f"An error occurred while processing certification body")
                certification_body.append(None)
            
            try: 
                expiry_date_element = other_data.find_element(By.ID, 'xFormTd-20').text.strip()
                expiry_date.append(expiry_date_element)

            except Exception as expiry_date_error:
                print(f"An error occurred while processing expiry date")
                expiry_date.append(None)

            try: 
                product_details_element = other_data.find_element(By.ID, 'xFormTd-17').text.strip()
                product_details.append(product_details_element)

            except Exception as product_details_error:
                print(f"An error occurred while processing product details")
                product_details.append(None)


            # Go back to the main page
            driver.back()

            # Refresh the rows to avoid stale element reference
            rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//table[@class="ui-table search-result-list"]//tr')))

            
        except Exception as details_error:
            print(f"An error occurred while processing details: {details_error}") 

except Exception as e:
    print(f"An error occurred in scraping rows: {e}")
# print(brand_name)
# print("contact_name: ",contact_name)
# print("email_address: ",email_address)
# print("address: ",address)

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

df.to_csv('gots_test_page1.csv', index= False)
# print(df) 
# df = pd.DataFrame({'company': company,  'contact_name': contact_name})
# df.to_csv('gots_test.csv', index= False)
# print(df) 

# def extract_element(element, text):
#     extracted_element = element.find_element(By.XPATH, text).text.encode('utf-8', errors='ignore').decode('utf-8')
#     return extracted_element
            # print("------------------------------------------------------------------")
