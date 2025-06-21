#analytics.py

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy.stats import pearsonr

# Caminho da pasta com os parquets
pasta = Path("/home/maabe/fashion-analysis/data/02_intermediate/cleaned_parquets")
arquivos = sorted([f for f in os.listdir(pasta) if f.endswith(".parquet")])

# Carrega os clusters dos clientes
clientes = pd.read_parquet("/home/maabe/fashion-analysis/data/07_model_output/clientes_clusterizados.parquet")

# Inicializa listas para resultados
horarios_compras = []
usuarios_cart = set()
usuarios_purchase = set()
tempos_cart_purchase = []
precos = []
clusters = []
marcas_view = []
marcas_cart = []
marcas_purchase = []

for arquivo in arquivos:
    df = pd.read_parquet(pasta / arquivo)
    df['event_time'] = pd.to_datetime(df['event_time'], utc=True)
    df['hora'] = df['event_time'].dt.hour
    df = df.merge(clientes[['user_id', 'cluster']], on='user_id', how='left')

    purchases = df[df['event_type'] == 'purchase']
    carts = df[df['event_type'] == 'cart']
    views = df[df['event_type'] == 'view']

    horarios_compras.append(purchases[['user_id', 'hora', 'cluster']])

    merged = pd.merge(
        carts,
        purchases,
        on=['user_id', 'product_id'],
        suffixes=('_cart', '_purchase')
    )
    merged['tempo_entre_cart_e_compra'] = merged['event_time_purchase'] - merged['event_time_cart']
    merged = merged[merged['tempo_entre_cart_e_compra'] > pd.Timedelta(0)]

    usuarios_cart.update(carts['user_id'].unique())
    usuarios_purchase.update(merged['user_id'].unique())
    tempos_cart_purchase.extend(merged['tempo_entre_cart_e_compra'].dt.total_seconds().tolist())
    precos.extend(merged['price_cart'].tolist())
    clusters.extend(merged['cluster_cart'].tolist())

    marcas_view.append(views.groupby(['cluster', 'brand']).size().reset_index(name='views'))
    marcas_cart.append(carts.groupby(['cluster', 'brand']).size().reset_index(name='cart'))
    marcas_purchase.append(purchases.groupby(['cluster', 'brand']).size().reset_index(name='purchase'))

horarios_df = pd.concat(horarios_compras)
hora_mais_comum = horarios_df.groupby('cluster')['hora'].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan)
print("\n🕒 Horário mais comum de compra por cluster:")
print(hora_mais_comum)

taxa_conversao = (len(usuarios_purchase) / len(usuarios_cart)) * 100 if usuarios_cart else 0
print(f"\n🛒 Taxa de conversão do carrinho: {taxa_conversao:.2f}%")

tempo_medio_compra = pd.to_timedelta(np.mean(tempos_cart_purchase), unit='s') if tempos_cart_purchase else pd.Timedelta(0)
print(f"⏱️ Tempo médio até a compra: {tempo_medio_compra}")

churn_users = usuarios_cart - usuarios_purchase
tempo_medio_churn = pd.Timedelta(minutes=30) if churn_users else pd.Timedelta(0)
print(f"\n❌ Tempo médio no carrinho dos churns (estimado): {tempo_medio_churn}")

if tempos_cart_purchase and precos:
    corr, pval = pearsonr(tempos_cart_purchase, precos)
    print("\n📈 Correlação entre tempo no carrinho e preço do item:")
    print(f"Correlação de Pearson: {corr:.4f} (p-valor: {pval:.4f})")

    plt.figure(figsize=(8, 5))
    sns.scatterplot(x=tempos_cart_purchase, y=precos, hue=clusters, alpha=0.6)
    plt.title("Tempo entre Cart e Compra vs. Preço do Produto")
    plt.xlabel("Tempo no Carrinho (segundos)")
    plt.ylabel("Preço do Produto")
    plt.tight_layout()
    plt.show()
else:
    print("\n⚠️ Dados insuficientes para correlação tempo x preço.")

view_df = pd.concat(marcas_view)
cart_df = pd.concat(marcas_cart)
purchase_df = pd.concat(marcas_purchase)

view_df = view_df[view_df['brand'].str.lower() != 'unknown']
cart_df = cart_df[cart_df['brand'].str.lower() != 'unknown']
purchase_df = purchase_df[purchase_df['brand'].str.lower() != 'unknown']

view_df = view_df.groupby(['cluster', 'brand']).sum().reset_index()
cart_df = cart_df.groupby(['cluster', 'brand']).sum().reset_index()
purchase_df = purchase_df.groupby(['cluster', 'brand']).sum().reset_index()

print("\n👁️ Marcas mais vistas por cluster:")
print(view_df.sort_values(by='views', ascending=False).groupby('cluster').head(5))

print("\n🛒 Marcas mais adicionadas ao carrinho por cluster:")
print(cart_df.sort_values(by='cart', ascending=False).groupby('cluster').head(5))

print("\n✅ Marcas mais compradas por cluster:")
print(purchase_df.sort_values(by='purchase', ascending=False).groupby('cluster').head(5))

# --- 6. LTV por user_id + brand e média por cluster ---

print("\n💸 Calculando LTV por cliente + marca...")

ltv_parcial = []

for arquivo in arquivos:
    df = pd.read_parquet(pasta / arquivo, columns=['user_id', 'brand', 'event_type', 'price'])
    df = df[df["event_type"] == "purchase"]
    df = df[df["brand"].str.lower() != "unknown"]

    df = df.merge(clientes[['user_id', 'cluster']], on='user_id', how='left')

    ltv_agg = df.groupby(["user_id", "brand"]).agg(
        total_compras=('event_type', 'count'),
        ticket_medio=('price', 'mean'),
        cluster=('cluster', 'first')
    ).reset_index()

    ltv_agg["ltv"] = ltv_agg["total_compras"] * ltv_agg["ticket_medio"]
    ltv_parcial.append(ltv_agg)

ltv_agrupado = pd.concat(ltv_parcial, ignore_index=True)

ltv_agrupado = ltv_agrupado.groupby(["user_id", "brand", "cluster"], as_index=False).agg(
    total_compras=('total_compras', 'sum'),
    ticket_medio=('ticket_medio', 'mean'),
    ltv=('ltv', 'sum')
)

ltv_cluster = ltv_agrupado.groupby("cluster")["ltv"].mean().reset_index(name="ltv_medio_cluster")

print("\n💰 Top 5 maiores LTVs por cluster:")
for cluster_id, grupo in ltv_agrupado.groupby("cluster"):
    top = grupo.sort_values(by="ltv", ascending=False).head(5)
    print(f"\nCluster {cluster_id}:")
    print(top[["user_id", "brand", "ltv"]])

print("\n📊 LTV médio por cluster:")
print(ltv_cluster)
