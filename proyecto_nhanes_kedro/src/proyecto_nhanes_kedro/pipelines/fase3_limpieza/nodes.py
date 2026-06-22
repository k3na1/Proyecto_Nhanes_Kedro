"""Nodos de limpieza para FASE 3: Tratamiento de nulos y valores especiales NHANES."""
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Valores especiales NHANES: Refused (77, 777, ...) y Don't Know (99, 999, ...)
NHANES_SPECIAL_VALUES = [77, 99, 777, 999, 7777, 9999, 77777, 99999]

def recode_nhanes_special_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    exclude_prefixes = ['SEQN', 'WT', 'SDM']
    cols_to_check = [c for c in numeric_cols if not any(c.startswith(p) for p in exclude_prefixes)]

    total_replaced = 0
    for col in cols_to_check:
        mask = df[col].isin(NHANES_SPECIAL_VALUES)
        count = mask.sum()
        if count > 0:
            total_replaced += count
            df.loc[mask, col] = np.nan

    logger.info(f"Recodificación NHANES: {total_replaced:,} valores especiales convertidos a NaN.")
    return df

def drop_high_null_columns(df: pd.DataFrame, threshold: float = 0.50) -> pd.DataFrame:
    df = df.copy()
    null_pct = df.isnull().mean()
    cols_to_drop = null_pct[null_pct > threshold].index.tolist()
    cols_to_drop = [c for c in cols_to_drop if c != 'SEQN']

    logger.info(
        f"Eliminación columnas: {len(cols_to_drop)} columnas con >{threshold*100:.0f}% nulos. "
        f"Antes: {len(df.columns)} -> Después: {len(df.columns) - len(cols_to_drop)}"
    )
    return df.drop(columns=cols_to_drop)

def drop_high_null_rows(df: pd.DataFrame, threshold: float = 0.70) -> pd.DataFrame:
    df = df.copy()
    null_pct_per_row = df.isnull().mean(axis=1)
    rows_to_drop = null_pct_per_row[null_pct_per_row > threshold].index

    logger.info(
        f"Eliminación filas: {len(rows_to_drop)} filas con >{threshold*100:.0f}% nulos. "
        f"Antes: {len(df)} -> Después: {len(df) - len(rows_to_drop)}"
    )
    return df.drop(index=rows_to_drop).reset_index(drop=True)

def drop_low_variance_columns(df: pd.DataFrame, threshold: float = 0.99) -> pd.DataFrame:
    df = df.copy()
    cols_to_drop = []
    for col in df.columns:
        if col == 'SEQN':
            continue
        top_freq = df[col].value_counts(normalize=True, dropna=True)
        if len(top_freq) > 0 and top_freq.iloc[0] >= threshold:
            cols_to_drop.append(col)

    logger.info(
        f"Eliminación baja varianza: {len(cols_to_drop)} columnas constantes/casi-constantes. "
        f"Restantes: {len(df.columns) - len(cols_to_drop)}"
    )
    return df.drop(columns=cols_to_drop)
