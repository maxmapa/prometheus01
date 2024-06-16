"""команда для виконання оновлення бази в Git терміналі: 
python update_database.py
за умови, що і база і файл оновлення знаходять в кореневому каталозі
"""
import sqlite3

# Підключення до бази даних (або створення нової, якщо вона не існує)
conn = sqlite3.connect('become_qa_auto.db')

# Створення курсора для виконання SQL команд
cursor = conn.cursor()

# SQL команди для вставки нових записів
sql_insert = """
INSERT INTO products (id, name, description, quantity) VALUES
(5, 'йогурт', 'з фруктами', 15),
(6, 'морозиво', 'ванільне', 35), 
(7, 'хліб', 'цільнозерновий', 20);
"""

# Виконання SQL команд
cursor.execute(sql_insert)

# Збереження змін
conn.commit()

# Закриття з'єднання
conn.close()
