from celery import Celery
from celery.utils.log import get_task_logger

app = Celery('cupom', broker='amqp://guest@localhost//', backend='rpc://',
             broker_connection_retry_on_startup=True)
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'

logger = get_task_logger(__name__)

@app.task(delivery_mode=2)
def bonificacao(user_id):
    logger.info(f"Verificando se o usuário {user_id} deve ganhar um cupom")
    print(f"Verificando se o usuário {user_id} deve ganhar um cupom")