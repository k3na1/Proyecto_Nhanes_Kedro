from kedro.pipeline import Pipeline, node
from .nodes import integrate_demolab

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=integrate_demolab,
            inputs=["demographics_master", "dietary_master", "examination_master", "laboratory_master"],
            outputs="demolab_master",
            name="integrate_demolab"
        )
    ])
