import streamlit as st
import requests

st.title("Monitor de Preços")

meses = st.number_input("Número de meses", min_value=1, value=3)
economia_percentual = st.slider("Percentual de economia", min_value=1, max_value=100, value=20)

if st.button("Buscar"):
    response = requests.get(
        "http://localhost:8000/monitor_de_precos",
        params={"meses": meses, "economia_percentual": economia_percentual},
    )
    produtos = response.json()

    if produtos:
        st.write("Produtos com preços abaixo da média:")
        st.table(produtos)
    else:
        st.write("Nenhum produto encontrado.")
