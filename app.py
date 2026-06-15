#EV3: Dashboard Google Play Store Analysis
#Paula Caro Romero y Vicente Cancino Riveros


import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

#Carga de datos
df = pd.read_csv("data/data_dashboard.csv")
df_metrics = pd.read_csv("data/model_metrics.csv")
df_imp = pd.read_csv("data/feature_importances.csv")

# Limpieza básica
df = df.drop_duplicates(subset="App")
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["Installs_M"] = df["Installs"] / 1_000_000
df["Type"] = df["Type"].replace("Unknown", "Free")

# Categorías disponibles
categories = sorted(df["Category"].dropna().unique())

#colores
COLORS = {
    "primary": "#01696f",
    "secondary": "#4f98a3",
    "accent": "#e8af34",
    "bg": "#f7f6f2",
    "surface": "#ffffff",
    "text": "#28251d",
    "muted": "#7a7974",
    "border": "#d4d1ca",
}
CLUSTER_COLORS = {
    "Apps Masivas": "#01696f",
    "Nicho Alta Satisfacción": "#e8af34",
    "Bajo Rendimiento": "#a86fdf",
}
SEQ_PALETTE = px.colors.sequential.Teal

#estilos reutilizados para no repetir el mismo dict en cada fila del layout
KPI_ROW_STYLE = {"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginBottom": "24px"}
ROW_STYLE = {"display": "flex", "gap": "16px", "marginBottom": "16px"}

#KPIs
total_apps = len(df)
avg_rating = df["Rating"].mean()
pct_free = (df["Type"] == "Free").mean() * 100
total_reviews = df["Reviews"].sum()
avg_sentiment = df["pct_positivo"].mean()


def kpi_card(title, value, subtitle="", color=COLORS["primary"]):
    return html.Div([
        html.P(title, style={"margin": 0, "fontSize": "0.78rem", "color": COLORS["muted"],
                              "fontWeight": "600", "textTransform": "uppercase",
                              "letterSpacing": "0.05em"}),
        html.H3(value, style={"margin": "4px 0 2px", "fontSize": "1.9rem",
                               "fontWeight": "700", "color": color}),
        html.P(subtitle, style={"margin": 0, "fontSize": "0.75rem", "color": COLORS["muted"]}),
    ], style={
        "background": COLORS["surface"],
        "borderRadius": "10px",
        "padding": "18px 22px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.07)",
        "flex": "1",
        "minWidth": "160px",
    })


#Layout
app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    title="Google Play Analytics",
    suppress_callback_exceptions=True,  #los IDs de la vista técnica se crean en un callback, no en el layout inicial
)

app.layout = html.Div(style={"fontFamily": "'Segoe UI', sans-serif",
                              "background": COLORS["bg"], "minHeight": "100vh"}, children=[

    #header
    html.Div([
        html.Div([
            html.H1("Google Play Store Analytics",
                    style={"margin": 0, "fontSize": "1.4rem", "fontWeight": "700",
                           "color": COLORS["surface"]}),
            html.P("EV3 · SCY1101 · Paula Caro & Vicente Cancino",
                   style={"margin": "2px 0 0", "fontSize": "0.8rem",
                          "color": "rgba(255,255,255,0.7)"}),
        ]),
        html.Div([
            dcc.Tabs(id="audience-tabs", value="gerencial", children=[
                dcc.Tab(label="Vista Gerencial", value="gerencial",
                        style={"color": "rgba(255,255,255,0.7)", "background": "transparent",
                               "border": "none", "padding": "8px 16px", "fontSize": "0.85rem"},
                        selected_style={"color": "#fff", "background": "rgba(255,255,255,0.15)",
                                        "borderRadius": "6px", "border": "none",
                                        "padding": "8px 16px", "fontSize": "0.85rem",
                                        "fontWeight": "600"}),
                dcc.Tab(label="Vista Técnica", value="tecnica",
                        style={"color": "rgba(255,255,255,0.7)", "background": "transparent",
                               "border": "none", "padding": "8px 16px", "fontSize": "0.85rem"},
                        selected_style={"color": "#fff", "background": "rgba(255,255,255,0.15)",
                                        "borderRadius": "6px", "border": "none",
                                        "padding": "8px 16px", "fontSize": "0.85rem",
                                        "fontWeight": "600"}),
            ], style={"border": "none"}),
        ]),
    ], style={
        "background": COLORS["primary"],
        "padding": "16px 32px",
        "display": "flex",
        "justifyContent": "space-between",
        "alignItems": "center",
        "flexWrap": "wrap",
        "gap": "12px",
    }),

    # el contenido principal
    html.Div(id="main-content", style={"padding": "24px 32px", "maxWidth": "1400px",
                                        "margin": "0 auto"}),
])


