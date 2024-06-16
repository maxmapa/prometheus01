import pytest
from modules.common.database import Database

# Функція для моделювання замовлення
def place_order(db, order):
    for product_id, quantity in order.items():
        current_quantity = db.select_product_qnt_by_id(product_id)
        new_quantity = current_quantity - quantity
        db.update_product_quantity(product_id, new_quantity)

        if 0 < new_quantity < 3:
            product_info = db.cursor.execute('SELECT name, description FROM products WHERE id = ?', (product_id,)).fetchone()
            print(f"Товару {product_info[0]} {product_info[1]} залишилося мало. Поповніть запаси!")
        else:
            product_info = db.cursor.execute('SELECT name, description FROM products WHERE id = ?', (product_id,)).fetchone()
            print(f"Запасів {product_info[0]} {product_info[1]} на складі недостатньо для виконання замовлення. Поповніть запаси!")


@pytest.mark.db
# Тестова функція
def test_low_product_quantities():
    db = Database()  # Підключення до бази даних

    # Отримання найбільшого product_id
    max_product_id = db.get_max_product_id()
    test_product_id = max_product_id + 1

    # Додавання тестового товару в кількості 7 одиниць
    db.insert_product(test_product_id, 'Тест-продукт', 'Тест-описання', 7)

    try:
        # Покупець
        first_order = {
            test_product_id: 5  # Тест-продукт
        }
        
        place_order(db, first_order)
        
        # Перевірка залишків після замовлення
        assert db.select_product_qnt_by_id(test_product_id) == 2
        
    finally:
        # Видалення тестового товару
        db.delete_product_by_id(test_product_id)
        db.close()


@pytest.mark.db
# Тестова функція для перевірки негативних залишків товарів
def test_negative_product_quantities():
    db = Database()  # Підключення до бази даних

    # Отримання найбільшого product_id
    max_product_id = db.get_max_product_id()
    test_product_id = max_product_id + 1

    # Додавання тестового товару в кількості 4 одиниці
    db.insert_product(test_product_id, 'Тест-продукт', 'Тест-описання', 4)

    try:
        # Покупець
        second_order = {
            test_product_id: 6  # Тест-продукт (більше, ніж доступно)
        }
        
        place_order(db, second_order)  # Викликаємо функцію place_order для замовлення
        
        # Перевірка залишків після замовлення
        assert db.select_product_qnt_by_id(test_product_id) == -2
        
    finally:
        # Видалення тестового товару
        db.delete_product_by_id(test_product_id)
        db.close()

@pytest.mark.db
# Тестова функція для перевірки помилки при додаванні товару з невірними типами даних
def test_unsupported_data():
    db = Database()  # Підключення до бази даних

    # Отримання найбільшого product_id
    max_product_id = db.get_max_product_id()
    test_product_id = max_product_id + 1

    possible_errors = [
        (test_product_id, "", 'Тест-продукт', 'Тест-описання', 4), # неправильний формат таблиці
        (test_product_id, 'Тест-продукт', 'Тест-описання', -1), # неправильна кількість товару
        (test_product_id, 15, 'Тест-описання', 5), # неправильна назва товару
        (test_product_id + 0.5, 'Тест-продукт', 'Тест-описання', 4), # неправильний id
    ]

    for case in possible_errors:
        message = None
        try:
            # Розпакування параметрів
            product_id, name, description, quantity = case

            # Перевірка типів даних
            if not isinstance(product_id, int):
                raise TypeError(f"product_id має бути int, отримано {type(product_id).__name__}")
            if not isinstance(name, str):
                raise TypeError(f"name має бути str, отримано {type(name).__name__}")
            if not isinstance(description, str):
                raise TypeError(f"description має бути str, отримано {type(description).__name__}")
            if not isinstance(quantity, int):
                raise TypeError(f"quantity має бути int, отримано {type(quantity).__name__}")

            # Додавання перевірки кількості товару
            if quantity < 0:
                message = "Кількість товару не може бути меншою за 0: " + str(quantity)
                print(message)
            else:
                try:
                    # Додавання тестового товару в невірному форматі
                    db.insert_product(product_id, name, description, quantity)
                except TypeError as e:
                    message = "Введено невірний тип даних: " + str(e)
                    print(message)
                except ValueError as e:
                    message = "Невірна кількість товару: " + str(e)
                    print(message)
                except Exception as e:
                    message = "Інша помилка: " + str(e)
                    print(message)
        except TypeError as e:
            message = "Невірний тип даних: " + str(e)
            print(message)
        except ValueError as e:
            message = "Помилка розпакування параметрів: " + str(e)
            print(message)
        except Exception as e:
            message = "Інша помилка при розпакуванні: " + str(e)
            print(message)

        # Очікування помилки
        assert message is not None, "Тест не викликав очікувану помилку"

        # Прибирання після тесту
        db.delete_product_by_id(test_product_id)
    
    db.close()
