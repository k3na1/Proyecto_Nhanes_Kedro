# Selección de Variables para el Modelo de Estimación de Vida

Este documento detalla las variables seleccionadas de cada dataset de la base de datos NHANES para entrenar un modelo predictivo enfocado en la estimación de la esperanza de vida (y riesgo de mortalidad). 

La selección se basó en los determinantes de salud más fuertes documentados en la literatura médica y epidemiológica: factores demográficos, cardiovasculares, metabólicos, renales y de estilo de vida.

> [!NOTE]
> Las variables de laboratorio (Sección 🧪 y 🔬) son **opcionales** en la aplicación web final. El modelo está diseñado con XGBoost/LightGBM para manejar nulos de forma nativa: si el usuario no dispone de sus exámenes de sangre, el modelo infiere la estimación usando únicamente las variables de cuestionario.

---

## 📊 P_DEMO (Demografía y Estatus Socioeconómico)

* **`SEQN`**: Identificador único (Necesario para cruzar las tablas).
* **`Estado_Entrevista` (RIDSTATR) (Estado de la entrevista/examen)**: Esencial para filtrar únicamente a los pacientes que pasaron tanto por la entrevista como por el examen médico (valor 2).
* **`Edad` (RIDAGEYR) (Edad)**: Es el factor predictor de mortalidad más fuerte e indispensable.
* **`Genero` (RIAGENDR) (Género)**: Las mujeres tienden a tener una mayor esperanza de vida que los hombres debido a factores biológicos, hormonales y de comportamiento.
* **`Etnia` (RIDRETH1) (Raza/Etnia)**: Funciona como un proxy para desigualdades en salud, vulnerabilidad genética poblacional y acceso histórico a sistemas de salud.
* **`Nivel_Educacion` (DMDEDUC2) (Nivel de educación)**: Fuerte indicador del nivel socioeconómico; una mayor educación está directamente correlacionada con mayor longevidad y mejores hábitos. Los códigos `7` (Rehusó) y `9` (No sabe) se tratan como `NaN`.
* **`Ratio_Ingresos_Familiares` (INDFMPIR) (Ratio de ingresos familiares)**: Los niveles bajos de ingresos limitan el acceso a salud preventiva, buena nutrición y entornos seguros.
* **`DMDMARTZ` (Estado civil)**: Múltiples metaanálisis confirman que las personas casadas o que viven en pareja tienen una esperanza de vida entre 5 y 10 años mayor que las solteras, viudas o divorciadas. El aislamiento social es un factor de riesgo de mortalidad equiparable al tabaquismo. Los códigos `77` y `99` se tratan como `NaN`.

## 🍺 P_ALQ (Consumo de Alcohol)

* **`Tomo_Alcohol` (ALQ111) (Alguna vez tomó alcohol)**: Pregunta filtro fundamental para diferenciar a verdaderos abstemios de bebedores con respuestas incompletas.
* **`Frecuencia_Alcohol` (ALQ121) (Frecuencia de consumo)** y **`Promedio_Bebidas_Alcohol` (ALQ130) (Promedio de bebidas diarias)**: El consumo excesivo de alcohol es hepatotóxico, aumenta el riesgo de varios tipos de cáncer, accidentes y miocardiopatías, disminuyendo drásticamente la esperanza de vida.

## 📏 P_BMX (Medidas Corporales)

* **`IMC` (BMXBMI) (Índice de Masa Corporal - IMC)**: Tanto la obesidad (IMC > 30) como el bajo peso crónico (IMC < 18.5) están asociados a una curva de mortalidad en forma de U.
* **`Circunferencia_Cintura` (BMXWAIST) (Circunferencia de cintura)**: Es un indicador excelente de grasa adiposa visceral, la cual está fuertemente relacionada con el síndrome metabólico y mayor riesgo de infarto fulminante.

## 🫀 P_BPXO (Presión Arterial)

* **`Presion_Sistolica` (BPXOSY1) (Presión arterial sistólica)** y **`Presion_Diastolica` (BPXODI1) (Diastólica)**: La hipertensión no controlada daña los vasos sanguíneos silenciosamente, siendo la principal causa de accidentes cerebrovasculares (strokes) e insuficiencia cardíaca.

