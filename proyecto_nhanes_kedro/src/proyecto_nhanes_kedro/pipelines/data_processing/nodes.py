import pandas as pd

VARIABLES_SELECCIONADAS = {
    'p_demo': ['SEQN', 'RIDAGEYR', 'RIAGENDR', 'RIDRETH1', 'DMDEDUC2', 'INDFMPIR', 'RIDSTATR', 'DMDMARTL'],
    'p_alq': ['SEQN', 'ALQ111', 'ALQ121', 'ALQ130'],
    'p_bmx': ['SEQN', 'BMXBMI', 'BMXWAIST'],
    'p_bpxo': ['SEQN', 'BPXOSY1', 'BPXODI1'],
    'p_diq': ['SEQN', 'DIQ010', 'DIQ160', 'DID040', 'DIQ050', 'DIQ080'],
    'p_ghb': ['SEQN', 'LBXGH'],
    'p_hdl': ['SEQN', 'LBDHDD'],
    'p_tchol': ['SEQN', 'LBXTC'],
    'p_trigly': ['SEQN', 'LBDLDL', 'LBXTR'],
    'p_mcq': ['SEQN', 'MCQ220', 'MCQ160C', 'MCQ160D', 'MCQ160O', 'MCQ160L'],
    'p_paq': ['SEQN', 'PAQ650', 'PAD680'],
    'p_slq': ['SEQN', 'SLD012', 'SLQ030', 'SLQ040'],
    'p_smq': ['SEQN', 'SMQ020', 'SMQ040', 'SMD057', 'SMD650', 'SMD030'],
    'p_biopro': ['SEQN', 'LBXSCR', 'LBXSBU', 'LBXSATSI', 'LBXSASSI', 'LBXSAL'],
    'p_mort': ['SEQN', 'ELIGSTAT', 'MORTSTAT', 'UCOD_LEADING', 'PERMTH_EXM']
}

PREFIJOS_ADICIONALES = {
    'p_mcq': ['MCQ160']
}


RENAME_MAP = {
    "RIDSTATR": "Estado_Entrevista",
    "RIDAGEYR": "Edad",
    "RIAGENDR": "Genero",
    "RIDRETH1": "Etnia",
    "DMDEDUC2": "Nivel_Educacion",
    "INDFMPIR": "Ratio_Ingresos_Familiares",
    "DMDMARTL": "Estado_Civil",
    "ALQ111": "Tomo_Alcohol",
    "ALQ121": "Frecuencia_Alcohol",
    "ALQ130": "Promedio_Bebidas_Alcohol",
    "BMXBMI": "IMC",
    "BMXWAIST": "Circunferencia_Cintura",
    "BPXOSY1": "Presion_Sistolica",
    "BPXODI1": "Presion_Diastolica",
    "DIQ010": "Diagnostico_Diabetes",
    "DIQ160": "Prediabetes",
    "DID040": "Edad_Diagnostico_Diabetes",
    "DIQ050": "Usa_Insulina",
    "DIQ080": "Tiene_Retinopatia",
    "LBXGH": "Glicohemoglobina",
    "LBDHDD": "Colesterol_HDL",
    "LBDLDL": "Colesterol_LDL",
    "LBXTR": "Trigliceridos",
    "MCQ220": "Tiene_Cancer",
    "MCQ160C": "Enfermedad_Coronaria",
    "MCQ160D": "Angina_Pecho",
    "MCQ160O": "Tiene_EPOC",
    "MCQ160L": "Enfermedad_Hepatica",
    "MCQ160E": "Tiene_Infarto",
    "MCQ160F": "Tiene_Derrame",
    "MCQ160B": "Insuficiencia_Cardiaca",
    "PAQ650": "Hace_Ejercicio_Intenso",
    "PAD680": "Minutos_Sedentario",
    "SLD012": "Horas_Sueno",
    "SLQ030": "Ronca",
    "SLQ040": "Apnea_Sueno",
    "SMQ020": "Fumo_100_Cigarrillos",
    "SMQ040": "Fuma_Actualmente",
    "SMD057": "Cigarrillos_Diarios_Ex_Fumador",
    "SMD650": "Cigarrillos_Diarios_Activo",
    "SMD030": "Edad_Inicio_Fumar",
    "LBXSCR": "Creatinina",
    "LBXSBU": "BUN",
    "LBXSATSI": "ALT_Enzima_Hepatica",
    "LBXSASSI": "AST_Enzima_Hepatica",
    "LBXSAL": "Albumina",
    "ELIGSTAT": "Estado_Elegibilidad",
    "MORTSTAT": "Estado_Mortalidad",
    "UCOD_LEADING": "Causa_Muerte",
    "PERMTH_EXM": "Meses_Seguimiento"
}

def _filter_df(df: pd.DataFrame, dataset_key: str) -> pd.DataFrame:
    """Función central para aplicar el filtro basado en el diccionario"""
    exact_features = VARIABLES_SELECCIONADAS.get(dataset_key, [])
    prefix_features = PREFIJOS_ADICIONALES.get(dataset_key, [])
    
    cols_to_keep = []
    for col in df.columns:
        if col in exact_features:
            cols_to_keep.append(col)
        elif any(col.startswith(p) for p in prefix_features):
            cols_to_keep.append(col)
            
    return df[cols_to_keep].rename(columns=RENAME_MAP)

def process_p_demo(df: pd.DataFrame) -> pd.DataFrame:
    return _filter_df(df, 'p_demo')

def process_p_alq(df: pd.DataFrame) -> pd.DataFrame:
    return _filter_df(df, 'p_alq')

def process_p_bmx(df: pd.DataFrame) -> pd.DataFrame:
    return _filter_df(df, 'p_bmx')

def process_p_bpxo(df: pd.DataFrame) -> pd.DataFrame:
    return _filter_df(df, 'p_bpxo')

def process_p_diq(df: pd.DataFrame) -> pd.DataFrame:
    return _filter_df(df, 'p_diq')

def process_p_ghb(df: pd.DataFrame) -> pd.DataFrame:
    return _filter_df(df, 'p_ghb')

def process_p_hdl(df: pd.DataFrame) -> pd.DataFrame:
    return _filter_df(df, 'p_hdl')

def process_p_tchol(df: pd.DataFrame) -> pd.DataFrame:
    return _filter_df(df, 'p_tchol')

def process_p_trigly(df: pd.DataFrame) -> pd.DataFrame:
    return _filter_df(df, 'p_trigly')

def process_p_mcq(df: pd.DataFrame) -> pd.DataFrame:
    return _filter_df(df, 'p_mcq')

def process_p_paq(df: pd.DataFrame) -> pd.DataFrame:
    return _filter_df(df, 'p_paq')

def process_p_slq(df: pd.DataFrame) -> pd.DataFrame:
    return _filter_df(df, 'p_slq')

def process_p_smq(df: pd.DataFrame) -> pd.DataFrame:
    return _filter_df(df, 'p_smq')

def process_p_biopro(df: pd.DataFrame) -> pd.DataFrame:
    return _filter_df(df, 'p_biopro')

def process_p_mort(df: pd.DataFrame) -> pd.DataFrame:
    import numpy as np
    # Limpieza de nulos de formato texto
    df = df.replace(['.', '..', '...', '    ', '        '], np.nan)
    # Convertir a numérico
    cols_numericas = ['SEQN', 'ELIGSTAT', 'MORTSTAT', 'PERMTH_EXM']
    for col in cols_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return _filter_df(df, 'p_mort')
