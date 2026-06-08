from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    clean_demo, engineer_alq, engineer_bmx, engineer_bpxo,
    engineer_diq, engineer_mcq, engineer_paq, engineer_slq,
    engineer_smq, engineer_ghb, engineer_hdl, engineer_tchol,
    engineer_trigly, engineer_biopro, create_model_input
)

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=clean_demo,
                inputs="p_demo_primary",
                outputs="f_demo",
                name="clean_demo_node"
            ),
            node(
                func=engineer_alq,
                inputs=["p_alq_primary", "f_demo"],
                outputs="f_alq",
                name="engineer_alq_node"
            ),
            node(
                func=engineer_bmx,
                inputs=["p_bmx_primary", "f_demo"],
                outputs="f_bmx",
                name="engineer_bmx_node"
            ),
            node(
                func=engineer_bpxo,
                inputs=["p_bpxo_primary", "f_demo"],
                outputs="f_bpxo",
                name="engineer_bpxo_node"
            ),
            node(
                func=engineer_diq,
                inputs=["p_diq_primary", "f_demo"],
                outputs="f_diq",
                name="engineer_diq_node"
            ),
            node(
                func=engineer_mcq,
                inputs=["p_mcq_primary", "f_demo"],
                outputs="f_mcq",
                name="engineer_mcq_node"
            ),
            node(
                func=engineer_paq,
                inputs=["p_paq_primary", "f_demo"],
                outputs="f_paq",
                name="engineer_paq_node"
            ),
            node(
                func=engineer_slq,
                inputs=["p_slq_primary", "f_demo"],
                outputs="f_slq",
                name="engineer_slq_node"
            ),
            node(
                func=engineer_smq,
                inputs=["p_smq_primary", "f_demo"],
                outputs="f_smq",
                name="engineer_smq_node"
            ),
            node(
                func=engineer_ghb,
                inputs=["p_ghb_primary", "f_demo"],
                outputs="f_ghb",
                name="engineer_ghb_node"
            ),
            node(
                func=engineer_hdl,
                inputs=["p_hdl_primary", "f_demo"],
                outputs="f_hdl",
                name="engineer_hdl_node"
            ),
            node(
                func=engineer_tchol,
                inputs=["p_tchol_primary", "f_demo"],
                outputs="f_tchol",
                name="engineer_tchol_node"
            ),
            node(
                func=engineer_trigly,
                inputs=["p_trigly_primary", "f_demo"],
                outputs="f_trigly",
                name="engineer_trigly_node"
            ),
            node(
                func=engineer_biopro,
                inputs=["p_biopro_primary", "f_demo"],
                outputs="f_biopro",
                name="engineer_biopro_node"
            ),
            node(
                func=create_model_input,
                inputs=[
                    "f_demo", "f_alq", "f_bmx", "f_bpxo", "f_diq",
                    "f_mcq", "f_paq", "f_slq", "f_smq", "f_ghb",
                    "f_hdl", "f_tchol", "f_trigly", "f_biopro",
                    "p_mort_primary"
                ],
                outputs="model_input",
                name="create_model_input_node"
            ),
        ]
    )
