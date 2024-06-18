from mock.models import generate_user, generate_product, generate_stock, generate_purchase_order
from server import process_user_data, process_product_data, process_stock_data, process_purchase_order_data
import random

# Quantidade de dados simulados a serem gerados
num_users = 10
num_products = 10
num_purchase_orders = 20

# Gerar usuários simulados
users = [generate_user() for _ in range(num_users)]

# Gerar produtos simulados
products = [generate_product() for _ in range(num_products)]

# Gerar estoque para cada produto simulado
stocks = [generate_stock(product.id, random.randint(1, 100)) for product in products]

# Gerar ordens de compra simuladas
purchase_orders = [
    generate_purchase_order(
        random.choice(users).id,
        random.choice(products).id,
        random.randint(1, 10)
    ) for _ in range(num_purchase_orders)
]

NUM_MESSAGES = 10

print("Users:")
for user in users:
    process_user_data.delay(user.__dict__)

print("\nProducts:")
for product in products:
    process_product_data.delay(product.__dict__)

print("\nStocks:")
for stock in stocks:
    process_stock_data.delay(stock.__dict__)

print("\nPurchase Orders:")
for order in purchase_orders:
    process_purchase_order_data.delay(order.__dict__)
