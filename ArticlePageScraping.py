import os
import random
import re
from urllib.parse import urlparse
import uuid
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException
import time

def getSummaryandLink(url):
    # Setup WebDriver
    time.sleep(random.randint(1, 5))

    driver = webdriver.Chrome()  # Ensure ChromeDriver is correctly installed and in PATH
    driver.get(url)

    try:
        # Wait for the page to load and locate the download link by using one of its classes
        download_link = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.download-link[title*="Download high-res image"]'))
        )

        # Extract and print the entire HTML of the download link element
        link_html = download_link.get_attribute('outerHTML')
        
        link_match = re.search(r'<a\s+[^>]*href="([^"]+)"[^>]*>', link_html)
        if link_match:
           return link_match.group(1)
        else:
            return link_html

    except StaleElementReferenceException:
        # Handle StaleElementReferenceException by retrying to locate the element
        return getSummaryandLink(url)
    
    except WebDriverException as e:
        print(f"Error processing link {url}: {e}")
        return None
    
    except TimeoutException:
        print(f"Timeout while processing link {url}")
        return None
    
    finally:    
        # Clean up
        driver.quit()
