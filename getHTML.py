import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

def buildURL(base, params):
    return base + "?" + "&".join([f"{key}={val}" for key, val in params.items()])    

REJECT_COOKIES_ID = "onetrust-reject-all-handler"
MORE_RESULTS_SELECTOR = ".button__button___fo2tk.forms__field___E4Q71.forms__formControlBase___3Cl7I.button__fluid___2ez5a.button__secondary___1xuZs.button__branded___3hDeX"

def getHTML(base, payload, max_expands=100):
    # Init driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.get(buildURL(base, payload))
    
    # Reject Cookies
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((
            By.ID, REJECT_COOKIES_ID
        )))
        reject = driver.find_element(By.ID, REJECT_COOKIES_ID)
        reject.click()
        time.sleep(1)
    except (NoSuchElementException, TimeoutException):
        print("No cookie popup!")

    # Get More Results until none left or max_expands reached
    more = driver.find_element(By.CSS_SELECTOR, MORE_RESULTS_SELECTOR)
    i = 0
    while i < max_expands:
        try:
            more.click()
            time.sleep(0.1)
            i += 1
        except StaleElementReferenceException:
            print("Last entry reached!")
            break
    if i == max_expands:
        print("Max Expands reached!")
    else:
        print(i)

    # Dump and cleanup
    html = driver.page_source
    driver.close()
    return html
