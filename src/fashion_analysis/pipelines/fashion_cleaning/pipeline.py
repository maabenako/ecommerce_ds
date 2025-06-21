from kedro.pipeline import Pipeline, node, pipeline
from .nodes import limpar_parquets_em_lote

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=limpar_parquets_em_lote,
            inputs=None,
            outputs="limpeza_finalizada",  # Output fictício só pra agradar o Kedro
            name="limpar_parquets_em_lote_node"
        )
    ])