#Callbacks
@app.callback(Output("main-content", "children"), Input("audience-tabs", "value"))
def render_content(tab):
    if tab == "gerencial":
        return gerencial_layout()
    return tecnica_layout()


#vista gerencial (público general)
def gerencial_layout():
    return html.Div([

        # KPIs
        html.Div([
            kpi_card("Total Apps Analizadas", f"{total_apps:,}", "Google Play Store"),
            kpi_card("Rating Promedio", f"{avg_rating:.2f} ★", "Escala 1–5"),
            kpi_card("Apps Gratuitas", f"{pct_free:.1f}%", f"{int(total_apps*pct_free/100):,} apps"),
            kpi_card("Reseñas Analizadas",
                     f"{total_reviews/1e6:.1f}M", "Total acumulado"),
            kpi_card("Sentimiento Positivo", f"{avg_sentiment:.1f}%",
                     "1,079 apps con NLP", color=COLORS["accent"]),
        ], style=KPI_ROW_STYLE),

        #fila 1
        html.Div([
            _card("Distribución de Apps por Categoría (Top 15)",
                  dcc.Graph(id="bar-category", figure=fig_bar_category(), config={"displayModeBar": False}),
                  flex=2),
            _card("Gratuitas vs. De Pago",
                  dcc.Graph(id="pie-type", figure=fig_pie_type(), config={"displayModeBar": False}),
                  flex=1),
        ], style=ROW_STYLE),

        # Fila 2
        html.Div([
            _card("Segmentación de Mercado (K-Means, K=3)",
                  dcc.Graph(id="scatter-clusters", figure=fig_clusters(),
                            config={"displayModeBar": False}),
                  flex=2),
            _card("Perfil de Segmentos",
                  dcc.Graph(id="radar-clusters", figure=fig_radar(),
                            config={"displayModeBar": False}),
                  flex=1),
        ], style=ROW_STYLE),

        # Fila 3
        html.Div([
            _card("Rating Promedio por Categoría",
                  dcc.Graph(id="heatmap-rating", figure=fig_rating_category(),
                            config={"displayModeBar": False}), flex=3),
        ], style=ROW_STYLE),
    ])


