import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

@pytest.mark.olx
def test_search_main_page():
    # Створення об'єкту для керування браузером
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    # Відкриваємо сторінку OLX
    driver.get("https://www.olx.ua")
    # Проходимо діалог щодо куків
    try:
        driver.find_element(By.XPATH, "//span[contains(text(),'Закрити')]").click()
    except:
        print("Куки вже прийняті")
    # Перевіряємо, що назва сторінки така, яку ми очікуємо
    assert "Оголошення OLX.ua: сервіс оголошень України — купівля/продаж бу та нових товарів, різноманітні послуги на сайті OLX.ua" in driver.title
    
    # Знаходимо поле пошуку товара
    search_item = driver.find_element(By.ID, "search")
    # Вводимо шуканий товар
    item = "RTX 2060"
    location = "Львів"
    search_item.send_keys(item)
    time.sleep(2)
    # Знаходимо поле пошуку локації
    search_geo = driver.find_element(By.ID, "location-input")
    # Вводимо локацію
    search_geo.send_keys(location)
    time.sleep(1)
    try: 
        driver.find_element(By.CLASS_NAME, "css-16tss5f").click() #вибираємо місто із дроп-даун підказок
        driver.find_element(By.XPATH, "//button[@data-testid='search-submit']").click() #клікаємо кнопку пошуку
        time.sleep(5)
    except:
        print("затик з локацїєю")
    expected_title = f"{item} в {location} - OLX.ua"
    assert expected_title in driver.title
    # Закриваємо браузер
    driver.quit()
    
    