"""
Nodos del pipeline 'data_ingestion' — ETL Extract.

Lee los 14 archivos .xpt crudos de NHANES y produce versiones limpias:
- Selecciona solo las variables relevantes definidas en parameters_nhanes.yml
- Reemplaza codigos especiales NHANES (7, 9, 77, 99, etc.) por NaN
- Elimina el valor ~5.4e-79 que SAS usa como placeholder
- Filtra participantes validos (con SEQN)
- Limpia valores fuera de rango medico
- Renombra columnas a nombres descriptivos en espanol
"""
from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# ────────────────────────────────────────────────────────────────
# Utilidades comunes
# ────────────────────────────────────────────────────────────────

XPT_NAN = 5.397605346934028e-79  # Valor que SAS XPT usa como NaN
NHANES_MISSING = {7, 9, 77, 99, 777, 999, 7777, 9999, 99999}


def _select_and_clean(
    df: pd.DataFrame,
    keep_cols: list[str],
    categorical_cols: list[str] | None = None,
) -> pd.DataFrame:
    """Selecciona columnas, reemplaza codigos NHANES y XPT NaN."""
    # Filtrar solo columnas que existen
    available = [c for c in keep_cols if c in df.columns]
    missing = set(keep_cols) - set(available)
    if missing:
        logger.warning(f"Columnas no encontradas (omitidas): {missing}")

    result = df[available].copy()

    # Reemplazar el valor XPT NaN (~5.4e-79)
    for col in result.select_dtypes(include=[np.number]).columns:
        mask = np.isclose(result[col], XPT_NAN, rtol=1e-10)
        result.loc[mask, col] = np.nan

    # Reemplazar codigos NHANES de missing en columnas categoricas
    cat_cols = categorical_cols or []
    for col in cat_cols:
        if col in result.columns:
            result.loc[result[col].isin(NHANES_MISSING), col] = np.nan

    # Eliminar filas sin SEQN
    if "SEQN" in result.columns:
        result = result.dropna(subset=["SEQN"])
        result["SEQN"] = result["SEQN"].astype(int)

    logger.info(f"Limpieza: {df.shape} -> {result.shape}")
    return result.reset_index(drop=True)


# ────────────────────────────────────────────────────────────────
# 1. DEMOGRAFIA
# ────────────────────────────────────────────────────────────────

