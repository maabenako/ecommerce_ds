import pandas as pd
from pathlib import Path

def gerar_parquets_a_partir_csv(caminho_csv: str) -> None:
    chunksize = 100_000
    base_path = Path(__file__).resolve().parents[4]  # chega até a raiz do projeto
    raw_path = base_path / "data" / "01_raw"

    for i, chunk in enumerate(pd.read_csv(caminho_csv, chunksize=chunksize)):
        print(f"📥 Gerando parte {i}...")
        chunk = chunk[chunk["price"] > 0]
        chunk["brand"] = chunk["brand"].fillna("unknown")
        chunk.to_parquet(raw_path / f"fash_nov_parte_{i}.parquet", index=False)

    print("✨ Parquets brutos gerados com sucesso!")
