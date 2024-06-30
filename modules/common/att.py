import sqlite3


class ATT:

    def __init__(self, db_name='att0624'):
        self.connection = sqlite3.connect(r'c:\\Users\\Max\\projects_py\\converter\\' +
                                          db_name + '.db')
        self.cursor = self.connection.cursor()

    def test_connection(self):
        sqlite_select_Query = "SELECT sqlite_version();"
        self.cursor.execute(sqlite_select_Query)
        record = self.cursor.fetchall()

        print(f"Connected successfully. SQLite Database Version is: {record}")
        
    def get_passengers(self):
        query = "SELECT id, Classe, Adultos, Criancas, Bebes, Provenincia FROM bookings"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def get_operador(self):
        query = "SELECT id, Tickets, Operador, Cob_Operador, Cob_Motorista, Cob_Parceiro, Provenincia FROM bookings"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data        

    def get_rate_by_hour(self):
        query = "SELECT id, Hora, Categoria, Val_Servico, Provenincia FROM bookings"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def get_user_address_by_name(self, name):
        query = f"SELECT address, city, postalCode, country FROM customers WHERE name = '{name}'"
        self.cursor.execute(query)
        record = self.cursor.fetchall()

        return record

    def select_product_qnt_by_id(self, product_id):
        query = f"SELECT quantity FROM products WHERE id = {product_id}"
        self.cursor.execute(query)
        record = self.cursor.fetchone()

        return record[0]  # Повертаємо лише значення кількості


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
