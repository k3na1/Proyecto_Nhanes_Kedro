import pandas as pd
import numpy as np
from functools import reduce

def clean_demo(df_demo: pd.DataFrame) -> pd.DataFrame:
    df_demo = df_demo[(df_demo['Estado_Entrevista'] == 2) & (df_demo['Edad'] >= 18)].copy()
    df_demo = df_demo.drop(columns=['Estado_Entrevista'])
    df_demo['Nivel_Educacion'] = df_demo['Nivel_Educacion'].replace([7.0, 9.0], np.nan)
    df_demo['age_group_temp'] = pd.cut(df_demo['Edad'], bins=[17, 35, 50, 65, 120])
    df_demo['Nivel_Educacion'] = df_demo.groupby(['Genero', 'age_group_temp'])['Nivel_Educacion'].transform(
        lambda x: x.fillna(x.mode()[0] if not x.mode().empty else np.nan)
    )
    df_demo['Estado_Civil'] = df_demo['Estado_Civil'].replace([77.0, 99.0], np.nan)
    df_demo['Estado_Civil'] = df_demo.groupby(['Genero', 'age_group_temp'])['Estado_Civil'].transform(
        lambda x: x.fillna(x.mode()[0] if not x.mode().empty else np.nan)
    )
    df_demo['Ratio_Ingresos_Familiares'] = df_demo.groupby(['Etnia', 'age_group_temp'])['Ratio_Ingresos_Familiares'].transform(
        lambda x: x.fillna(x.median())
    )
    df_demo = df_demo.drop(columns=['age_group_temp'])
    return df_demo

def engineer_alq(df_alq: pd.DataFrame, df_demo: pd.DataFrame) -> pd.DataFrame:
    ids_validos = set(df_demo['SEQN'])
    df_alq = df_alq[df_alq['SEQN'].isin(ids_validos)].copy()
    SAS_NAN = 5.397605346934028e-79
    for col in ['Frecuencia_Alcohol', 'Promedio_Bebidas_Alcohol']:
        mask = np.isclose(df_alq[col], SAS_NAN, rtol=1e-10, atol=1e-10)
        df_alq.loc[mask, col] = np.nan
    df_alq['Frecuencia_Alcohol'] = df_alq['Frecuencia_Alcohol'].replace([77.0, 99.0], np.nan)
    df_alq['Promedio_Bebidas_Alcohol'] = df_alq['Promedio_Bebidas_Alcohol'].replace([777.0, 999.0], np.nan)
    df_alq.loc[df_alq['Tomo_Alcohol'] == 2.0, 'Frecuencia_Alcohol'] = 0
    df_alq.loc[df_alq['Tomo_Alcohol'] == 2.0, 'Promedio_Bebidas_Alcohol'] = 0
    df_alq.loc[df_alq['Frecuencia_Alcohol'] == 0, 'Promedio_Bebidas_Alcohol'] = 0
    df_alq = df_alq.merge(df_demo[['SEQN', 'Genero', 'Edad']], on='SEQN', how='left')
    df_alq['age_group'] = pd.cut(df_alq['Edad'], bins=[17, 35, 50, 65, 120])
    df_alq['Tomo_Alcohol'] = df_alq.groupby(['Genero', 'age_group'])['Tomo_Alcohol'].transform(
        lambda x: x.fillna(x.mode()[0] if not x.mode().empty else np.nan)
    )
    df_alq['Frecuencia_Alcohol'] = df_alq.groupby(['Genero', 'age_group'])['Frecuencia_Alcohol'].transform(lambda x: x.fillna(x.median()))
    df_alq['Promedio_Bebidas_Alcohol'] = df_alq.groupby(['Genero', 'age_group'])['Promedio_Bebidas_Alcohol'].transform(lambda x: x.fillna(x.median()))
    df_alq.loc[df_alq['Tomo_Alcohol'] == 2.0, 'Frecuencia_Alcohol'] = 0
    df_alq.loc[df_alq['Tomo_Alcohol'] == 2.0, 'Promedio_Bebidas_Alcohol'] = 0
    df_alq = df_alq.drop(columns=['Genero', 'Edad', 'age_group'])
    return df_alq

