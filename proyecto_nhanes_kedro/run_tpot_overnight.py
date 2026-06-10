import os
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tpot import TPOTRegressor
import warnings
warnings.filterwarnings('ignore')

def main():
    print("Iniciando entorno de Kedro...")
    # Aseguramos que el script pueda correr desde la raíz del proyecto
    project_path = Path(__file__).resolve().parent
    bootstrap_project(project_path)
    
    with KedroSession.create(project_path) as session:
        context = session.load_context()
        df = context.catalog.load('model_input')

    print("Preparando los datos para TPOT...")
    # Solo fallecidos
    df_dead = df[df['Estado_Mortalidad'] == 1].copy()
    # Target: Edad de fallecimiento
    df_dead['Edad_Fallecimiento'] = df_dead['Edad'] + (df_dead['Meses_Seguimiento'] / 12.0)

    # Las 10 variables elegidas por la Regresión Lineal Base (RFECV)
    cols_ganadoras = [
        'Ratio_Ingresos_Familiares', 'Promedio_Bebidas_Alcohol', 'IMC', 
        'Presion_Sistolica', 'Presion_Diastolica', 'Anios_Fumando', 
        'Glicohemoglobina', 'Colesterol_LDL', 'Creatinina', 'ALT_Enzima_Hepatica'
    ]

    X_raw = df_dead[cols_ganadoras]
    y = df_dead['Edad_Fallecimiento']

    # Escalar datos (importante para redes neuronales y SVR que TPOT probará)
    preprocessor = StandardScaler()
    X_processed = preprocessor.fit_transform(X_raw)

    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

    # Nota para el compañero: 
    # n_jobs=1 (Secuencial en Windows para evitar TimeoutError con Dask). 
    # generations=50 y population_size=50 evaluará 2500 pipelines.
    # Puede demorar horas. ¡Déjalo corriendo toda la noche!
    print("Iniciando TPOT AutoML. ¡Esto tomará varias horas!")
    print("TPOT probará miles de modelos y seleccionará al ganador por selección natural.")
    
    tpot = TPOTRegressor(
        generations=50, 
        population_size=50, 
        verbosity=2, 
        random_state=42, 
        n_jobs=1,
        scoring='neg_mean_absolute_error' # Minimizar error absoluto
    )
    
    tpot.fit(X_train, y_train)

    print(f"\nTPOT Test Score (Neg MAE): {tpot.score(X_test, y_test)}")

    output_file = project_path / 'tpot_best_pipeline.py'
    tpot.export(str(output_file))
    print(f"\n¡Proceso finalizado! El mejor pipeline se ha guardado en: {output_file}")
    print("Sube ese archivo al repositorio para que podamos implementarlo en el API.")

if __name__ == '__main__':
    main()
