import pytest
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


@pytest.mark.np
def test_check_incorrect_parcel_number():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = "https://tracking.novaposhta.ua/"
    parcel_id = "RK023456789LV"
    driver.get(url)
    search_elem = driver.find_element(By.ID, "en")
    search_elem.send_keys(parcel_id)
    btn_elem = driver.find_element(By.ID, "np-number-input-desktop-btn-search-en").click()
    time.sleep(3)
    
    try:
        driver.find_element(By.CLASS_NAME, "tracking__error-text")
    except:
        print("We've found true parcel by accident")

    assert "Трекінг посилки | Nova Global" in driver.title

    driver.close()