def engineer_bmx(df_bmx: pd.DataFrame, df_demo: pd.DataFrame) -> pd.DataFrame:
    ids_validos = set(df_demo['SEQN'])
    df_bmx = df_bmx[df_bmx['SEQN'].isin(ids_validos)].copy()
    df_bmx.loc[~df_bmx['IMC'].between(10, 100) & df_bmx['IMC'].notna(), 'IMC'] = np.nan
    df_bmx.loc[~df_bmx['Circunferencia_Cintura'].between(30, 200) & df_bmx['Circunferencia_Cintura'].notna(), 'Circunferencia_Cintura'] = np.nan
    df_bmx = pd.merge(df_bmx, df_demo[['SEQN', 'Genero', 'Edad']], on='SEQN', how='left')
    df_bmx['grupo_edad'] = pd.cut(df_bmx['Edad'], bins=[17, 30, 45, 60, 80, 120])
    df_bmx['IMC'] = df_bmx.groupby(['Genero', 'grupo_edad'])['IMC'].transform(lambda x: x.fillna(x.median()))
    df_bmx['Circunferencia_Cintura'] = df_bmx.groupby(['Genero', 'grupo_edad'])['Circunferencia_Cintura'].transform(lambda x: x.fillna(x.median()))
    df_bmx = df_bmx.drop(columns=['Genero', 'Edad', 'grupo_edad'])
    return df_bmx

def engineer_bpxo(df_bpxo: pd.DataFrame, df_demo: pd.DataFrame) -> pd.DataFrame:
    ids_validos = set(df_demo['SEQN'])
    df_bpxo = df_bpxo[df_bpxo['SEQN'].isin(ids_validos)].copy()
    df_bpxo.loc[~df_bpxo['Presion_Sistolica'].between(40, 250) & df_bpxo['Presion_Sistolica'].notna(), 'Presion_Sistolica'] = np.nan
    df_bpxo.loc[~df_bpxo['Presion_Diastolica'].between(30, 150) & df_bpxo['Presion_Diastolica'].notna(), 'Presion_Diastolica'] = np.nan
    df_bpxo = df_bpxo.merge(df_demo[['SEQN', 'Genero', 'Edad']], on='SEQN', how='left')
    df_bpxo['age_group'] = pd.cut(df_bpxo['Edad'], bins=[17, 35, 50, 65, 120])
    df_bpxo['Presion_Sistolica'] = df_bpxo.groupby(['Genero', 'age_group'])['Presion_Sistolica'].transform(lambda x: x.fillna(x.median()))
    df_bpxo['Presion_Diastolica'] = df_bpxo.groupby(['Genero', 'age_group'])['Presion_Diastolica'].transform(lambda x: x.fillna(x.median()))
    df_bpxo = df_bpxo.drop(columns=['Genero', 'Edad', 'age_group'])
    return df_bpxo

