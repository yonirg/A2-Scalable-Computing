from fastapi import APIRouter, Query
from typing import List
from ..models.product import Product
from ..spark import get_spark_session

router = APIRouter()

@router.get("/monitor_de_precos", response_model=List[Product])
def monitor_de_precos(meses: int = Query(...), economia_percentual: float = Query(...)):
    spark = get_spark_session()
    produtos = buscar_produtos_com_preco_abaixo_da_media(spark, meses, economia_percentual)
    return produtos

def buscar_produtos_com_preco_abaixo_da_media(spark, meses: int, economia_percentual: float):
    df = spark.sql(f"""
        SELECT nome, preco_atual, economia_percentual
        FROM produtos
        WHERE economia_percentual >= {economia_percentual}
        AND data >= DATE_SUB(CURRENT_DATE, {meses} * 30)
    """)
    
    produtos = [Product(nome=row["nome"], preco_atual=row["preco_atual"], economia_percentual=row["economia_percentual"]) for row in df.collect()]
    return produtos
