"""Project pipelines."""
from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines(raise_errors=True)
    
    # Ensuring the default pipeline executes phases in the correct order
    default_pipeline = (
        pipelines.get("fase1_tablas_master", Pipeline([])) +
        pipelines.get("fase2_integracion", Pipeline([])) +
        pipelines.get("fase3_limpieza", Pipeline([])) +
        pipelines.get("fase4_feature_engineering", Pipeline([])) +
        pipelines.get("fase5_dataset_final", Pipeline([])) +
        pipelines.get("fase6_modelamiento", Pipeline([]))
    )
    pipelines["__default__"] = default_pipeline
    return pipelines
