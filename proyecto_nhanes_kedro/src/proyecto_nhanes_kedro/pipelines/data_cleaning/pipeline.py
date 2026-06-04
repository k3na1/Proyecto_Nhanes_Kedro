"""
Pipeline 'data_cleaning'.

Lee los 12 archivos .parquet de data/03_primary, los limpia
individualmente, los une en una master table, trata los NaN
y produce una tabla final con 0 valores nulos.

Nodos:
  1-12. Limpieza individual por tabla (12 nodos paralelos)
  13.   Crear master table (LEFT JOIN por SEQN)
  14.   Tratar nulos (estructurales + adultos + imputacion + residuales)
"""
from __future__ import annotations

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    crear_master_table,
    limpiar_alq,
    limpiar_biopro,
    limpiar_bmx,
    limpiar_bpxo,
    limpiar_diq,
    limpiar_demo,
    limpiar_ghb,
    limpiar_hdl,
    limpiar_mcq,
    limpiar_paq,
    limpiar_slq,
    limpiar_smq,
    tratar_nulos,
)


def create_pipeline(**kwargs) -> Pipeline:
    # --- Nodos de limpieza individual (12 tablas) ---
    cleaning_nodes = [
        node(
            func=limpiar_demo,
            inputs="p_demo_primary",
            outputs="demo_cleaned",
            name="limpiar_demo_node",
        ),
        node(
            func=limpiar_alq,
            inputs="p_alq_primary",
            outputs="alq_cleaned",
            name="limpiar_alq_node",
        ),
        node(
            func=limpiar_bmx,
            inputs="p_bmx_primary",
            outputs="bmx_cleaned",
            name="limpiar_bmx_node",
        ),
        node(
            func=limpiar_bpxo,
            inputs="p_bpxo_primary",
            outputs="bpxo_cleaned",
            name="limpiar_bpxo_node",
        ),
        node(
            func=limpiar_diq,
            inputs="p_diq_primary",
            outputs="diq_cleaned",
            name="limpiar_diq_node",
        ),
        node(
            func=limpiar_ghb,
            inputs="p_ghb_primary",
            outputs="ghb_cleaned",
            name="limpiar_ghb_node",
        ),
        node(
            func=limpiar_hdl,
            inputs="p_hdl_primary",
            outputs="hdl_cleaned",
            name="limpiar_hdl_node",
        ),
        node(
            func=limpiar_mcq,
            inputs="p_mcq_primary",
            outputs="mcq_cleaned",
            name="limpiar_mcq_node",
        ),
        node(
            func=limpiar_paq,
            inputs="p_paq_primary",
            outputs="paq_cleaned",
            name="limpiar_paq_node",
        ),
        node(
            func=limpiar_slq,
            inputs="p_slq_primary",
            outputs="slq_cleaned",
            name="limpiar_slq_node",
        ),
        node(
            func=limpiar_smq,
            inputs="p_smq_primary",
            outputs="smq_cleaned",
            name="limpiar_smq_node",
        ),
        node(
            func=limpiar_biopro,
            inputs="p_biopro_primary",
            outputs="biopro_cleaned",
            name="limpiar_biopro_node",
        ),
    ]

    # --- Nodo de union en master table ---
    merge_node = node(
        func=crear_master_table,
        inputs=[
            "demo_cleaned",
            "alq_cleaned",
            "bmx_cleaned",
            "bpxo_cleaned",
            "diq_cleaned",
            "ghb_cleaned",
            "hdl_cleaned",
            "mcq_cleaned",
            "paq_cleaned",
            "slq_cleaned",
            "smq_cleaned",
            "biopro_cleaned",
        ],
        outputs="master_table_raw",
        name="crear_master_table_node",
    )

    # --- Nodo de tratamiento de NaN ---
    nan_node = node(
        func=tratar_nulos,
        inputs="master_table_raw",
        outputs="master_table_clean",
        name="tratar_nulos_node",
    )

    return pipeline(cleaning_nodes + [merge_node, nan_node])
