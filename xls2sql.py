import pandas as pd
import sqlite3

# Задайте шлях до вашого CSV файлу
excel_file_path = 'converter\\att0724.xlsx'

# Задайте назву бази даних SQLite
db_file_path = 'converter\\att0724.db'

# Задайте назву таблиці в базі даних
table_name = 'bookings'

# Читаємо CSV файл у DataFrame, вказуємо розділювач колонок і кодування
df = pd.read_excel(excel_file_path)

# Замінюємо значення в назвах колонок

df.columns = df.columns.str.replace("Ações", "id")
df.columns = df.columns.str.replace("Serviço", "Servico")
df.columns = df.columns.str.replace("Proveniência", "Provenincia")
df.columns = df.columns.str.replace("Crianças", "Criancas")
df.columns = df.columns.str.replace("Bebés", "Bebes")
df.columns = df.columns.str.replace(". ", "_")

# Замінюємо значення в комірках відповідно до правил заміни
replacements = {
    r"Receção": "Recessao",
    r"Temáticos": "Tematicos"    
}

df = df.replace(replacements, regex=True)

# Отримуємо кількість рядків і колонок
num_rows, num_cols = df.shape

# Створюємо SQLite підключення
conn = sqlite3.connect(db_file_path)

# Конвертуємо DataFrame у SQLite таблицю
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Закриваємо підключення до бази даних
conn.close()

# Виводимо повідомлення про успішну конвертацію з кількістю рядків і колонок
print(f"Success! Excel file converted to SQLite {num_cols} columns x {num_rows} rows database.")
