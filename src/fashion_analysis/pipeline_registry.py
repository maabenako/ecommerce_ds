from kedro.pipeline import Pipeline
from fashion_analysis.pipelines import fashion_cleaning as fc
from fashion_analysis.pipelines import cluster_clientes as cc
from fashion_analysis.pipelines import classificar_marcas as classificar_marcas_pipeline

def register_pipelines() -> dict[str, Pipeline]:
    return {
        "__default__": fc.create_pipeline() + cc.create_pipeline() + classificar_marcas_pipeline.create_pipeline(),
        "fashion_cleaning": fc.create_pipeline(),
        "cluster_clientes": cc.create_pipeline(),
        "classificar_marcas": classificar_marcas_pipeline.create_pipeline(),
    }
