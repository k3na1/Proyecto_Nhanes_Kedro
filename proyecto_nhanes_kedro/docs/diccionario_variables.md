# Diccionario de Variables - Proyecto NHANES (Ciclo 2017-2020)

Este documento contiene la descripción detallada, rangos de valores y codificaciones de los datasets de la capa intermedia para el proyecto **NHANES Kedro**. Utiliza este diccionario para guiar tus análisis exploratorios, procesos de imputación y tratamiento de outliers.

---

## 📌 Índice de Datasets
* 📊 [P_DEMO (Demografía)](#-p_demo-demografía)
* 🍺 [P_ALQ (Uso de Alcohol)](#-p_alq-uso-de-alcohol)
* 📏 [P_BMX (Medidas Corporales)](#-p_bmx-medidas-corporales)
* 🫀 [P_BPXO (Presión Arterial - Oscilométrica)](#-p_bpxo-presión-arterial---oscilométrica)
* 🩸 [P_DIQ (Diabetes)](#-p_diq-diabetes)
* 🧪 [Laboratorios de Sangre (P_GHB, P_HDL, P_TCHOL, P_TRIGLY)](#-laboratorios-de-sangre-p_ghb-p_hdl-p_tchol-p_trigly)
* 🏥 [P_MCQ (Condiciones Médicas)](#-p_mcq-condiciones-médicas)
* 🏃‍♂️ [P_PAQ (Actividad Física)](#-p_paq-actividad-física)
* 😴 [P_SLQ (Trastornos del Sueño)](#-p_slq-trastornos-del-sueño)
* 🚬 [P_SMQ (Tabaquismo - Uso de Cigarrillos)](#-p_smq-tabaquismo---uso-de-cigarrillos)
* 🔬 [P_BIOPRO (Perfil Bioquímico Estándar)](#-p_biopro-perfil-bioquímico-estándar)

---

## 📊 P_DEMO (Demografía)

| Variable | Tipo de Dato | Descripción | Codificación de Valores |
| :--- | :--- | :--- | :--- |
| **SEQN** | Identificador | Número de identidad único del participante. | Numérico continuo |
| **SDDSRVYR** | Categórica | Ciclo de datos de la encuesta. | `66` = NHANES 2017-2020 |
| **RIDSTATR** | Categórica | Estado de la entrevista o examen. | `1` = Solo entrevistado<br>`2` = Entrevistado y examinado en MEC |
| **RIAGENDR** | Categórica | Género del participante. | `1` = Masculino<br>`2` = Femenino |
| **RIDAGEYR** | Continua | Edad del participante al momento del screening. | Rango: `0` a `79` años<br>`80` = 80 años o más |
| **RIDAGEMN** | Continua | Edad en meses para participantes de 0 a 24 meses. | Rango: `0` a `24`<br>`.` = Faltante / No aplica |
| **RIDRETH1** | Categórica | Raza u origen hispano (agrupación básica). | `1` = Mexicano Americano<br>`2` = Otro Hispano<br>`3` = Blanco no hispano<br>`4` = Negro no hispano<br>`5` = Otra raza/multirracial |
| **RIDRETH3** | Categórica | Raza u origen hispano (detallado). | Igual a RIDRETH1 pero añade:<br>`6` = Asiático no hispano |
| **RIDEXMON** | Categórica | Semestre de examen (período del año). | `1` = Noviembre 1 a Abril 30<br>`2` = Mayo 1 a Octubre 31 |
| **DMDBORN4** | Categórica | País de nacimiento del participante. | `1` = Nacido en los 50 estados de EE.UU./DC<br>`2` = Otros países<br>`77` = Se negó<br>`99` = No sabe |
| **DMDYRUSZ** | Categórica | Rango de tiempo que ha vivido en EE.UU. | `1` = < 5 años<br>`2` = 5 a < 15 años<br>`3` = 15 a < 30 años<br>`4` = 30 años o más<br>`77` = Se negó<br>`99` = No sabe |
| **DMDEDUC2** | Categórica | Nivel máximo de educación (adultos 20+). | `1` = < 9no grado<br>`2` = 9-11mo grado<br>`3` = Graduado de secundaria/GED<br>`4` = Algo de universidad o grado técnico (AA)<br>`5` = Graduado universitario o más<br>`7` = Se negó<br>`9` = No sabe |
| **DMDMARTZ** | Categórica | Estado civil del participante. | `1` = Casado / Viviendo en pareja<br>`2` = Viudo, Divorciado o Separado<br>`3` = Nunca casado<br>`77` = Se negó<br>`99` = No sabe |
| **RIDEXPRG** | Categórica | Estado de embarazo en el examen (12-59 años). | `1` = Sí<br>`2` = No<br>`3` = No se pudo determinar |
| **SIALANG** / **FIALANG** / **MIALANG** | Categórica | Idioma utilizado en los cuestionarios (Paciente / Familia / MEC). | `1` = Inglés<br>`2` = Español |
| **SIAPROXY** / **FIAPROXY** / **MIAPROXY** | Categórica | Indica si el cuestionario fue respondido por un tercero (Proxy). | `1` = Sí<br>`2` = No |
| **SIAINTRP** / **FIAINTRP** / **MIAINTRP** | Categórica | Indica si se requirió la ayuda de un intérprete. | `1` = Sí<br>`2` = No |
| **AIALANGA** | Categórica | Idioma utilizado en la computadora autoadministrada (ACASI). | `1` = Inglés<br>`2` = Español<br>`3` = Lenguas asiáticas |
| **WTINTPRP** / **WTMECPRP** | Continua | Ponderaciones del diseño muestral (entrevista y MEC). | Rangos numéricos continuos |
| **SDMVPSU** / **SDMVSTRA** | Continua | Unidades primarias de muestreo y estratos para cálculo de varianza. | Rangos numéricos |
| **INDFMPIR** | Continua | Ratio entre ingresos familiares y el umbral de pobreza de EE.UU. | Rango: `0` a `4.98`<br>`5.00` = Valores mayores o iguales a 5.00 |

---

## 🍺 P_ALQ (Uso de Alcohol)

| Variable | Tipo | Descripción | Codificación de Valores |
| :--- | :--- | :--- | :--- |
| **SEQN** | Identificador | Número de identidad único. | Numérico continuo |
| **ALQ111** | Categórica | ¿Alguna vez ha tomado una bebida alcohólica? | `1` = Sí<br>`2` = No<br>`7` = Se negó<br>`9` = No sabe |
| **ALQ121** | Categórica | Frecuencia de consumo de alcohol en los últimos 12 meses. | `0` = Nunca en el último año<br>`1` = Todos los días<br>`2` = Casi todos los días<br>`3` = 3 a 4 veces/semana<br>`4` = 2 veces/semana<br>`5` = Una vez/semana<br>`6` = 2 a 3 veces/mes<br>`7` = Una vez/mes<br>`8` = 7 a 11 veces/año<br>`9` = 3 a 6 veces/año<br>`10` = 1 a 2 veces/año<br>`77` = Se negó<br>`99` = No sabe |
| **ALQ130** | Continua | Número promedio de bebidas alcohólicas diarias en los últimos 12 meses. | Rango: `1` a `13` tragos<br>`15` = 15 tragos o más<br>`777` = Se negó<br>`999` = No sabe |
| **ALQ142** / **ALQ270** / **ALQ280** / **ALQ290** | Categórica | Frecuencia de consumo de grandes cantidades de alcohol (4 o 5 tragos en 2 horas, 8+, 12+ tragos). | Igual a la escala de **ALQ121** |
| **ALQ151** | Categórica | ¿Alguna vez ha tomado 4 (mujeres) o 5 (hombres) bebidas alcohólicas casi todos los días? | `1` = Sí<br>`2` = No<br>`7` = Se negó<br>`9` = No sabe |
| **ALQ170** | Continua | Número de veces en las que tomó 4 o 5 bebidas en una misma ocasión en los últimos 30 días. | Rango: `0` a `20` ocasiones<br>`30` = Más de 20 veces al mes<br>`777` = Se negó<br>`999` = No sabe |

---

## 📏 P_BMX (Medidas Corporales)

| Variable | Tipo | Descripción | Rango de Valores y Comentarios |
| :--- | :--- | :--- | :--- |
| **SEQN** | Identificador | Número de identidad del participante. | Numérico |
| **BMDSTATS** | Categórica | Estado de la toma de medidas corporales. | `1` = Datos completos para la edad<br>`2` = Datos parciales (solo peso/altura)<br>`3` = Otro examen parcial<br>`4` = Sin datos |
| **BMXWT** | Continua | Peso corporal en kilogramos (kg). | Rango: `3.2` a `254.3` kg |
| **BMIWT** | Categórica | Comentario u observación sobre el peso. | `1` = No se pudo obtener<br>`3` = Llevaba ropa<br>`4` = Aparato médico |
| **BMXRECUM** | Continua | Longitud recostado en centímetros (para menores). | Rango: `49.1` a `113.9` cm |
| **BMIRECUM** | Categórica | Comentario sobre la longitud recostado. | `1` = No se pudo obtener<br>`3` = El niño no estaba completamente estirado |
| **BMXHEAD** | Continua | Circunferencia de la cabeza en centímetros. | Rango: `32.4` a `48.3` cm |
| **BMIHEAD** | Categórica | Comentario sobre la medida de la cabeza. | `1` = No se pudo obtener |
| **BMXHT** | Continua | Altura de pie en centímetros. | Rango: `78.3` a `199.6` cm |
| **BMIHT** | Categórica | Comentario sobre la altura de pie. | `1` = No se pudo obtener<br>`3` = El participante no estaba recto |
| **BMXBMI** | Continua | Índice de Masa Corporal (IMC) en kg/m². | Rango: `11.9` a `92.3` |
| **BMDBMIC** | Categórica | Categoría de percentil de IMC (niños y adolescentes 2-19 años). | `1` = Bajo peso<br>`2` = Peso normal<br>`3` = Sobrepeso<br>`4` = Obesidad |
| **BMXLEG** | Continua | Longitud de la parte superior de la pierna en cm. | Rango: `24.8` a `55.0` cm |
| **BMILEG** | Categórica | Comentario sobre la longitud de la pierna. | `1` = No se pudo obtener |
| **BMXARML** | Continua | Longitud del brazo en centímetros. | Rango: `9.4` a `49.9` cm |
| **BMIARML** | Categórica | Comentario sobre la longitud del brazo. | `1` = No se pudo obtener |
| **BMXARMC** | Continua | Circunferencia del brazo en centímetros. | Rango: `11.2` a `64.5` cm |
| **BMIARMC** | Categórica | Comentario sobre la circunferencia del brazo. | `1` = No se pudo obtener |
| **BMXWAIST** | Continua | Circunferencia de la cintura en centímetros. | Rango: `40.0` a `187.5` cm |
| **BMIWAIST** | Categórica | Comentario sobre la medida de la cintura. | `1` = No se pudo obtener |
| **BMXHIP** | Continua | Circunferencia de la cadera en centímetros. | Rango: `62.5` a `187.5` cm |
| **BMIHIP** | Categórica | Comentario sobre la medida de la cadera. | `1` = No se pudo obtener |

---

## 🫀 P_BPXO (Presión Arterial - Oscilométrica)

> [!NOTE]
> Estas mediciones se realizan de forma consecutiva mediante un dispositivo oscilométrico automático. 

| Variable | Tipo | Descripción | Rango de Valores y Comentarios |
| :--- | :--- | :--- | :--- |
| **SEQN** | Identificador | Número de identidad. | Numérico |
| **BPAOARM** | Categórica | Brazo seleccionado para la medición. | `L` = Brazo izquierdo<br>`R` = Brazo derecho |
| **BPAOCSZ** | Categórica | Tamaño del manguito inflable utilizado. | `2` = Pequeño (17-21.9 cm)<br>`3` = Adulto (22-31.9 cm)<br>`4` = Grande (32-41.9 cm)<br>`5` = Muslo (42-50.0 cm) |
| **BPXOSY1** / **BPXOSY2** / **BPXOSY3** | Continua | Presión arterial sistólica en mmHg (Lecturas 1, 2 y 3). | Rango continuo, ej. Lectura 1: `52` a `225` mmHg |
| **BPXODI1** / **BPXODI2** / **BPXODI3** | Continua | Presión arterial diastólica en mmHg (Lecturas 1, 2 y 3). | Rango continuo, ej. Lectura 1: `31` a `151` mmHg |
| **BPXOPLS1** / **BPXOPLS2** / **BPXOPLS3** | Continua | Frecuencia del pulso en latidos por minuto (Lecturas 1, 2 y 3). | Rango continuo, ej. Lectura 1: `34` a `142` lpm |

---

## 🩸 P_DIQ (Diabetes)

| Variable | Tipo | Descripción | Codificación de Valores |
| :--- | :--- | :--- | :--- |
| **SEQN** | Identificador | Número de identidad. | Numérico |
| **DIQ010** | Categórica | ¿Alguna vez le ha dicho un médico que tiene diabetes? | `1` = Sí<br>`2` = No<br>`3` = Borderline (En el límite)<br>`7` = Se negó<br>`9` = No sabe |
| **DID040** | Continua | Edad en la que fue diagnosticado con diabetes. | Rango: `1` a `79` años<br>`80` = 80 o más años<br>`666` = Menos de 1 año<br>`777` = Se negó<br>`999` = No sabe |
| **DIQ160** | Categórica | ¿Alguna vez le han dicho que tiene prediabetes? | `1` = Sí<br>`2` = No<br>`7` = Se negó<br>`9` = No sabe |
| **DIQ180** / **DIQ050** / **DIQ070** / **DIQ240** / **DIQ275** | Categórica | Preguntas de control (Examen de sangre, uso de insulina, toma de pastillas, único médico especialista, prueba de A1C en el último año). | `1` = Sí<br>`2` = No<br>`7` = Se negó<br>`9` = No sabe |
| **DID060** | Continua | ¿Cuánto tiempo lleva usando insulina? | Rango: `1` a `59`<br>`666` = Menos de 1 mes<br>`777` = Se negó<br>`999` = No sabe |
| **DIQ060U** | Categórica | Unidad de tiempo para el uso de insulina. | `1` = Meses<br>`2` = Años |
| **DIQ230** | Categórica | ¿Hace cuánto tiempo vio a su especialista en diabetes? | `1` = 1 año o menos<br>`2` = >1 a 2 años<br>`3` = >2 a 5 años<br>`4` = >5 años<br>`5` = Nunca<br>`7` = Se negó<br>`9` = No sabe |
| **DID250** | Continua | Veces en los últimos 12 meses que vio a un médico por su diabetes. | Rango: `1` a `40`<br>`0` = Ninguna<br>`7777` = Se negó<br>`9999` = No sabe |
| **DID260** / **DID350** | Continua | Frecuencia de chequeo personal de azúcar (glucosa) / revisión de pies. | Rangos numéricos continuos según unidad |
| **DIQ260U** / **DIQ350U** | Categórica | Unidad de frecuencia de chequeo (glucosa / pies). | `1` = Por día<br>`2` = Por semana<br>`3` = Por mes<br>`4` = Por año |
| **DIQ280** | Continua | Último valor de Glicohemoglobina (A1C) registrado por su médico. | Rango continuo: `2.3` a `16.0`<br>`777` = Se negó<br>`999` = No sabe |
| **DIQ291** | Categórica | Meta ideal de nivel A1C recomendada por su médico. | `1` = < 6%<br>`2` = < 7%<br>`3` = < 8%<br>`4` = < 9%<br>`5` = < 10%<br>`6` = El médico no especificó meta<br>`77` = Se negó<br>`99` = No sabe |
| **DIQ300S** / **DIQ300D** | Continua | Presión arterial sistólica / diastólica más reciente informada al paciente. | Rangos numéricos continuos de presión |
| **DID310S** / **DID310D** / **DID330** | Continua | Nivel ideal meta de presión (sistólica/diastólica) o colesterol LDL. | Rangos numéricos continuos (mmHg / mg/dL)<br>`6666` = No especificó meta |
| **DID320** | Continua | Valor más reciente de colesterol LDL conocido por el paciente. | Rango: `8` a `340` mg/dL<br>`5555` = Nunca ha oído de LDL<br>`6666` = Nunca se ha hecho la prueba |
| **DID341** | Continua | Número de veces en el último año que un médico le revisó los pies. | Rango: `1` a `106` veces<br>`0` = Ninguna vez |
| **DIQ360** | Categórica | ¿Cuándo fue su último examen de fondo de ojo con pupilas dilatadas? | `1` = < 1 mes<br>`2` = 1-12 meses<br>`3` = 13-24 meses<br>`4` = > 2 años<br>`5` = Nunca |
| **DIQ080** | Categórica | ¿Le ha dicho un médico que la diabetes afectó sus ojos (retinopatía)? | `1` = Sí<br>`2` = No<br>`7` = Se negó<br>`9` = No sabe |

---

## 🧪 Laboratorios de Sangre (P_GHB, P_HDL, P_TCHOL, P_TRIGLY)

> [!NOTE]
> Estas variables representan resultados directos obtenidos de los exámenes químicos de las muestras de sangre. Son exclusivamente variables continuas con alta densidad informativa.

### 🧪 P_GHB (Glicohemoglobina)
* **LBXGH**: Porcentaje (%) de Glicohemoglobina en sangre. (Rango: `2.8` a `16.2` %).

### 🧪 P_HDL (Colesterol HDL)
* **LBDHDD**: Colesterol HDL en mg/dL. (Rango: `5` a `189` mg/dL).
* **LBDHDDSI**: Colesterol HDL en unidades internacionales (mmol/L). (Rango: `0.13` a `4.89` mmol/L).

### 🧪 P_TCHOL (Colesterol Total)
* **LBXTC**: Colesterol Total en mg/dL. (Rango: `71` a `446` mg/dL).
* **LBDTCSI**: Colesterol Total en unidades internacionales (mmol/L). (Rango: `1.84` a `11.53` mmol/L).

### 🧪 P_TRIGLY (Triglicéridos y LDL Calculado)
* **LBXTR**: Triglicéridos en sangre en mg/dL. (Rango: `10` a `2684` mg/dL).
* **LBDTRSI**: Triglicéridos en unidades internacionales (mmol/L). (Rango: `0.11` a `30.3` mmol/L).
* **LBDLDL**: Colesterol LDL calculado mediante la fórmula de Friedewald en mg/dL. (Rango: `10` a `350` mg/dL).

---

## 🏥 P_MCQ (Condiciones Médicas)

| Variable | Tipo | Descripción | Codificación de Valores |
| :--- | :--- | :--- | :--- |
| **SEQN** | Identificador | Número de identidad. | Numérico |
| **MCQ010**, **MCQ035**, **MCQ040**, **MCQ050**, **AGQ030**, **MCQ053**, **MCQ080**, **MCQ092**, **MCQ149**, **MCQ160** *(a a l, p)*, **MCQ170m**, **MCQ170l**, **MCQ500**, **MCQ520**, **MCQ540**, **MCQ550**, **MCQ560**, **MCQ220**, **MCQ300** *(a, b, c)*, **MCQ366** *(a a d)*, **MCQ371** *(a a d)*, **OSQ230** | Categórica | Preguntas binarias sobre enfermedades diagnosticadas (Asma, alergias, sobrepeso, artritis, problemas cardíacos, hepáticos, cáncer, antecedentes familiares, etc.). | `1` = Sí<br>`2` = No<br>`7` = Se negó<br>`9` = No sabe |
| **MCQ025**, **MCD180** *(b, c, d, e, f, m, l)*, **MCQ570** | Continua | Edad aproximada a la que se diagnosticó la enfermedad o se realizó el procedimiento médico. | Rango: `1` a `79` años<br>`80` = 80 años o más<br>`77777` = Se negó<br>`99999` = No sabe |
| **MCD093** | Categórica | Año en el que el paciente recibió su primera transfusión de sangre. | `1` = Antes de 1972<br>`2` = 1972 a 1991<br>`3` = 1992 al presente |
| **MCQ151** | Continua | Edad en la que ocurrió el primer período menstrual (menarquía). | Rango: `7` a `11` años (escala reducida) |
| **RHD018** | Continua | Meses aproximados de edad de menarquía. | Rango continuo de meses: `86` a `142` meses |
| **MCQ195** | Categórica | Tipo de artritis diagnosticada. | `1` = Osteoartritis<br>`2` = Artritis reumatoide<br>`3` = Artritis psoriásica<br>`4` = Otro tipo |
| **MCQ510a** a **MCQ510f** | Categórica | Subtipos específicos de afecciones del hígado diagnosticadas. | `1` = Hígado graso (esteatosis)<br>`2` = Fibrosis hepática<br>`3` = Cirrosis<br>`4` = Hepatitis viral<br>`5` = Hepatitis autoinmune<br>`6` = Otro tipo |
| **MCQ530** | Categórica | Zona anatómica donde se concentra el dolor abdominal recurrente. | `1` = Cuadrante superior derecho<br>`2` = Zona superior media (epigastrio)<br>`3` = Cuadrante superior izquierdo |
| **MCQ230a** / **MCQ230b** / **MCQ230c** | Categórica | Tipos de cáncer diagnosticados. | `10` al `39` = Códigos de tipos de cáncer (ej. 14=Mama, 16=Colon)<br>`66` = Más de 3 tipos de cáncer |

---

## 🏃‍♂️ P_PAQ (Actividad Física)

| Variable | Tipo | Descripción | Rango de Valores y Comentarios |
| :--- | :--- | :--- | :--- |
| **SEQN** | Identificador | Número de identidad. | Numérico |
| **PAQ605** / **PAQ620** / **PAQ635** / **PAQ650** / **PAQ665** | Categórica | ¿Realiza actividades de intensidad vigorosa o moderada en su trabajo, tiempo libre o transporte? | `1` = Sí<br>`2` = No<br>`7` = Se negó a responder<br>`9` = No sabe |
| **PAQ610** / **PAQ625** / **PAQ640** / **PAQ655** / **PAQ670** | Continua | Número de días a la semana en los que realiza dicha actividad física. | Rango: `1` a `7` días a la semana |
| **PAD615** / **PAD630** / **PAD645** / **PAD660** / **PAD675** / **PAD680** | Continua | Minutos dedicados en promedio a la actividad física vigorosa/moderada, o minutos diarios de sedentarismo. | Rango en minutos: `10` a `840` minutos al día |

---

## 😴 P_SLQ (Trastornos del Sueño)

| Variable | Tipo | Descripción | Rango de Valores y Comentarios |
| :--- | :--- | :--- | :--- |
| **SEQN** | Identificador | Número de identidad. | Numérico |
| **SLQ300** / **SLQ310** / **SLQ320** / **SLQ330** | Hora | Horas estimadas en las que el paciente suele acostarse y despertarse (días hábiles y fines de semana). | Formato de hora `HH:MM` de 24 horas |
| **SLD012** / **SLD013** | Continua | Total de horas de sueño calculadas para días laborables y libres. | Rango: `3` a `13.5` horas de sueño<br>`2` = Menos de 3 horas<br>`14` = 14 horas o más |
| **SLQ030** / **SLQ040** | Categórica | Frecuencia de ronquidos fuertes o episodios de apnea (dejar de respirar al dormir). | `0` = Nunca<br>`1` = Rara vez (1-2 noches por semana)<br>`2` = Ocasionalmente (3-4 noches por semana)<br>`3` = Frecuentemente (5 o más noches por semana) |
| **SLQ050** | Categórica | ¿Alguna vez le ha mencionado a un médico sus dificultades para conciliar o mantener el sueño? | `1` = Sí<br>`2` = No |
| **SLQ120** | Categórica | Frecuencia con la que siente excesiva somnolencia durante el día. | `0` = Nunca<br>`1` = Rara vez (1 vez al mes)<br>`2` = A veces (2-4 veces al mes)<br>`3` = A menudo (5-15 veces al mes)<br>`4` = Casi siempre (16-30 veces al mes) |

---

## 🚬 P_SMQ (Tabaquismo - Uso de Cigarrillos)

| Variable | Tipo | Descripción | Rango de Valores y Comentarios |
| :--- | :--- | :--- | :--- |
| **SEQN** | Identificador | Número de identidad. | Numérico |
| **SMQ020** / **SMQ670** | Categórica | ¿Ha fumado al menos 100 cigarrillos en su vida? / ¿Ha intentado dejar de fumar en el último año? | `1` = Sí<br>`2` = No |
| **SMD030** | Continua | Edad aproximada a la que empezó a fumar regularmente. | Rango: `7` a `76` años<br>`0` = Nunca fumó de forma regular |
| **SMQ040** | Categórica | ¿Fuma cigarrillos actualmente? | `1` = Todos los días<br>`2` = Algunos días<br>`3` = En absoluto |
| **SMQ050Q** | Continua | Cantidad de tiempo que ha transcurrido desde que dejó de fumar completamente. | Rango continuo: `1` a `366` unidades<br>`66666` = 50 años o más |
| **SMQ050U** | Categórica | Unidad de medida del tiempo transcurrido desde que dejó de fumar. | `1` = Días<br>`2` = Semanas<br>`3` = Meses<br>`4` = Años |
| **SMD057** / **SMD650** | Continua | Número promedio de cigarrillos que fuma o fumaba al día. | Rango: `2` a `90` cigarrillos diarios<br>`1` = 1 o menos cigarrillos al día<br>`95` = 95 o más cigarrillos al día |
| **SMQ078** | Categórica | Tiempo transcurrido desde que se despierta hasta que fuma su primer cigarrillo. | `1` = Dentro de los primeros 5 minutos<br>`2` = De 6 a 30 minutos<br>`3` = De 31 minutos a 1 hora<br>`4` = De 1 a 2 horas<br>`5` = De 2 a 3 horas<br>`6` = De 3 a 4 horas<br>`7` = Más de 4 horas |
| **SMD641** | Continua | Número de días que fumó cigarrillos en los últimos 30 días. | Rango: `0` a `30` días |
| **SMD100MN** | Categórica | ¿Su marca de cigarrillos habitual es o era mentolada? | `0` = No mentolado<br>`1` = Mentolado |
| **SMQ621** | Categórica | Total de cigarrillos consumidos a lo largo de su vida (escala detallada para jóvenes). | `1` = Nunca frotó/fumó<br>`2` = 1 o más pitadas pero nunca un cigarrillo entero<br>`3` = 1 cigarrillo completo<br>`4` = 2 a 5 cigarrillos<br>`5` = 6 a 15 cigarrillos<br>`6` = 16 a 25 cigarrillos<br>`7` = 26 a 99 cigarrillos<br>`8` = 100 o más cigarrillos |
| **SMD630** | Continua | Edad a la que fumó su primer cigarrillo completo. | Rango: `8` a `17` años<br>`6` = 6 años o menos |
| **SMAQUEX2** | Categórica | Modalidad en la que se aplicó el cuestionario de tabaquismo. | `1` = Entrevista personal en el hogar<br>`2` = Computadora privada autoadministrada (ACASI) |

---

## 🔬 P_BIOPRO (Perfil Bioquímico Estándar)

> [!TIP]
> **Perfil Bioquímico:** Prácticamente la totalidad de este dataset consiste en mediciones de laboratorio bioquímico continuas. Las variables que comienzan con `LBD` suelen ser conversiones en unidades internacionales (SI) o códigos de control analítico (`LC`).

| Variable | Tipo | Parámetro Analizado | Rango de Valores y Comentarios |
| :--- | :--- | :--- | :--- |
| **SEQN** | Identificador | Número de identidad único. | Numérico |
| **LBXSATSI** | Continua | ALT (Alanina aminotransferasa) en U/L | Rango: `2` a `682` U/L |
| **LBDSATLC** | Categórica | Código comentario para ALT (Límites de detección) | `0` = En o por encima del límite inferior de detección<br>`1` = Por debajo del límite inferior |
| **LBXSAL** | Continua | Albúmina en g/dL | Rango: `2.1` a `5.4` g/dL |
| **LBDSALSI** | Continua | Albúmina en g/L (SI) | Rango: `21` a `54` g/L |
| **LBXSAPSI** | Continua | ALP (Fosfatasa alcalina) en U/L | Rango: `16` a `638` U/L |
| **LBXSASSI** | Continua | AST (Aspartato aminotransferasa) en U/L | Rango: `6` a `489` U/L |
| **LBXSC3SI** | Continua | Bicarbonato en mmol/L | Rango: `14` a `38` mmol/L |
| **LBXSBU** | Continua | Nitrógeno ureico en sangre (BUN) en mg/dL | Rango: `2` a `79` mg/dL |
| **LBDSBUSI** | Continua | Nitrógeno ureico en sangre (BUN) en mmol/L (SI) | Rango: `0.71` a `28.2` mmol/L |
| **LBXSCLSI** | Continua | Cloruro en mmol/L | Rango: `84` a `117` mmol/L |
| **LBXSCK** | Continua | CPK (Creatina fosfocinasa) en U/L | Rango: `11` a `16,959` U/L |
| **LBXSCR** | Continua | Creatinina sérica en mg/dL | Rango: `0.25` a `14.97` mg/dL |
| **LBDSCRSI** | Continua | Creatinina sérica en umol/L (SI) | Rango: `22.1` a `1,323.35` umol/L |
| **LBXSGB** | Continua | Globulina sérica en g/dL | Rango: `1.3` a `6.0` g/dL |
| **LBDSGBSI** | Continua | Globulina sérica en g/L (SI) | Rango: `13` a `60` g/L |
| **LBXSGL** | Continua | Glucosa sérica en mg/dL | Rango: `39` a `626` mg/dL |
| **LBDSGLSI** | Continua | Glucosa sérica en mmol/L (SI) | Rango: `2.16` a `34.75` mmol/L |
| **LBXSGTSI** | Continua | GGT (Gamma-glutamil transferasa) en U/L | Rango: `2` a `2,394` U/L |
| **LBDSGTLC** | Categórica | Código comentario para GGT (Límites de detección) | `0` = Nivel detectable normal<br>`1` = Por debajo del límite analítico |
| **LBXSIR** | Continua | Hierro sérico en ug/dL | Rango: `8` a `476` ug/dL |
| **LBDSIRSI** | Continua | Hierro sérico en umol/L (SI) | Rango: `1.4` a `85.3` umol/L |
| **LBXSLDSI** | Continua | LDH (Lactato deshidrogenasa) en U/L | Rango: `49` a `779` U/L |
| **LBXSOSSI** | Continua | Osmolalidad sérica calculada en mmol/kg | Rango: `246` a `314` mmol/kg |
| **LBXSPH** | Continua | Fósforo sérico en mg/dL | Rango: `1.6` a `9.6` mg/dL |
| **LBDSPHSI** | Continua | Fósforo sérico en mmol/L (SI) | Rango: `0.517` a `3.10` mmol/L |
| **LBXSKSI** | Continua | Potasio sérico en mmol/L | Rango: `2.6` a `7.1` mmol/L |
| **LBXSNASI** | Continua | Sodio sérico en mmol/L | Rango: `121` a `151` mmol/L |
| **LBXSTB** | Continua | Bilirrubina sérica total en mg/dL | Rango: `0.1` a `3.8` mg/dL |
| **LBDSTBSI** | Continua | Bilirrubina sérica total en umol/L (SI) | Rango: `1.71` a `64.98` umol/L |
| **LBDSTBLC** | Categórica | Código comentario para Bilirrubina (Límites de detección) | `0` = Nivel detectable normal<br>`1` = Por debajo del límite analítico |
| **LBXSCA** | Continua | Calcio sérico total en mg/dL | Rango: `6.4` a `12.3` mg/dL |
| **LBDSCASI** | Continua | Calcio sérico total en mmol/L (SI) | Rango: `1.60` a `3.075` mmol/L |
| **LBXSCH** | Continua | Colesterol total sérico en mg/dL | Rango: `72` a `438` mg/dL |
| **LBDSCHSI** | Continua | Colesterol total sérico en mmol/L (SI) | Rango: `1.862` a `11.327` mmol/L |
| **LBXSTP** | Continua | Proteína sérica total en g/dL | Rango: `4.4` a `10.0` g/dL |
| **LBDSTPSI** | Continua | Proteína sérica total en g/L (SI) | Rango: `44` a `100` g/L |
| **LBXSTR** | Continua | Triglicéridos en mg/dL (Perfil Bioquímico) | Rango: `25` a `2,923` mg/dL |
| **LBDSTRSI** | Continua | Triglicéridos en mmol/L (SI) | Rango: `0.282` a `33.001` mmol/L |
| **LBXSUA** | Continua | Ácido úrico en mg/dL | Rango: `0.8` a `15.1` mg/dL |
| **LBDSUASI** | Continua | Ácido úrico en umol/L (SI) | Rango: `47.6` a `898.1` umol/L |