def engineer_diq(df_diq: pd.DataFrame, df_demo: pd.DataFrame) -> pd.DataFrame:
    ids_validos = set(df_demo['SEQN'])
    df_diq = df_diq[df_diq['SEQN'].isin(ids_validos)].copy()
    df_diq = df_diq.merge(df_demo[['SEQN', 'Edad']], on='SEQN', how='left')
    for col in ['Diagnostico_Diabetes', 'Prediabetes', 'Usa_Insulina', 'Tiene_Retinopatia']:
        df_diq[col] = df_diq[col].replace([7.0, 9.0], np.nan)
    df_diq['Edad_Diagnostico_Diabetes'] = df_diq['Edad_Diagnostico_Diabetes'].replace([777.0, 999.0], np.nan)
    df_diq['Edad_Diagnostico_Diabetes'] = df_diq['Edad_Diagnostico_Diabetes'].replace([666.0], 0)
    
    df_diq['Estado_Diabetes'] = 0
    df_diq.loc[(df_diq['Diagnostico_Diabetes'] == 3.0) | (df_diq['Prediabetes'] == 1.0), 'Estado_Diabetes'] = 1
    df_diq.loc[df_diq['Diagnostico_Diabetes'] == 1.0, 'Estado_Diabetes'] = 2
    
    df_diq['Anios_Diabetes'] = 0
    mask_diabetico = (df_diq['Estado_Diabetes'] == 2)
    df_diq.loc[mask_diabetico, 'Anios_Diabetes'] = df_diq['Edad'] - df_diq['Edad_Diagnostico_Diabetes']
    
    df_diq['Usa_Insulina_Final'] = 0
    df_diq.loc[mask_diabetico & (df_diq['Usa_Insulina'] == 1.0), 'Usa_Insulina_Final'] = 1
    
    df_diq['Tiene_Retinopatia_Final'] = 0
    df_diq.loc[mask_diabetico & (df_diq['Tiene_Retinopatia'] == 1.0), 'Tiene_Retinopatia_Final'] = 1
    
    df_diq = df_diq.drop(columns=['Diagnostico_Diabetes', 'Prediabetes', 'Edad_Diagnostico_Diabetes', 'Usa_Insulina', 'Tiene_Retinopatia', 'Edad'])
    df_diq = df_diq.rename(columns={'Usa_Insulina_Final': 'Usa_Insulina', 'Tiene_Retinopatia_Final': 'Tiene_Retinopatia'})
    
    mediana_anios = df_diq.loc[df_diq['Anios_Diabetes'] > 0, 'Anios_Diabetes'].median()
    df_diq['Anios_Diabetes'] = df_diq['Anios_Diabetes'].fillna(mediana_anios)
    df_diq.loc[df_diq['Anios_Diabetes'] < 0, 'Anios_Diabetes'] = 0
    return df_diq

def engineer_mcq(df_mcq: pd.DataFrame, df_demo: pd.DataFrame) -> pd.DataFrame:
    ids_validos = set(df_demo['SEQN'])
    df_mcq = df_mcq[df_mcq['SEQN'].isin(ids_validos)].copy()
    columnas_mcq = [col for col in df_mcq.columns if col != 'SEQN']
    for col in columnas_mcq:
        df_mcq[col] = df_mcq[col].apply(lambda x: 1 if x == 1.0 else 0)
        
    df_mcq_limpio = pd.DataFrame()
    df_mcq_limpio['SEQN'] = df_mcq['SEQN']
    df_mcq_limpio['Tiene_Infarto'] = df_mcq['Tiene_Infarto']
    df_mcq_limpio['Tiene_Derrame'] = df_mcq['Tiene_Derrame']
    df_mcq_limpio['Insuficiencia_Cardiaca'] = df_mcq['Insuficiencia_Cardiaca']
    df_mcq_limpio['Enfermedad_Coronaria'] = df_mcq[['Enfermedad_Coronaria', 'Angina_Pecho']].max(axis=1)
    df_mcq_limpio['Tiene_Cancer'] = df_mcq['Tiene_Cancer']
    df_mcq_limpio['Tiene_EPOC'] = df_mcq['Tiene_EPOC']
    df_mcq_limpio['Enfermedad_Hepatica'] = df_mcq['Enfermedad_Hepatica']
    return df_mcq_limpio

def engineer_paq(df_paq: pd.DataFrame, df_demo: pd.DataFrame) -> pd.DataFrame:
    ids_validos = set(df_demo['SEQN'])
    df_paq = df_paq[df_paq['SEQN'].isin(ids_validos)].copy()
    demo_temp = df_demo[['SEQN', 'Genero', 'Edad']].copy()
    demo_temp['age_group'] = pd.cut(demo_temp['Edad'], bins=[17, 30, 50, 70, 120])
    df_paq = df_paq.merge(demo_temp[['SEQN', 'Genero', 'age_group']], on='SEQN', how='left')
    df_paq['Hace_Ejercicio_Intenso'] = df_paq['Hace_Ejercicio_Intenso'].replace([7.0, 9.0], np.nan)
    df_paq['Minutos_Sedentario'] = df_paq['Minutos_Sedentario'].replace([7777.0, 9999.0], np.nan)
    df_paq['Hace_Ejercicio_Intenso'] = df_paq.groupby(['Genero', 'age_group'])['Hace_Ejercicio_Intenso'].transform(
        lambda x: x.fillna(x.mode()[0] if not x.mode().empty else 2.0)
    )
    df_paq['Minutos_Sedentario'] = df_paq.groupby(['Genero', 'age_group'])['Minutos_Sedentario'].transform(lambda x: x.fillna(x.median()))
    df_paq['Hace_Ejercicio_Intenso'] = df_paq['Hace_Ejercicio_Intenso'].apply(lambda x: 1 if x == 1.0 else 0)
    df_paq = df_paq[['SEQN', 'Hace_Ejercicio_Intenso', 'Minutos_Sedentario']]
    return df_paq

