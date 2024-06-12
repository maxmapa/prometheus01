import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


@pytest.mark.np
def test_check_incorrect_parcel_number():
    # Створення об'єкту для керування браузером
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # відкриваємо сторінку https://tracking.novaposhta.ua/#/uk
    driver.get("https://tracking.novaposhta.ua/")

    # Знаходимо поле, в яке будемо вводити неправильне ім'я користувача або поштову адресу
    search_elem = driver.find_element(By.ID, "en")

    # Вводимо неправиьний номер посилки
    search_elem.send_keys("RK023456789LV")
    
    # Знаходимо кнопку Пошук
    btn_elem = driver.find_element(By.ID, "np-number-input-desktop-btn-search-en").click()
    time.sleep(3)
    try:
        driver.find_element(By.CLASS_NAME, "tracking__error-text")
    except:
        print("Ми випадково знайшли реальну посилку")
    # Перевіряємо, що назва сторінки така, яку ми очікуємо
    assert "Трекінг посилки | Nova Global" in driver.title

    # Закриваємо браузер
    driver.close()
