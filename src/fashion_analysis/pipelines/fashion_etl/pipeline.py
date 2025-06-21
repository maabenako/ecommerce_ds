from kedro.pipeline import Pipeline, node, pipeline
from .nodes import gerar_parquets_a_partir_csv

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=gerar_parquets_a_partir_csv,
            inputs="params:caminho_csv",
            outputs=None,
            name="gerar_parquets_raw_node",
        )
    ])