def clean_demo(demo_raw: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    """Limpia tabla de demografia (P_DEMO).

    - Selecciona variables core: edad, genero, raza, educacion, etc.
    - Filtra solo participantes examinados (RIDSTATR == 2)
    - Reemplaza codigos missing NHANES
    - Valida rangos (edad 0-85, genero 1-2)
    """
    keep = parameters.get("demo_vars", [])
    df = _select_and_clean(
        demo_raw, keep,
        categorical_cols=["RIAGENDR", "RIDRETH3", "DMDEDUC2", "DMDMARTZ"],
    )

    # Filtrar solo examinados si la columna esta disponible
    if "RIDSTATR" in demo_raw.columns:
        examined_seqns = demo_raw.loc[demo_raw["RIDSTATR"] == 2, "SEQN"]
        df = df[df["SEQN"].isin(examined_seqns.astype(int))]

    # Validar rango de edad
    if "RIDAGEYR" in df.columns:
        df = df[(df["RIDAGEYR"] >= 0) & (df["RIDAGEYR"] <= 85)]

    # Validar genero
    if "RIAGENDR" in df.columns:
        df = df[df["RIAGENDR"].isin([1, 2]) | df["RIAGENDR"].isna()]

    logger.info(f"DEMO limpio: {df.shape[0]} participantes")
    return df.reset_index(drop=True)


# ────────────────────────────────────────────────────────────────
# 2. CUESTIONARIOS
# ────────────────────────────────────────────────────────────────

def clean_alq(alq_raw: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    """Limpia tabla de consumo de alcohol (P_ALQ)."""
    keep = parameters.get("alq_vars", [])
    df = _select_and_clean(
        alq_raw, keep,
        categorical_cols=["ALQ111", "ALQ121", "ALQ142"],
    )

    # ALQ130: cantidad promedio, debe ser >= 0
    if "ALQ130" in df.columns:
        df.loc[df["ALQ130"] < 0, "ALQ130"] = np.nan
        df.loc[df["ALQ130"] > 50, "ALQ130"] = np.nan  # Max razonable

    logger.info(f"ALQ limpio: {df.shape[0]} registros")
    return df.reset_index(drop=True)


def clean_paq(paq_raw: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    """Limpia tabla de actividad fisica (P_PAQ)."""
    keep = parameters.get("paq_vars", [])
    df = _select_and_clean(
        paq_raw, keep,
        categorical_cols=["PAQ605", "PAQ620", "PAQ635", "PAQ650", "PAQ665"],
    )

    # PAD680: minutos sedentario, debe ser 0-1440 (24h)
    if "PAD680" in df.columns:
        df.loc[df["PAD680"] < 0, "PAD680"] = np.nan
        df.loc[df["PAD680"] > 1440, "PAD680"] = np.nan

    logger.info(f"PAQ limpio: {df.shape[0]} registros")
    return df.reset_index(drop=True)


def clean_slq(slq_raw: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    """Limpia tabla de sueno (P_SLQ)."""
    keep = parameters.get("slq_vars", [])
    df = _select_and_clean(
        slq_raw, keep,
        categorical_cols=["SLQ050"],
    )

    # Horas de sueno: rango valido 2-16
    for col in ["SLD012", "SLD013"]:
        if col in df.columns:
            df.loc[(df[col] < 2) | (df[col] > 16), col] = np.nan

    logger.info(f"SLQ limpio: {df.shape[0]} registros")
    return df.reset_index(drop=True)


def clean_smq(smq_raw: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    """Limpia tabla de tabaquismo (P_SMQ)."""
    keep = parameters.get("smq_vars", [])
    df = _select_and_clean(
        smq_raw, keep,
        categorical_cols=["SMQ020", "SMQ040"],
    )

    # Filtrar solo adultos (SMAQUEX2 == 2 si esta disponible)
    if "SMAQUEX2" in df.columns:
        df = df[df["SMAQUEX2"] == 2].drop(columns=["SMAQUEX2"], errors="ignore")

    logger.info(f"SMQ limpio: {df.shape[0]} registros")
    return df.reset_index(drop=True)


def clean_diq(diq_raw: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    """Limpia tabla de diabetes (P_DIQ)."""
    keep = parameters.get("diq_vars", [])
    df = _select_and_clean(
        diq_raw, keep,
        categorical_cols=["DIQ010", "DIQ160", "DIQ050", "DIQ070"],
    )

    logger.info(f"DIQ limpio: {df.shape[0]} registros")
    return df.reset_index(drop=True)


def clean_mcq(mcq_raw: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    """Limpia tabla de condiciones medicas (P_MCQ)."""
    keep = parameters.get("mcq_vars", [])
    df = _select_and_clean(
        mcq_raw, keep,
        categorical_cols=[
            "MCQ010", "MCQ080", "MCQ160A", "MCQ160B", "MCQ160C",
            "MCQ160D", "MCQ160E", "MCQ160F", "MCQ220",
        ],
    )

    # Convertir respuestas Si/No a binario (1=Si, 2=No -> 1/0)
    binary_cols = [
        "MCQ010", "MCQ080", "MCQ160A", "MCQ160B", "MCQ160C",
        "MCQ160D", "MCQ160E", "MCQ160F", "MCQ220",
    ]
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].map({1: 1, 2: 0})

    logger.info(f"MCQ limpio: {df.shape[0]} registros")
    return df.reset_index(drop=True)


# ────────────────────────────────────────────────────────────────
# 3. EXAMENES FISICOS
# ────────────────────────────────────────────────────────────────

def clean_bmx(bmx_raw: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    """Limpia tabla de medidas corporales (P_BMX)."""
    keep = parameters.get("bmx_vars", [])
    df = _select_and_clean(bmx_raw, keep)

    # Validar rangos medicos
    if "BMXWT" in df.columns:
        df.loc[(df["BMXWT"] < 10) | (df["BMXWT"] > 300), "BMXWT"] = np.nan
    if "BMXHT" in df.columns:
        df.loc[(df["BMXHT"] < 50) | (df["BMXHT"] > 220), "BMXHT"] = np.nan
    if "BMXBMI" in df.columns:
        df.loc[(df["BMXBMI"] < 10) | (df["BMXBMI"] > 80), "BMXBMI"] = np.nan
    if "BMXWAIST" in df.columns:
        df.loc[(df["BMXWAIST"] < 30) | (df["BMXWAIST"] > 200), "BMXWAIST"] = np.nan

    logger.info(f"BMX limpio: {df.shape[0]} registros")
    return df.reset_index(drop=True)


def clean_bpxo(bpxo_raw: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    """Limpia tabla de presion arterial (P_BPXO)."""
    keep = parameters.get("bpxo_vars", [])
    df = _select_and_clean(bpxo_raw, keep)

    # Validar rangos de presion arterial
    sys_cols = ["BPXOSY1", "BPXOSY2", "BPXOSY3"]
    dia_cols = ["BPXODI1", "BPXODI2", "BPXODI3"]

    for col in sys_cols:
        if col in df.columns:
            df.loc[(df[col] < 50) | (df[col] > 300), col] = np.nan
    for col in dia_cols:
        if col in df.columns:
            # Diastolica 0 es valida en NHANES (significa inaudible)
            df.loc[(df[col] < 0) | (df[col] > 200), col] = np.nan

    # Calcular promedio de lecturas validas
    sys_available = [c for c in sys_cols if c in df.columns]
    dia_available = [c for c in dia_cols if c in df.columns]

    if sys_available:
        df["presion_sistolica"] = df[sys_available].mean(axis=1)
    if dia_available:
        df["presion_diastolica"] = df[dia_available].mean(axis=1)

    # Eliminar columnas individuales, quedarnos con promedios
    drop_cols = [c for c in sys_cols + dia_cols if c in df.columns]
    df = df.drop(columns=drop_cols)

    logger.info(f"BPXO limpio: {df.shape[0]} registros")
    return df.reset_index(drop=True)


# ────────────────────────────────────────────────────────────────
# 4. LABORATORIO
# ────────────────────────────────────────────────────────────────

def clean_ghb(ghb_raw: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    """Limpia tabla de hemoglobina glicosilada (P_GHB)."""
    keep = parameters.get("ghb_vars", [])
    df = _select_and_clean(ghb_raw, keep)

    # HbA1c: rango valido 3-20%
    if "LBXGH" in df.columns:
        df.loc[(df["LBXGH"] < 3) | (df["LBXGH"] > 20), "LBXGH"] = np.nan

    logger.info(f"GHB limpio: {df.shape[0]} registros")
    return df.reset_index(drop=True)


def clean_hdl(hdl_raw: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    """Limpia tabla de colesterol HDL (P_HDL)."""
    keep = parameters.get("hdl_vars", [])
    df = _select_and_clean(hdl_raw, keep)

    # HDL: rango valido 10-150 mg/dL
    if "LBDHDD" in df.columns:
        df.loc[(df["LBDHDD"] < 10) | (df["LBDHDD"] > 150), "LBDHDD"] = np.nan

    logger.info(f"HDL limpio: {df.shape[0]} registros")
    return df.reset_index(drop=True)


def clean_tchol(tchol_raw: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    """Limpia tabla de colesterol total (P_TCHOL)."""
    keep = parameters.get("tchol_vars", [])
    df = _select_and_clean(tchol_raw, keep)

    # Colesterol total: rango valido 50-500 mg/dL
    if "LBXTC" in df.columns:
        df.loc[(df["LBXTC"] < 50) | (df["LBXTC"] > 500), "LBXTC"] = np.nan

    logger.info(f"TCHOL limpio: {df.shape[0]} registros")
    return df.reset_index(drop=True)


def clean_trigly(trigly_raw: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    """Limpia tabla de trigliceridos y LDL (P_TRIGLY)."""
    keep = parameters.get("trigly_vars", [])
    df = _select_and_clean(trigly_raw, keep)

    # Trigliceridos: rango valido 10-2000 mg/dL
    if "LBXTR" in df.columns:
        df.loc[(df["LBXTR"] < 10) | (df["LBXTR"] > 2000), "LBXTR"] = np.nan

    # LDL: rango valido 10-400 mg/dL
    if "LBDLDL" in df.columns:
        df.loc[(df["LBDLDL"] < 10) | (df["LBDLDL"] > 400), "LBDLDL"] = np.nan

    logger.info(f"TRIGLY limpio: {df.shape[0]} registros")
    return df.reset_index(drop=True)


def clean_biopro(biopro_raw: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    """Limpia tabla de perfil bioquimico (P_BIOPRO)."""
    keep = parameters.get("biopro_vars", [])
    df = _select_and_clean(biopro_raw, keep)

    # Validar rangos de laboratorio
    ranges = {
        "LBXSGL": (30, 600),     # Glucosa mg/dL
        "LBXSCR": (0.1, 20),     # Creatinina mg/dL
        "LBXSUA": (0.5, 20),     # Acido urico mg/dL
        "LBXSTP": (2, 12),       # Proteina total g/dL
        "LBXSAL": (1, 7),        # Albumina g/dL
        "LBXSGB": (0.5, 8),      # Globulina g/dL
        "LBXSBU": (1, 100),      # BUN mg/dL
        "LBXSPH": (1, 10),       # Fosforo mg/dL
        "LBXSCA": (5, 15),       # Calcio mg/dL
    }
    for col, (lo, hi) in ranges.items():
        if col in df.columns:
            df.loc[(df[col] < lo) | (df[col] > hi), col] = np.nan

    logger.info(f"BIOPRO limpio: {df.shape[0]} registros")
    return df.reset_index(drop=True)
