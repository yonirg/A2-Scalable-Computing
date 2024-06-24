import os
import sqlite3

user_create = '''
            CREATE TABLE user (
                id_database INTEGER PRIMARY KEY AUTOINCREMENT,
                id TEXT,
                name TEXT,
                email TEXT,
                address TEXT,
                registration_date TEXT,
                birth_date TEXT,
                timestamp TEXT
            )
        '''

product_create = '''
            CREATE TABLE product (
                id_database INTEGER PRIMARY KEY AUTOINCREMENT,
                id TEXT,
                name TEXT,
                image TEXT,
                description TEXT,
                price REAL, 
                timestamp TEXT
            )
        '''

store_create = '''
            CREATE TABLE store (
                id_database INTEGER PRIMARY KEY AUTOINCREMENT,
                id_store TEXT,
                name TEXT,
                url TEXT               
            )
        '''

stock_create = '''
            CREATE TABLE stock (
                id_product TEXT,
                id_store TEXT,
                quantity INT,
                PRIMARY KEY (id_product, id_store)             
            )
        '''

purchase_order_create = '''
            CREATE TABLE purchase_order (
                id_database INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                product_id TEXT,
                store_id TEXT,
                quantity INT,
                creation_date TEXT,
                payment_date TEXT, 
                delivery_date TEXT, 
                timestamp TEXT
            )
        '''

user_insert = '''
        INSERT INTO user (id, name, email, address, registration_date, birth_date, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''

product_insert = '''
        INSERT INTO product (id, name, image, description, price, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    '''

store_insert = '''
        INSERT INTO store (id_store, name, url)  
        VALUES (?, ?, ?)
    '''

stock_insert = '''
        INSERT INTO stock (id_product, id_store, quantity)  
        VALUES (?, ?, ?)
    '''

purchase_order_insert = '''
        INSERT INTO purchase_order (user_id, product_id, store_id, quantity, creation_date,
            payment_date, delivery_date, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?,  ?)
    '''

create = {'user': user_create, 'product': product_create, 'store': store_create, 'stock': stock_create, 'purchase_order': purchase_order_create}
insert = {'user': user_insert, 'product': product_insert, 'store': store_insert, 'stock': stock_insert, 'purchase_order': purchase_order_insert}

def get_database_connection(data_type, data):
    db_path = data_type + '.sqlite3'
    db_exists = os.path.exists(db_path)
    
    # Conectar ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Criar tabela se o banco de dados não existir
    if not db_exists:
        cursor.execute(create[data_type])

        conn.commit()

    valores = list(data.values())
    if data_type != "stock":
        valores = valores[1:]

    cursor.execute(insert[data_type], valores)
    conn.commit()
    conn.close()