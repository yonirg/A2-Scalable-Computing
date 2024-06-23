from mock.models import generate_user, generate_product, generate_stock, generate_purchase_order, generate_store, generate_purchase_order_recent
from server import process_user_data, process_product_data, process_store_data, process_stock_data, process_purchase_order_data
from concurrent.futures import ThreadPoolExecutor
import random
import json

mult = 10
# Quantidade de dados simulados a serem gerados
num_users = 10 * mult
num_products = 10 * mult
num_stores = 1 * mult
num_purchase_orders = 20 * mult

# Gerar usuários simulados
users = [generate_user() for _ in range(num_users)]

# Gerar produtos simulados
products = [generate_product() for _ in range(num_products)]

# Gerar lojas simuladas
stores = [generate_store() for _ in range(num_stores)]

# Gerar estoque para cada produto simulado
stocks = [generate_stock(product.id, store.id, random.randint(1, 100)) for product in products for store in stores]

# Gerar ordens de compra simuladas
purchase_orders = [
    generate_purchase_order(
        random.choice(users).id,
        random.choice(products).id,
        random.choice(stores).id,
        random.randint(1, 10)
    ) for _ in range(num_purchase_orders)
]

purchase_orders_recent = [
    generate_purchase_order_recent(
        random.choice(users).id,
        random.choice(products).id,
        random.choice(stores).id,
        random.randint(1, 10)
    ) for _ in range(num_purchase_orders)
]

NUM_MESSAGES = 10

# Assume que process_user_data, process_product_data, process_store_data, process_stock_data, process_purchase_order_data are defined

# Define functions to handle delayed processing for each type
def process(process_name, data):
    print(process_name)
    for row in data:
        row_json = json.dumps(row.__dict__)
        process_user_data.delay()    


def process_users():
    print("Users:")
    for user in users:
        dados = json.dumps(user.__dict__)
        process_user_data.delay(dados)

def process_products():
    print("\nProducts:")
    for product in products:
        dados = json.dumps(product.__dict__)
        process_product_data.delay(dados)

def process_stores():
    print("\nLojas:")
    for store in stores:
        dados = json.dumps(store.__dict__) 
        process_store_data.delay(dados)

def process_stocks():
    print("\nStocks:")
    for stock in stocks:
        dados = json.dumps(stock.__dict__)
        process_stock_data.delay(dados)

def process_purchase_orders():
    print("\nPurchase Orders:")
    for order in purchase_orders:
        dados = json.dumps(order.__dict__)
        process_purchase_order_data.delay(dados)

def process_purchase_orders_recent():
    print("\nRecent purchase Orders:")
    for order in purchase_orders_recent:
        dados = json.dumps(order.__dict__)
        process_purchase_order_data.delay(dados)

# Create a ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=5) as executor:
    # Submit each processing function to its own thread
    executor.submit(process_users)
    executor.submit(process_products)
    executor.submit(process_stores)
    executor.submit(process_stocks)
    executor.submit(process_purchase_orders)
    #executor.submit(process_purchase_orders_recent)

