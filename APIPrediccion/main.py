"""
main.py — API de Predicción de Esperanza de Vida con FastAPI.

Carga un pipeline de Scikit-Learn serializado con pickle y expone un endpoint
/predict que genera dos escenarios: hábitos actuales vs. hábitos óptimos.
"""

import copy
import logging
import os
import pickle
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import PredictionInput, PredictionOutput

# ── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(message)s",
)
logger = logging.getLogger(__name__)

# ── Constantes ──────────────────────────────────────────────────────────────
# Ruta del modelo: acepta variable de entorno para portabilidad entre equipos
MODEL_PATH: Path = Path(
    os.getenv("MODEL_PATH", str(Path(__file__).resolve().parent / "model" / "regressor.pickle"))
)

# Orden estricto de las 10 columnas que espera el pipeline
FEATURE_COLUMNS: list[str] = [
    "Ratio_Ingresos_Familiares",
    "Promedio_Bebidas_Alcohol",
    "IMC",
    "Presion_Sistolica",
    "Presion_Diastolica",
    "Anios_Fumando",
    "Glicohemoglobina",
    "Colesterol_LDL",
    "Creatinina",
    "ALT_Enzima_Hepatica",
]

# Valores de "hábitos óptimos" para el Escenario B (What-If)
OPTIMAL_OVERRIDES: dict[str, float] = {
    "Anios_Fumando": 0.0,
    "Promedio_Bebidas_Alcohol": 0.0,
    "IMC": 22.0,
}


# ── Mock Model (respaldo para desarrollo) ──────────────────────────────────
class MockModel:
    """
    Modelo simulado que imita la interfaz de un pipeline Scikit-Learn.

    Se utiliza como respaldo cuando el archivo .pickle no se encuentra,
    permitiendo probar el flujo completo sin bloquear el desarrollo del frontend.
    """

    @staticmethod
    def predict(X: pd.DataFrame) -> np.ndarray:  # noqa: N803
        """Devuelve predicciones simuladas de esperanza de vida."""
        n_samples: int = len(X)
        # Simula valores realistas: base ≈ 68.0, óptimo ≈ 82.0
        imc_col = X["IMC"].values
        is_optimal = np.where(np.isnan(imc_col), False, imc_col == 22.0)
        predictions = np.where(is_optimal, 82.0, 68.0)
        return predictions.astype(np.float64).reshape(n_samples)


# ── Variable global del modelo ──────────────────────────────────────────────
model: Any = None


# ── Lifespan: carga del modelo al arrancar ──────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carga el modelo al inicio del servidor y libera recursos al cerrar."""
    global model  # noqa: PLW0603

    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)  # noqa: S301
        logger.info("Modelo cargado exitosamente desde: %s", MODEL_PATH)

        # Validar que las features del pipeline coincidan con las esperadas
        if hasattr(model, "feature_names_in_"):
            model_features = list(model.feature_names_in_)
            if model_features != FEATURE_COLUMNS:
                logger.error(
                    "Las features del modelo %s NO coinciden con las esperadas %s",
                    model_features,
                    FEATURE_COLUMNS,
                )
                raise ValueError("Desajuste en las features del pipeline.")
            logger.info("Features del modelo validadas: %s", model_features)

    except FileNotFoundError:
        logger.warning(
            "Archivo del modelo no encontrado en '%s'. "
            "Inicializando MockModel para pruebas de desarrollo.",
            MODEL_PATH,
        )
        model = MockModel()
    except Exception as exc:
        logger.error(
            "Error inesperado al cargar el modelo: %s. "
            "Inicializando MockModel como respaldo.",
            exc,
        )
        model = MockModel()

    yield  # ← El servidor corre aquí

    logger.info("Servidor apagándose. Liberando recursos del modelo.")
    model = None


