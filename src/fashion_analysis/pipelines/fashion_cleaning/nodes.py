import pandas as pd
import glob
import os
import re

def limpar_parquets_em_lote() -> None:
    # 🧹 Encontra os arquivos na ordem correta (por número)
    arquivos = glob.glob("data/01_raw/fash_oct_parte_*.parquet")
    arquivos = sorted(arquivos, key=lambda x: int(re.search(r"parte_(\d+)", x).group(1)))

    # 🗂️ Cria pasta de saída, se necessário
    os.makedirs("data/02_intermediate/cleaned_parquets", exist_ok=True)

    for i, arquivo in enumerate(arquivos):
        print(f"🧼 Limpando {arquivo}...")

        df = pd.read_parquet(arquivo)

        # Limpeza leve
        df = df[df["price"] > 0]
        df["brand"] = df["brand"].fillna("unknown")
        df["category_code"] = df["category_code"].fillna("sem_categoria")

        # Salva parquet limpo
        output_path = f"data/02_intermediate/cleaned_parquets/cleaned_parte_{i}.parquet"
        df.to_parquet(output_path, index=False)

    print("🌟 Limpeza finalizada com sucesso!")
    return "ok"  # ← ou qualquer coisa, só pra não ser None

