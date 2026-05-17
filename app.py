import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

print("⏳ Iniciando Dashboard con Formateo de Códigos Forzado...")

# 1. CARGAR DATOS (Tu nuevo archivo unificado)
df_mortalidad = pd.read_excel("NoFetal2019_Modificado.xlsx", sheet_name="No_Fetales_2019")
df_codigos = pd.read_excel("CodigosDeMuerte.xlsx", sheet_name="Final")

# --- CORRECCIÓN CRÍTICA DE FORMATO DE CÓDIGOS ---
# Convertimos a string, quitamos decimales (.0) si los hay, rellenamos con ceros a la izquierda
df_mortalidad["COD_DANE"] = df_mortalidad["COD_DANE"].astype(str).str.split('.').str[0].str.strip().str.zfill(5)
df_mortalidad["COD_DEPARTAMENTO"] = df_mortalidad["COD_DEPARTAMENTO"].astype(str).str.split('.').str[0].str.strip().str.zfill(2)

# Crear la etiqueta limpia para el Dropdown
df_mortalidad["FILTRO_ETIQUETA"] = (
    df_mortalidad["COD_DANE"] + " - " + 
    df_mortalidad["MUNICIPIO_TEXTO"].astype(str).str.upper() + " - " + 
    df_mortalidad["DEPARTAMENTO_TEXTO"].astype(str).str.upper()
)

# Extraer opciones únicas para el Dropdown
df_dropdown_limpio = df_mortalidad.drop_duplicates(subset=["COD_DANE"]).sort_values("MUNICIPIO_TEXTO")

opciones_dropdown = [
    {"label": row["FILTRO_ETIQUETA"], "value": row["COD_DANE"]}
    for _, row in df_dropdown_limpio.iterrows() 
    if str(row["COD_DANE"]) != "nan" and row["MUNICIPIO_TEXTO"] != "DESCONOCIDO"
]

# 3. NORMALIZAR VARIABLES ADICIONALES
df_codigos = df_codigos.rename(columns={
    "Código de la CIE-10 cuatro caracteres": "COD_MUERTE",
    "Descripcion  de códigos mortalidad a cuatro caracteres": "DESCRIPCION"
})

if "SEXO" in df_mortalidad.columns:
    df_mortalidad["SEXO"] = df_mortalidad["SEXO"].astype(str).str.upper().str.strip().replace({"1": "MASCULINO", "2": "FEMENINO", "M": "MASCULINO", "F": "FEMENINO"})
else:
    df_mortalidad["SEXO"] = "MASCULINO"

mapa_edades = {
    0: "Mortalidad neonatal", 1: "Mortalidad neonatal", 2: "Mortalidad neonatal", 3: "Mortalidad neonatal", 4: "Mortalidad neonatal",
    5: "Mortalidad infantil", 6: "Mortalidad infantil", 7: "Primera infancia", 8: "Primera infancia",
    9: "Niñez", 10: "Niñez", 11: "Adolescencia", 12: "Juventud", 13: "Juventud",
    14: "Adultez temprana", 15: "Adultez temprana", 16: "Adultez temprana",
    17: "Adultez intermedia", 18: "Adultez intermedia", 19: "Adultez intermedia",
    20: "Vejez", 21: "Vejez", 22: "Vejez", 23: "Vejez", 24: "Vejez",
    25: "Longevidad / Centenarios", 26: "Longevidad / Centenarios", 27: "Longevidad / Centenarios", 28: "Longevidad / Centenarios",
    29: "Edad desconocida"
}
df_mortalidad["CATEGORIA_EDAD"] = pd.to_numeric(df_mortalidad["GRUPO_EDAD1"], errors='coerce').fillna(29).astype(int).map(mapa_edades)
orden_ciclo_vida = ["Mortalidad neonatal", "Mortalidad infantil", "Primera infancia", "Niñez", "Adolescencia", "Juventud", "Adultez temprana", "Adultez intermedia", "Vejez", "Longevidad / Centenarios", "Edad desconocida"]

