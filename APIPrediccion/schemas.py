"""
schemas.py — Esquemas de validación Pydantic para la API de Predicción de Esperanza de Vida.

Define los modelos de entrada (request) y salida (response) con tipado estricto
y validaciones personalizadas para garantizar la integridad de los datos.
"""

from pydantic import BaseModel, Field, field_validator


class PredictionInput(BaseModel):
    """
    Esquema de entrada para el endpoint /predict.

    Attributes:
        edad_actual: Edad actual del usuario (obligatoria, entre 1 y 120 años).
        Las 10 variables continuas del formulario admiten valores nulos (None)
        para que el SimpleImputer del pipeline se encargue de la imputación.
    """

    edad_actual: int = Field(
        ...,
        ge=1,
        le=120,
        description="Edad actual del usuario en años (obligatoria).",
        json_schema_extra={"example": 35},
    )

    # ── 10 variables continuas (admiten None → np.nan) ──────────────────────
    Ratio_Ingresos_Familiares: float | None = Field(
        default=None,
        description="Ratio de ingresos familiares.",
        json_schema_extra={"example": 3.5},
    )
    Promedio_Bebidas_Alcohol: float | None = Field(
        default=None,
        description="Promedio de bebidas alcohólicas consumidas por día.",
        json_schema_extra={"example": 2.0},
    )
    IMC: float | None = Field(
        default=None,
        description="Índice de Masa Corporal.",
        json_schema_extra={"example": 27.4},
    )
    Presion_Sistolica: float | None = Field(
        default=None,
        description="Presión arterial sistólica (mmHg).",
        json_schema_extra={"example": 130.0},
    )
    Presion_Diastolica: float | None = Field(
        default=None,
        description="Presión arterial diastólica (mmHg).",
        json_schema_extra={"example": 85.0},
    )
    Anios_Fumando: float | None = Field(
        default=None,
        description="Años que lleva fumando.",
        json_schema_extra={"example": 10.0},
    )
    Glicohemoglobina: float | None = Field(
        default=None,
        description="Nivel de glicohemoglobina (%).",
        json_schema_extra={"example": 5.7},
    )
    Colesterol_LDL: float | None = Field(
        default=None,
        description="Colesterol LDL (mg/dL).",
        json_schema_extra={"example": 120.0},
    )
    Creatinina: float | None = Field(
        default=None,
        description="Nivel de creatinina en sangre (mg/dL).",
        json_schema_extra={"example": 0.9},
    )
    ALT_Enzima_Hepatica: float | None = Field(
        default=None,
        description="Nivel de la enzima hepática ALT (U/L).",
        json_schema_extra={"example": 25.0},
    )

    # ── Validadores ─────────────────────────────────────────────────────────
    @field_validator(
        "IMC",
        "Presion_Sistolica",
        "Presion_Diastolica",
        "Anios_Fumando",
        "Glicohemoglobina",
        "Colesterol_LDL",
        "Creatinina",
        "ALT_Enzima_Hepatica",
        "Promedio_Bebidas_Alcohol",
        "Ratio_Ingresos_Familiares",
        mode="before",
    )
    @classmethod
    def validate_non_negative(cls, value: float | None) -> float | None:
        """Las variables continuas, cuando se proporcionan, no deben ser negativas."""
        if value is not None and value < 0:
            raise ValueError("El valor no puede ser negativo.")
        return value


class PredictionOutput(BaseModel):
    """
    Esquema de respuesta para el endpoint /predict.

    Attributes:
        status: Estado de la operación ('success').
        esperanza_vida_actual: Predicción con hábitos actuales (1 decimal).
        esperanza_vida_optima: Predicción con hábitos optimizados (1 decimal).
        anios_ganados: Diferencia entre óptima y actual (1 decimal).
        mensaje: Mensaje descriptivo dinámico para el usuario.
    """

    status: str = Field(
        default="success",
        description="Estado de la operación.",
        json_schema_extra={"example": "success"},
    )
    esperanza_vida_actual: float = Field(
        ...,
        description="Esperanza de vida predicha con hábitos actuales.",
        json_schema_extra={"example": 65.2},
    )
    esperanza_vida_optima: float = Field(
        ...,
        description="Esperanza de vida predicha con hábitos óptimos.",
        json_schema_extra={"example": 78.5},
    )
    anios_ganados: float = Field(
        ...,
        description="Años de vida ganados al optimizar hábitos.",
        json_schema_extra={"example": 13.3},
    )
    mensaje: str = Field(
        ...,
        description="Mensaje descriptivo para el frontend.",
        json_schema_extra={
            "example": (
                "Con tus hábitos actuales vivirás hasta los 65.2 años,"
                "pero podrías vivir hasta los 78.5 años si mejoras tu salud."
                "¡Puedes ganar 13.3 años de vida!"
            )
        },
    )
