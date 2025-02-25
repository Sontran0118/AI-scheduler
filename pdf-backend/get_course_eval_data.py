from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_chart_data():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # You can remove this if you want to see the browser
    driver_path = r'C:\Users\AD\Desktop\chromedriver.exe'

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the website
    driver.get("https://classie-evals.stonybrook.edu/Section/details/CSE/101/L10/LAB/1248/97581")

    try:
        # Wait for the element to appear
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="page"]/script[4]'))
        )

        # Print the full page source to debug
        print(driver.page_source)  # Check if the page has been fully loaded with the content you're looking for
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':
    scrape_chart_data()