#  VISTA TÉCNICA
def tecnica_layout():
    return html.Div([

        #KPIs técnicos
        html.Div([
            kpi_card("R² Random Forest (EV2)", "0.9240", "Test set 20%", COLORS["primary"]),
            kpi_card("MAE Random Forest (EV2)", "0.1671", "Desv. estándar escalada", COLORS["secondary"]),
            kpi_card("R² Validación Cruzada K=5", "0.9177 ± 0.004", "Estabilidad confirmada", COLORS["primary"]),
            kpi_card("Clusters K-Means", "K = 3", "Silhouette + Elbow Method", COLORS["accent"]),
            kpi_card("Features del Modelo", "173", "One-Hot + Log transforms", COLORS["secondary"]),
        ], style=KPI_ROW_STYLE),

        #Fila 1 técnica
        html.Div([
            _card("Feature Importance — Top 15 Variables Predictoras",
                  dcc.Graph(id="fi-chart", figure=fig_feature_importance(),
                            config={"displayModeBar": False}), flex=2),
            _card("Comparativa de Modelos (EV2)",
                  dcc.Graph(id="model-compare", figure=fig_model_comparison(),
                            config={"displayModeBar": False}), flex=1),
        ], style=ROW_STYLE),

        #fila 2 técnica
        html.Div([
            _card("Distribución de Ratings",
                  dcc.Graph(id="hist-rating", figure=fig_hist_rating(),
                            config={"displayModeBar": False}), flex=1),
            _card("Correlación: Reseñas vs Rating",
                  dcc.Graph(id="scatter-reviews", figure=fig_scatter_reviews(),
                            config={"displayModeBar": False}), flex=1),
            _card("Análisis de Sentimiento NLP",
                  dcc.Graph(id="sentiment-chart", figure=fig_sentiment(),
                            config={"displayModeBar": False}), flex=1),
        ], style=ROW_STYLE),

        # fila 3 técnica, explorador interactivo
        _card("Explorador Interactivo por Categoría y Tipo",
              html.Div([
                  html.Div([
                      html.Label("Categoría:", style={"fontWeight": "600", "fontSize": "0.85rem",
                                                       "color": COLORS["muted"]}),
                      dcc.Dropdown(
                          id="dd-category",
                          options=[{"label": "Todas", "value": "Todas"}] +
                                  [{"label": c, "value": c} for c in categories],
                          value="Todas",
                          clearable=False,
                          style={"fontSize": "0.85rem"},
                      ),
                  ], style={"flex": 1}),
                  html.Div([
                      html.Label("Tipo:", style={"fontWeight": "600", "fontSize": "0.85rem",
                                                  "color": COLORS["muted"]}),
                      dcc.RadioItems(
                          id="radio-type",
                          options=[{"label": t, "value": t} for t in ["Todos", "Free", "Paid"]],
                          value="Todos",
                          inline=True,
                          inputStyle={"marginRight": "4px"},
                          labelStyle={"marginRight": "16px", "fontSize": "0.85rem"},
                      ),
                  ], style={"flex": 1}),
              ], style={"display": "flex", "gap": "24px", "marginBottom": "16px",
                         "flexWrap": "wrap"}),
              extra=dcc.Graph(id="scatter-explorer", config={"displayModeBar": False})),

        #notita
        html.Div([
            html.H4(" Notas: ",
                    style={"margin": "0 0 10px", "color": COLORS["primary"], "fontSize": "1rem"}),
            html.P([
                "El dataset fue preprocesado en EV1 (limpieza, transformaciones logarítmicas, escalado StandardScaler, OneHotEncoding: 173 features). "
                "En la EV2 se entrenó un Random Forest Regressor (R²=0.9240) y K-Means (K=3, validado con Elbow y silhouette). "
                "Las métricas MAE/RMSE están expresadas en desviaciones estándar (escala StandardScaler). "
                "El análisis NLP de sentimiento cubre 1,079 apps."
            ], style={"fontSize": "0.88rem", "color": COLORS["muted"], "lineHeight": "1.7", "margin": 0}),
        ], style={
            "background": "#f0f4f4", "borderRadius": "10px", "padding": "18px 22px",
            "border": f"1px solid {COLORS['border']}",
        }),
    ])


# callback explorador
@app.callback(
    Output("scatter-explorer", "figure"),
    Input("dd-category", "value"),
    Input("radio-type", "value"),
)
def update_explorer(cat, tipo):
    dff = df.copy()
    if cat != "Todas":
        dff = dff[dff["Category"] == cat]
    if tipo != "Todos":
        dff = dff[dff["Type"] == tipo]
    dff = dff.dropna(subset=["Rating", "Reviews_Log", "Installs_M"])

    fig = px.scatter(
        dff.sample(min(2000, len(dff)), random_state=42),
        x="Reviews_Log", y="Rating",
        color="Cluster_Name",
        color_discrete_map=CLUSTER_COLORS,
        size="Installs_M",
        size_max=30,
        hover_name="App",
        hover_data={"Category": True, "Type": True, "Installs_M": ":.2f",
                    "Reviews_Log": False, "Rating": True, "Cluster_Name": False},
        labels={"Reviews_Log": "Log(Reseñas)", "Rating": "Rating",
                "Cluster_Name": "Segmento", "Installs_M": "Instalaciones (M)"},
        opacity=0.7,
        template="plotly_white",
    )
    fig.update_layout(
        margin=dict(t=10, b=40, l=40, r=20),
        legend=dict(orientation="h", y=-0.15),
        height=360,
        font=dict(size=11),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(showgrid=True, gridcolor="#eee")
    fig.update_yaxes(showgrid=True, gridcolor="#eee")
    return fig


#Gráficos
def fig_bar_category():
    top15 = df["Category"].value_counts().head(15).reset_index()
    top15.columns = ["Category", "Count"]
    fig = px.bar(
        top15.sort_values("Count"),
        x="Count", y="Category",
        orientation="h",
        color="Count",
        color_continuous_scale=SEQ_PALETTE,
        labels={"Count": "N° de Apps", "Category": ""},
        template="plotly_white",
    )
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320,
                      coloraxis_showscale=False, showlegend=False,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(size=11))
    fig.update_xaxes(showgrid=True, gridcolor="#eee")
    fig.update_yaxes(showgrid=False)
    return fig


