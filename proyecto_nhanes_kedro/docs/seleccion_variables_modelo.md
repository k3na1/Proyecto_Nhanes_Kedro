# Selección de Variables para el Modelo de Estimación de Vida

Este documento detalla las variables seleccionadas de cada dataset de la base de datos NHANES para entrenar un modelo predictivo enfocado en la estimación de la esperanza de vida (y riesgo de mortalidad). 

La selección se basó en los determinantes de salud más fuertes documentados en la literatura médica y epidemiológica: factores demográficos, cardiovasculares, metabólicos, renales y de estilo de vida.

---

## 📊 P_DEMO (Demografía y Estatus Socioeconómico)
* **`SEQN`**: Identificador único (Necesario para cruzar las tablas).
* **`RIDAGEYR` (Edad)**: Es el factor predictor de mortalidad más fuerte e indispensable.
* **`RIAGENDR` (Género)**: Las mujeres tienden a tener una mayor esperanza de vida que los hombres debido a factores biológicos, hormonales y de comportamiento.
* **`RIDRETH1` (Raza/Etnia)**: Funciona como un proxy para desigualdades en salud, vulnerabilidad genética poblacional y acceso histórico a sistemas de salud.
* **`DMDEDUC2` (Nivel de educación)**: Fuerte indicador del nivel socioeconómico; una mayor educación está directamente correlacionada con mayor longevidad y mejores hábitos.
* **`INDFMPIR` (Ratio de ingresos familiares)**: Los niveles bajos de ingresos limitan el acceso a salud preventiva, buena nutrición y entornos seguros.

## 🍺 P_ALQ (Consumo de Alcohol)
* **`ALQ121` (Frecuencia de consumo)** y **`ALQ130` (Promedio de bebidas diarias)**: El consumo excesivo de alcohol es hepatotóxico, aumenta el riesgo de varios tipos de cáncer, accidentes y miocardiopatías, disminuyendo drásticamente la esperanza de vida.

## 📏 P_BMX (Medidas Corporales)
* **`BMXBMI` (Índice de Masa Corporal - IMC)**: Tanto la obesidad (IMC > 30) como el bajo peso crónico (IMC < 18.5) están asociados a una curva de mortalidad en forma de U.
* **`BMXWAIST` (Circunferencia de cintura)**: Es un indicador excelente de grasa adiposa visceral, la cual está fuertemente relacionada con el síndrome metabólico y mayor riesgo de infarto fulminante.

## 🫀 P_BPXO (Presión Arterial)
* **`BPXOSY1` (Presión arterial sistólica)** y **`BPXODI1` (Diastólica)**: La hipertensión no controlada daña los vasos sanguíneos silenciosamente, siendo la principal causa de accidentes cerebrovasculares (strokes) e insuficiencia cardíaca.

## 🩸 P_DIQ (Diabetes - Cuestionario)
* **`DIQ010` (Diagnóstico de diabetes)**: La diabetes mal controlada acelera el envejecimiento celular, daña los riñones, ojos y el corazón vascular, reduciendo la esperanza de vida en varios años.

## 🧪 Laboratorios (Metabolismo y Riesgo Cardiovascular)
* **`LBXGH` (Glicohemoglobina - P_GHB)**: Refleja el nivel medio de glucosa en sangre en los últimos 3 meses. Es el estándar de oro para medir el control glucémico.
* **`LBDHDD` (Colesterol HDL - P_HDL)**: Conocido como colesterol "bueno". Niveles altos tienen un efecto protector comprobado sobre el sistema cardiovascular.
* **`LBDLDL` (Colesterol LDL - P_TRIGLY)**: El colesterol "malo". Niveles elevados causan aterosclerosis, tapando las arterias e incrementando fuertemente el riesgo de eventos coronarios.
* **`LBXTR` (Triglicéridos - P_TRIGLY)**: Otro marcador de grasa en sangre fuertemente asociado a riesgo cardiovascular y resistencia a la insulina.

## 🏥 P_MCQ (Condiciones Médicas Previas)
* **`MCQ160` (Historial de enfermedades cardíacas)**: Las variables de esta serie cubren diagnósticos previos de infarto, angina y stroke. El antecedente de daño cardíaco merma significativamente la expectativa de vida futura.
* **`MCQ220` (Diagnóstico de cáncer)**: El cáncer activo o en remisión es una de las principales causas directas de mortalidad.

## 🏃‍♂️ P_PAQ (Actividad Física)
* **`PAQ650` (Actividad física vigorosa/moderada)**: El ejercicio cardiovascular regular fortalece el miocardio, reduce la resistencia a la insulina y prolonga la vida saludable.
* **`PAD680` (Minutos diarios de sedentarismo)**: Un estilo de vida extremadamente sedentario es considerado un factor de riesgo independiente tan grave como el tabaquismo para la mortalidad prematura.

## 😴 P_SLQ (Trastornos del Sueño)
* **`SLD012` (Horas de sueño estimadas)**: Dormir menos de 6 horas o más de 9 horas de forma crónica está asociado a deterioro metabólico, estrés cardiovascular y mayor riesgo de mortalidad temprana.
* **`SLQ030` / `SLQ040` (Ronquidos / Apnea del sueño)**: La apnea del sueño genera hipoxia nocturna recurrente, disparando la presión arterial y el riesgo de arritmias fatales durante el sueño.

## 🚬 P_SMQ (Tabaquismo)
* **`SMQ040` (Fuma actualmente)** y **`SMD057` (Número de cigarrillos diarios)**: El tabaquismo es la principal causa prevenible de muerte en el mundo (cáncer de pulmón, EPOC, enfisema, infartos).

## 🔬 P_BIOPRO (Perfil Bioquímico Estándar)
* **`LBXSCR` (Creatinina)** y **`LBXSBU` (BUN)**: Biomarcadores críticos de la función renal. La falla renal crónica disminuye aceleradamente la esperanza de vida si no se detecta a tiempo.
* **`LBXSATSI` (ALT)** y **`LBXSASSI` (AST)**: Enzimas hepáticas. Su elevación crónica indica inflamación y daño al hígado (hígado graso, cirrosis).
* **`LBXSAL` (Albúmina)**: Es un indicador general del estado nutricional y de síntesis hepática. Niveles séricos bajos (especialmente en adultos mayores) son un fortísimo predictor independiente de mortalidad a corto/mediano plazo.

---

### Siguientes Pasos (Implementación Kedro)
Al desarrollar la canalización (*pipeline*) de datos, nuestro objetivo en el nodo de limpieza será extraer exactamente estas columnas listadas, unir los datasets a través del identificador `SEQN`, y tratar los valores nulos (NaN) para maximizar la calidad predictiva del modelo final.
