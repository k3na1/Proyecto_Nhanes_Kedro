import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Crea variables derivadas con relevancia clínica para predicción de diabetes."""
    df = df.copy()

    # 1. HOMA-IR (resistencia a la insulina)
    if 'LBXGLU' in df.columns and 'LBXIN' in df.columns:
        df['HOMA_IR'] = (df['LBXGLU'] * df['LBXIN']) / 405
        logger.info(f"HOMA_IR creado. Mediana: {df.get('HOMA_IR').median():.2f}")

    # 2. Ratio Cintura/Estatura
    if 'BMXWAIST' in df.columns and 'BMXHT' in df.columns:
        df['WAIST_HEIGHT_RATIO'] = df['BMXWAIST'] / df['BMXHT']
        logger.info(f"WAIST_HEIGHT_RATIO creado. Mediana: {df.get('WAIST_HEIGHT_RATIO').median():.3f}")

    # 3. Presión Arterial Media (MAP)
    sys_cols = [c for c in ['BPXOSY1', 'BPXOSY2', 'BPXOSY3'] if c in df.columns]
    dia_cols = [c for c in ['BPXODI1', 'BPXODI2', 'BPXODI3'] if c in df.columns]
    if sys_cols and dia_cols:
        df['BP_SYSTOLIC_AVG'] = df[sys_cols].mean(axis=1)
        df['BP_DIASTOLIC_AVG'] = df[dia_cols].mean(axis=1)
        df['MAP'] = df['BP_DIASTOLIC_AVG'] + (1 / 3) * (df['BP_SYSTOLIC_AVG'] - df['BP_DIASTOLIC_AVG'])
        logger.info(f"MAP creado. Mediana: {df.get('MAP').median():.1f}")

    # 4. Categoría de IMC
    if 'BMXBMI' in df.columns:
        df['BMI_CATEGORY'] = pd.cut(
            df['BMXBMI'],
            bins=[0, 18.5, 25, 30, 35, 40, 100],
            labels=[0, 1, 2, 3, 4, 5],
        ).astype('Int64')
        logger.info("BMI_CATEGORY creado.")

    # 5. Ratio Triglicéridos / HDL
    if 'LBXTR' in df.columns and 'LBDHDD' in df.columns:
        df['TG_HDL_RATIO'] = df['LBXTR'] / df['LBDHDD']
        logger.info(f"TG_HDL_RATIO creado. Mediana: {df.get('TG_HDL_RATIO').median():.2f}")

    # 6. Ratio Albúmina/Creatinina Urinaria (ACR)
    if 'URXUMA' in df.columns and 'URXUCR' in df.columns:
        df['ACR'] = (df['URXUMA'] / df['URXUCR']) * 100
        logger.info(f"ACR creado. Mediana: {df.get('ACR').median():.2f}")

    # 7. Grupo de Edad
    if 'RIDAGEYR' in df.columns:
        df['AGE_GROUP'] = pd.cut(
            df['RIDAGEYR'],
            bins=[0, 20, 40, 60, 80, 120],
            labels=[0, 1, 2, 3, 4],
        ).astype('Int64')
        logger.info("AGE_GROUP creado.")

    # 8. Ratio Carbohidratos/Fibra
    if 'DR1TCARB' in df.columns and 'DR1TFIBE' in df.columns:
        df['CARB_FIBER_RATIO'] = df['DR1TCARB'] / df['DR1TFIBE'].replace(0, np.nan)
        logger.info(f"CARB_FIBER_RATIO creado. Mediana: {df.get('CARB_FIBER_RATIO').median():.1f}")

    # 9. Colesterol No-HDL
    if 'LBXTC' in df.columns and 'LBDHDD' in df.columns:
        df['NON_HDL_CHOL'] = df['LBXTC'] - df['LBDHDD']
        logger.info(f"NON_HDL_CHOL creado. Mediana: {df.get('NON_HDL_CHOL').median():.1f}")

    # 10. eGFR estimado (función renal - CKD-EPI simplificada)
    if 'LBXSCR' in df.columns and 'RIDAGEYR' in df.columns and 'RIAGENDR' in df.columns:
        k = np.where(df['RIAGENDR'] == 2, 0.7, 0.9)
        alpha = np.where(df['RIAGENDR'] == 2, -0.329, -0.411)
        factor = np.where(df['RIAGENDR'] == 2, 1.018, 1.0)
        scr_k = df['LBXSCR'] / k
        df['eGFR'] = (
            141
            * (np.minimum(scr_k, 1) ** alpha)
            * (np.maximum(scr_k, 1) ** (-1.209))
            * (0.993 ** df['RIDAGEYR'])
            * factor
        )
        logger.info(f"eGFR creado. Mediana: {df.get('eGFR').median():.1f}")

    logger.info(f"Feature Engineering completado. Shape: {df.shape}")
    return df
