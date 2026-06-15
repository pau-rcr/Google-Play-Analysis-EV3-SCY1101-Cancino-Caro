# Dashboard Google Play Store - EV3 SCY1101

Programación para la Ciencia de Datos - DuocUC
Paula Caro Romero y Vicente Cancino Riveros

## Descripción

Este repositorio contiene el dashboard interactivo de la Evaluación Parcial 3. Es la
continuación del trabajo hecho en EV1 (limpieza y preprocesamiento del dataset de
Google Play Store) y EV2 (entrenamiento de un Random Forest y de un modelo K-Means
para segmentar el mercado de apps).

El dashboard está hecho con Dash y Plotly, y tiene dos vistas pensadas para
audiencias distintas:

- **Vista Gerencial**: KPIs generales (apps analizadas, rating promedio, % de apps
  gratuitas, reseñas analizadas, sentimiento positivo), distribución de apps por
  categoría, proporción gratis/pago, segmentación de mercado (K-Means) y rating
  promedio por categoría.
- **Vista Técnica**: métricas de los modelos de EV2 (R², MAE, validación cruzada),
  importancia de variables del Random Forest, comparación entre modelos, distribución
  de ratings, correlación entre número de reseñas y rating, análisis de sentimiento
  (NLP) por segmento, y un explorador interactivo que permite filtrar el gráfico de
  reseñas vs rating por categoría y por tipo (gratis/pago).

## Estructura del proyecto

```
EV3-Cancino-Caro/
├── app.py                       # Dashboard (Dash/Plotly)
├── data/
│   ├── data_dashboard.csv       # Apps con clusters, transformaciones y sentimiento
│   ├── feature_importances.csv  # Importancia de variables del Random Forest (EV2)
│   └── model_metrics.csv        # R2, MAE y RMSE de los modelos comparados en EV2
├── requirements.txt
└── README.md
```

## Instalación y ejecución

Crear un entorno virtual (opcional pero recomendado) e instalar las dependencias:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Ejecutar el dashboard:

```
python app.py
```

Abrir en el navegador: http://127.0.0.1:8050

## Datos

- `data_dashboard.csv`: dataset de Google Play Store.
  Tiene 11.096 filas; al cargarlo se eliminan apps duplicadas y quedan 9.628 apps
  únicas, cada una con su cluster asignado (Apps Masivas, Nicho Alta Satisfacción o
  Bajo Rendimiento) y, para 1.079 apps, el porcentaje de reseñas positivas obtenido
  con análisis NLP.
- `feature_importances.csv`: importancia relativa de las variables del Random Forest
  entrenado en EV2 (las 15 más relevantes se muestran en la vista técnica).
- `model_metrics.csv`: R², MAE y RMSE de los tres modelos comparados en EV2.

## Modelos (resultados de EV2)

| Modelo | R² | MAE |
|---|---|---|
| Regresión Lineal | 0.9236 | 0.1866 |
| Random Forest | 0.9240 | 0.1671 |
| Random Forest (CV K=5) | 0.9177 ± 0.004 | - |

El Random Forest se entrenó sobre 173 features (One-Hot Encoding + transformaciones
logarítmicas + escalado con StandardScaler), por lo que el MAE/RMSE están en
desviaciones estándar de esa escala, no en estrellas de rating. El K-Means (K=3) se
validó con el método del codo y el coeficiente de silhouette.

## Integrantes:

- Paula Caro Romero
- Vicente Cancino Riveros
