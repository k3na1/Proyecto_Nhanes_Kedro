/**
 * app.js — Lógica del Dashboard de Predicción de Esperanza de Vida.
 *
 * Gestiona el formulario, la comunicación con la API FastAPI
 * y la renderización animada de los resultados.
 */

// ── Configuración ──────────────────────────────────────────────────
const API_URL = "http://localhost:8000";

// ── DOM Elements ───────────────────────────────────────────────────
const form = document.getElementById("prediction-form");
const btnSubmit = document.getElementById("btn-submit");
const errorBanner = document.getElementById("error-banner");
const errorText = document.getElementById("error-text");

const placeholder = document.getElementById("results-placeholder");
const resultsContent = document.getElementById("results-content");
const gaugeValue = document.getElementById("gauge-value");
const gaugeFill = document.getElementById("gauge-fill");
const statCurrent = document.getElementById("stat-current");
const statOptimal = document.getElementById("stat-optimal");
const gainNumber = document.getElementById("gain-number");
const resultMessage = document.getElementById("result-message");

// ── Constantes del Gauge ───────────────────────────────────────────
const GAUGE_CIRCUMFERENCE = 2 * Math.PI * 90; // r=90 → C≈565.48
const MAX_LIFE = 120; // Escala máxima del gauge

// ── Nombres de los campos del modelo ───────────────────────────────
const MODEL_FIELDS = [
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
];

// ── Helpers ─────────────────────────────────────────────────────────

/**
 * Muestra el banner de error con un mensaje.
 * @param {string} msg - Mensaje de error a mostrar.
 */
function showError(msg) {
  errorText.textContent = msg;
  errorBanner.classList.add("active");
  setTimeout(() => errorBanner.classList.remove("active"), 8000);
}

/** Oculta el banner de error. */
function hideError() {
  errorBanner.classList.remove("active");
}

/**
 * Activa / desactiva el estado de carga del botón.
 * @param {boolean} loading
 */
function setLoading(loading) {
  btnSubmit.disabled = loading;
  btnSubmit.classList.toggle("loading", loading);
}

/**
 * Anima un número desde 0 hasta el valor objetivo.
 * @param {HTMLElement} el - Elemento donde mostrar el valor.
 * @param {number} target - Valor objetivo.
 * @param {number} duration - Duración de la animación en ms.
 * @param {string} suffix - Sufijo a agregar (ej. " años").
 */
function animateNumber(el, target, duration = 1200, suffix = "") {
  const start = performance.now();
  const initial = 0;

  function tick(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    // Easing: ease-out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = initial + (target - initial) * eased;
    el.textContent = current.toFixed(1) + suffix;

    if (progress < 1) {
      requestAnimationFrame(tick);
    }
  }

  requestAnimationFrame(tick);
}

/**
 * Actualiza el gauge circular SVG.
 * @param {number} value - Valor de esperanza de vida.
 */
function updateGauge(value) {
  const ratio = Math.min(value / MAX_LIFE, 1);
  const offset = GAUGE_CIRCUMFERENCE * (1 - ratio);
  gaugeFill.style.strokeDashoffset = offset;
}

// ── Construir Payload ──────────────────────────────────────────────

/**
 * Recolecta los datos del formulario y construye el JSON para la API.
 * Convierte campos vacíos a null para que el pipeline maneje NaN.
 * @returns {object} Payload para POST /predict.
 */
function buildPayload() {
  const edad = parseInt(document.getElementById("edad_actual").value, 10);

  if (isNaN(edad) || edad < 1 || edad > 120) {
    throw new Error("La edad debe ser un número entre 1 y 120.");
  }

  const payload = { edad_actual: edad };

  for (const field of MODEL_FIELDS) {
    const input = document.getElementById(field);
    const raw = input.value.trim();
    payload[field] = raw === "" ? null : parseFloat(raw);

    if (raw !== "" && isNaN(payload[field])) {
      throw new Error(`El campo "${input.previousElementSibling?.textContent || field}" debe ser un número válido.`);
    }
  }

  return payload;
}

// ── Renderizar Resultados ──────────────────────────────────────────

/**
 * Muestra los resultados de la predicción con animaciones.
 * @param {object} data - Respuesta JSON de la API.
 */
function renderResults(data) {
  placeholder.style.display = "none";
  resultsContent.classList.add("active");

  // Gauge
  updateGauge(data.esperanza_vida_optima);
  animateNumber(gaugeValue, data.esperanza_vida_optima, 1400);

  // Stats
  animateNumber(statCurrent, data.esperanza_vida_actual, 1000);
  animateNumber(statOptimal, data.esperanza_vida_optima, 1000);

  // Gain
  animateNumber(gainNumber, data.anios_ganados, 1200);

  // Message
  resultMessage.textContent = data.mensaje;
}

// ── Enviar Predicción ──────────────────────────────────────────────

/**
 * Maneja el submit del formulario: valida, envía a la API y renderiza.
 * @param {Event} e
 */
async function handleSubmit(e) {
  e.preventDefault();
  hideError();

  let payload;
  try {
    payload = buildPayload();
  } catch (err) {
    showError(err.message);
    return;
  }

  setLoading(true);

  try {
    const res = await fetch(`${API_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const errBody = await res.json().catch(() => null);
      const detail = errBody?.detail || `Error del servidor (${res.status})`;
      throw new Error(detail);
    }

    const data = await res.json();
    renderResults(data);
  } catch (err) {
    if (err.message.includes("Failed to fetch") || err.message.includes("NetworkError")) {
      showError("No se pudo conectar con la API. Asegurate de que el servidor esté corriendo en " + API_URL);
    } else {
      showError(err.message);
    }
  } finally {
    setLoading(false);
  }
}

// ── Init ───────────────────────────────────────────────────────────
form.addEventListener("submit", handleSubmit);
