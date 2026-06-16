import pandas as pd
import logging

logger = logging.getLogger(__name__)

def standarize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte todas las columnas a mayúsculas para asegurar consistencia.
    Retorna el DataFrame para ser guardado como intermediate.
    """
    df.columns = df.columns.str.upper()
    logger.info(f"Estandarizadas {len(df.columns)} columnas. Shape: {df.shape}")
    return df

def build_section_master(*datasets: pd.DataFrame) -> pd.DataFrame:
    """
    Une múltiples DataFrames de una sección usando SEQN (outer merge) 
    y guarda el master en la capa primary.
    """
    master_df = None
    
    for df in datasets:
        if 'SEQN' not in df.columns:
            logger.warning("Columna clave 'SEQN' no encontrada. Saltando DataFrame.")
            continue
            
        if master_df is None:
            master_df = df
        else:
            initial_rows = master_df.shape[0]
            # Eliminar duplicados de SEQN para evitar explosión de memoria
            df_dedup = df.drop_duplicates(subset=['SEQN'])
            
            # Eliminar columnas solapadas (excepto SEQN)
            cols_to_drop = [c for c in df_dedup.columns if c in master_df.columns and c != 'SEQN']
            df_to_merge = df_dedup.drop(columns=cols_to_drop)
            
            master_df = master_df.drop_duplicates(subset=['SEQN'])
            master_df = master_df.merge(df_to_merge, on='SEQN', how='outer')
            
            if master_df.shape[0] < initial_rows:
                logger.warning("Posible pérdida de filas tras el cruce.")
                
    if master_df is not None:
        logger.info(f"MASTER CREADO | Shape Final: {master_df.shape} | SEQN Únicos: {master_df['SEQN'].nunique()}")
    else:
        logger.error("No se pudo crear el master. Faltan datos o SEQN.")
        
    return master_df
