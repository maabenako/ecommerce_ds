#forecast_user_brand.py

import pandas as pd
import os
from pathlib import Path
import re
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error

# Caminhos
pasta = Path("/home/maabe/fashion-analysis/data/02_intermediate/cleaned_parquets")
arquivos = sorted(pasta.glob("*.parquet"), key=lambda x: int(re.search(r"parte_(\d+)", str(x)).group(1)))

# Acumulador: {(user_id, brand, month): [compras, soma_price]}
acumulador = {}

for arquivo in arquivos:
    print(f"🔄 Processando {arquivo.name}")
    df = pd.read_parquet(arquivo)

    df = df[df["event_type"] == "purchase"].copy()

    df["event_time"] = pd.to_datetime(df["event_time"], utc=True)
    df["month"] = df["event_time"].dt.to_period("M").dt.to_timestamp()

    # Agrupa por user_id, brand, month
    df_agg = (
        df.groupby(["user_id", "brand", "month"])
        .agg(compras=("event_type", "count"), soma_price=("price", "sum"))
        .reset_index()
    )

    for _, row in df_agg.iterrows():
        chave = (row["user_id"], row["brand"], row["month"])
        if chave not in acumulador:
            acumulador[chave] = {"compras": 0, "soma_price": 0}
        acumulador[chave]["compras"] += row["compras"]
        acumulador[chave]["soma_price"] += row["soma_price"]

# Converte para DataFrame
compras_final = pd.DataFrame([
    (uid, brand, month, data["compras"], data["soma_price"])
    for (uid, brand, month), data in acumulador.items()
], columns=["user_id", "brand", "month", "compras", "soma_price"])

# Ordena e calcula ticket médio mensal
compras_final = compras_final.sort_values(by=["user_id", "brand", "month"])
compras_final["ticket_mensal"] = compras_final["soma_price"] / compras_final["compras"]

# Features históricas
df = compras_final.copy()
df["compras_anteriores"] = df.groupby(["user_id", "brand"])["compras"].cumsum() - df["compras"]
df["compras_futuras"] = df.groupby(["user_id", "brand"])["compras"].shift(-1)
df["meses_ativos"] = df.groupby(["user_id", "brand"])["month"].transform("count")
df["frequencia_mensal"] = df["compras_anteriores"] / (df["meses_ativos"] - 1).replace(0, 1)
df["recencia"] = df.groupby(["user_id", "brand"])["month"].rank(method="first", ascending=False)

# Ticket médio acumulado até mês anterior
df["ticket_medio"] = df.groupby(["user_id", "brand"])["ticket_mensal"].expanding().mean().reset_index(level=[0,1], drop=True)
df["ticket_medio"] = df.groupby(["user_id", "brand"])["ticket_medio"].shift(1)

# Remove últimos meses (sem target)
df_model = df.dropna(subset=["compras_futuras"])

# Salva o CSV final
output_path = "/home/maabe/fashion-analysis/data/07_model_output/user_brand_features.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df_model.to_csv(output_path, index=False)
print(f"\n✅ Arquivo salvo em: {output_path}")

# 🎯 Modelagem
features = ["compras", "compras_anteriores", "meses_ativos", "frequencia_mensal", "recencia", "ticket_medio"]
target = "compras_futuras"

X = df_model[features]
y = df_model[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
rmse = root_mean_squared_error(y_test, y_pred)
print(f"\n🧪 RMSE: {rmse:.2f}")

# 🔍 Importância das features
importances = model.feature_importances_
for feature, importance in zip(features, importances):
    print(f"{feature}: {importance:.4f}")

# 📊 Distribuição do target
plt.hist(df_model["compras_futuras"], bins=30)
plt.title("Distribuição das Compras Futuras")
plt.xlabel("Compras Futuras")
plt.ylabel("Frequência")
plt.show()

# 📈 Gráfico de importância
plt.bar(features, importances)
plt.title("Importância das Features")
plt.ylabel("Peso")
plt.xticks(rotation=45)
plt.show()
