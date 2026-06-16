import pandas as pd
import numpy as np
import logging
from typing import Dict, Any

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import f1_score
from xgboost import XGBClassifier

logger = logging.getLogger(__name__)

def build_preprocessor(num_cols, cat_cols):
    """Construye el preprocesador dinámico para el ColumnTransformer."""
    num_tf = Pipeline([
        ('imp', SimpleImputer(strategy='median')), 
        ('sc', StandardScaler())
    ])
    tfs = [('num', num_tf, num_cols)]
    if cat_cols:
        cat_tf = Pipeline([
            ('imp', SimpleImputer(strategy='most_frequent')),
            ('enc', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
        ])
        tfs.append(('cat', cat_tf, cat_cols))
    return ColumnTransformer(transformers=tfs, remainder='drop')

def train_hierarchical_model(df_master: pd.DataFrame, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entrena el modelo jerárquico usando solo las variables seleccionadas (Web Form).
    Retorna un diccionario con los pipelines y el umbral, listo para exportar a Pickle.
    """
    # Extraer parámetros
    web_features = parameters['web_features']
    target_col = parameters['target_col']
    test_size = parameters['test_size']
    random_state = parameters['random_state']
    xgb_params = parameters['xgboost']
    
    # Filtrar dataset
    X = df_master[web_features].copy()
    y = df_master[target_col].copy()
    
    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
    
    logger.info(f"Entrenando modelo Web Form con {len(web_features)} variables: {web_features}")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # ---------------------------------------------------------
    # MODELO 1: Diabetes vs No Diabetes
    # ---------------------------------------------------------
    y_train_m1 = (y_train == 2).astype(int)
    
    model1_pipeline = Pipeline([
        ('preprocessor', build_preprocessor(numeric_cols, categorical_cols)),
        ('classifier', XGBClassifier(
            objective='binary:logistic', eval_metric='logloss',
            n_estimators=xgb_params['n_estimators'],
            max_depth=xgb_params['max_depth'],
            learning_rate=xgb_params['learning_rate'],
            min_child_weight=xgb_params['min_child_weight'],
            subsample=xgb_params['subsample'],
            colsample_bytree=xgb_params['colsample_bytree'],
            gamma=xgb_params['gamma'],
            reg_alpha=xgb_params['reg_alpha'],
            reg_lambda=xgb_params['reg_lambda'],
            scale_pos_weight=(len(y_train_m1) - y_train_m1.sum()) / y_train_m1.sum(),
            random_state=random_state, n_jobs=-1
        ))
    ])
    
    logger.info("Buscando umbral óptimo para Modelo 1 mediante CV...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
    y_proba_cv_m1 = cross_val_predict(model1_pipeline, X_train, y_train_m1, cv=cv, method='predict_proba')[:, 1]
    
    thresholds = np.linspace(0.3, 0.8, 51)
    f1_scores = [f1_score(y_train_m1, (y_proba_cv_m1 >= t).astype(int)) for t in thresholds]
    best_th_m1 = thresholds[np.argmax(f1_scores)]
    logger.info(f"Umbral óptimo Modelo 1: {best_th_m1:.3f}")
    
    logger.info("Entrenando Modelo 1 final...")
    model1_pipeline.fit(X_train, y_train_m1)
    
    # ---------------------------------------------------------
    # MODELO 2: Prediabetes en Sanos
    # ---------------------------------------------------------
    mask_train = y_train < 2
    X_train_m2 = X_train[mask_train]
    y_train_m2 = y_train[mask_train]
    
    model2_pipeline = Pipeline([
        ('preprocessor', build_preprocessor(numeric_cols, categorical_cols)),
        ('classifier', XGBClassifier(
            objective='binary:logistic', eval_metric='logloss',
            n_estimators=xgb_params['n_estimators'],
            max_depth=xgb_params['max_depth'],
            learning_rate=xgb_params['learning_rate'],
            min_child_weight=xgb_params['min_child_weight'],
            subsample=xgb_params['subsample'],
            colsample_bytree=xgb_params['colsample_bytree'],
            gamma=xgb_params['gamma'],
            reg_alpha=xgb_params['reg_alpha'],
            reg_lambda=xgb_params['reg_lambda'],
            scale_pos_weight=(len(y_train_m2) - y_train_m2.sum()) / y_train_m2.sum(),
            random_state=random_state, n_jobs=-1
        ))
    ])
    
    logger.info("Entrenando Modelo 2 final...")
    model2_pipeline.fit(X_train_m2, y_train_m2)
    
    # ---------------------------------------------------------
    # EMPAQUETAR Y RETORNAR
    # ---------------------------------------------------------
    logger.info("Empaquetando diccionario final para exportación.")
    model_dict = {
        "model1": model1_pipeline,
        "model2": model2_pipeline,
        "threshold_m1": float(best_th_m1)
    }
    
    return model_dict
