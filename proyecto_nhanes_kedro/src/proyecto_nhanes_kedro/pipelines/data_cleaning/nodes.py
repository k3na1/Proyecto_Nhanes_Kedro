"""
Nodos del pipeline 'data_cleaning'.

Replica la logica probada en notebooks/01_limpieza_datos.ipynb:
  - Limpieza individual de 12 tablas (codigos NHANES, rangos, binarios)
  - Union en master table por SEQN
  - Relleno de NaN estructurales
  - Filtro de adultos (>= 18)
  - Imputacion (mediana / moda)
  - Eliminacion de residuales
  - Resultado: 0 NaN
"""
from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# =====================================================================
# CONSTANTES
# =====================================================================

# Valor placeholder SAS XPT que actua como NaN
XPT_NAN = 5.397605346934028e-79

# Codigos NHANES que representan datos faltantes
NHANES_MISSING_CODES = {7, 9, 77, 99, 777, 999, 7777, 9999, 99999}

# Variables categoricas donde los codigos 7/9/77/99 significan "missing"
CATEGORICAS_CON_MISSING = {
    "P_DEMO": ["RIAGENDR", "RIDRETH1", "DMDEDUC2"],
    "P_ALQ":  ["ALQ121"],
    "P_DIQ":  ["DIQ010"],
    "P_MCQ":  ["MCQ160A", "MCQ160B", "MCQ160C", "MCQ160D",
               "MCQ160E", "MCQ160F", "MCQ220"],
    "P_PAQ":  ["PAQ650"],
    "P_SLQ":  ["SLQ030", "SLQ040"],
    "P_SMQ":  ["SMQ040"],
}


# =====================================================================
# FUNCION BASE DE LIMPIEZA
# =====================================================================

def _base_clean(df: pd.DataFrame, nombre_tabla: str) -> pd.DataFrame:
    """Limpieza base comun a todas las tablas.

    1. Reemplaza el placeholder SAS XPT (~5.4e-79) por NaN.
    2. Reemplaza codigos NHANES missing (7, 9, 77, 99...) en categoricas.
    3. Asegura SEQN como int sin nulos.
    """
    result = df.copy()

    # 1. Reemplazar XPT NaN
    for col in result.select_dtypes(include=[np.number]).columns:
        mask = np.isclose(result[col], XPT_NAN, rtol=1e-10)
        if mask.any():
            result.loc[mask, col] = np.nan
            logger.info(f"  {nombre_tabla}.{col}: {mask.sum()} XPT NaN reemplazados")

    # 2. Reemplazar codigos NHANES missing en categoricas
    cat_cols = CATEGORICAS_CON_MISSING.get(nombre_tabla, [])
    for col in cat_cols:
        if col in result.columns:
            mask = result[col].isin(NHANES_MISSING_CODES)
            if mask.any():
                result.loc[mask, col] = np.nan
                logger.info(f"  {nombre_tabla}.{col}: {mask.sum()} codigos NHANES -> NaN")

    # 3. SEQN como int
    if "SEQN" in result.columns:
        result = result.dropna(subset=["SEQN"])
        result["SEQN"] = result["SEQN"].astype(int)

    return result.reset_index(drop=True)


# =====================================================================
# FUNCIONES DE LIMPIEZA POR TABLA (12 tablas)
# =====================================================================

