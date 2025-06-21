from kedro.pipeline import node, Pipeline, pipeline
from .nodes import classificar_marcas_pipeline

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=classificar_marcas_pipeline,
            inputs=None,
            outputs="marcas_classificadas",
            name="classificacao_zero_shot"
        )
    ])
