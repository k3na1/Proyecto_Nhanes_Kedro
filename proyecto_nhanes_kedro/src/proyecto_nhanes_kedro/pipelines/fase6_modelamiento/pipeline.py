from kedro.pipeline import Pipeline, node, pipeline
from .nodes import train_hierarchical_model

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=train_hierarchical_model,
                inputs=["df_master", "params:model_params"],
                outputs="diabetes_web_model",
                name="train_hierarchical_model_node",
            )
        ]
    )
