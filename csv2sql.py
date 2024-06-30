import pandas as pd
import sqlite3

# Задайте шлях до вашого CSV файлу
csv_file_path = 'converter\\att0724.csv'

# Задайте назву бази даних SQLite
db_file_path = 'converter\\att0724.db'

# Задайте назву таблиці в базі даних
table_name = 'bookings'

# Читаємо CSV файл у DataFrame, вказуємо розділювач колонок і кодування
df = pd.read_csv(csv_file_path, sep=';', encoding='latin1')

# Замінюємо значення в назвах колонок

df.columns = df.columns.str.replace("A??es", "id")
df.columns = df.columns.str.replace("Servi?o", "Servico")
df.columns = df.columns.str.replace("Proveni?ncia", "Provenincia")
df.columns = df.columns.str.replace("Crian?as", "Criancas")
df.columns = df.columns.str.replace("Beb?s", "Bebes")
df.columns = df.columns.str.replace("Val. ", "Val_")
df.columns = df.columns.str.replace("Cob. ", "Cob_")

# Замінюємо значення в комірках відповідно до правил заміни
replacements = {
    r"Rece\?\?o": "Recessao",
    r"Tem\?ticos": "Tematicos"    
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
print(f"Success! CSV file converted to SQLite {num_cols} columns x {num_rows} rows database.")
