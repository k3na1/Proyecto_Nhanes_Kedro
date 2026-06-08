from kedro.pipeline import Pipeline, node, pipeline
from .nodes import convert_to_parquet

def create_pipeline(**kwargs) -> Pipeline:
    datasets = [
        "p_alq", "p_biopro", "p_bmx", "p_bpxo", "p_demo", "p_diq",
        "p_ghb", "p_hdl", "p_mcq", "p_paq", "p_slq", "p_smq",
        "p_tchol", "p_trigly"
    ]
    
    nodes = []
    for ds in datasets:
        nodes.append(
            node(
                func=convert_to_parquet,
                inputs=f"{ds}_raw",
                outputs=f"{ds}_intermediate",
                name=f"convert_{ds}_to_parquet"
            )
        )
    nodes.append(
        node(
            func=convert_to_parquet,
            inputs="p_mort_raw",
            outputs="p_mort_intermediate",
            name="convert_p_mort_node"
        )
    )
        
    return pipeline(nodes)
