#celery -A server worker --pool=solo --loglevel=info --concurrency=4
from celery import Celery
from celery.utils.log import get_task_logger
from datarepo import *
from cupom import bonificacao
import json

app = Celery('tasks', broker='amqp://guest@localhost//', backend='rpc://',
             broker_connection_retry_on_startup=True )
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'

# Configuração do logger
logger = get_task_logger(__name__)

@app.task(delivery_mode=2)
def process_click_data(click_data_json):
    click_data = json.loads(click_data_json)
    logger.info(f"Recebido dados de click: {click_data}")

@app.task(delivery_mode=2)
def process_zoom_data(zoom_data_json):
    zoom_data = json.loads(zoom_data_json)
    logger.info(f"Recebido dados de click: {zoom_data}")

@app.task(delivery_mode=2)
def process_scrolling_data(scrolling_data_json):
    scrolling_data = json.loads(scrolling_data_json)
    logger.info(f"Recebido dados de click: {scrolling_data}")

# Tarefa para processar dados do usuário e salvar no banco de dados
@app.task(delivery_mode=2)
def process_user_data(user_data_json):
    user_data = json.loads(user_data_json)
    logger.info(f"Recebido dados do usuário: {user_data}")
    get_database_connection('user', user_data)
    logger.info(f"Dados do usuário salvos no banco de dados")


# Tarefa para processar dados do produto e salvar no banco de dados
@app.task(delivery_mode=2)
def process_product_data(product_data_json):
    product_data = json.loads(product_data_json)
    logger.info(f"Recebido dados do produto: {product_data}")
    get_database_connection('product', product_data)

@app.task(delivery_mode=2)
def process_store_data(store_data_json):
    store_data = json.loads(store_data_json)
    logger.info(f"Recebido dados da loja: {store_data}")
    get_database_connection('store', store_data)

@app.task(delivery_mode=2)
def process_stock_data(stock_data_json):
    stock_data = json.loads(stock_data_json)
    logger.info(f"Recebido dados do estoque: {stock_data}")
    get_database_connection('stock', stock_data)

@app.task(delivery_mode=2)
def process_purchase_order_data(purchase_order_data_json):
    purchase_order_data = json.loads(purchase_order_data_json)    
    logger.info(f"Recebido dados do pedido de compra: {purchase_order_data}")
    #bonificacao("purchase_order_data['user_id']")
    get_database_connection('purchase_order', purchase_order_data)