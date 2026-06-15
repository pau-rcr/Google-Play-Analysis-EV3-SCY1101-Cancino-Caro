# 📊 Google Play Store Analytics Dashboard
## EV3 — SCY1101 Programación para la Ciencia de Datos
**Paula Caro & Vicente Cancino | DuocUC 2025**

---

## 📌 Descripción del Proyecto

Solución analítica **end-to-end** del ecosistema de la Google Play Store. A partir de 10.326 aplicaciones, se construyó un pipeline de análisis que integra **EDA, Machine Learning supervisado y no supervisado, análisis NLP de sentimiento** y un **dashboard interactivo** para apoyar la toma de decisiones en dos audiencias: gerencial y técnica.

**Problema de negocio:** ¿Qué factores determinan el éxito de una aplicación en Google Play Store, y cómo segmentar el mercado para diseñar estrategias diferenciadas?

---

## 🗂️ Estructura del Proyecto

```
google-play-analytics/
├── data/
│   ├── data_dashboard.csv          # Dataset consolidado con clusters
│   ├── feature_importances.csv     # Importancia de variables del modelo
│   └── model_metrics.csv           # Métricas de los modelos (EV2)
├── notebooks/
│   └── EV2_PCDD_Caro_Cancino.ipynb # Análisis EV2: EDA + ML + Clustering
├── dashboards/
│   └── app.py                      # Dashboard Dash/Plotly (EV3)
├── docs/
│   └── README.md                   # Este archivo
└── requirements.txt
```

---

## 🚀 Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/<usuario>/google-play-analytics.git
cd google-play-analytics
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate          # Linux/Mac
# venv\Scripts\activate          # Windows

pip install -r requirements.txt
```

### 3. Ejecutar el dashboard

```bash
cd dashboards
python app.py
```

Abrir en el navegador: **http://localhost:8050**

---

## 📦 Dependencias

Ver `requirements.txt`:

```
dash>=2.14.0
plotly>=5.17.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
statsmodels>=0.14.0
```

---

## 📊 Datasets

| Archivo | Descripción | Filas |
|---|---|---|
| `googleplaystore_clean.csv` | Datos limpios, base de todo | 10,326 |
| `googleplaystore_merged.csv` | Con sentimiento NLP | 1,079 |
| `googleplaystore_ml_ready.csv` | One-Hot + StandardScaler (EV1) | 10,326 × 173 |

---

## 🤖 Modelos ML (EV2)

| Modelo | R² | MAE | Contexto |
|---|---|---|---|
| Regresión Lineal (Baseline) | 0.9236 | 0.1866 | Test 20% |
| Random Forest Regressor | **0.9240** | **0.1671** | Test 20% |
| Random Forest CV K=5 | 0.9177 ± 0.004 | — | Cross-validation |

> Los valores MAE/RMSE están en **desviaciones estándar** (escala StandardScaler).

**Top 3 features predictoras:** `Reviews_Log`, `Size_MB`, `Review_Ratio`

---

## 🔍 Segmentación K-Means (K=3)

| Cluster | Perfil | Estrategia |
|---|---|---|
| **Apps Masivas** | Instalaciones +2σ, reviews altas | Mantener liderazgo, monitorear sentimiento |
| **Nicho Alta Satisfacción** | Sentimiento +2.3σ, instalaciones moderadas | Escalar con menor competencia |
| **Bajo Rendimiento** | Por debajo del promedio | Priorizar: generar reseñas + reducir tamaño |

---

## 📈 Dashboard

El dashboard tiene **dos vistas diferenciadas por audiencia**:

- **Vista Gerencial**: KPIs de negocio, distribución de mercado, segmentación visual, hallazgos clave
- **Vista Técnica**: Feature Importance, comparativa de modelos, explorador interactivo, análisis NLP

---

## 👥 Colaboración (Git)

El repositorio usa el siguiente flujo de trabajo:

- **Branches**: `main`, `feature/dashboard`, `feature/ml-model`, `feature/eda`
- **Issues**: tareas asignadas por integrante
- **Pull Requests**: revisión cruzada antes de merge a `main`

---

## 📚 Referencias

- Google Play Store Dataset: https://www.kaggle.com/datasets/lava18/google-play-store-apps
- Dash Documentation: https://dash.plotly.com
- Scikit-learn: https://scikit-learn.org
