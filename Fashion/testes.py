import pandas as pd
from pathlib import Path

# Caminho até o CSV (ajuste se necessário)
caminho_csv = Path(__file__).resolve().parent / "2019-Oct.csv"

# Lê as 1000 primeiras linhas
df = pd.read_csv(caminho_csv, nrows=1000)

# Mostra as 10 primeiras linhas
print("📌 Primeiras linhas:")
print(df.head(10), "\n")

# Mostra colunas e tipos
print("🧠 Tipos de dados:")
print(df.dtypes, "\n")

# Verifica valores faltantes
print("❗ Valores faltando por coluna:")
print(df.isnull().sum(), "\n")

print("📊 Percentual de valores faltando:")
print((df.isnull().mean() * 100).round(2), "\n")

# Sugestões automáticas de tratamento
print("💡 Sugestões de tratamento:")

for coluna in df.columns:
    faltantes = df[coluna].isnull().mean()
    tipo = df[coluna].dtype

    if faltantes > 0:
        if tipo == "object":
            print(f"🔹 '{coluna}': preencher com 'unknown'")
        elif "float" in str(tipo) or "int" in str(tipo):
            print(f"🔹 '{coluna}': preencher com média ou mediana")
    else:
        print(f"✅ '{coluna}': sem valores faltantes")

print(df.info())
print(df)
print(df["event_type"].unique())



###

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Lê os dados clusterizados
df = pd.read_parquet("/home/maabe/fashion-analysis/data/07_model_output/clientes_clusterizados.parquet")

# Mostra os primeiros registros
print("📋 Prévia dos dados:")
print(df.head())

# Distribuição por cluster
print("\n👥 Quantidade de clientes por cluster:")
print(df["cluster"].value_counts())

# Estatísticas por cluster
print("\n📊 Médias por cluster:")
print(df.groupby("cluster").mean(numeric_only=True))

# Visualização
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df.sample(10000),  # reduz visualização pra não travar
    x="total_gasto",
    y="media_gasto",
    hue="cluster",
    palette="tab10"
)
plt.title("Clusterização de Clientes por Poder de Compra")
plt.xlabel("Total Gasto")
plt.ylabel("Gasto Médio")
plt.tight_layout()
plt.show()

# Ver os centroides dos clusters
print("\n📍 Centroides dos clusters (total_gasto x media_gasto):")

centroides = df.groupby("cluster")[["total_gasto", "media_gasto"]].mean().reset_index()
print(centroides)

centroides.to_csv("centroides_clusters.csv", index=False)
print("📁 Arquivo 'centroides_clusters.csv' salvo com sucesso!")


import pandas as pd
import os

# Caminho da pasta com os Parquets
pasta = "/home/maabe/fashion-analysis/data/02_intermediate/cleaned_parquets"

# Lista os arquivos
arquivos = sorted([f for f in os.listdir(pasta) if f.endswith(".parquet")])

# Carrega só o primeiro pedaço para inspecionar
df = pd.read_parquet(os.path.join(pasta, arquivos[0]))

# Mostra as colunas e os primeiros registros
print("Colunas:", df.columns.tolist())
print("\nTipos de dados:")
print(df.dtypes)

print("\nAmostra de dados:")
print(df.head())

###

# Parquet de classificação de marcas com NLP

import pandas as pd

# Caminho do arquivo
caminho = "/home/maabe/fashion-analysis/data/08_reporting/marcas_classificadas.parquet"

# Lê o Parquet
df = pd.read_parquet(caminho)

# Mostra info geral e uma amostra
print("📊 Informações do DataFrame:")
print(df.info())

print("\n🔍 Primeiras 10 linhas:")
print(df.sample(10, random_state=42))  # amostra aleatória
