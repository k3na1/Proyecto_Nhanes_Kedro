import pandas as pd
import logging

logger = logging.getLogger(__name__)

def integrate_demolab(
    demographics_df: pd.DataFrame,
    dietary_df: pd.DataFrame,
    examination_df: pd.DataFrame,
    laboratory_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Une las tablas maestras de las distintas secciones en un único archivo consolidado.
    La tabla de demografía actúa como la base (manda).
    """
    logger.info("Iniciando integración de Phase 2: DemoLab_Master")
    
    # 1. Base = Demographics
    df_base = demographics_df.drop_duplicates(subset=['SEQN'])
    logger.info(f"Base Demographics: {df_base.shape}")
    
    # 2. Join Laboratory
    lab_dedup = laboratory_df.drop_duplicates(subset=['SEQN'])
    cols_to_drop = [c for c in lab_dedup.columns if c in df_base.columns and c != 'SEQN']
    lab_to_merge = lab_dedup.drop(columns=cols_to_drop)
    df_base = df_base.merge(lab_to_merge, on='SEQN', how='left')
    logger.info(f"Tras Laboratory: {df_base.shape}")
    
    # 3. Join Examination
    exam_dedup = examination_df.drop_duplicates(subset=['SEQN'])
    cols_to_drop = [c for c in exam_dedup.columns if c in df_base.columns and c != 'SEQN']
    exam_to_merge = exam_dedup.drop(columns=cols_to_drop)
    df_base = df_base.merge(exam_to_merge, on='SEQN', how='left')
    logger.info(f"Tras Examination: {df_base.shape}")
    
    # 4. Join Dietary
    diet_dedup = dietary_df.drop_duplicates(subset=['SEQN'])
    cols_to_drop = [c for c in diet_dedup.columns if c in df_base.columns and c != 'SEQN']
    diet_to_merge = diet_dedup.drop(columns=cols_to_drop)
    df_base = df_base.merge(diet_to_merge, on='SEQN', how='left')
    logger.info(f"Tras Dietary: {df_base.shape}")
    
    logger.info(f"Integración completada. Shape final: {df_base.shape}")
    return df_base
