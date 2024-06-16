import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

@pytest.mark.olx
def test_search_main_page():
    # Створення об'єкту для керування браузером
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    # Відкриваємо сторінку OLX
    driver.get("https://www.olx.ua")
    # Handle the cookie consent
    try:
        driver.find_element(By.XPATH, "//span[contains(text(),'Закрити')]").click()
    except:
        print("Куки вже прийняті")
    # Перевіряємо, що назва сторінки така, яку ми очікуємо
    assert "Оголошення OLX.ua: сервіс оголошень України — купівля/продаж бу та нових товарів, різноманітні послуги на сайті OLX.ua" in driver.title
    
    # Знаходимо поле пошуку товара
    search_item = driver.find_element(By.ID, "search")
    # Вводимо шуканий товар
    search_item.send_keys("RTX 2060")
    time.sleep(2)
    # Знаходимо поле пошуку локації
    search_geo = driver.find_element(By.ID, "location-input")
    # Вводимо локацію
    search_geo.send_keys("Львів")
    time.sleep(2)
    try: 
        driver.find_element(By.CLASS_NAME, "css-16tss5f").click() #вибираємо місто із дроп-даун підказок
        driver.find_element(By.XPATH, "//button[@data-testid='search-submit']").click() #клікаємо кнопку пошуку
        time.sleep(5)
    except:
        print("затик з локацїєю")
    expected_title = "RTX 2060 в Львів - OLX.ua"
    assert expected_title in driver.title
    # Закриваємо браузер
    driver.quit()
    
@pytest.mark.olx
def test_search_main_page_cycle():
    # Створення об'єкту для керування браузером
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    start_url = "https://www.olx.ua"
    
    # Відкриваємо сторінку OLX
    driver.get(start_url)
    
    # Handle the cookie consent
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Закрити')]"))
        ).click()
    except:
        print("Куки вже прийняті")
    
    # Перевіряємо, що назва сторінки така, яку ми очікуємо
    assert "Оголошення OLX.ua: сервіс оголошень України — купівля/продаж бу та нових товарів, різноманітні послуги на сайті OLX.ua" in driver.title
    
    item = "RTX 2060"
    locations = ["Київ", "Дніпро", "Одеса", "Харків"]
    
    for city in locations:
        # Закриваємо модальне вікно у разі появи
        try:
            survey_modal = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.ID, "survey-modal"))
            )
            if survey_modal:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
                ).click()
                print("Модальне вікно успішно заблоковане")
        except:
            print("Вікно опитування не з'явилося")
        
        # Знаходимо поле пошуку товара
        search_item = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        # Очищуємо та вводимо шуканий товар
        search_item.clear()
        search_item.send_keys(item)
        
        # Знаходимо поле пошуку локації
        search_geo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "location-input"))
        )
        # Очищуємо та вводимо локацію
        search_geo.clear()
        search_geo.send_keys(city)
        
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "css-16tss5f"))
            ).click()  # Вибираємо місто із дроп-даун підказок
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='search-submit']"))
            ).click()  # Клікаємо кнопку пошуку
            
            # Очікуємо зміни заголовку сторінки
            WebDriverWait(driver, 10).until(
                EC.title_contains(f"{item} в {city} - OLX.ua")
            )
        except:
            print(f"Затик з локацїєю: {city}")
        
        expected_title = f"{item} в {city} - OLX.ua"
        assert expected_title in driver.title
        
        # Перехід на домашню сторінку
        driver.get(start_url)
    
    # Закриваємо браузер
    driver.quit()
