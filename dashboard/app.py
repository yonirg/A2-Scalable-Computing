import streamlit as st
import pandas as pd

def load_data():
    # Placeholder: Implement data loading
    return pd.DataFrame()

st.title("E-commerce Data Dashboard")

data = load_data()

st.write("Número de produtos comprados por minuto")
st.line_chart(data['productsBought'])

st.write("Valor faturado por minuto")
st.line_chart(data['totalRevenue'])

st.write("Número de usuários únicos visualizando cada produto por minuto")
st.line_chart(data['uniqueViewers'])

st.write("Ranking de produtos mais visualizados na última hora")
st.bar_chart(data['productRank'])

st.write("Mediana do número de vezes que um usuário visualiza um produto antes de efetuar uma compra")
st.line_chart(data['medianViewsBeforePurchase'])

st.write("Número de produtos vendidos sem disponibilidade no estoque")
st.line_chart(data['soldOutProducts'])