## 🩸 P_DIQ (Diabetes - Cuestionario)

* **`Diagnostico_Diabetes` (DIQ010) (Diagnóstico de diabetes)**: La diabetes mal controlada acelera el envejecimiento celular, daña los riñones, ojos y el corazón vascular.
* **`Prediabetes` (DIQ160) (Prediabetes)**: Permite identificar un riesgo metabólico intermedio entre sano y diabético.
* **`Edad_Diagnostico_Diabetes` (DID040) (Edad de diagnóstico)**: Se utiliza para calcular la variable derivada `Anios_Diabetes = Edad_Actual - Edad_Diagnostico`. A mayor duración con la enfermedad, mayor deterioro acumulado en órganos.
* **`Usa_Insulina` (DIQ050) (Uso de insulina)**: Separa pacientes diabéticos por gravedad. La insulino-dependencia indica un control glucémico deteriorado.
* **`Tiene_Retinopatia` (DIQ080) (Retinopatía diabética)**: Indica daño microvascular ya establecido, fuerte predictor clínico de problemas cardiovasculares y renales futuros.

## 🧪 Laboratorios de Sangre — Opcionales (Mayor Precisión)

* **`Glicohemoglobina` (LBXGH) (Glicohemoglobina - P_GHB)**: Refleja el nivel medio de glucosa en sangre en los últimos 3 meses. Estándar de oro para medir el control glucémico.
* **`Colesterol_HDL` (LBDHDD) (Colesterol HDL - P_HDL)**: Colesterol "bueno". Niveles altos protegen el sistema cardiovascular.
* **`Colesterol_LDL` (LBDLDL) (Colesterol LDL - P_TRIGLY)**: Colesterol "malo". Niveles elevados causan aterosclerosis y eventos coronarios.
* **`Trigliceridos` (LBXTR) (Triglicéridos - P_TRIGLY)**: Marcador de grasa en sangre asociado a riesgo cardiovascular y resistencia a la insulina.

## 🏥 P_MCQ (Condiciones Médicas Previas)

* **`Tiene_Infarto`** (`Tiene_Infarto` (MCQ160E)): Ataque al corazón previo. Daño irreversible al miocardio.
* **`Tiene_Derrame`** (`Tiene_Derrame` (MCQ160F)): Accidente cerebrovascular. Secuelas neurológicas y alto riesgo de recurrencia.
* **`Tiene_Insuficiencia_Cardiaca`** (`Insuficiencia_Cardiaca` (MCQ160B)): El corazón no bombea sangre de forma eficiente, reduciendo directamente la esperanza de vida.
* **`Tiene_Enfermedad_Coronaria`** (`Enfermedad_Coronaria` (MCQ160C), `Angina_Pecho` (MCQ160D)): Angina o enfermedad coronaria confirmada. Factor de riesgo cardiovascular grave.
* **`Tiene_Cancer`** (`Tiene_Cancer` (MCQ220)): El cáncer activo o en remisión es una de las principales causas directas de mortalidad.
* **`Tiene_EPOC`** (`MCQ160P`): Enfermedad Pulmonar Obstructiva Crónica. Reduce la función pulmonar de forma progresiva e irreversible.
* **`Tiene_Enfermedad_Hepatica`** (`Enfermedad_Hepatica` (MCQ160L)): Condición hepática crónica (hígado graso avanzado, cirrosis, hepatitis). Interfiere con la desintoxicación, síntesis proteica y metabolismo.

## 🏃‍♂️ P_PAQ (Actividad Física)

* **`Hace_Ejercicio_Intenso` (PAQ650) → `Hace_Ejercicio`**: El ejercicio cardiovascular regular fortalece el miocardio, reduce la resistencia a la insulina y prolonga la vida saludable.
* **`Minutos_Sedentario` (PAD680) → `Minutos_Sedentario`**: El sedentarismo extremo es un factor de riesgo independiente de mortalidad, equiparable al tabaquismo.

## 😴 P_SLQ (Trastornos del Sueño)

* **`Horas_Sueno` (SLD012) (Horas de sueño)**: Dormir menos de 6 o más de 9 horas crónicamante está asociado a deterioro metabólico y mayor riesgo de mortalidad temprana.
* **`Ronca` (SLQ030) (Ronquidos fuertes)** y **`Apnea_Sueno` (SLQ040) (Apnea del sueño)**: La apnea genera hipoxia nocturna recurrente, disparando la presión arterial y el riesgo de arritmias cardíacas.

