import sqlite3


class Database:
    def __init__(self, db_name='become_qa_auto'):
        self.connection = sqlite3.connect(r'c:\\Users\\Max\\prometheus01\\' + db_name + '.db')
        self.cursor = self.connection.cursor()

    def test_connection(self):
        sqlite_select_Query = "SELECT sqlite_version();"
        self.cursor.execute(sqlite_select_Query)
        record = self.cursor.fetchall()
        print(f"Connected successfully. SQLite Database Version is: {record}")

    def get_all_users(self):
        query = "SELECT name, address, city FROM customers"
        self.cursor.execute(query)
        record = self.cursor.fetchall()
        return record

    def get_user_address_by_name(self, name):
        query = f"SELECT address, city, postalCode, country FROM customers WHERE name = '{name}'"
        self.cursor.execute(query)
        record = self.cursor.fetchall()
        return record
        
    def update_product_quantity(self, product_id, quantity):
        query = f"UPDATE products SET quantity = {quantity} WHERE id = {product_id}"
        self.cursor.execute(query)
        """or oneliner instead of two lines 
        self.cursor.execute('UPDATE products SET quantity = ? WHERE id = ?', (quantity, product_id))"""
        self.connection.commit()
    
    def select_product_qnt_by_id(self, product_id):
        query = f"SELECT quantity FROM products WHERE id = {product_id}"
        self.cursor.execute(query)
        record = self.cursor.fetchone()
        return record[0] # Повертаємо лише значення кількості
           
    def get_first_n_products(self, n):
        self.cursor.execute(f"SELECT * FROM products LIMIT {n}")
        return self.cursor.fetchall()

    def get_max_product_id(self):
        self.cursor.execute("SELECT MAX(id) FROM products")
        return self.cursor.fetchone()[0]
        
    def insert_product(self, product_id, name, description, quantity):
        query = f"INSERT OR REPLACE INTO products (id, name, description, quantity) \
            VALUES ({product_id}, '{name}', '{description}', {quantity})"
        self.cursor.execute(query)
        self.connection.commit()        
        
    def delete_product_by_id(self, product_id):
        query = f"DELETE FROM products WHERE id = {product_id}"
        self.cursor.execute(query)
        self.connection.commit()       

    def get_detailed_orders(self):
        query = "SELECT orders.id, customers.name, products.name, \
                products.description, orders.order_date \
                FROM orders \
                JOIN customers ON orders.customer_id = customers.id \
                JOIN products ON orders.product_id = products.id"
        self.cursor.execute(query)
        record = self.cursor.fetchall()
        return record

    def close(self):
        self.connection.close()
        