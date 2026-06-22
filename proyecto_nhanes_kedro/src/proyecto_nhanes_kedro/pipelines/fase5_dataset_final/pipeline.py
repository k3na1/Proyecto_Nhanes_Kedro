from kedro.pipeline import Pipeline, node
from .nodes import create_diabetes_target, finalize_dataset

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=create_diabetes_target,
            inputs="demolab_engineered",
            outputs="demolab_with_target",
            name="create_target"
        ),
        node(
            func=finalize_dataset,
            inputs="demolab_with_target",
            outputs="df_master",
            name="finalize_dataset"
        )
    ])