def fig_pie_type():
    counts = df["Type"].value_counts().reset_index()
    counts.columns = ["Type", "Count"]
    counts = counts[counts["Type"].isin(["Free", "Paid"])]
    fig = px.pie(counts, names="Type", values="Count",
                 color="Type",
                 color_discrete_map={"Free": COLORS["primary"], "Paid": COLORS["accent"]},
                 hole=0.55, template="plotly_white")
    fig.update_traces(textinfo="percent+label", textfont_size=12)
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320,
                      showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                      font=dict(size=11))
    return fig


def fig_clusters():
    dff = df.dropna(subset=["Rating", "Reviews_Log", "Installs_M"])
    sample = dff.sample(min(3000, len(dff)), random_state=42)
    fig = px.scatter(
        sample, x="Reviews_Log", y="Rating",
        color="Cluster_Name",
        color_discrete_map=CLUSTER_COLORS,
        size="Installs_M", size_max=25,
        hover_name="App",
        labels={"Reviews_Log": "Log(Reseñas)", "Rating": "Rating", "Cluster_Name": "Segmento"},
        opacity=0.65, template="plotly_white",
    )
    fig.update_layout(margin=dict(t=10, b=30, l=40, r=20), height=340,
                      legend=dict(orientation="h", y=-0.18, font=dict(size=10)),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(size=11))
    fig.update_xaxes(showgrid=True, gridcolor="#eee")
    fig.update_yaxes(showgrid=True, gridcolor="#eee")
    return fig


def fig_radar():
    profiles = df.groupby("Cluster_Name").agg(
        Rating=("Rating", "mean"),
        Reviews_Log=("Reviews_Log", "mean"),
        Installs_Log=("Installs_Log", "mean"),
        pct_positivo=("pct_positivo", lambda x: x.mean() / 100 * 5),
    ).reset_index()

    categories_r = ["Rating", "Reviews_Log", "Installs_Log", "pct_positivo"]

    # normalizamos cada columna a un rango 0-1 para poder compararlas en el mismo radar
    mins = profiles[categories_r].min()
    maxs = profiles[categories_r].max()

    fig = go.Figure()
    for _, row in profiles.iterrows():
        vals_norm = [(row[c] - mins[c]) / (maxs[c] - mins[c] + 1e-9) for c in categories_r]
        fig.add_trace(go.Scatterpolar(
            r=vals_norm + [vals_norm[0]],
            theta=["Rating", "Reseñas", "Instalaciones", "Sentimiento+"] + ["Rating"],
            fill="toself",
            name=row["Cluster_Name"],
            line=dict(color=CLUSTER_COLORS.get(row["Cluster_Name"], "#888")),
            opacity=0.7,
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1], showticklabels=False)),
        legend=dict(orientation="h", y=-0.15, font=dict(size=10)),
        margin=dict(t=20, b=40, l=20, r=20), height=340,
        paper_bgcolor="rgba(0,0,0,0)", font=dict(size=11),
    )
    return fig


def fig_rating_category():
    cat_rating = df.groupby("Category")["Rating"].mean().sort_values(ascending=False).reset_index()
    cat_rating.columns = ["Category", "Avg_Rating"]
    fig = px.bar(cat_rating, x="Category", y="Avg_Rating",
                 color="Avg_Rating",
                 color_continuous_scale=SEQ_PALETTE,
                 labels={"Avg_Rating": "Rating Promedio", "Category": ""},
                 template="plotly_white")
    fig.update_layout(margin=dict(t=10, b=80, l=40, r=10), height=320,
                      coloraxis_showscale=False,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(size=10))
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(range=[3, 5], showgrid=True, gridcolor="#eee")
    return fig


