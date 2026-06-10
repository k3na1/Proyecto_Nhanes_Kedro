import pandas as pd
import logging
from typing import Dict, Tuple, Any
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score

logger = logging.getLogger(__name__)

def split_data(data: pd.DataFrame, parameters: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Filtra a los pacientes fallecidos, selecciona las variables óptimas y hace el split de entrenamiento y test.
    """
    # 1. Filtrar solo a los fallecidos
    df_dead = data[data['Estado_Mortalidad'] == 1].copy()
    
    # 2. Variable Objetivo: Edad exacta de defunción
    df_dead['Edad_Fallecimiento'] = df_dead['Edad'] + (df_dead['Meses_Seguimiento'] / 12.0)
    
    # 3. Seleccionar las variables (features) configuradas en parameters.yml
    features = parameters['model_features']
    
    X = df_dead[features]
    y = df_dead['Edad_Fallecimiento']
    
    # 4. Split de datos
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=parameters['model_options']['test_size'], 
        random_state=parameters['model_options']['random_state']
    )
    
    logger.info(f"Split de datos completado. X_train shape: {X_train.shape}, X_test shape: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test

def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> Pipeline:
    """
    Entrena el modelo de regresión lineal robusto.
    """
    # Pipeline: Imputación media -> Escalado estándar -> Regresión Lineal
    model = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler()),
        ('model', LinearRegression())
    ])
    
    model.fit(X_train, y_train)
    logger.info("Modelo de Regresión Lineal entrenado exitosamente.")
    
    return model

def evaluate_model(model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series):
    """
    Evalúa el modelo y registra las métricas MAE y R2.
    """
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    logger.info(f"Evaluación del Modelo - MAE Test: {mae:.2f} años")
    logger.info(f"Evaluación del Modelo - R2 Test: {r2:.4f}")