# ── Instancia de FastAPI ────────────────────────────────────────────────────
app = FastAPI(
    title="API de Predicción de Esperanza de Vida",
    description=(
        "Consume un modelo de Regresión Lineal Simple (pipeline Scikit-Learn) "
        "para predecir la esperanza de vida bajo dos escenarios: "
        "hábitos actuales y hábitos óptimos."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS (permitir peticiones del frontend) ─────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Helpers ─────────────────────────────────────────────────────────────────
def _build_dataframe(data: PredictionInput) -> pd.DataFrame:
    """
    Convierte el esquema Pydantic a un DataFrame de Pandas respetando
    el orden estricto de columnas y mapeando None → np.nan.

    Args:
        data: Datos validados del request.

    Returns:
        DataFrame de una fila con las 10 features en el orden correcto.
    """
    row: dict[str, float | None] = {
        col: getattr(data, col) for col in FEATURE_COLUMNS
    }
    df = pd.DataFrame([row], columns=FEATURE_COLUMNS)

    # Mapeo explícito: None de Python → np.nan (garantía para SimpleImputer)
    df = df.where(df.notna(), other=np.nan)

    return df


# ── Endpoints ───────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    """Health check del servicio."""
    return {
        "status": "online",
        "service": "API de Predicción de Esperanza de Vida",
        "version": "1.0.0",
    }


@app.post(
    "/predict",
    response_model=PredictionOutput,
    tags=["Predicción"],
    summary="Predice la esperanza de vida bajo dos escenarios.",
    response_description="Predicciones de esperanza de vida actual y optimizada.",
)
async def predict(data: PredictionInput) -> PredictionOutput:
    """
    Recibe las variables del formulario y retorna dos predicciones:

    - **Escenario A (Actual):** Predicción con los hábitos reportados.
    - **Escenario B (Óptimo):** Predicción forzando hábitos saludables
      (sin fumar, sin alcohol, IMC = 22.0).

    La respuesta incluye la ganancia en años de vida entre ambos escenarios.
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="El modelo no está disponible. Intente nuevamente más tarde.",
        )

    # ── Escenario A: Hábitos Actuales ───────────────────────────────────
    df_actual: pd.DataFrame = _build_dataframe(data)
    logger.info("DataFrame actual:\n%s", df_actual.to_string())

    try:
        pred_actual: float = float(model.predict(df_actual)[0])
    except Exception as exc:
        logger.error("Error en predicción (Escenario A): %s", exc)
        raise HTTPException(
            status_code=500,
            detail=f"Error al ejecutar la predicción con hábitos actuales: {exc}",
        ) from exc

    # ── Escenario B: Hábitos Óptimos (What-If) ─────────────────────────
    df_optimo: pd.DataFrame = copy.deepcopy(df_actual)
    for col, value in OPTIMAL_OVERRIDES.items():
        df_optimo[col] = value

    logger.info("DataFrame óptimo:\n%s", df_optimo.to_string())

    try:
        pred_optima: float = float(model.predict(df_optimo)[0])
    except Exception as exc:
        logger.error("Error en predicción (Escenario B): %s", exc)
        raise HTTPException(
            status_code=500,
            detail=f"Error al ejecutar la predicción con hábitos óptimos: {exc}",
        ) from exc

    # ── Cálculo de Ganancia ─────────────────────────────────────────────
    esperanza_actual: float = round(pred_actual + data.edad_actual, 1)
    esperanza_optima: float = round(pred_optima + data.edad_actual, 1)
    anios_ganados: float = round(max(esperanza_optima - esperanza_actual, 0.0), 1)

    mensaje: str = (
        f"Con tus hábitos actuales vivirás hasta los {esperanza_actual} años, "
        f"pero podrías vivir hasta los {esperanza_optima} años si mejoras tu salud. "
        f"¡Puedes ganar {anios_ganados} años de vida!"
    )

    logger.info("Predicción completada — %s", mensaje)

    return PredictionOutput(
        status="success",
        esperanza_vida_actual=esperanza_actual,
        esperanza_vida_optima=esperanza_optima,
        anios_ganados=anios_ganados,
        mensaje=mensaje,
    )