def fig_feature_importance():
    dff = df_imp.head(15).sort_values("importance")
    labels = {
        "Reviews_Log": "Log(Reseñas)",
        "Size_MB": "Tamaño (MB)",
        "Review_Ratio": "Ratio Reseñas/Inst.",
        "Installs_Log": "Log(Instalaciones)",
        "Price": "Precio",
        "is_free": "Es Gratuita",
        "Cat_FAMILY": "Categoría: Family",
        "Cat_MEDICAL": "Categoría: Medical",
        "Cat_GAME": "Categoría: Game",
        "Cat_OTHER": "Otras Categorías",
        "Cat_TOOLS": "Categoría: Tools",
    }
    dff["label"] = dff["feature"].map(labels).fillna(dff["feature"])
    fig = px.bar(dff, x="importance", y="label",
                 orientation="h",
                 color="importance",
                 color_continuous_scale=SEQ_PALETTE,
                 labels={"importance": "Importancia Relativa", "label": ""},
                 template="plotly_white")
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=360,
                      coloraxis_showscale=False,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(size=11))
    fig.update_xaxes(showgrid=True, gridcolor="#eee")
    return fig


def fig_model_comparison():
    fig = go.Figure()
    colors = [COLORS["muted"], COLORS["primary"], COLORS["secondary"]]
    names = ["Regresión Lineal\n(Baseline)", "Random Forest\n(Base)", "Random Forest\n(CV K=5)"]
    r2_vals = [0.9236, 0.9240, 0.9177]
    for i, (name, r2, c) in enumerate(zip(names, r2_vals, colors)):
        fig.add_trace(go.Bar(
            name=name, x=[name.replace("\n", "<br>")], y=[r2],
            marker_color=c,
            text=[f"R²={r2:.4f}"],
            textposition="outside",
        ))
    fig.update_layout(
        margin=dict(t=20, b=20, l=40, r=20), height=360,
        yaxis=dict(range=[0.90, 0.93], title="R² Score", showgrid=True, gridcolor="#eee"),
        showlegend=False, barmode="group",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=11),
    )
    return fig


def fig_hist_rating():
    dff = df.dropna(subset=["Rating"])
    dff = dff[dff["Rating"] > 0]
    fig = px.histogram(dff, x="Rating", nbins=30,
                       color_discrete_sequence=[COLORS["primary"]],
                       labels={"Rating": "Rating", "count": "N° Apps"},
                       template="plotly_white")
    fig.update_layout(margin=dict(t=10, b=10, l=40, r=10), height=300,
                      bargap=0.05, showlegend=False,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(size=11))
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#eee")
    return fig


def fig_scatter_reviews():
    dff = df.dropna(subset=["Rating", "Reviews_Log"]).sample(min(2000, len(df)), random_state=1)
    dff = dff[dff["Rating"] > 0]
    fig = px.scatter(dff, x="Reviews_Log", y="Rating",
                     trendline="ols",
                     color_discrete_sequence=[COLORS["secondary"]],
                     opacity=0.4,
                     labels={"Reviews_Log": "Log(N° Reseñas)", "Rating": "Rating"},
                     template="plotly_white")
    fig.data[1].line.color = COLORS["accent"]
    fig.update_layout(margin=dict(t=10, b=10, l=40, r=10), height=300,
                      showlegend=False,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(size=11))
    fig.update_xaxes(showgrid=True, gridcolor="#eee")
    fig.update_yaxes(showgrid=True, gridcolor="#eee")
    return fig


def fig_sentiment():
    dff = df.dropna(subset=["pct_positivo", "Cluster_Name"])
    fig = px.box(dff, x="Cluster_Name", y="pct_positivo",
                 color="Cluster_Name",
                 color_discrete_map=CLUSTER_COLORS,
                 labels={"pct_positivo": "% Reseñas Positivas", "Cluster_Name": ""},
                 template="plotly_white")
    fig.update_layout(margin=dict(t=10, b=10, l=40, r=10), height=300,
                      showlegend=False,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(size=11))
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#eee")
    return fig


#helper para las tarjetas
def _card(title, *content, flex=1, extra=None):
    children = [
        html.P(title, style={"margin": "0 0 12px", "fontWeight": "600", "fontSize": "0.88rem",
                               "color": COLORS["text"]}),
    ] + list(content)
    if extra is not None:
        children.append(extra)
    return html.Div(children, style={
        "background": COLORS["surface"],
        "borderRadius": "10px",
        "padding": "16px 18px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.06)",
        "flex": flex,
        "minWidth": "260px",
        "overflow": "hidden",
    })


# Run
if __name__ == "__main__":
    app.run(debug=True, port=8050)