def limpiar_demo(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia P_DEMO: filtra examinados (RIDSTATR=2), valida edad y genero."""
    result = _base_clean(df, "P_DEMO")

    # Filtrar solo participantes examinados
    if "RIDSTATR" in result.columns:
        result = result[result["RIDSTATR"] == 2].drop(columns=["RIDSTATR"])

    # Validar rango de edad (0-80 en NHANES)
    if "RIDAGEYR" in result.columns:
        result = result[(result["RIDAGEYR"] >= 0) & (result["RIDAGEYR"] <= 80)]

    # Validar genero (1=Masculino, 2=Femenino)
    if "RIAGENDR" in result.columns:
        result = result[result["RIAGENDR"].isin([1, 2]) | result["RIAGENDR"].isna()]

    logger.info(f"P_DEMO limpio: {len(result):,} registros")
    return result.reset_index(drop=True)


def limpiar_alq(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia P_ALQ: frecuencia (ALQ121 escala 0-10) y cantidad (ALQ130 1-15)."""
    result = _base_clean(df, "P_ALQ")

    if "ALQ121" in result.columns:
        result.loc[~result["ALQ121"].between(0, 10) & result["ALQ121"].notna(), "ALQ121"] = np.nan

    if "ALQ130" in result.columns:
        result.loc[~result["ALQ130"].between(1, 15) & result["ALQ130"].notna(), "ALQ130"] = np.nan

    logger.info(f"P_ALQ limpio: {len(result):,} registros")
    return result.reset_index(drop=True)


def limpiar_bmx(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia P_BMX: valida rangos IMC (10-100) y cintura (30-200 cm)."""
    result = _base_clean(df, "P_BMX")

    if "BMXBMI" in result.columns:
        result.loc[~result["BMXBMI"].between(10, 100) & result["BMXBMI"].notna(), "BMXBMI"] = np.nan

    if "BMXWAIST" in result.columns:
        result.loc[~result["BMXWAIST"].between(30, 200) & result["BMXWAIST"].notna(), "BMXWAIST"] = np.nan

    logger.info(f"P_BMX limpio: {len(result):,} registros")
    return result.reset_index(drop=True)


def limpiar_bpxo(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia P_BPXO: valida sistolica (50-250) y diastolica (0-200)."""
    result = _base_clean(df, "P_BPXO")

    if "BPXOSY1" in result.columns:
        result.loc[~result["BPXOSY1"].between(50, 250) & result["BPXOSY1"].notna(), "BPXOSY1"] = np.nan

    if "BPXODI1" in result.columns:
        result.loc[~result["BPXODI1"].between(0, 200) & result["BPXODI1"].notna(), "BPXODI1"] = np.nan

    logger.info(f"P_BPXO limpio: {len(result):,} registros")
    return result.reset_index(drop=True)


def limpiar_diq(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia P_DIQ: diagnostico diabetes (1=Si, 2=No, 3=Borderline)."""
    result = _base_clean(df, "P_DIQ")

    if "DIQ010" in result.columns:
        result.loc[~result["DIQ010"].isin([1, 2, 3]) & result["DIQ010"].notna(), "DIQ010"] = np.nan

    logger.info(f"P_DIQ limpio: {len(result):,} registros")
    return result.reset_index(drop=True)


def limpiar_ghb(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia P_GHB: HbA1c en porcentaje (rango 2.5-20%)."""
    result = _base_clean(df, "P_GHB")

    if "LBXGH" in result.columns:
        result.loc[~result["LBXGH"].between(2.5, 20) & result["LBXGH"].notna(), "LBXGH"] = np.nan

    logger.info(f"P_GHB limpio: {len(result):,} registros")
    return result.reset_index(drop=True)


def limpiar_hdl(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia P_HDL: colesterol HDL (rango 5-200 mg/dL)."""
    result = _base_clean(df, "P_HDL")

    if "LBDHDD" in result.columns:
        result.loc[~result["LBDHDD"].between(5, 200) & result["LBDHDD"].notna(), "LBDHDD"] = np.nan

    logger.info(f"P_HDL limpio: {len(result):,} registros")
    return result.reset_index(drop=True)


def limpiar_mcq(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia P_MCQ: convierte respuestas Si=1/No=2 a binario 1/0."""
    result = _base_clean(df, "P_MCQ")

    binary_cols = ["MCQ160A", "MCQ160B", "MCQ160C", "MCQ160D",
                   "MCQ160E", "MCQ160F", "MCQ220"]
    for col in binary_cols:
        if col in result.columns:
            result[col] = result[col].map({1: 1, 2: 0})

    logger.info(f"P_MCQ limpio: {len(result):,} registros")
    return result.reset_index(drop=True)


def limpiar_paq(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia P_PAQ: convierte PAQ650 a binario, valida PAD680 (0-1440 min)."""
    result = _base_clean(df, "P_PAQ")

    if "PAQ650" in result.columns:
        result["PAQ650"] = result["PAQ650"].map({1: 1, 2: 0})

    if "PAD680" in result.columns:
        result.loc[~result["PAD680"].between(0, 1440) & result["PAD680"].notna(), "PAD680"] = np.nan

    logger.info(f"P_PAQ limpio: {len(result):,} registros")
    return result.reset_index(drop=True)


def limpiar_slq(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia P_SLQ: horas sueno (2-14), ronquidos y apnea (0-3)."""
    result = _base_clean(df, "P_SLQ")

    if "SLD012" in result.columns:
        result.loc[~result["SLD012"].between(2, 14) & result["SLD012"].notna(), "SLD012"] = np.nan

    for col in ["SLQ030", "SLQ040"]:
        if col in result.columns:
            result.loc[~result[col].isin([0, 1, 2, 3]) & result[col].notna(), col] = np.nan

    logger.info(f"P_SLQ limpio: {len(result):,} registros")
    return result.reset_index(drop=True)


def limpiar_smq(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia P_SMQ: SMQ040 (1=Diario,2=Algunos,3=No) y SMD057 (1-95 cig/dia)."""
    result = _base_clean(df, "P_SMQ")

    if "SMQ040" in result.columns:
        result.loc[~result["SMQ040"].isin([1, 2, 3]) & result["SMQ040"].notna(), "SMQ040"] = np.nan

    if "SMD057" in result.columns:
        result.loc[~result["SMD057"].between(1, 95) & result["SMD057"].notna(), "SMD057"] = np.nan

    logger.info(f"P_SMQ limpio: {len(result):,} registros")
    return result.reset_index(drop=True)


def limpiar_biopro(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia P_BIOPRO: valida rangos de creatinina, BUN, ALT, AST, albumina."""
    result = _base_clean(df, "P_BIOPRO")

    rangos = {
        "LBXSCR":  (0.25, 14.97),  # Creatinina mg/dL
        "LBXSBU":  (2, 79),        # BUN mg/dL
        "LBXSATSI": (2, 682),      # ALT U/L
        "LBXSASSI": (6, 489),      # AST U/L
        "LBXSAL":  (2.1, 5.4),     # Albumina g/dL
    }
    for col, (lo, hi) in rangos.items():
        if col in result.columns:
            result.loc[~result[col].between(lo, hi) & result[col].notna(), col] = np.nan

    logger.info(f"P_BIOPRO limpio: {len(result):,} registros")
    return result.reset_index(drop=True)


# =====================================================================
# CREAR MASTER TABLE (Union por SEQN)
# =====================================================================

def crear_master_table(
    demo: pd.DataFrame,
    alq: pd.DataFrame,
    bmx: pd.DataFrame,
    bpxo: pd.DataFrame,
    diq: pd.DataFrame,
    ghb: pd.DataFrame,
    hdl: pd.DataFrame,
    mcq: pd.DataFrame,
    paq: pd.DataFrame,
    slq: pd.DataFrame,
    smq: pd.DataFrame,
    biopro: pd.DataFrame,
) -> pd.DataFrame:
    """Une las 12 tablas limpias en una master table por SEQN (LEFT JOIN).

    La tabla base es DEMO (todos los participantes examinados).
    """
    master = demo.copy()
    logger.info(f"Base: P_DEMO -> {len(master):,} filas x {master.shape[1]} cols")

    tablas = [
        ("P_ALQ", alq), ("P_BMX", bmx), ("P_BPXO", bpxo),
        ("P_DIQ", diq), ("P_GHB", ghb), ("P_HDL", hdl),
        ("P_MCQ", mcq), ("P_PAQ", paq), ("P_SLQ", slq),
        ("P_SMQ", smq), ("P_BIOPRO", biopro),
    ]

    for nombre, df_tabla in tablas:
        master = master.merge(df_tabla, on="SEQN", how="left")
        logger.info(f"  + {nombre}: {df_tabla.shape[0]:,} registros unidos")

    logger.info(f"Master table: {master.shape[0]:,} filas x {master.shape[1]} columnas")
    logger.info(f"Total NaN: {master.isnull().sum().sum():,}")
    return master


# =====================================================================
# TRATAMIENTO DE NaN (Estrategia combinada: opcion 3)
# =====================================================================

def tratar_nulos(master: pd.DataFrame) -> pd.DataFrame:
    """Aplica la estrategia combinada de tratamiento de NaN:

    Paso 1: Rellenar NaN estructurales (valores logicos).
    Paso 2: Filtrar solo adultos (>= 18 anos).
    Paso 3: Imputar restantes (mediana continuas / moda categoricas).
    Paso 4: Eliminar filas con NaN residuales.

    Returns:
        DataFrame con 0 NaN.
    """
    result = master.copy()
    n_total_nan_inicio = result.isnull().sum().sum()
    logger.info(f"NaN totales al inicio: {n_total_nan_inicio:,}")

    # ── PASO 1: Rellenar NaN Estructurales ──────────────────────
    logger.info("PASO 1: Rellenando NaN estructurales...")

    # Tabaquismo: NaN = no fue preguntado -> nunca fumo 100+ cigarrillos
    mask_no_fumador = result["SMQ040"].isna()
    result.loc[mask_no_fumador, "SMQ040"] = 3   # No fuma en absoluto
    result.loc[mask_no_fumador, "SMD057"] = 0   # 0 cigarrillos/dia
    # Fumadores que no reportaron cantidad
    mask_fuma_sin_cant = (result["SMQ040"].isin([1, 2])) & (result["SMD057"].isna())
    result.loc[mask_fuma_sin_cant, "SMD057"] = 1  # Minimo: 1 cig/dia
    logger.info(f"  SMQ040: {mask_no_fumador.sum():,} no-fumadores rellenados")

    # Alcohol: NaN = no fue preguntado o no bebe
    mask_no_bebe = result["ALQ121"].isna()
    result.loc[mask_no_bebe, "ALQ121"] = 0   # Nunca en el ultimo ano
    result.loc[mask_no_bebe, "ALQ130"] = 0   # 0 tragos/dia
    mask_bebe_sin_cant = (result["ALQ121"] > 0) & (result["ALQ130"].isna())
    result.loc[mask_bebe_sin_cant, "ALQ130"] = 1  # Minimo: 1 trago/dia
    logger.info(f"  ALQ121: {mask_no_bebe.sum():,} no-bebedores rellenados")

    # Condiciones Medicas: NaN = jovenes sin historial -> 0 (no tiene)
    mcq_cols = ["MCQ160A", "MCQ160B", "MCQ160C", "MCQ160D",
                "MCQ160E", "MCQ160F", "MCQ220"]
    for col in mcq_cols:
        mask = result[col].isna()
        result.loc[mask, col] = 0
        logger.info(f"  {col}: {mask.sum():,} NaN -> 0 (sin condicion)")

    # Sueno: SLQ030/SLQ040 NaN = no se pregunto -> 0 (no ronca/no apnea)
    result.loc[result["SLQ030"].isna(), "SLQ030"] = 0
    result.loc[result["SLQ040"].isna(), "SLQ040"] = 0
    logger.info("  SLQ030/SLQ040: NaN -> 0")

    # Diabetes: muy pocos NaN -> 2 (no diabetico)
    mask_diq = result["DIQ010"].isna()
    result.loc[mask_diq, "DIQ010"] = 2
    logger.info(f"  DIQ010: {mask_diq.sum():,} NaN -> 2")

    n_post_paso1 = result.isnull().sum().sum()
    logger.info(f"  NaN eliminados Paso 1: {n_total_nan_inicio - n_post_paso1:,}")

    # ── PASO 2: Filtrar adultos >= 18 ───────────────────────────
    logger.info("PASO 2: Filtrando adultos >= 18...")
    n_antes = len(result)
    result = result[result["RIDAGEYR"] >= 18].reset_index(drop=True)
    logger.info(f"  {n_antes:,} -> {len(result):,} ({n_antes - len(result):,} menores eliminados)")

    n_post_paso2 = result.isnull().sum().sum()
    logger.info(f"  NaN restantes: {n_post_paso2:,}")

    # ── PASO 3: Imputacion ──────────────────────────────────────
    logger.info("PASO 3: Imputando NaN restantes...")

    cols_continuas = [
        "RIDAGEYR", "INDFMPIR", "ALQ121", "ALQ130",
        "BMXBMI", "BMXWAIST", "BPXOSY1", "BPXODI1",
        "LBXGH", "LBDHDD", "PAD680", "SLD012", "SMD057",
        "LBXSCR", "LBXSBU", "LBXSATSI", "LBXSASSI", "LBXSAL",
    ]
    cols_categoricas = [
        "RIAGENDR", "RIDRETH1", "DMDEDUC2", "DIQ010",
        "MCQ160A", "MCQ160B", "MCQ160C", "MCQ160D",
        "MCQ160E", "MCQ160F", "MCQ220",
        "PAQ650", "SLQ030", "SLQ040", "SMQ040",
    ]

    # Continuas -> mediana
    for col in cols_continuas:
        if col in result.columns:
            n_null = result[col].isnull().sum()
            if n_null > 0:
                mediana = result[col].median()
                result[col] = result[col].fillna(mediana)
                logger.info(f"  {col}: {n_null:,} NaN -> mediana={mediana:.2f}")

    # Categoricas -> moda
    for col in cols_categoricas:
        if col in result.columns:
            n_null = result[col].isnull().sum()
            if n_null > 0:
                moda = result[col].mode()[0]
                result[col] = result[col].fillna(moda)
                logger.info(f"  {col}: {n_null:,} NaN -> moda={moda:.0f}")

    n_post_paso3 = result.isnull().sum().sum()
    logger.info(f"  NaN restantes tras imputacion: {n_post_paso3:,}")

    # ── PASO 4: Eliminar residuales ─────────────────────────────
    logger.info("PASO 4: Eliminando filas con NaN residuales...")
    n_antes = len(result)
    result = result.dropna().reset_index(drop=True)
    logger.info(f"  Filas eliminadas: {n_antes - len(result):,}")

    # ── Validacion Final ────────────────────────────────────────
    total_nan = result.isnull().sum().sum()
    logger.info(f"[RESULTADO FINAL] {len(result):,} filas x {result.shape[1]} cols, NaN={total_nan}")
    assert total_nan == 0, f"ERROR: Quedan {total_nan} NaN en la master table"

    return result
