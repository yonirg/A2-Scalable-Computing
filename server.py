#celery -A server worker --pool=solo --loglevel=info --concurrency=4
import random
import time
import os
import sqlite3
from celery import Celery
from celery.utils.log import get_task_logger
from cupom import bonificacao

app = Celery('tasks', broker='amqp://guest@localhost//', backend='rpc://',
             broker_connection_retry_on_startup=True )
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'

# Configuração do logger
logger = get_task_logger(__name__)

# Função para criar ou conectar ao banco de dados SQLite
def get_database_connection():
    db_path = 'celery_database.sqlite3'
    db_exists = os.path.exists(db_path)
    
    # Conectar ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Criar tabela se o banco de dados não existir
    if not db_exists:
        cursor.execute('''
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_type TEXT,
                data TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()
        logger.info('Criada nova tabela "tasks" no banco de dados')

    return conn

# Tarefa para processar dados do usuário e salvar no banco de dados
@app.task(delivery_mode=2)
def process_user_data(user_data):
    logger.info(f"Recebido dados do usuário: {user_data}")
    
    # Salvar dados no banco de dados
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (task_type, data, timestamp)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    ''', ('user', str(user_data)))
    conn.commit()
    conn.close()

    logger.info(f"Dados do usuário salvos no banco de dados")


# Tarefa para processar dados do produto e salvar no banco de dados
@app.task(delivery_mode=2)
def process_product_data(product_data):
    logger.info(f"Recebido dados do produto: {product_data}")
    
    # Salvar dados no banco de dados
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (task_type, data, timestamp)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    ''', ('product', str(product_data)))
    conn.commit()
    conn.close()

@app.task(delivery_mode=2)
def process_stock_data(stock_data):
    logger.info(f"Recebido dados do estoque: {stock_data}")

        # Salvar dados no banco de dados
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (task_type, data, timestamp)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    ''', ('stock', str(stock_data)))
    conn.commit()
    conn.close()

@app.task(delivery_mode=2)
def process_purchase_order_data(purchase_order_data):
    logger.info(f"Recebido dados do pedido de compra: {purchase_order_data}")

    bonificacao("purchase_order_data['user_id']")

    # Salvar dados no banco de dados
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (task_type, data, timestamp)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    ''', ('purchase', str(purchase_order_data)))
    conn.commit()
    conn.close()