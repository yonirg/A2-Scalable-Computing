import os
from dataclasses import dataclass
from random import choice, randint, random, choices, shuffle
import models
from collections import deque
from graph_user_flow import *
import time
from datetime import datetime, timedelta
import sqlite3

X = 1000  # Minimum value of purchases in the last 10 minutes
Y = 5000  # Minimum value of purchases in the last 6 hours

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
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    '''

product_insert = '''
        INSERT INTO product (id, name, image, description, price, timestamp)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
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
        VALUES (?, ?, ?, ?, ?, ?, ?,  CURRENT_TIMESTAMP)
    '''

create = {'user': user_create, 'product': product_create, 'store': store_create, 'stock': stock_create, 'purchase_order': purchase_order_create}
insert = {'user': user_insert, 'product': product_insert, 'store': store_insert, 'stock': stock_insert, 'purchase_order': purchase_order_insert}

@dataclass
class SimulationParams:
    cycle_duration: float
    num_initial_users: int
    num_initial_products: int
    num_initial_stores: int
    qtd_stock_initial: int
    max_simultaneus_users: int
    num_new_users_per_cycle: int
    num_new_products_per_cycle: int

class Simulation:
    params: SimulationParams
    cycle: int
    silent: bool = True

    def __init__(self, params: SimulationParams, silent: bool = True):
        self.cycle = 0
        self.params = params
        self.silent = silent
        self.users = []
        self.new_users = []
        self.products = []
        self.products_prices = {}
        self.new_products = []
        self.stores = []
        self.new_stores = []
        self.stock = {}
        self.new_stock_decreases = {}
        self.purchase_orders = []
        self.new_purchase_orders = []
        self.waiting_users = deque()
        self.logged_users = deque()
        self.depuration = []
        self.log_flow = []
        self.user_flow_report = []
        self.purchase_history = []
        self.issued_coupons = {}

        self.G = G

        self.folder_name = "mock/mock_files"
        self.subfolder_sqlite3 = "sqlite3"
        self.subfolder_log = "log"
        self.subfolder_http_request = "request"
        self.log_filename = "log_simulation.txt"
        self.log_complete_path = f"{self.folder_name}/{self.subfolder_log}/{self.log_filename}"
        self.sqlite3_file_names = ["users.sqlite3", "products.sqlite3", "store.sqlite3", "stock.sqlite3", "purchase_orders.sqlite3"]
        self.sqlite3_complete_path = [f"{self.folder_name}/{self.subfolder_sqlite3}/{file_name}" for file_name in self.sqlite3_file_names]
        self.request_file_name = "request"
        self.request_complete_path = f"{self.subfolder_http_request}/{self.request_file_name}"

        # If the folder exists, delete its contents
        if os.path.exists(self.folder_name):
            self.remove_folder_contents(self.folder_name)
        else:
            os.makedirs(self.folder_name)

        # Create inside folder_name or delete other folder if they exist for the other subfolders
        sqlite3_folder = f"{self.folder_name}/{self.subfolder_sqlite3}"
        logs_folder = f"{self.folder_name}/{self.subfolder_log}"
        http_request_folder = f"{self.folder_name}/{self.subfolder_http_request}"

        for folder in [sqlite3_folder, logs_folder, http_request_folder]:
            if os.path.exists(folder):
                self.remove_folder_contents(folder)
            else:
                os.makedirs(folder)

        # Generate users at the start of the simulation
        for _ in range(self.params.num_initial_users):
            self.__generate_user()

        # Generate products at the start of the simulation
        for _ in range(self.params.num_initial_products):
            self.__generate_product()

        # Generate products at the start of the simulation
        for _ in range(self.params.num_initial_stores):
            self.__generate_store()

        # Generate stock for the products
        for store in self.stores:
            for product in self.products:
                self.__generate_stock(product, store, self.params.qtd_stock_initial)

        self.__report_initial_cycle()

    def __connect(self, data_type, index):
            db_path = self.sqlite3_complete_path[index]
            db_exists = os.path.exists(db_path)
            
            # Conectar ao banco de dados
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Criar tabela se o banco de dados não existir
            if not db_exists:
                cursor.execute(create[data_type])

                conn.commit()
            
            return conn
    
    def __report_initial_cycle(self):
         # Report users, products and stocks created, creating the new data bases
        data_type = 'user'
        conn = self.__connect(data_type, 0)
        cursor = conn.cursor()

        content = [[user.id, user.name, user.email, user.address, user.registration_date, user.birth_date] for user in self.new_users]
        for item in content:
            cursor.execute(insert[data_type], item)

        conn.commit()
        conn.close()
        self.new_users = []
        
        data_type = 'product'
        conn = self.__connect(data_type, 1)
        cursor = conn.cursor()

        content = [[product.id, product.name, product.image, product.description, product.price] for product in self.new_products]
        for item in content:
            cursor.execute(insert[data_type], item)

        conn.commit()
        conn.close()
        self.new_products = []

        data_type = 'store'
        conn = self.__connect(data_type, 2)
        cursor = conn.cursor()

        content = [[store.id, store.name, store.url] for store in self.new_stores]
        for item in content:
            cursor.execute(insert[data_type], item)

        conn.commit()
        conn.close()
        self.new_stores = []

        data_type = 'stock'
        conn = self.__connect(data_type, 3)
        cursor = conn.cursor()

        content = [[store_product_id[1], store_product_id[0], quantity] for store_product_id, quantity in self.stock.items()]
        for item in content:
            cursor.execute(insert[data_type], item)

        conn.commit()
        conn.close()

        data_type = 'purchase_order'
        self.__connect(data_type, 4)

    def remove_folder_contents(self, folder_path):
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)     
    
    def run(self):
        END = time.time() + 15 # Run for 15 seconds
        while time.time() < END:
            self.cycle += 1

            # CONTA VERDE
            for _ in range(self.params.num_new_users_per_cycle):
                self.__generate_user()
            for _ in range(self.params.num_new_products_per_cycle):
                self.__generate_product()
            self.__generate_stock_for_new_products()
            
            # Allow users to enter and perform actions on the system, after they have logged
            # DATACAT & DataAnalytics
            self.__select_waiting_users()
            self.__select_users_to_login()    

            # CONTA VERDE
            self.__update_cycle_stock()

            # DATACAT
            self.__introduct_errors_for_log()

            self.__print_status()
            self.__report_cycle()
            time.sleep(self.params.cycle_duration)
           
    def __introduct_errors_for_log(self):
        
        # Choose a random integer between 0 and 5
        component_error = randint(0, 5)
        message = f";Error;{component_error}\n"
        self.__add_message_to_log(message)
        
    def __select_waiting_users(self):

        num_users = min(self.params.max_simultaneus_users, len(self.users))
        user_copy = self.users.copy()
        shuffle(user_copy)
        for i in range(num_users):
            self.waiting_users.append(user_copy[i])

        
    def __select_users_to_login(self):

        for _ in self.waiting_users.copy():
            user = self.waiting_users.popleft()
            # Apply userflow to the user, without using threads
            self.__user_flow(user)


    def __user_flow(self, user):
        # Let the user perform actions on the system until it reaches the EXIT node
        current_node = LOGIN
        message = f";Audit;{user};{LOGIN}\n"
        self.__add_message_to_log(message)

        current_product_store_list = []
        current_product_store = None

        
        while current_node != EXIT:
            # Select the next as the current node's successor, based on the probability of each neighbor in the edge
            current_node_neighbors = {}
            for u, v, d in G.edges(data=True):
                current_node_neighbors.setdefault(u, []).append((v, d["prob"]))
            next_node = choices(*zip(*current_node_neighbors[current_node]))[0]

            if next_node == HOME:
                self.__home(user)

            elif next_node == VIEW_PRODUCT:
                products_in_stock = [(store, product) for store in self.stores.copy() for product in self.products.copy() if self.stock[(store, product)] > 0]
                if not products_in_stock:
                    next_node = EXIT
                else:
                    current_product_store = choice(products_in_stock)
                    self.__view_product(user, current_product_store[0], current_product_store[1])

            elif next_node == CART:
                current_product_store_list.append(current_product_store)
                self.__cart(user, current_product_store[0], current_product_store[1])

            elif next_node == CHECKOUT:
                self.__checkout(user, current_product_store_list)

            current_node = next_node
        self.__exit(user)

    def get_timestamp_string(self):
        return str(time.time_ns())  # Use nanoseconds for best resolution
    
    def __add_message_to_log(self, message):
        cur_time = self.get_timestamp_string()
        self.log_flow.append(cur_time + message)

    def __add_message_to_user_flow_report(self, message):
        cur_time = self.get_timestamp_string()
        self.user_flow_report.append(cur_time + message)

    def __home(self, user):
        msg = f";User;{user};{STIMUL_SCROLLING};{HOME}.\n"
        self.__add_message_to_user_flow_report(msg)

    def __view_product(self, user, product, store):
        msg = f";User;{user};{STIMUL_ZOOM};{VIEW_PRODUCT} {(store, product)}.\n"
        self.__add_message_to_user_flow_report(msg)


    def __cart(self, user, product, store):
        msg = f";User;{user};{STIMUL_CLICK};{CART} with {(store, product)}.\n"
        self.__add_message_to_user_flow_report(msg)

    def __checkout(self, user, product_store_list):
        product_list = 0
        msg = f";User;{user};{STIMUL_CLICK};{CHECKOUT} with {product_store_list}.\n"
        self.__add_message_to_user_flow_report(msg)

        # total_value = sum([self.products_prices[product[0]] for product in product_store_list])
        # self.purchase_history.append(models.Purchase_History(user, total_value, datetime.now()))
        
        # self.__evaluate_bonus(user)
        
        def add_purchase_order():
            dictionary_products = {}
            for key in product_store_list:
                dictionary_products[key] = dictionary_products.get(key, 0) + 1
            for key, quantity in dictionary_products.items():
                store,product = key
                purchase_order = self.__generate_purchase_order(user, product, store, quantity)
                
                for _ in range(quantity):
                    mesage = f";Audit;{user};BUY;{(purchase_order.store_id, purchase_order.product_id)}\n"
                    self.__add_message_to_log(mesage)

                self.__decrease_stock(product, store, quantity)
        add_purchase_order()

    def __evaluate_bonus(self, user_id):
        now = datetime.now()
        ten_minutes_ago = now - timedelta(minutes=10)
        six_hours_ago = now - timedelta(hours=6)

        last_10_minutes_purchases = [
            p.total_value for p in self.purchase_history 
            if p.user_id == user_id and p.timestamp >= ten_minutes_ago
        ]
        last_6_hours_purchases = [
            p.total_value for p in self.purchase_history 
            if p.user_id == user_id and p.timestamp >= six_hours_ago
        ]

        if sum(last_10_minutes_purchases) > X and sum(last_6_hours_purchases) > Y:
            self.__issue_coupon(user_id)

    def __issue_coupon(self, user_id):
        coupon_code = f"DISCOUNT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{user_id}"
        self.issued_coupons[user_id] = coupon_code
        self.__notify_web_application(user_id, coupon_code)

    def __notify_web_application(self, user_id, coupon_code):
        msg = f";Bonus;{coupon_code};{user_id}\n"
        self.__add_message_to_log(msg)
        
    def __exit(self, user):
        msg = f";User;{user};{STIMUL_CLICK};{EXIT}\n"
        self.__add_message_to_user_flow_report(msg)

        msg = f";Audit;{user};{EXIT}\n"
        self.__add_message_to_log(msg)



    def __generate_user(self):
        user = models.generate_user()
        self.users.append(user.id)
        self.new_users.append(user)

    def __generate_users(self):
        # Choose a random number of users to generate, between 0 and 1, with 70% chance of generating 0 users
        num_users = 1 if random() > 0.3 else 0
        for _ in range(num_users):
            self.__generate_user()

    def __generate_stock(self, product_id, store_id, quantity):
        stock_product = models.generate_stock(product_id, store_id, quantity)
        key = (stock_product.id_store, stock_product.id_product)
        self.stock[key] = stock_product.quantity

    def __generate_product(self):
        product = models.generate_product()
        self.products.append(product.id)
        self.products_prices[product.id] = product.price
        self.new_products.append(product)        

    def __generate_products(self):
        # Choose a random number of products to generate, between 0 and 1, with 80% chance of generating 0 products
        num_products = 1 if random() > 0.2 else 0
        for _ in range(num_products):
            self.__generate_product()

    def __generate_store(self):
        store = models.generate_store()
        self.stores.append(store.id)
        self.new_stores.append(store)

    def __generate_stock_for_new_products(self):
        for store in self.stores:
            for product in self.new_products:
                self.__generate_stock(product.id, store, randint(1, 100))

    def __decrease_stock(self, product_id, store_id, quantity):
        key = (store_id, product_id)
        self.new_stock_decreases[key] = self.new_stock_decreases.get(key, 0) + quantity

    def __update_cycle_stock(self):
        for key, quantity in self.new_stock_decreases.items():
            self.stock[key] -= quantity

    def __generate_purchase_order(self, user_id, product_id, store_id, quantity):
        purchase_order = models.generate_purchase_order(user_id, product_id, store_id, quantity)
        self.purchase_orders.append(purchase_order)
        self.new_purchase_orders.append(purchase_order)
        return purchase_order
    
    def __print_status(self):
        if self.silent:
            return

    def __report_cycle(self):
        # Add cycle to the beginning of the base name of the log file
        log_cycle = f"{self.folder_name}/{self.subfolder_log}/{self.cycle}{self.log_filename}"

        # Add cycle to the beginning of the base name of the http request file
        request_cycle = f"{self.folder_name}/{self.subfolder_http_request}/{self.cycle}{self.request_file_name}"

        
        first_half = self.user_flow_report[len(self.user_flow_report)//2:]
        self.user_flow_report = self.user_flow_report[:len(self.user_flow_report)//2]

        log_flow_colunms = ["timestamp", "type", "content", "extra_1", "extra_2"]


        first_half.insert(0, ";".join(log_flow_colunms) + "\n")
        # Add to the beginning of the log_flow the first half of the user_flow_report
        self.log_flow = first_half + self.log_flow

        self.write_log(log_cycle)
        self.log_flow = []

        self.write_log_dataAnalytics(request_cycle)
        self.user_flow_report = []

        # Update (create if doesn't exists) new_users in a .csv file, keeping existing ones
        self.add_new_users_to_csv()
        self.new_users = []

        self.new_method()
        self.new_products = []

        self.rewrite_full_stock_to_sqlite3()
        self.new_stock_decreases = {}

        self.add_new_purchase_orders_to_sqlite3()
        self.new_purchase_orders = []


        # Log issued coupons
        if self.issued_coupons:
            with open(self.log_complete_path, 'a') as log_file:
                for user_id, coupon_code in self.issued_coupons.items():
                    log_file.write(f"Coupon issued to user {user_id}: {coupon_code}\n")
            self.issued_coupons.clear()

    def add_new_purchase_orders_to_sqlite3(self):
        if self.new_purchase_orders:
            data_type = 'purchase_order'
            conn = self.__connect(data_type, 4)
            cursor = conn.cursor()

            content = [[purchase_order.user_id, purchase_order.product_id, purchase_order.store_id, purchase_order.quantity, purchase_order.creation_date, purchase_order.payment_date, purchase_order.delivery_date] for purchase_order in self.new_purchase_orders]
            for item in content:
                cursor.execute(insert[data_type], item)
            conn.commit()
            conn.close()       
    
    def rewrite_full_stock_to_sqlite3(self):
        if self.new_stock_decreases:
            data_type = 'stock'
            conn = self.__connect(data_type, 3)
            cursor = conn.cursor()

            upsert_query = '''
                INSERT INTO stock (id_product, id_store, quantity)
                VALUES (?, ?, ?)
                ON CONFLICT(id_product, id_store) 
                DO UPDATE SET quantity = stock.quantity - excluded.quantity
            '''

            content = [[product_id, store_id, quantity] for (store_id, product_id), quantity in self.new_stock_decreases.items()]
            for item in content:
                cursor.execute(upsert_query, item)

            conn.commit()
            conn.close()

    def new_method(self):
        if self.new_products:
            data_type = 'product'
            conn = self.__connect(data_type, 1)
            cursor = conn.cursor()

            content = [[product.id, product.name, product.image, product.description, product.price] for product in self.new_products]
            for item in content:
                cursor.execute(insert[data_type], item)

            conn.commit()
            conn.close()
    
    def add_new_users_to_csv(self):
        if self.new_users:
            data_type = 'user'
            conn = self.__connect(data_type, 0)
            cursor = conn.cursor()

            content = [[user.id, user.name, user.email, user.address, user.registration_date, user.birth_date] for user in self.new_users]
            for item in content:
                cursor.execute(insert[data_type], item)

            conn.commit()
            conn.close()

    def write_log_dataAnalytics(self, request_cycle):
        if self.user_flow_report:
            with open(request_cycle, "a") as f:
                f.writelines(self.user_flow_report)
    
    def write_log(self, log_cycle):
        if self.log_flow:
            with open(log_cycle, "a") as f:
                f.writelines(self.log_flow)
