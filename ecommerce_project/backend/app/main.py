from fastapi import FastAPI
from .routers import monitor, products, users
from ..spark import get_spark_session, process_logs, process_transactions, process_users

app = FastAPI()

app.include_router(monitor.router)
app.include_router(products.router)
app.include_router(users.router)

@app.on_event("startup")
async def startup_event():
    spark = get_spark_session()
    # Processar logs
    process_logs(spark, "/path/to/logs")
    # Processar transações
    process_transactions(spark, "/path/to/transactions")
    # Processar usuários
    process_users(spark, "/path/to/users")

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce Data Processing API"}
