"""
Pipeline 'data_ingestion' — ETL Extract.

Lee los 14 archivos .xpt crudos y produce tablas limpias en la capa intermediate.
Cada nodo limpia una tabla individual: filtra columnas, reemplaza codigos
NHANES missing, valida rangos medicos y produce un DataFrame limpio.
"""
from __future__ import annotations

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    clean_alq,
    clean_biopro,
    clean_bmx,
    clean_bpxo,
    clean_demo,
    clean_diq,
    clean_ghb,
    clean_hdl,
    clean_mcq,
    clean_paq,
    clean_slq,
    clean_smq,
    clean_tchol,
    clean_trigly,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        # --- Demografia (tabla base) ---
        node(
            func=clean_demo,
            inputs=["demo_raw", "parameters"],
            outputs="demo_clean",
            name="clean_demo_node",
            tags=["data_ingestion", "etl_extract"],
        ),
        # --- Cuestionarios ---
        node(
            func=clean_alq,
            inputs=["alq_raw", "parameters"],
            outputs="alq_clean",
            name="clean_alq_node",
            tags=["data_ingestion", "etl_extract"],
        ),
        node(
            func=clean_paq,
            inputs=["paq_raw", "parameters"],
            outputs="paq_clean",
            name="clean_paq_node",
            tags=["data_ingestion", "etl_extract"],
        ),
        node(
            func=clean_slq,
            inputs=["slq_raw", "parameters"],
            outputs="slq_clean",
            name="clean_slq_node",
            tags=["data_ingestion", "etl_extract"],
        ),
        node(
            func=clean_smq,
            inputs=["smq_raw", "parameters"],
            outputs="smq_clean",
            name="clean_smq_node",
            tags=["data_ingestion", "etl_extract"],
        ),
        node(
            func=clean_diq,
            inputs=["diq_raw", "parameters"],
            outputs="diq_clean",
            name="clean_diq_node",
            tags=["data_ingestion", "etl_extract"],
        ),
        node(
            func=clean_mcq,
            inputs=["mcq_raw", "parameters"],
            outputs="mcq_clean",
            name="clean_mcq_node",
            tags=["data_ingestion", "etl_extract"],
        ),
        # --- Examenes fisicos ---
        node(
            func=clean_bmx,
            inputs=["bmx_raw", "parameters"],
            outputs="bmx_clean",
            name="clean_bmx_node",
            tags=["data_ingestion", "etl_extract"],
        ),
        node(
            func=clean_bpxo,
            inputs=["bpxo_raw", "parameters"],
            outputs="bpxo_clean",
            name="clean_bpxo_node",
            tags=["data_ingestion", "etl_extract"],
        ),
        # --- Laboratorio ---
        node(
            func=clean_ghb,
            inputs=["ghb_raw", "parameters"],
            outputs="ghb_clean",
            name="clean_ghb_node",
            tags=["data_ingestion", "etl_extract"],
        ),
        node(
            func=clean_hdl,
            inputs=["hdl_raw", "parameters"],
            outputs="hdl_clean",
            name="clean_hdl_node",
            tags=["data_ingestion", "etl_extract"],
        ),
        node(
            func=clean_tchol,
            inputs=["tchol_raw", "parameters"],
            outputs="tchol_clean",
            name="clean_tchol_node",
            tags=["data_ingestion", "etl_extract"],
        ),
        node(
            func=clean_trigly,
            inputs=["trigly_raw", "parameters"],
            outputs="trigly_clean",
            name="clean_trigly_node",
            tags=["data_ingestion", "etl_extract"],
        ),
        node(
            func=clean_biopro,
            inputs=["biopro_raw", "parameters"],
            outputs="biopro_clean",
            name="clean_biopro_node",
            tags=["data_ingestion", "etl_extract"],
        ),
    ])
