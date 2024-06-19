import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.mark.olx #basic technique
def test_search_main_page():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get("https://www.olx.ua")
    
    # Handle the cookie consent
    try:
        driver.find_element(By.XPATH, "//span[contains(text(),'Закрити')]").click()
    except:
        print("Cookies accepted")
    assert "Оголошення OLX.ua: сервіс оголошень України — купівля/продаж бу та нових товарів, різноманітні послуги на сайті OLX.ua" in driver.title
    
    search_item = driver.find_element(By.ID, "search")
    search_item.send_keys("RTX 2060")
    time.sleep(2)
    search_geo = driver.find_element(By.ID, "location-input")
    search_geo.send_keys("Львів")
    time.sleep(2)
    try: 
        driver.find_element(By.CLASS_NAME, "css-16tss5f").click()
        driver.find_element(By.XPATH, "//button[@data-testid='search-submit']").click()
        time.sleep(5)
    except:
        print("Location issue")
    expected_title = "RTX 2060 в Львів - OLX.ua"
    assert expected_title in driver.title

    driver.quit()
    
    
@pytest.mark.olx #advanced technique + cycles
def test_search_main_page_cycle():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    start_url = "https://www.olx.ua"    
    driver.get(start_url)
    
    # Handle the cookie consent
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Закрити')]"))
        ).click()
    except:
        print("Cookies accepted")
    
    assert "Оголошення OLX.ua: сервіс оголошень України — купівля/продаж бу та нових товарів, різноманітні послуги на сайті OLX.ua" in driver.title
    
    item = "RTX 2060"
    locations = ["Київ", "Дніпро", "Одеса", "Харків"]
    
    for city in locations:
        try:
            survey_modal = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.ID, "survey-modal"))
            )
            if survey_modal:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
                ).click()
                print("survey-modal successfuly blocked")
        except:
            print("survey-modal did not appear")
        
        search_item = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )

        search_item.clear()
        search_item.send_keys(item)

        search_geo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "location-input"))
        )
        search_geo.clear()
        search_geo.send_keys(city)
        
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "css-16tss5f"))
            ).click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='search-submit']"))
            ).click()
            
            WebDriverWait(driver, 10).until(
                EC.title_contains(f"{item} в {city} - OLX.ua")
            )
        except:
            print(f"Location issue: {city}")
        
        expected_title = f"{item} в {city} - OLX.ua"
        assert expected_title in driver.title

        driver.get(start_url)
    
    driver.quit()
