import pandas as pd

VARIABLES_SELECCIONADAS = {
    'p_demo': ['SEQN', 'RIDAGEYR', 'RIAGENDR', 'RIDRETH1', 'DMDEDUC2', 'INDFMPIR'],
    'p_alq': ['SEQN', 'ALQ121', 'ALQ130'],
    'p_bmx': ['SEQN', 'BMXBMI', 'BMXWAIST'],
    'p_bpxo': ['SEQN', 'BPXOSY1', 'BPXODI1'],
    'p_diq': ['SEQN', 'DIQ010'],
    'p_ghb': ['SEQN', 'LBXGH'],
    'p_hdl': ['SEQN', 'LBDHDD'],
    'p_tchol': ['SEQN', 'LBXTC'],
    'p_trigly': ['SEQN', 'LBDLDL', 'LBXTR'],
    'p_mcq': ['SEQN', 'MCQ220'],
    'p_paq': ['SEQN', 'PAQ650', 'PAD680'],
    'p_slq': ['SEQN', 'SLD012', 'SLQ030', 'SLQ040'],
    'p_smq': ['SEQN', 'SMQ040', 'SMD057'],
    'p_biopro': ['SEQN', 'LBXSCR', 'LBXSBU', 'LBXSATSI', 'LBXSASSI', 'LBXSAL']
}

PREFIJOS_ADICIONALES = {
    'p_mcq': ['MCQ160']
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
            
    return df[cols_to_keep]

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
