import pytest
from modules.common.database import Database


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
def test_low_product_quantities():
    db = Database() 
    max_product_id = db.get_max_product_id()
    test_product_id = max_product_id + 1

    db.insert_product(test_product_id, 'Тест-продукт', 'Тест-описання', 7)

    try:
        first_order = {
            test_product_id: 5
        }
        
        place_order(db, first_order)
        
        assert db.select_product_qnt_by_id(test_product_id) == 2
        
    finally:
        db.delete_product_by_id(test_product_id)
        db.close()


@pytest.mark.db
def test_negative_product_quantities():
    db = Database()  
    max_product_id = db.get_max_product_id()
    test_product_id = max_product_id + 1

    db.insert_product(test_product_id, 'Тест-продукт', 'Тест-описання', 4)

    try:
        second_order = {
            test_product_id: 6 
        }
        place_order(db, second_order)  
        assert db.select_product_qnt_by_id(test_product_id) == -2
        
    finally:
        db.delete_product_by_id(test_product_id)
        db.close()


@pytest.mark.db
def test_unsupported_data():
    db = Database()
    max_product_id = db.get_max_product_id()
    test_product_id = max_product_id + 1

    possible_errors = [
        (test_product_id, "", 'Тест-продукт', 'Тест-описання', 4), # wrong table format
        (test_product_id, 'Тест-продукт', 'Тест-описання', -1), # wrong quantity
        (test_product_id, 15, 'Тест-описання', 5), # wrong name
        (test_product_id + 0.5, 'Тест-продукт', 'Тест-описання', 4), # wrong id
    ]

    for case in possible_errors:
        message = None
        try:
            product_id, name, description, quantity = case

            if not isinstance(product_id, int):
                raise TypeError(f"product_id має бути int, отримано {type(product_id).__name__}")
            if not isinstance(name, str):
                raise TypeError(f"name має бути str, отримано {type(name).__name__}")
            if not isinstance(description, str):
                raise TypeError(f"description має бути str, отримано {type(description).__name__}")
            if not isinstance(quantity, int):
                raise TypeError(f"quantity має бути int, отримано {type(quantity).__name__}")

            if quantity < 0:
                message = "Кількість товару не може бути меншою за 0: " + str(quantity)
                print(message)
            else:
                try:
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

        assert message is not None, "Тест не викликав очікувану помилку"

        db.delete_product_by_id(test_product_id)
    
    db.close()