meses_dic = {1:"Ene", 2:"Feb", 3:"Mar", 4:"Abr", 5:"May", 6:"Jun", 7:"Jul", 8:"Ago", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dic"}

df_mortalidad["ES_HOMICIDIO"] = (df_mortalidad["MANERA_MUERTE"].astype(str).str.upper() == "HOMICIDIO") | (df_mortalidad["MANERA_MUERTE"].astype(str) == "3") | (df_mortalidad["COD_MUERTE"].astype(str).str.startswith("X95", na=False))
df_mortalidad["ES_SUICIDIO"] = (df_mortalidad["MANERA_MUERTE"].astype(str).str.upper() == "SUICIDIO") | (df_mortalidad["MANERA_MUERTE"].astype(str) == "4")
df_mortalidad["ES_ACCIDENTE"] = (df_mortalidad["MANERA_MUERTE"].astype(str).str.upper() == "ACCIDENTE") | (df_mortalidad["MANERA_MUERTE"].astype(str) == "2")

print("✅ RE-CONEXIÓN EXITOSA COMPLETA.")

# ==============================================================================
# INTERFAZ GRÁFICA (DASH)
# ==============================================================================
app = dash.Dash(__name__)
server = app.server

ESTILO_CENTRO = {
    "backgroundColor": "#ffffff", "padding": "25px", "borderRadius": "12px",
    "boxShadow": "0 4px 10px rgba(0,0,0,0.06)", "marginBottom": "30px",
    "width": "85%", "margin": "0 auto 30px auto", "textAlign": "center"
}

ESTILO_TABLA = {
    "style_table": {"overflowX": "auto", "width": "85%", "margin": "15px auto", "borderRadius": "6px"},
    "style_header": {"backgroundColor": "#f8fafc", "fontWeight": "bold", "color": "#334155"},
    "style_cell": {"fontFamily": "Arial", "fontSize": "13px", "padding": "8px", "textAlign": "center"}
}

app.layout = html.Div(style={"fontFamily": "Arial, sans-serif", "padding": "20px", "backgroundColor": "#f4f6f9"}, children=[
    html.H1("Dashboard Estadístico de Mortalidad en Colombia (2019)", style={"textAlign": "center", "color": "#1e272e", "marginBottom": "30px"}),
    
    html.Div(id="tarjetas-kpi-contenedor", style={"display": "flex", "justifyContent": "space-around", "width": "85%", "margin": "0 auto 25px auto"}),

    html.Div([
        html.Label("🔍 Buscar por Código, Municipio o Departamento:", style={"fontWeight": "bold", "color": "#485460"}),
        dcc.Dropdown(
            id="filtro-municipio", 
            options=opciones_dropdown, 
            placeholder="🌍 Escribe o selecciona: CÓDIGO - MUNICIPIO - DEPARTAMENTO", 
            clearable=True
        )
    ], style={**ESTILO_CENTRO, "width": "65%"}),

    html.Div([dcc.Graph(id="mapa-dinamico")], style=ESTILO_CENTRO),
    html.Div([dcc.Graph(id="grafico-lineas-mes")], style=ESTILO_CENTRO),
    
    html.Div([
        dcc.Graph(id="grafico-barras-violencia"),
        html.Div(id="tabla-barras-violencia-contenedor")
    ], style=ESTILO_CENTRO),

    html.Div([dcc.Graph(id="grafico-circular-menor")], style=ESTILO_CENTRO),
    
    html.Div([
        dcc.Graph(id="grafico-barras-sexo"),
        html.Div(id="tabla-barras-sexo-contenedor")
    ], style=ESTILO_CENTRO),

    html.Div([dcc.Graph(id="grafico-histograma-edad")], style=ESTILO_CENTRO),

    html.Div([
        html.H3("📋 Top 10 Principales Causas de Muerte (CIE-10)", style={"fontWeight": "bold"}),
        html.Div(id="tabla-causas-contenedor")
    ], style={**ESTILO_CENTRO, "height": "400px", "overflowY": "auto"})
])

# ==============================================================================
# CALLBACK REACTIVO CORREGIDO
# ==============================================================================
@app.callback(
    [Output("tarjetas-kpi-contenedor", "children"),
     Output("mapa-dinamico", "figure"),
     Output("grafico-lineas-mes", "figure"),
     Output("grafico-histograma-edad", "figure"),
     Output("grafico-barras-violencia", "figure"),
     Output("tabla-barras-violencia-contenedor", "children"),
     Output("grafico-circular-menor", "figure"),
     Output("grafico-barras-sexo", "figure"),
     Output("tabla-barras-sexo-contenedor", "children"),
     Output("tabla-causas-contenedor", "children")],
    [Input("filtro-municipio", "value")]
)
def actualizar_tablero_grafico(muni_seleccionado):
    if muni_seleccionado:
        # Aseguramos formato estricto de string de 5 dígitos para comparar con el filtro
        val_muni = str(muni_seleccionado).split('.')[0].strip().zfill(5)
        df_filtrado = df_mortalidad[df_mortalidad["COD_DANE"] == val_muni]
        
        nombre_muni = df_filtrado["MUNICIPIO_TEXTO"].iloc[0] if not df_filtrado.empty else "Seleccionado"
        sufijo = f" en {nombre_muni}"
        zoom_mapa = 10.5
        centro_mapa = {"lat": df_filtrado["LATITUD"].mean() if not df_filtrado.empty else 4.5709, 
                       "lon": df_filtrado["LONGITUD"].mean() if not df_filtrado.empty else -74.2973}
    else:
        df_filtrado = df_mortalidad
        sufijo = " en Colombia"
        zoom_mapa = 4.8
        centro_mapa = {"lat": 4.5709, "lon": -74.2973}

    t_m = len(df_filtrado)
    t_h = int(df_filtrado["ES_HOMICIDIO"].sum())
    t_s = int(df_filtrado["ES_SUICIDIO"].sum())
    t_a = int(df_filtrado["ES_ACCIDENTE"].sum())

    kpis = [
        html.Div([html.P("Total Defunciones"), html.H2(f"{t_m:,}")], style={"backgroundColor": "#fff", "padding": "15px", "borderRadius": "8px", "width": "22%", "borderLeft": "5px solid #1abc9c"}),
        html.Div([html.P("Homicidios"), html.H2(f"{t_h:,}")], style={"backgroundColor": "#fff", "padding": "15px", "borderRadius": "8px", "width": "22%", "borderLeft": "5px solid #e74c3c"}),
        html.Div([html.P("Suicidios"), html.H2(f"{t_s:,}")], style={"backgroundColor": "#fff", "padding": "15px", "borderRadius": "8px", "width": "22%", "borderLeft": "5px solid #9b59b6"}),
        html.Div([html.P("Accidentes"), html.H2(f"{t_a:,}")], style={"backgroundColor": "#fff", "padding": "15px", "borderRadius": "8px", "width": "22%", "borderLeft": "5px solid #e67e22"})
    ]

    # MAPA
    df_mapa = df_filtrado.groupby(["MUNICIPIO_TEXTO", "DEPARTAMENTO_TEXTO", "LATITUD", "LONGITUD"]).size().reset_index(name="MUERTES")
    
    fig_mapa = px.scatter_mapbox(
        df_mapa, 
        lat="LATITUD", 
        lon="LONGITUD", 
        size="MUERTES", 
        color="MUERTES",
        color_continuous_scale="Reds" if muni_seleccionado else "Blues", 
        hover_name="MUNICIPIO_TEXTO", 
        hover_data={"DEPARTAMENTO_TEXTO": True, "MUERTES": True, "LATITUD": False, "LONGITUD": False},
        size_max=40 if muni_seleccionado else 25,
        zoom=zoom_mapa, 
        center=centro_mapa, 
        mapbox_style="carto-positron", 
        height=500,
        title=f"📍 Ubicación y Registro de Casos{sufijo}"
    )
    fig_mapa.update_layout(margin={"r": 0, "t": 35, "l": 0, "b": 0})

    muertes_mes = df_filtrado.groupby("MES").size().reset_index(name="MUERTES")
    muertes_mes["NOMBRE_MES"] = muertes_mes["MES"].map(meses_dic)
    fig_lineas = px.line(muertes_mes, x="NOMBRE_MES", y="MUERTES", markers=True, text="MUERTES", title=f"Tendencia Mensual de Defunciones{sufijo}")

    df_homicidios = df_filtrado[df_filtrado["ES_HOMICIDIO"]]
    if df_homicidios.empty:
        top5_sexo = pd.DataFrame(columns=["MUNICIPIO_TEXTO", "SEXO", "HOMICIDIOS"])
        top5_munis = []
    else:
        top5_munis = df_homicidios.groupby("MUNICIPIO_TEXTO").size().nlargest(5).index.tolist()
        top5_sexo = df_homicidios[df_homicidios["MUNICIPIO_TEXTO"].isin(top5_munis)].groupby(["MUNICIPIO_TEXTO", "SEXO"]).size().reset_index(name="HOMICIDIOS")

    fig_barras_violencia = px.bar(
        top5_sexo, x="MUNICIPIO_TEXTO", y="HOMICIDIOS", color="SEXO", barmode="group", text="HOMICIDIOS",
        category_orders={"MUNICIPIO_TEXTO": top5_munis}, title=f"Distribución de Homicidios por Sexo{sufijo}",
        color_discrete_map={"MASCULINO": "#1e3a8a", "FEMENINO": "#be185d"}
    )
    t_violencia = pd.DataFrame(columns=["MUNICIPIO_TEXTO"]) if top5_sexo.empty else top5_sexo.pivot(index="MUNICIPIO_TEXTO", columns="SEXO", values="HOMICIDIOS").reset_index().fillna(0)
    tabla_violencia_html = dash_table.DataTable(data=t_violencia.to_dict('records'), columns=[{"name": str(i), "id": str(i)} for i in t_violencia.columns], **ESTILO_TABLA)

    bottom10 = df_filtrado.groupby("MUNICIPIO_TEXTO").size().nsmallest(10).reset_index(name="MUERTES")
    fig_circular = px.pie(bottom10, values="MUERTES", names="MUNICIPIO_TEXTO", title=f"Municipios con Menor Índice de Mortalidad{sufijo}", hole=0.4)

    eje_x = "MUNICIPIO_TEXTO" if muni_seleccionado else "COD_DEPARTAMENTO"
    top_regiones = df_filtrado.groupby(eje_x).size().nlargest(15).index.tolist()
    df_sexo_gen = df_filtrado[df_filtrado[eje_x].isin(top_regiones)]
    muertes_sexo = df_sexo_gen.groupby([eje_x, "SEXO"]).size().reset_index(name="MUERTES")

    fig_barras_sexo = px.bar(
        muertes_sexo, x=eje_x, y="MUERTES", color="SEXO", barmode="group", text="MUERTES",
        category_orders={eje_x: top_regiones}, title=f"Mortalidad Estructural por Sexo{sufijo}",
        color_discrete_map={"MASCULINO": "#1e3a8a", "FEMENINO": "#be185d"}
    )
    t_sexo = pd.DataFrame() if muertes_sexo.empty else muertes_sexo.pivot(index=eje_x, columns='SEXO', values='MUERTES').reset_index().fillna(0)
    tabla_sexo_html = dash_table.DataTable(data=t_sexo.to_dict('records'), columns=[{"name": str(i), "id": str(i)} for i in t_sexo.columns], **ESTILO_TABLA)

    fig_histograma = px.histogram(df_filtrado, x="CATEGORIA_EDAD", category_orders={"CATEGORIA_EDAD": orden_ciclo_vida}, title=f"Mortalidad por Ciclo de Vida DANE{sufijo}", color="CATEGORIA_EDAD")

    top_causas = df_filtrado.groupby("COD_MUERTE").size().reset_index(name="CASOS").merge(df_codigos, on="COD_MUERTE", how="left").sort_values("CASOS", ascending=False).head(10)
    top_causas["DESCRIPCION"] = top_causas["DESCRIPCION"].fillna("Causa No Especificada")
    
    tabla_causas_html = html.Table([
        html.Thead(html.Tr([html.Th("Código"), html.Th("Descripción"), html.Th("Casos registrados")])),
        html.Tbody([html.Tr([html.Td(top_causas.iloc[i]["COD_MUERTE"]), html.Td(top_causas.iloc[i]["DESCRIPCION"]), html.Td(f"{top_causas.iloc[i]['CASOS']:,}")]) for i in range(len(top_causas))])
    ], style={"width": "100%", "borderCollapse": "collapse", "textAlign": "left"})

    return kpis, fig_mapa, fig_lineas, fig_histograma, fig_barras_violencia, tabla_violencia_html, fig_circular, fig_barras_sexo, tabla_sexo_html, tabla_causas_html

if __name__ == "__main__":
    app.run(debug=False, port=8099, host="127.0.0.1")