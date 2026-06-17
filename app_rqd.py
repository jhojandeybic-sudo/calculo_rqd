import streamlit as st
import os
import sys

# ==============================================================================
# TRUCO DEL TRIÁNGULO: Auto-ejecución de Streamlit al presionar Play en VS Code
# ==============================================================================
if __name__ == "__main__":
    if not st.runtime.exists():
        script_path = os.path.abspath(__file__)
        sys.argv = ["streamlit", "run", script_path]
        import streamlit.web.cli as stcli
        sys.exit(stcli.main())
# ==============================================================================

st.set_page_config(
    page_title="GSI Modificado - Ultra Compacto", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# ARQUITECTURA CSS: Compresión Extrema de Espacios y Contraste de Inputs en Negro
# ==============================================================================
st.markdown("""
    <style>
    /* Eliminar márgenes globales redundantes de Streamlit */
    .stApp { background-color: #090d16 !important; }
    
    /* Contenedor principal derecho con padding mínimo */
    .block-container {
        background-color: #0f172a;
        padding: 1rem 1.5rem !important;
        border-radius: 12px;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.5);
        margin-top: 0.2rem !important;
    }

    /* BARRA LATERAL: Ajuste hipercompacto */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    
    /* Reducir espacio vertical muerto entre elementos de la barra lateral */
    [data-testid="stSidebar"] .stElementContainer {
        margin-bottom: 0.15rem !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: #f8fafc !important;
    }

    /* CONTROL DE INPUTS: Cajas claras con texto/números en NEGRO INTENSO */
    [data-testid="stSidebar"] div[data-baseweb="input"] {
        background-color: #ffffff !important; 
        border: 2px solid #38bdf8 !important;  
        border-radius: 5px !important;
        height: 36px !important; /* Más compacto */
    }
    [data-testid="stSidebar"] input {
        color: #000000 !important; 
        font-weight: bold !important;
    }
    
    /* Selector de Condición Superficial compacto en negro */
    [data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 5px !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: #000000 !important; 
        font-weight: bold !important;
    }
    
    /* Elementos del panel de resultados */
    h1, h2, h3, p, span, label { color: #f8fafc !important; }
    div[data-testid="stMetricValue"] { color: #38bdf8 !important; font-weight: bold; font-size: 1.8rem !important; }
    div[data-testid="stMetricLabel"] { color: #94a3b8 !important; margin-bottom: 0px !important; }
    .stMetric { background-color: #1e293b; padding: 8px 12px; border-radius: 6px; border: 1px solid #334155; }
    
    /* Cuadro de la picota comprimido */
    .panel-orientacion-oscuro {
        background-color: #1e293b;
        padding: 8px 10px;
        border-radius: 6px;
        border-left: 4px solid #38bdf8;
        margin-top: 3px;
        font-size: 11px;
        color: #cbd5e1;
    }
    
    /* TABLA GSI HIPERCOMPACTA */
    .tabla-gsi-oscura { 
        width: 100%; 
        border-collapse: collapse; 
        text-align: center; 
        font-family: sans-serif; 
        font-size: 11px; 
        border: 1px solid #334155;
        background-color: #111827;
        margin-top: 4px;
    }
    .tabla-gsi-oscura th { 
        background-color: #1e293b; 
        color: #38bdf8; 
        padding: 5px; 
        border: 1px solid #334155; 
    }
    .tabla-gsi-oscura td { padding: 5px; border: 1px solid #334155; color: #e2e8f0; }
    
    hr { margin: 0.6rem 0 !important; border-color: #334155 !important; }
    </style>
""", unsafe_allow_html=True)

# Títulos compactos
st.markdown("<h2 style='margin:0px; padding:0px;'>💎 Analizador Geotécnico GSI Modificado Real</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; margin:0px;'>Mapeo exacto de isolíneas y consistencia litológica de campo.</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ==============================================================================
# BARRA LATERAL: ENTRADA DE DATOS DINÁMICA Y EDITABLE
# ==============================================================================
st.sidebar.markdown("<h3 style='margin:0px;'>🛠️ 1. Datos del Testigo</h3>", unsafe_allow_html=True)
longitud_total = st.sidebar.number_input("Longitud Total del Tramo (cm):", min_value=10, max_value=1000, value=200, step=10)

# ¡REPARADO! El usuario puede cambiar libremente el número de fragmentos
num_fragmentos = st.sidebar.number_input("N° de Fragmentos Registrados:", min_value=1, max_value=30, value=4, step=1)

st.sidebar.markdown("<p style='margin:2px 0px 0px 0px; font-weight:bold; font-size:13px;'>📐 Registro de Longitudes (cm):</p>", unsafe_allow_html=True)

# Valores por defecto para mantener tus datos iniciales de 4 fragmentos
valores_predeterminados = [25, 15, 18, 32]
fragmentos = []

for i in range(int(num_fragmentos)):
    # Si el índice está dentro de los 4 iniciales, se usa; si no, se inicializa en 10
    val_def = valores_predeterminados[i] if i < len(valores_predeterminados) else 10
    val = st.sidebar.number_input(f"Fragmento L{i+1}:", min_value=0, max_value=200, value=val_def, step=1, key=f"l_{i}")
    fragmentos.append(val)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='margin:0px;'>⛏️ 2. Clasificación Superficial</h3>", unsafe_allow_html=True)

condicion_seleccionada = st.sidebar.selectbox(
    "Condición Superficial:",
    options=["MUY BUENA (MB)", "BUENA (B)", "REGULAR (R)", "POBRE (P)", "MUY POBRE (MP)"],
    index=2
)

# Descripciones y comportamiento con picota
datos_condicion = {
    "MUY BUENA (MB)": {"desc": "Fresca. Discontinuidades muy rugosas, cerradas. (Rc > 250 MPa).", "picota": "Se astilla con golpes de picota.", "color": "#38bdf8"},
    "BUENA (B)": {"desc": "Leve. alterada. Rugosas, oxidación, lig. abierta. (Rc 100 a 250 MPa).", "picota": "Se rompe con varios golpes de picota.", "color": "#4ade80"},
    "REGULAR (R)": {"desc": "Leve. alterada. Lisas, ligeramente abierta. (Rc 50 a 100 MPa).", "picota": "Se rompe con uno o dos golpes de picota.", "color": "#f59e0b"},
    "POBRE (P)": {"desc": "Mod. resistente/alterada. Pulida, relleno compacto. (Rc 25 a 50 MPa).", "picota": "Se indenta superficialmente con la picota.", "color": "#f87171"},
    "MUY POBRE (MP)": {"desc": "Blanda. Pulida y estriada, relleno de arcillas. (Rc < 25 MPa).", "picota": "Se disgrega o indenta con la picota.", "color": "#ef4444"}
}

info_activa = datos_condicion[condicion_seleccionada]
st.sidebar.markdown(f"""
    <div class="panel-orientacion-oscuro" style="border-left-color: {info_activa['color']};">
        <b style="color: {info_activa['color']};">🔬 Ensayo (Picota):</b> {info_activa['desc']}<br>
        <b>Reacción:</b> <span style='color: #000000; background-color:#ffffff; padding:0px 3px; border-radius:2px; font-weight:bold;'>{info_activa['picota']}</span>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# ALGORITMO GEOMECÁNICO (CÁLCULO RQD Y MATRIZ GSI)
# ==============================================================================
fragmentos_validos = [f for f in fragmentos if f >= 10]
suma_validos = sum(fragmentos_validos)
rqd = (suma_validos / longitud_total) * 100 if longitud_total > 0 else 0.0

# Clasificación por filas según rangos oficiales de RQD
if rqd > 75 and rqd <= 90:
    fila_activa, estructura_label = 0, "LEVEMENTE FRACTURADA (LF)"
elif rqd > 50 and rqd <= 75:
    fila_activa, estructura_label = 1, "MODERADAMENTE FRACTURADA (F)"
elif rqd > 25 and rqd <= 50:
    fila_activa, estructura_label = 2, "MUY FRACTURADA (MF)"
else:
    # Si hay fragmentación intensa y el tamaño máximo es bajo, entra a Triturada
    if num_fragmentos >= 4 and (len(fragmentos) == 0 or max(fragmentos) <= 35) and rqd < 25:
        fila_activa, estructura_label = 4, "TRITURADA O BRECHADA (T)"
    else:
        fila_activa, estructura_label = 3, "INTENSAMENTE FRACTURADA (IF)"

col_activa = ["MUY BUENA (MB)", "BUENA (B)", "REGULAR (R)", "POBRE (P)", "MUY POBRE (MP)"].index(condicion_seleccionada)

matriz_letras = [
    ["LF/MB", "LF/B", "LF/R", "LF/P", "LF/MP"],
    ["F/MB",  "F/B",  "F/R",  "F/P",  "F/MP"],
    ["MF/MB", "MF/B", "MF/R", "MF/P", "MF/MP"],
    ["IF/MB", "IF/B", "IF/R", "IF/P", "IF/MP"],
    ["T/MB",  "T/B",  "T/R",  "T/P",  "T/MP"]
]

# Valores mapeados estrictamente de las curvas del ábaco real
matriz_valores_gsi = [
    ["95-90", "85-80", "75-70", "60-55", "N/A"],
    ["90-80", "75-70", "65-60", "55-50", "40-35"],
    ["N/A",   "65-55", "55-45", "45-40", "30-25"],
    ["N/A",   "N/A",   "45-35", "35-25", "20-15"],
    ["N/A",   "N/A",   "30-20", "15-10", "5"]
]

codigo_final = matriz_letras[fila_activa][col_activa]
valor_gsi_final = matriz_valores_gsi[fila_activa][col_activa]

# ==============================================================================
# DESPLIEGUE DEL PANEL DE CONTROL (DISPOSICIÓN COMPACTADA)
# ==============================================================================
col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.metric(label="RQD Resultante", value=f"{rqd:.1f} %")
    st.markdown(f"<p style='margin:2px 0px;'><b>Estructura:</b> <span style='color:#38bdf8;'>{estructura_label}</span><br><b>Condición:</b> <span style='color:{info_activa['color']};'>{condicion_seleccionada}</span></p>", unsafe_allow_html=True)
    
    if valor_gsi_final == "N/A":
        st.markdown(f"<div style='background-color: #7f1d1d; padding: 6px 10px; border-radius: 6px; border: 1px solid #f87171; margin-top: 4px; color:#ffffff;'><b>Valor GSI: No Existe (N/A)</b><br><small style='color:#fca5a5;'>Combinación {codigo_final} vacía en el ábaco.</small></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background-color: #1e293b; padding: 6px 10px; border-radius: 6px; border: 1px solid #334155; margin-top: 4px; color:#4ade80; font-size:18px;'><b>Rango GSI: {valor_gsi_final}</b> <span style='color:#cbd5e1; font-size:12px;'>({codigo_final})</span></div>", unsafe_allow_html=True)

with col_der:
    st.markdown("<p style='margin:0px 0px 2px 0px; font-weight:bold; font-size:13px;'>📐 Reconstrucción del Testigo:</p>", unsafe_allow_html=True)
    
    html_sondaje = "<div style='border: 1px solid #334155; background-color: #111827; width: 100%; height: 38px; display: table; border-collapse: collapse; border-radius: 4px; overflow: hidden;'>"
    for idx, frag in enumerate(fragmentos):
        if frag > 0:
            pct = (frag / longitud_total) * 100
            color = "#0284c7" if frag >= 10 else "#dc2626"
            html_sondaje += f"<div style='display: table-cell; width: {pct}%; background-color: {color}; border-right: 1px solid #0f172a; color: #ffffff; text-align: center; vertical-align: middle; font-weight: bold; font-size: 9px;'>L{idx+1}<br>{frag}cm</div>"
            
    suma_piezas = sum(fragmentos)
    perdida_total = longitud_total - suma_piezas
    if perdida_total > 0:
        pct_p = (perdida_total / longitud_total) * 100
        html_sondaje += f"<div style='display: table-cell; width: {pct_p}%; background-color: #334155; color: #94a3b8; text-align: center; vertical-align: middle; font-size: 9px; font-style: italic;'>Pérdida<br>{perdida_total}cm</div>"
    html_sondaje += "</div>"
    st.markdown(html_sondaje, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==============================================================================
# AUDITORÍA DE MATRIZ DE DOBLE ENTRADA HOMOLOGADA (SIN ESPACIOS VACÍOS)
# ==============================================================================
st.markdown("<b style='font-size:14px;'>🗺️ Matriz GSI de Doble Entrada Real</b>", unsafe_allow_html=True)

filas_tabla = [
    "<b>LF</b> <small style='color:#94a3b8;'>(75-90%)</small>",
    "<b>F</b> <small style='color:#94a3b8;'>(50-75%)</small>",
    "<b>MF</b> <small style='color:#94a3b8;'>(25-50%)</small>",
    "<b>IF</b> <small style='color:#94a3b8;'>(0-25%)</small>",
    "<b>T</b> <small style='color:#94a3b8;'>(Sin RQD)</small>"
]

headers = [
    "<th>MB<br><small style='color:#94a3b8;'>Astilla</small></th>", 
    "<th>B<br><small style='color:#94a3b8;'>Varios g.</small></th>", 
    "<th>R<br><small style='color:#94a3b8;'>1-2 g.</small></th>", 
    "<th>P<br><small style='color:#94a3b8;'>Indenta</small></th>", 
    "<th>MP<br><small style='color:#94a3b8;'>Disgrega</small></th>"
]

html = f"<table class='tabla-gsi-oscura'><thead><tr><th>Estructura ↓ / Condición →</th>{"".join(headers)}</tr></thead><tbody>"

for i, fila in enumerate(filas_tabla):
    html += f"<tr><td style='background-color: #1e293b; text-align: left; font-weight: bold; color: #ffffff;'>{fila}</td>"
    for j in range(5):
        val_gsi = matriz_valores_gsi[i][j]
        cod_gsi = matriz_letras[i][j]
        
        if val_gsi == "N/A":
            if i == fila_activa and j == col_activa:
                bg = "#7f1d1d"; border = "border: 2px solid #ef4444; font-weight: bold;"
                contenido = f"<b>{cod_gsi}</b><br><span style='color:#f87171; font-size:10px;'>Vacío</span>"
            else:
                bg = "#1f1616"; border = "border: 1px dashed #453131;"
                contenido = f"<span style='color:#453131;'>- - -</span>"
        else:
            if i == fila_activa and j == col_activa:
                bg = "#064e3b"; border = "border: 2.5px solid #4ade80; font-weight: bold;"
            else:
                bg = "#111827"; border = "border: 1px solid #334155;"
            contenido = f"<b>{cod_gsi}</b><br><span style='color:#ffffff; font-size:10px;'><b>{val_gsi}</b></span>"
            
        html += f"<td style='background-color: {bg}; {border}'>{contenido}</td>"
    html += "</tr>"
    
html += "</tbody></table>"
st.markdown(html, unsafe_allow_html=True)