## 🚬 P_SMQ (Tabaquismo)

* **`Fumo_100_Cigarrillos` (SMQ020) (Fumó al menos 100 cigarrillos)**: Pregunta filtro fundamental. Si la respuesta es No, el participante no es considerado fumador y se salta el resto del cuestionario.
* **`Fuma_Actualmente` (SMQ040) (Fuma actualmente)**: Indicador del estado actual de exposición al tabaco.
* **`Cigarrillos_Diarios_Ex_Fumador` (SMD057) y `Cigarrillos_Diarios_Activo` (SMD650) (Cigarrillos diarios)**: La variable `Cigarrillos_Diarios_Ex_Fumador` (SMD057) registra los cigarrillos diarios de los ex-fumadores (cuando lo dejaron), y la variable `Cigarrillos_Diarios_Activo` (SMD650) registra los de los fumadores activos (en los últimos 30 días). Ambas se fusionan para obtener la dosis total.
* **`Edad_Inicio_Fumar` (SMD030) (Edad de inicio)**: Permite calcular la variable derivada `Anios_Fumando = Edad_Actual - SMD030`. Un fumador de 30 años tiene un perfil de riesgo completamente diferente a uno de 2 años, aunque ambos fumen el mismo número de cigarrillos al día.

## 🔬 P_BIOPRO (Perfil Bioquímico Estándar — Opcional)

* **`Creatinina` (LBXSCR) (Creatinina)** y **`BUN` (LBXSBU) (BUN)**: Biomarcadores críticos de la función renal. La falla renal crónica disminuye aceleradamente la esperanza de vida.
* **`ALT_Enzima_Hepatica` (LBXSATSI) (ALT)** y **`AST_Enzima_Hepatica` (LBXSASSI) (AST)**: Enzimas hepáticas. Su elevación crónica indica inflamación y daño (hígado graso, cirrosis).
* **`Albumina` (LBXSAL) (Albúmina)**: Indicador del estado nutricional y síntesis hepática. Niveles bajos son un predictor independiente y robusto de mortalidad a corto y mediano plazo en cualquier franja de edad.

---

## 🗂️ Variables Derivadas (Feature Engineering)

Estas variables no existen en los datos crudos, sino que son calculadas durante la limpieza:

| Variable Derivada | Origen | Fórmula/Lógica |
| :--- | :--- | :--- |
| `Estado_Diabetes` | `Diagnostico_Diabetes` (DIQ010), `Prediabetes` (DIQ160) | 0=Normal, 1=Prediabetes, 2=Diabetes |
| `Anios_Diabetes` | `Edad_Diagnostico_Diabetes` (DID040), `Edad` (RIDAGEYR) | `RIDAGEYR - DID040` (0 si no es diabético) |
| `Usa_Insulina` | `Usa_Insulina` (DIQ050) | Binaria 1/0 (0 si no es diabético) |
| `Tiene_Retinopatia` | `Tiene_Retinopatia` (DIQ080) | Binaria 1/0 (0 si no es diabético) |
| `Hace_Ejercicio` | `Hace_Ejercicio_Intenso` (PAQ650) | Binaria 1/0 |
| `Minutos_Sedentario` | `Minutos_Sedentario` (PAD680) | Continua (minutos al día) |
| `Anios_Fumando` | `Edad_Inicio_Fumar` (SMD030), `Edad` (RIDAGEYR) | `RIDAGEYR - SMD030` (0 si no fumador) |
| `Estado_Fumador` | `Fumo_100_Cigarrillos` (SMQ020), `Fuma_Actualmente` (SMQ040) | 0=Nunca fumó, 1=Ex-fumador, 2=Fumador activo |

---

### Siguientes Pasos (Implementación Kedro)
Al desarrollar la canalización (*pipeline*) de datos, nuestro objetivo en el nodo de limpieza será extraer exactamente estas columnas listadas, unir los datasets a través del identificador `SEQN`, y tratar los valores nulos (NaN) para maximizar la calidad predictiva del modelo final.
