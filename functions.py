from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException



def get_column(row, html_text, column):
    element = row.find_element(By.XPATH, html_text).text.encode('utf-8', errors='ignore').decode('utf-8')
    column.append(element)

# def click_on(html_text, wait, seconds):
#     button = wait.until(EC.element_to_be_clickable((By.XPATH, html_text)))
#     button.click()
#     # print("it clicked succesfully")
#     time.sleep(seconds)


def get_details(table, column, html_text):
    try: 
        element = table.find_element(By.ID, html_text).text.strip()
        column.append(element)

    except NoSuchElementException:
        print(f"Element with ID '{html_text}' not found.")
        column.append(None)