from mock.models import generate_user, generate_product, generate_stock, generate_purchase_order, generate_store, generate_purchase_order_recent
from server import process_user_data, process_product_data, process_store_data, process_stock_data, process_purchase_order_data
from concurrent.futures import ThreadPoolExecutor
import random
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType
from pyspark.sql.functions import lit
import sqlite3
import os


diretorio = 'mock\\mock_files\\sqlite3'

arquivos = [
    'users.sqlite3',
    'products.sqlite3',
    'store.sqlite3',
    'stock.sqlite3',
    'purchase_orders.sqlite3'
]

tabelas = ['user', 'product', 'store', 'stock', 'purchase_order']

def executar_consulta(database_file, query):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute(query)
    
    # Obtém os nomes das colunas
    colunas = [desc[0] for desc in cursor.description]
    
    # Obtém os resultados como lista de dicionários
    resultados = []
    for linha in cursor.fetchall():
        resultado_dict = dict(zip(colunas, linha))
        resultados.append(resultado_dict)
    
    conn.close()
    return resultados

def process(process_name, data):
    print(process_name)
    for row in data:
        row_json = json.dumps(row.__dict__)
        process_user_data.delay()    

def process_users(users):
    print("Users:")
    for user in users:
        dados = json.dumps(user)
        process_user_data.delay(dados)

def process_products(products):
    print("\nProducts:")
    for product in products:
        dados = json.dumps(product)
        process_product_data.delay(dados)

def process_stores(stores):
    print("\nLojas:")
    for store in stores:
        dados = json.dumps(store) 
        process_store_data.delay(dados)

def process_stocks(stocks):
    print("\nStocks:")
    for stock in stocks:
        dados = json.dumps(stock)
        process_stock_data.delay(dados)

def process_purchase_orders(purchase_orders):
    print("\nPurchase Orders:")
    for order in purchase_orders:
        dados = json.dumps(order)
        process_purchase_order_data.delay(dados)

# Inicia uma sessão Spark
# spark = SparkSession.builder \
#     .appName("ContaVerde") \
#     .master("local[*]") \
#     .getOrCreate()

for index, arquivo in enumerate(arquivos):
    caminho_arquivo = os.path.join(diretorio, arquivo)
    consulta_sql = f'SELECT * FROM {tabelas[index]};'
    resultados = executar_consulta(caminho_arquivo, consulta_sql)
    if index == 0:
        process_users(resultados)
    elif index == 1:
        process_products(resultados)
    elif index == 2:
        process_stores(resultados)
    elif index == 3:
        process_stocks(resultados)
    elif index == 4:
        process_purchase_orders(resultados)