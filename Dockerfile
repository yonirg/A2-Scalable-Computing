# Use a imagem oficial do Python para Alpine Linux
FROM python:3.8-alpine

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

RUN echo "TEsTE"

# Copia os arquivos necessários para o diretório de trabalho
COPY requirements.txt .

# Instalações necessárias para Alpine Linux
RUN set -ex \
    && apk update \
    && apk add --no-cache postgresql-dev \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/cache/apk/* \
    && rm -rf /root/.cache \
    && find / -name "*.pyc" -exec rm -f {} \;

COPY server.py .
COPY client.py .
COPY datarepo.py .
#COPY cupom.py .
COPY mock/ ./mock/