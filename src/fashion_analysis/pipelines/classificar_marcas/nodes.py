from transformers import pipeline
import pandas as pd
from pathlib import Path
import re
from tqdm import tqdm  # ⭐ importando tqdm

# Inicializa o modelo com BART estável
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classificar_marcas_pipeline() -> pd.DataFrame:
    pasta = Path("/home/maabe/fashion-analysis/data/02_intermediate/cleaned_parquets")
    arquivos = sorted(pasta.glob("*.parquet"), key=lambda x: int(re.search(r"parte_(\d+)", str(x)).group(1)))

    # Conjunto para evitar duplicatas
    marcas_unicas = set()

    for arquivo in arquivos:
        print(f"🔍 Lendo {arquivo.name}")
        df = pd.read_parquet(arquivo, columns=["brand"])
        marcas_validas = df["brand"].dropna().unique()
        marcas_unicas.update(marcas_validas)

    print(f"🎯 Total de marcas únicas: {len(marcas_unicas)}")

    # Categorias para classificação
    categorias = [
        "outros", "roupas", "calçados", "acessórios", "moda íntima", "moda praia", "joias",
        "maquiagem", "cabelos", "perfumaria", "cuidados com a pele",
        "medicamentos", "aparelhos médicos", "suplementos",
        "celulares", "informática", "tv e vídeo", "áudio", "eletrodomésticos",
        "papelaria", "brinquedos", "presentes", "automotivo",
        "alimentos", "bebidas alcoólicas", "bebidas não alcoólicas",
        "pet shop", "livros", "decoração", "esporte", "ferramentas"
    ]

    resultado = []

    # 🔁 tqdm para acompanhar o progresso
    for marca in tqdm(marcas_unicas, desc="🧠 Classificando marcas"):
        try:
            pred = classifier(marca, categorias, hypothesis_template="This brand is about {}.")
            categoria = pred["labels"][0]
            resultado.append({"brand": marca, "categoria": categoria})
        except Exception as e:
            print(f"⚠️ Erro ao classificar '{marca}': {e}")

    return pd.DataFrame(resultado)
