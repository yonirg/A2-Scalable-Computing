# E-commerce Data Processing Project

## Estrutura do Projeto

- **backend/**: Contém a aplicação backend desenvolvida com FastAPI.
  - **app/**: Aplicação principal do backend.
    - **routers/**: Define as rotas da API.
    - **models/**: Define os modelos de dados.
  - **spark/**: Scripts para processamento distribuído de dados utilizando Apache Spark.
  - **database/**: Configuração do banco de dados e modelos SQLAlchemy.
  - **requirements.txt**: Dependências do backend.
- **frontend/**: Contém a aplicação frontend desenvolvida com Streamlit.
  - **app.py**: Interface do usuário para monitorar os preços.
  - **requirements.txt**: Dependências do frontend.
