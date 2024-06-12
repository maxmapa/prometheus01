import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

@pytest.mark.yt
def test_dialog_before_you_continue_to_YouTube():
    # Створення об'єкту для керування браузером
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    # Відкриваємо сторінку YouTube каналу
    driver.get("https://www.youtube.com/@Prometheus_Ukraine")
    # Проходимо діалог щодо куків
    try:
        driver.find_element(By.XPATH, "//span[contains(text(),'Reject all')]").click()
    except:
        try:
            driver.find_element(By.XPATH, "//span[contains(text(),'Отклонить все')]").click()
        except:
            print("Кнопка 'Reject all' або 'Отклонить все' не знайдена або вже була натиснута")
    # Перевіряємо, що назва сторінки така, яку ми очікуємо
    assert "Prometheus - YouTube" in driver.title
    
    # Закриваємо браузер
    driver.quit()

@pytest.mark.yt
def test_subscribe_dialog():
    # Створення об'єкту для керування браузером
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    # Відкриваємо сторінку YouTube каналу
    driver.get("https://www.youtube.com/@Prometheus_Ukraine")
    # Проходимо діалог щодо куків
    try:
        driver.find_element(By.XPATH, "//span[contains(text(),'Reject all')]").click()
    except:
        try:
            driver.find_element(By.XPATH, "//span[contains(text(),'Отклонить все')]").click()
        except:
            print("Кнопка 'Reject all' або 'Отклонить все' не знайдена або вже була натиснута")
    # Перевіряємо, що назва сторінки така, яку ми очікуємо
    assert "Prometheus - YouTube" in driver.title
    
    try:
        driver.find_element(By.XPATH, "//span[contains(text(),'Підписатися')]").click()
    except:
        print("Треба залогінитись перш ніж оформити підписку на канал")
        
    # Закриваємо браузер
    driver.quit()