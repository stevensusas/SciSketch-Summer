import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


def GetArticleLinks():
    # Specify your download directory here
    download_dir = "/Users/stevensu/Desktop/SciSketch-Dataset/Training Data/Review Articles"

    # Set Chrome options to specify the download directory
    chrome_options = Options()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Setup Chrome WebDriver with custom options
    driver = webdriver.Chrome(options = chrome_options)
    try:
        for j in range(2024, 2025):
            for i in range(0, 5900, 100):
                url = "https://www.sciencedirect.com/search?pub=Cell&articleTypes=FLA&show=100&years="+str(j)+"&offset="+str(i)
                try:
                    # Navigate to the specified UR
                    driver.get(url)
                    if i == 0 and j == 2024:
                        time.sleep(3)
                    # Wait and click the checkbox to select all results
                    checkbox = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".SelectAllCheckbox.result-header-check-all-download"))
                    )
                    checkbox.click()

                    # Wait for the Export button to be clickable and click it
                    export_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-aa-button='srp-export-multi-expand']"))
                    )
                    export_button.click()

                    # Wait for the "Export citation to text" button in the modal and click it
                    export_to_text_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-aa-button='srp-export-multi-text']"))
                    )
                    export_to_text_button.click()
                    # Generate a random time between min_time and max_time

                    # Pause the program for the random time
                    time.sleep(random.uniform(1, 5))

                except TimeoutException as e:
                    break
                        
    finally:
        driver.quit()

GetArticleLinks()