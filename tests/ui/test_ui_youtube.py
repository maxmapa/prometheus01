import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


@pytest.mark.yt
def test_dialog_before_you_continue_to_YouTube():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get("https://www.youtube.com/@Prometheus_Ukraine")
    
    # Handle the cookie consent
    try:
        driver.find_element(By.XPATH, "//span[contains(text(),'Reject all')]").click()
    except:
        try:
            driver.find_element(By.XPATH, "//span[contains(text(),'Отклонить все')]").click()
        except:
            print("Button 'Reject all' or 'Отклонить все' not found")

    assert "Prometheus - YouTube" in driver.title

    driver.quit()


@pytest.mark.yt
def test_subscribe_dialog():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get("https://www.youtube.com/@Prometheus_Ukraine")
    
    # Handle the cookie consent
    try:
        driver.find_element(By.XPATH, "//span[contains(text(),'Reject all')]").click()
    except:
        try:
            driver.find_element(By.XPATH, "//span[contains(text(),'Отклонить все')]").click()
        except:
            print("Button 'Reject all' or 'Отклонить все' not found")

    assert "Prometheus - YouTube" in driver.title
    
    try:
        driver.find_element(By.XPATH, "//span[contains(text(),'Підписатися')]").click()
    except:
        print("Login first!")

    driver.quit()