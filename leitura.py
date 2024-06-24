from pyspark.sql import SparkSession
from pyspark.sql.functions import to_json, struct
import os
from server import *
import time

def listar_arquivos(diretorio):
    # Lista para armazenar os caminhos dos arquivos
    arquivos = []
    
    # Percorre o diretório e subdiretórios
    for raiz, dirs, files in os.walk(diretorio):
        for file in files:
            # Adiciona o caminho completo do arquivo à lista
            arquivos.append(os.path.join(raiz, file))
    
    return arquivos

diretorio = 'mock/mock_files/log/'
arquivos = listar_arquivos(diretorio)

spark = SparkSession.builder \
    .appName("DataCat") \
    .master("local[*]") \
    .getOrCreate()
start_time = time.time()
for path in arquivos:
    # Ler todos os arquivos de log do diretório
    df = spark.read.option("delimiter", ";").csv(path, header=True, inferSchema=True)

    for extra_1 in ["SCROLLING", "ZOOM", "CLICK"]:

        df_extra_1 = df.filter(df['extra_1'] == extra_1)

        json_rdd = df_extra_1.toJSON()

        # Coleta os dados JSON para uma lista no driver (opcional)
        json_list = json_rdd.collect()

        # Mostra os primeiros 5 itens da lista
        for json_data in json_list:
            if extra_1 == "SCROLLING":
                process_scrolling_data.delay(json_data)
            elif extra_1 == "ZOOM":
                process_zoom_data.delay(json_data)
            elif extra_1 == "CLICK":
                process_click_data.delay(json_data)

# Parar a SparkSession
spark.stop()

end_time = time.time() - start_time
print(f"Tempo de operação: {end_time} segundos")