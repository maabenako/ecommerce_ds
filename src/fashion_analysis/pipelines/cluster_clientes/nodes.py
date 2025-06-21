import pandas as pd
import glob
import re
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def clusterizar_clientes_por_lote() -> pd.DataFrame:
    arquivos = glob.glob("data/02_intermediate/cleaned_parquets/cleaned_parte_*.parquet")
    arquivos = sorted(
        arquivos,
        key=lambda x: int(re.search(r"cleaned_parte_(\d+)", x).group(1))
    )

    print(f"🔍 Lendo {len(arquivos)} arquivos limpos...")

    resultados = []

    for arquivo in arquivos:
        print(f"📥 Processando {arquivo}...")

        df = pd.read_parquet(arquivo)

        agrupado = (
            df.groupby("user_id")
            .agg(
                total_gasto=("price", "sum"),
                media_gasto=("price", "mean"),
                num_eventos=("event_type", "count"),
                num_compras=("event_type", lambda x: (x == "purchase").sum()),
                num_carrinhos=("event_type", lambda x: (x == "cart").sum()),
                num_visualizacoes=("event_type", lambda x: (x == "view").sum()),
            )
            .reset_index()
        )

        resultados.append(agrupado)

    # Junta todos os resultados (já agregados)
    todos_clientes = pd.concat(resultados, ignore_index=True)

    # Agrupa novamente, somando dados dos mesmos user_ids que apareceram em arquivos diferentes
    clientes_final = (
        todos_clientes.groupby("user_id")
        .agg({
            "total_gasto": "sum",
            "media_gasto": "mean",
            "num_eventos": "sum",
            "num_compras": "sum",
            "num_carrinhos": "sum",
            "num_visualizacoes": "sum"
        })
        .reset_index()
    )

    print(f"👥 Clientes únicos: {len(clientes_final)}")

    # Normaliza e clusteriza
    scaler = StandardScaler()
    X = scaler.fit_transform(clientes_final.drop(columns=["user_id"]))

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X)

    clientes_final["cluster"] = clusters

    print("✅ Clusterização finalizada com sucesso!")
    return clientes_final
