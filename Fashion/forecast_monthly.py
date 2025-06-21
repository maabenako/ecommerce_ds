#forecast_monthly.py

import pandas as pd
import os
from pathlib import Path
from prophet import Prophet
import matplotlib.pyplot as plt

# Caminho da pasta com os parquets
pasta = Path("/home/maabe/fashion-analysis/data/02_intermediate/cleaned_parquets")
arquivos = sorted([f for f in os.listdir(pasta) if f.endswith(".parquet")])

# Lista para armazenar dados mensais
compras_mensais = []

for arquivo in arquivos:
    df = pd.read_parquet(pasta / arquivo)
    df['event_time'] = pd.to_datetime(df['event_time'], utc=True)
    compras = df[df['event_type'] == 'purchase'].copy()

    # Converte para mês (removendo timezone de forma segura)
    compras.loc[:, 'month'] = compras['event_time'].dt.tz_localize(None).dt.to_period("M").dt.to_timestamp()

    mensal = compras.groupby('month').size().reset_index(name='compras')
    compras_mensais.append(mensal)

# Concatena resultados
df_agg = pd.concat(compras_mensais).groupby('month').sum().reset_index()

# Verifica se há dados suficientes para o modelo
if df_agg.shape[0] < 2:
    print("⚠️ Dados insuficientes para previsão com Prophet. Tente rodar com mais arquivos.")
else:
    # Renomeia colunas para Prophet
    df_agg.columns = ['ds', 'y']

    # Cria e ajusta o modelo
    model = Prophet()
    model.fit(df_agg)

    # Cria datas futuras para previsão
    future = model.make_future_dataframe(periods=3, freq='M')
    forecast = model.predict(future)

    # Plota a previsão
    fig = model.plot(forecast)
    plt.title("Previsão de Compras Mensais")
    plt.xlabel("Mês")
    plt.ylabel("Compras")
    plt.tight_layout()
    plt.show()