def engineer_slq(df_slq: pd.DataFrame, df_demo: pd.DataFrame) -> pd.DataFrame:
    ids_validos = set(df_demo['SEQN'])
    df_slq = df_slq[df_slq['SEQN'].isin(ids_validos)].copy()
    SAS_NAN = 5.397605346934028e-79
    for col in ['Ronca', 'Apnea_Sueno']:
        mask_raros = np.isclose(df_slq[col].fillna(0), SAS_NAN, atol=1e-78)
        df_slq.loc[mask_raros, col] = np.nan
    df_slq['Ronca'] = df_slq['Ronca'].replace([9.0], np.nan)
    df_slq['Apnea_Sueno'] = df_slq['Apnea_Sueno'].replace([9.0], np.nan)
    df_slq.loc[~df_slq['Horas_Sueno'].between(2, 14) & df_slq['Horas_Sueno'].notna(), 'Horas_Sueno'] = np.nan
    df_slq = df_slq.merge(df_demo[['SEQN', 'Genero', 'Edad']], on='SEQN', how='left')
    df_slq['age_group'] = pd.cut(df_slq['Edad'], bins=[17, 35, 50, 65, 120])
    df_slq['Horas_Sueno'] = df_slq.groupby(['Genero', 'age_group'])['Horas_Sueno'].transform(lambda x: x.fillna(x.median()))
    for col in ['Ronca', 'Apnea_Sueno']:
        df_slq[col] = df_slq.groupby(['Genero', 'age_group'])[col].transform(
            lambda x: x.fillna(x.mode()[0] if not x.mode().empty else 0.0)
        )
    df_slq = df_slq.drop(columns=['Genero', 'Edad', 'age_group'])
    return df_slq

def engineer_smq(df_smq: pd.DataFrame, df_demo: pd.DataFrame) -> pd.DataFrame:
    ids_validos = set(df_demo['SEQN'])
    df_smq = df_smq[df_smq['SEQN'].isin(ids_validos)].copy()
    df_smq = df_smq.merge(df_demo[['SEQN', 'Edad']], on='SEQN', how='left')
    df_smq['Fumo_100_Cigarrillos'] = df_smq['Fumo_100_Cigarrillos'].replace([7.0, 9.0], np.nan)
    df_smq['Fuma_Actualmente'] = df_smq['Fuma_Actualmente'].replace([7.0, 9.0], np.nan)
    df_smq['Edad_Inicio_Fumar'] = df_smq['Edad_Inicio_Fumar'].replace([77.0, 99.0], np.nan)
    
    df_smq['Estado_Fumador'] = 0
    df_smq.loc[df_smq['Fuma_Actualmente'] == 3.0, 'Estado_Fumador'] = 1
    df_smq.loc[df_smq['Fuma_Actualmente'].isin([1.0, 2.0]), 'Estado_Fumador'] = 2
    
    df_smq['Cigarrillos_Diarios'] = 0
    df_smq.loc[df_smq['Estado_Fumador'] == 1, 'Cigarrillos_Diarios'] = df_smq['Cigarrillos_Diarios_Ex_Fumador']
    df_smq.loc[df_smq['Estado_Fumador'] == 2, 'Cigarrillos_Diarios'] = df_smq['Cigarrillos_Diarios_Activo']
    
    mediana_cigarrillos = df_smq.loc[df_smq['Cigarrillos_Diarios'] > 0, 'Cigarrillos_Diarios'].median()
    mask_fumo = df_smq['Estado_Fumador'].isin([1, 2])
    df_smq.loc[mask_fumo & df_smq['Cigarrillos_Diarios'].isna(), 'Cigarrillos_Diarios'] = mediana_cigarrillos
    
    df_smq['Anios_Fumando'] = 0
    df_smq.loc[mask_fumo, 'Anios_Fumando'] = df_smq['Edad'] - df_smq['Edad_Inicio_Fumar']
    mediana_anios_fumo = df_smq.loc[df_smq['Anios_Fumando'] > 0, 'Anios_Fumando'].median()
    df_smq.loc[mask_fumo & df_smq['Anios_Fumando'].isna(), 'Anios_Fumando'] = mediana_anios_fumo
    df_smq.loc[df_smq['Anios_Fumando'] < 0, 'Anios_Fumando'] = 0
    
    df_smq = df_smq[['SEQN', 'Estado_Fumador', 'Cigarrillos_Diarios', 'Anios_Fumando']]
    return df_smq

