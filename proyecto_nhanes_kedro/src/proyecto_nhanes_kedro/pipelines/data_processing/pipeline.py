from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    process_p_demo, process_p_alq, process_p_bmx, process_p_bpxo,
    process_p_diq, process_p_ghb, process_p_hdl, process_p_tchol,
    process_p_trigly, process_p_mcq, process_p_paq, process_p_slq,
    process_p_smq, process_p_biopro
)

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=process_p_demo,
                inputs="p_demo_intermediate",
                outputs="p_demo_primary",
                name="process_p_demo_node"
            ),
            node(
                func=process_p_alq,
                inputs="p_alq_intermediate",
                outputs="p_alq_primary",
                name="process_p_alq_node"
            ),
            node(
                func=process_p_bmx,
                inputs="p_bmx_intermediate",
                outputs="p_bmx_primary",
                name="process_p_bmx_node"
            ),
            node(
                func=process_p_bpxo,
                inputs="p_bpxo_intermediate",
                outputs="p_bpxo_primary",
                name="process_p_bpxo_node"
            ),
            node(
                func=process_p_diq,
                inputs="p_diq_intermediate",
                outputs="p_diq_primary",
                name="process_p_diq_node"
            ),
            node(
                func=process_p_ghb,
                inputs="p_ghb_intermediate",
                outputs="p_ghb_primary",
                name="process_p_ghb_node"
            ),
            node(
                func=process_p_hdl,
                inputs="p_hdl_intermediate",
                outputs="p_hdl_primary",
                name="process_p_hdl_node"
            ),
            node(
                func=process_p_tchol,
                inputs="p_tchol_intermediate",
                outputs="p_tchol_primary",
                name="process_p_tchol_node"
            ),
            node(
                func=process_p_trigly,
                inputs="p_trigly_intermediate",
                outputs="p_trigly_primary",
                name="process_p_trigly_node"
            ),
            node(
                func=process_p_mcq,
                inputs="p_mcq_intermediate",
                outputs="p_mcq_primary",
                name="process_p_mcq_node"
            ),
            node(
                func=process_p_paq,
                inputs="p_paq_intermediate",
                outputs="p_paq_primary",
                name="process_p_paq_node"
            ),
            node(
                func=process_p_slq,
                inputs="p_slq_intermediate",
                outputs="p_slq_primary",
                name="process_p_slq_node"
            ),
            node(
                func=process_p_smq,
                inputs="p_smq_intermediate",
                outputs="p_smq_primary",
                name="process_p_smq_node"
            ),
            node(
                func=process_p_biopro,
                inputs="p_biopro_intermediate",
                outputs="p_biopro_primary",
                name="process_p_biopro_node"
            ),
        ]
    )
