# dashboards.py

import streamlit as st
import pandas as pd
import plotly.express as px
import os


st.set_page_config(layout="wide", page_title="📊 Ecommerce Dashboard")

st.title("🛍️ Painel de Insights - Ecommerce Fashion")

# --- Carregando os dados ---
@st.cache_data
def load_data():
    clientes = pd.read_parquet("/home/maabe/fashion-analysis/data/07_model_output/clientes_clusterizados.parquet")
    user_brand = pd.read_csv("/home/maabe/fashion-analysis/data/07_model_output/user_brand_features.csv")
    user_monthly = pd.read_csv("/home/maabe/fashion-analysis/data/07_model_output/user_brand_monthly.csv")
    marcas = pd.read_parquet("/home/maabe/fashion-analysis/data/08_reporting/marcas_classificadas.parquet")
    return clientes, user_brand, user_monthly, marcas

clientes, user_brand, user_monthly, marcas = load_data()

# --- Aba de Clusterização ---
st.subheader("👥 Clusterização de Clientes")
col1, col2 = st.columns(2)

with col1:
    st.metric("Total de Clientes", clientes["user_id"].nunique())
    st.dataframe(clientes["cluster"].value_counts().reset_index(), use_container_width=True)

with col2:
    fig_cluster = px.histogram(clientes, x="cluster", title="Distribuição de Clientes por Cluster")
    st.plotly_chart(fig_cluster, use_container_width=True)

# --- Aba de LTV ---
st.subheader("💸 Lifetime Value (LTV)")
ltv = user_brand.groupby("user_id").agg(ltv=("compras_futuras", "sum")).reset_index()
fig_ltv = px.histogram(ltv, x="ltv", nbins=50, title="Distribuição do LTV por Usuário")
st.plotly_chart(fig_ltv, use_container_width=True)

# --- Previsão mensal (de forecast_monthly.py) ---
st.subheader("📅 Previsão de Compras Mensais")
monthly_path = "data/07_model_output/user_brand_monthly.csv"
if os.path.exists(monthly_path):
    monthly = pd.read_csv(monthly_path, parse_dates=["month"])
    fig_month = px.line(monthly, x="month", y="compras", title="Compras Mensais")
    st.plotly_chart(fig_month, use_container_width=True)
else:
    st.warning("Arquivo de previsão mensal não encontrado.")

# --- Marcas Classificadas ---
st.subheader("🏷️ Classificação de Marcas")
st.dataframe(marcas.head(10), use_container_width=True)