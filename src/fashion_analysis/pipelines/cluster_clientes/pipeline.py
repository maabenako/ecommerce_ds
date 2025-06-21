from kedro.pipeline import Pipeline, node, pipeline
from .nodes import clusterizar_clientes_por_lote

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=clusterizar_clientes_por_lote,
            inputs=None,
            outputs="clientes_clusterizados",
            name="clusterizar_clientes_por_lote_node",
        )
    ])
