# 🛍️ Ecommerce Analysis com Kedro
Este projeto é uma pipeline robusta e modular para **análise e tratamento de dados de e-commerce**, com foco em marcas, comportamento do consumidor e inteligência de classificação. Desenvolvido com [Kedro](https://kedro.org/) e técnicas modernas de Machine Learning, ele processa grandes volumes de dados de forma eficiente e escalável.

## 💡 Objetivo

Criar uma arquitetura de dados analítica, performática e inteligente que permita:
- Processar dados brutos de eventos do e-commerce
- Limpar, enriquecer e salvar dados em parquets organizados
- Gerar métricas estatísticas para análise comportamental
- **Classificar automaticamente marcas por categoria** com zero-shot learning

---

## 🔍 Funcionalidades

### 🔹 Fatiamento e Organização de Dados
- Leitura eficiente de datasets massivos
- Salvamento em arquivos `.parquet` otimizados por lote

### 🔹 Limpeza e Enriquecimento
- Padronização e filtragem de eventos
- Extração de colunas úteis como mês, tipo de evento, preços

### 🔹 Análises Estatísticas
- Geração de métricas por cliente, marca, período e categoria
- Clusterização de clientes por poder de compra e comportamento

### 🔹 Classificação de Marcas (NLP Zero-Shot)
- Uso de modelos da Hugging Face (`facebook/bart-large-mnli`)
- Inferência inteligente de categorias sem rótulos manuais
- Resultados salvos em `.parquet` prontos para uso analítico

---

## 📦 Estrutura Kedro

```bash
fashion-analysis/
├── data/
│   ├── 01_raw/
│   ├── 02_intermediate/
│   ├── 03_primary/
│   └── 04_feature/
├── src/
│   └── fashion_analysis/
│       ├── pipelines/
│       │   ├── fashion_etl/
│       │   ├── fashion_cleaning/
│       │   ├── cluster_clientes/
│       │   └── classificar_marcas/
│       └── data_catalog.yml
├── conf/
│   └── base/
│       ├── catalog.yml
│       ├── parameters.yml
│       └── logging.yml
├── notebooks/
└── README.md
```
## 🤖 Tecnologias Utilizadas

- **Kedro**: estrutura profissional de pipelines com modularização, versionamento de dados e reprodutibilidade
- **Pandas** e **PyArrow**: para manipulação e leitura eficiente de arquivos Parquet
- **NumPy**: usado para operações vetoriais em análises e clusters
- **Scikit-learn**: para clustering de clientes com KMeans e métricas de avaliação
- **Hugging Face Transformers**: classificação inteligente de marcas por categoria via zero-shot learning
- **tqdm**: acompanhamento de progresso em loops longos
- **Matplotlib**: geração de gráficos e visualizações estatísticas
- **Jupyter Notebooks**: apoio nas análises exploratórias e validação de hipóteses
- **Python 3.12**: com ambiente virtual gerenciado por Conda

---

## 🧠 Estrutura das Pipelines

- `fashion_etl`: Fatiamento e organização de grandes arquivos em múltiplos Parquets otimizados
- `fashion_cleaning`: Limpeza de dados com remoção de ruídos, tratamento de campos ausentes e transformação de colunas
- `cluster_clientes`: Agrupamento de usuários com base em comportamento de compra, visualizações e poder aquisitivo
- `classificar_marcas`: Classificação automática de marcas usando NLP (zero-shot) para definição de categoria sem regras manuais

---

## 📊 Métricas e Análises

- Clientes únicos, tíquete médio, churn, tempo médio de carrinho, conversão por cluster
- Estatísticas descritivas para apoiar decisões de negócios
- Análise temporal dos eventos por tipo e valor de compra
- Agrupamento de sellers com base em comportamento para prospecção inteligente

---

## 📊 Dashboards Analíticos

- Visualização interativa via **Streamlit** com insights por cluster, marca e comportamento
- Análises de **LTV**, conversão, churn, tempo médio no carrinho e horário mais comum de compra
- Ranking de marcas por ação do usuário (*view*, *cart*, *purchase*)
- Previsões de compras mensais com **Prophet** e regressão por cliente + marca
- Visualização dos dados pré e pós-modelagem para apoio estratégico

---

## 📈 Potenciais Aplicações

- Segmentação de usuários e sellers para campanhas e recomendações
- Inteligência comercial por tipo de marca
- Apoio a dashboards de vendas e acompanhamento estratégico
- Priorização de leads de sellers com base em cluster de comportamento

---

## 💌 Contribuição

Este projeto é uma iniciativa independente e experimental de análise de dados com foco em e-commerce.  
Sinta-se à vontade para contribuir com melhorias, ideias ou feedbacks!

---

🚀 Feito com 💖 por uma mente analítica e criativa que transforma dados em inteligência.

---

## 👩‍💻 Author

Developed with 💙 by **Marcela Nako**  
🔗 [LinkedIn](https://www.linkedin.com/in/marcelaabe-alvim/)  
💼 [GitHub](https://github.com/maabenako?tab=repositories)

---

# Ennglish:

---
# 🛍️ Ecommerce Analysis with Kedro

This project is a robust and modular pipeline for **e-commerce data analysis and processing**, focusing on brands, consumer behavior, and intelligent classification. Built with [Kedro](https://kedro.org/) and modern Machine Learning techniques, it efficiently processes large volumes of data in a scalable architecture.

## 💡 Objective

To build an intelligent and high-performance data architecture that enables:
- Processing raw e-commerce event data  
- Cleaning, enriching, and saving structured Parquet files  
- Generating statistical metrics for behavioral analysis  
- **Automatically classifying brands by category** using zero-shot learning

---

## 🔍 Features

### 🔹 Data Slicing & Organization
- Efficient loading of massive datasets  
- Saving optimized `.parquet` files in batches

### 🔹 Cleaning & Enrichment
- Standardization and filtering of events  
- Extraction of useful columns such as month, event type, and prices

### 🔹 Statistical Analysis
- Metrics by customer, brand, period, and category  
- Clustering of clients by purchasing power and behavior

### 🔹 Brand Classification (Zero-Shot NLP)
- Leverages Hugging Face models (`facebook/bart-large-mnli`)  
- Intelligent category inference without manual labeling  
- Results saved in `.parquet` format for analytical use

---

## 📦 Kedro Structure

```bash
fashion-analysis/
├── data/
│   ├── 01_raw/
│   ├── 02_intermediate/
│   ├── 03_primary/
│   └── 04_feature/
├── src/
│   └── fashion_analysis/
│       ├── pipelines/
│       │   ├── fashion_etl/
│       │   ├── fashion_cleaning/
│       │   ├── cluster_clientes/
│       │   └── classificar_marcas/
│       └── data_catalog.yml
├── conf/
│   └── base/
│       ├── catalog.yml
│       ├── parameters.yml
│       └── logging.yml
├── notebooks/
└── README.md
```

---

## 🤖 Technologies Used

- **Kedro**: Professional pipeline framework with modularity, data versioning, and reproducibility  
- **Pandas** & **PyArrow**: For fast and efficient manipulation of Parquet files  
- **NumPy**: Used for vector operations in analysis and clustering  
- **Scikit-learn**: Customer clustering with KMeans and evaluation metrics  
- **Hugging Face Transformers**: Intelligent brand classification via zero-shot learning  
- **tqdm**: Progress tracking for long loops  
- **Matplotlib**: Visualization of statistical charts  
- **Jupyter Notebooks**: Support for exploratory analysis and hypothesis testing  
- **Python 3.12**: Environment managed with Conda

---

## 🧠 Pipeline Structure

- `fashion_etl`: Slicing and organizing large files into multiple optimized Parquet files  
- `fashion_cleaning`: Data cleaning with noise removal, missing value treatment, and column transformation  
- `cluster_clientes`: User grouping based on purchasing behavior, views, and income potential  
- `classificar_marcas`: Automated brand classification using NLP (zero-shot) for category assignment without rules

---

## 📊 Metrics & Analysis

- Unique customers, average ticket size, churn, average cart time, conversion by cluster  
- Descriptive statistics to support business decisions  
- Temporal analysis of events by type and value  
- Clustering of sellers for intelligent prospecting

---

## 📊 Analytical Dashboards

- Interactive **Streamlit** dashboard showing insights by cluster, brand, and behavior
- Analysis of **LTV**, conversion, churn, average cart time, and most common purchase time
- Brand ranking by user interaction (*view*, *cart*, *purchase*)
- Monthly purchase forecasting using **Prophet** and user+brand-level regressions
- Data visualization before and after modeling for strategic decision support

---

## 📈 Potential Applications

- User and seller segmentation for campaigns and recommendations  
- Commercial intelligence by brand type  
- Support for sales dashboards and strategic monitoring  
- Prioritization of seller leads based on behavior clusters

---

## 💌 Contribution

This is an independent and experimental data analysis project focused on e-commerce.  
Feel free to contribute with improvements, ideas, or feedback!

---

🚀 Made with 💖 by an analytical and creative mind turning data into intelligence.

---

## 👩‍💻 Author

Developed with 💙 by **Marcela Nako**  
🔗 [LinkedIn](https://www.linkedin.com/in/marcelaabe-alvim/)  
💼 [GitHub](https://github.com/maabenako?tab=repositories)