def engineer_ghb(df_ghb: pd.DataFrame, df_demo: pd.DataFrame) -> pd.DataFrame:
    ids_validos = set(df_demo['SEQN'])
    df_ghb = df_ghb[df_ghb['SEQN'].isin(ids_validos)].copy()
    mask_error = ~df_ghb['Glicohemoglobina'].between(3.0, 18.0) & df_ghb['Glicohemoglobina'].notna()
    df_ghb.loc[mask_error, 'Glicohemoglobina'] = np.nan
    df_ghb = df_ghb.merge(df_demo[['SEQN', 'Genero', 'Edad']], on='SEQN', how='left')
    df_ghb['age_group'] = pd.cut(df_ghb['Edad'], bins=[17, 35, 50, 65, 120])
    df_ghb['Glicohemoglobina'] = df_ghb.groupby(['Genero', 'age_group'])['Glicohemoglobina'].transform(lambda x: x.fillna(x.median()))
    df_ghb = df_ghb[['SEQN', 'Glicohemoglobina']]
    return df_ghb

def engineer_hdl(df_hdl: pd.DataFrame, df_demo: pd.DataFrame) -> pd.DataFrame:
    ids_validos = set(df_demo['SEQN'])
    df_hdl = df_hdl[df_hdl['SEQN'].isin(ids_validos)].copy()
    mask_error = ~df_hdl['Colesterol_HDL'].between(5.0, 200.0) & df_hdl['Colesterol_HDL'].notna()
    df_hdl.loc[mask_error, 'Colesterol_HDL'] = np.nan
    df_hdl = df_hdl.merge(df_demo[['SEQN', 'Genero', 'Edad']], on='SEQN', how='left')
    df_hdl['age_group'] = pd.cut(df_hdl['Edad'], bins=[17, 35, 50, 65, 120])
    df_hdl['Colesterol_HDL'] = df_hdl.groupby(['Genero', 'age_group'])['Colesterol_HDL'].transform(lambda x: x.fillna(x.median()))
    df_hdl = df_hdl[['SEQN', 'Colesterol_HDL']]
    return df_hdl

def engineer_tchol(df_tchol: pd.DataFrame, df_demo: pd.DataFrame) -> pd.DataFrame:
    ids_validos = set(df_demo['SEQN'])
    df_tchol = df_tchol[df_tchol['SEQN'].isin(ids_validos)].copy()
    mask_error = ~df_tchol['LBXTC'].between(50.0, 500.0) & df_tchol['LBXTC'].notna()
    df_tchol.loc[mask_error, 'LBXTC'] = np.nan
    df_tchol = df_tchol.merge(df_demo[['SEQN', 'Genero', 'Edad']], on='SEQN', how='left')
    df_tchol['age_group'] = pd.cut(df_tchol['Edad'], bins=[17, 35, 50, 65, 120])
    df_tchol['LBXTC'] = df_tchol.groupby(['Genero', 'age_group'])['LBXTC'].transform(lambda x: x.fillna(x.median()))
    df_tchol = df_tchol[['SEQN', 'LBXTC']]
    return df_tchol

