"""command to update database in Git terminal: 
python update_database.py
if both file.py and database.db located in same main catalog
"""
import sqlite3

# Connect to database (or create new, if not exist)
conn = sqlite3.connect('become_qa_auto.db')
cursor = conn.cursor()

sql_insert = """
INSERT INTO products (id, name, description, quantity) VALUES
(5, 'йогурт', 'з фруктами', 15),
(6, 'морозиво', 'ванільне', 35), 
(7, 'хліб', 'цільнозерновий', 20);
"""
cursor.execute(sql_insert)
conn.commit()

conn.close()
