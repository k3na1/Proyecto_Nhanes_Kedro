import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def create_diabetes_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea la variable objetivo DIABETES_RISK basada en criterios ADA:
    - 0 (Sin riesgo): HbA1c < 5.7% Y Glucosa < 100 mg/dL
    - 1 (Prediabetes): HbA1c 5.7-6.4% O Glucosa 100-125 mg/dL
    - 2 (Diabetes): HbA1c >= 6.5% O Glucosa >= 126 mg/dL
    """
    df = df.copy()
    df['DIABETES_RISK'] = np.nan

    hba1c = df.get('LBXGH')
    glucose = df.get('LBXGLU')

    diabetes_mask = pd.Series(False, index=df.index)
    prediabetes_mask = pd.Series(False, index=df.index)
    no_risk_mask = pd.Series(False, index=df.index)

    if hba1c is not None:
        diabetes_mask = diabetes_mask | (hba1c >= 6.5)
        prediabetes_mask = prediabetes_mask | ((hba1c >= 5.7) & (hba1c < 6.5))
        no_risk_mask = no_risk_mask | (hba1c < 5.7)

    if glucose is not None:
        diabetes_mask = diabetes_mask | (glucose >= 126)
        prediabetes_mask = prediabetes_mask | ((glucose >= 100) & (glucose < 126))
        no_risk_mask = no_risk_mask | (glucose < 100)

    # Prioridad: Diabetes > Prediabetes > Sin Riesgo
    df.loc[no_risk_mask, 'DIABETES_RISK'] = 0
    df.loc[prediabetes_mask, 'DIABETES_RISK'] = 1
    df.loc[diabetes_mask, 'DIABETES_RISK'] = 2
    df['DIABETES_RISK'] = df['DIABETES_RISK'].astype('Int64')

    labels = {0: 'Sin riesgo', 1: 'Prediabetes', 2: 'Diabetes'}
    for val, count in df['DIABETES_RISK'].value_counts().sort_index().items():
        pct = count / len(df) * 100
        logger.info(f"Target {val} ({labels.get(val)}): {count:,} ({pct:.1f}%)")

    null_count = df['DIABETES_RISK'].isna().sum()
    logger.info(f"Target NaN (sin datos suficientes): {null_count:,}")
    return df

def finalize_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina filas sin target, remueve columnas de data leakage
    y produce el df_master final listo para modelado.
    """
    df = df.copy()

    # Eliminar filas sin variable objetivo
    rows_before = len(df)
    df = df.dropna(subset=['DIABETES_RISK']).reset_index(drop=True)
    logger.info(f"Filas eliminadas sin target: {rows_before - len(df)}. Restantes: {len(df)}")

    # Eliminar columnas de data leakage (usadas para construir el target)
    leakage_cols = ['LBXGH', 'LBXGLU']
    cols_to_remove = [c for c in leakage_cols if c in df.columns]
    df = df.drop(columns=cols_to_remove)
    logger.info(f"Columnas de leakage eliminadas: {cols_to_remove}")

    logger.info(f"df_master FINAL: {df.shape} | SEQN únicos: {df['SEQN'].nunique()}")
    return df