def engineer_trigly(df_trigly: pd.DataFrame, df_demo: pd.DataFrame) -> pd.DataFrame:
    ids_validos = set(df_demo['SEQN'])
    df_trigly = df_trigly[df_trigly['SEQN'].isin(ids_validos)].copy()
    mask_err_tr = ~df_trigly['Trigliceridos'].between(10.0, 3000.0) & df_trigly['Trigliceridos'].notna()
    mask_err_ldl = ~df_trigly['Colesterol_LDL'].between(10.0, 400.0) & df_trigly['Colesterol_LDL'].notna()
    df_trigly.loc[mask_err_tr, 'Trigliceridos'] = np.nan
    df_trigly.loc[mask_err_ldl, 'Colesterol_LDL'] = np.nan
    df_trigly = df_trigly.merge(df_demo[['SEQN', 'Genero', 'Edad']], on='SEQN', how='left')
    df_trigly['age_group'] = pd.cut(df_trigly['Edad'], bins=[17, 35, 50, 65, 120])
    for col in ['Trigliceridos', 'Colesterol_LDL']:
        df_trigly[col] = df_trigly.groupby(['Genero', 'age_group'])[col].transform(lambda x: x.fillna(x.median()))
    df_trigly = df_trigly[['SEQN', 'Trigliceridos', 'Colesterol_LDL']]
    return df_trigly

def engineer_biopro(df_biopro: pd.DataFrame, df_demo: pd.DataFrame) -> pd.DataFrame:
    ids_validos = set(df_demo['SEQN'])
    df_biopro = df_biopro[df_biopro['SEQN'].isin(ids_validos)].copy()
    rangos = {
        'Creatinina': (0.1, 20.0),
        'BUN': (1.0, 150.0),
        'ALT_Enzima_Hepatica': (1.0, 2000.0),
        'AST_Enzima_Hepatica': (1.0, 2000.0),
        'Albumina': (1.0, 6.0),
    }
    for col, (low, high) in rangos.items():
        mask_err = ~df_biopro[col].between(low, high) & df_biopro[col].notna()
        df_biopro.loc[mask_err, col] = np.nan
    df_biopro = df_biopro.merge(df_demo[['SEQN', 'Genero', 'Edad']], on='SEQN', how='left')
    df_biopro['age_group'] = pd.cut(df_biopro['Edad'], bins=[17, 35, 50, 65, 120])
    cols_biopro = list(rangos.keys())
    for col in cols_biopro:
        df_biopro[col] = df_biopro.groupby(['Genero', 'age_group'])[col].transform(lambda x: x.fillna(x.median()))
    df_biopro = df_biopro[['SEQN'] + cols_biopro]
    return df_biopro

def create_model_input(
    df_demo, df_alq, df_bmx, df_bpxo, df_diq, df_mcq, df_paq, df_slq, df_smq,
    df_ghb, df_hdl, df_tchol, df_trigly, df_biopro, p_mort
) -> pd.DataFrame:
    # 1. Crear flag Test_Sangre_Ayunas basado en quienes tienen Triglicéridos
    seqn_con_trigly = set(df_trigly['SEQN'])
    df_demo['Test_Sangre_Ayunas'] = df_demo['SEQN'].apply(lambda x: 1 if x in seqn_con_trigly else 0)
    
    # 2. Merge de todas las X
    dataframes_X = [df_demo, df_alq, df_bmx, df_bpxo, df_diq, df_mcq, df_paq, df_slq, df_smq, df_ghb, df_hdl, df_tchol, df_trigly, df_biopro]
    df_master_x = reduce(lambda left, right: pd.merge(left, right, on='SEQN', how='left'), dataframes_X)
    
    # 3. Imputación final de Triglicéridos/LDL para los que no ayunaron
    for col in ['Trigliceridos', 'Colesterol_LDL']:
        mediana = df_master_x[col].median()
        df_master_x[col] = df_master_x[col].fillna(mediana)
        
    # 4. Merge con Mortalidad y aplicar regla de negocio
    df_final = pd.merge(df_master_x, p_mort, on='SEQN', how='left')
    df_final = df_final.dropna(subset=['Estado_Mortalidad'])
    
    return df_final
