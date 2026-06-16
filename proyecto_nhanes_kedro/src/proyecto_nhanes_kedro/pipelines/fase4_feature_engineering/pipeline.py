from kedro.pipeline import Pipeline, node
from .nodes import engineer_features

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=engineer_features,
            inputs="demolab_clean",
            outputs="demolab_engineered",
            name="engineer_features_demolab"
        )
    ])
