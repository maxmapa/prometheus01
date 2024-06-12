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
