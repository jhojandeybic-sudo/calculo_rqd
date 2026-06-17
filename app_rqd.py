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
    page_title="GSI Modificado - Ajuste Estricto", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# ARQUITECTURA CSS: Control Absoluto de Contraste (Fondo Oscuro + Letras Visibles)
# ==============================================================================
st.markdown("""
    <style>
    /* Fondo del cuerpo principal de la aplicación */
    .stApp { 
        background-color: #090d16 !important; 
    }
    
    /* Contenedor del panel derecho (Datos y Resultados) */
    .block-container {
        background-color: #0f172a;
        padding: 2.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.5);
        margin-top: 1rem;
    }

    /* BARRA LATERAL IZQUIERDA: Forzar tema oscuro y eliminar fondo blanco nativo */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    
    /* Forzar visibilidad de textos y etiquetas en la barra lateral */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] span {
        color: #38bdf8 !important; /* Blanco nítido de alta visibilidad */
    }

    /* SOLUCIÓN AL ERROR DE INPUTS: Forzar fondo oscuro y texto blanco dentro de las cajas de llenado */
    [data-testid="stSidebar"] div[data-baseweb="input"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
    }
    [data-testid="stSidebar"] input {
        color: #38bdf8 !important; /* Texto que digita el usuario en blanco */
    }
    [data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
    }
    
    /* Estilos de fuentes generales y métricas */
    h1, h2, h3, p, span, label { color: #f8fafc !important; }
    div[data-testid="stMetricValue"] { color: #38bdf8 !important; font-weight: bold; }
    div[data-testid="stMetricLabel"] { color: #94a3b8 !important; }
    .stMetric { background-color: #1e293b; padding: 18px; border-radius: 8px; border: 1px solid #334155; }
    
    /* Panel de orientación geomecánica */
    .panel-orientacion-oscuro {
        background-color: #1e293b;
        padding: 14px;
        border-radius: 6px;
        border-left: 4px solid #38bdf8;
        margin-top: 10px;
        font-size: 13px;
        color: #cbd5e1;
    }
    
    /* TABLA DE DOBLE ENTRADA GSI */
    .tabla-gsi-oscura { 
        width: 100%; 
        border-collapse: collapse; 
        text-align: center; 
        font-family: sans-serif; 
        font-size: 11px; 
        border: 1px solid #334155;
        background-color: #111827;
    }
    .tabla-gsi-oscura th { 
        background-color: #1e293b; 
        color: #38bdf8; 
        padding: 12px; 
        border: 1px solid #334155; 
        vertical-align: top;
    }
    .tabla-gsi-oscura td { padding: 12px; border: 1px solid #334155; color: #e2e8f0; }
    </style>
""", unsafe_allow_html=True)

st.title("💎 Analizador Geotécnico GSI Modificado Real")
st.markdown("<p style='color: #94a3b8;'>Cálculo automatizado con control estricto de isolíneas y consistencia litológica de campo.</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)

# ==============================================================================
# BARRA LATERAL: ENTRADA DE DATOS (ALTO CONTRASTE GARANTIZADO)
# ==============================================================================
st.sidebar.header("🛠️ 1. Datos del Testigo (Core Run)")

longitud_total = st.sidebar.number_input("Longitud Total del Tramo (cm):", min_value=10, max_value=1000, value=200, step=10)
num_fragmentos = st.sidebar.number_input("N° de Fragmentos Registrados:", min_value=1, max_value=20, value=5, step=1)

st.sidebar.subheader("📐 Registro de Longitudes (cm):")
fragmentos = []
valores_defecto = [25, 15, 18, 32, 32]

for i in range(int(num_fragmentos)):
    val_def = valores_defecto[i] if i < len(valores_defecto) else 10
    val = st.sidebar.number_input(f"Fragmento L{i+1}:", min_value=0, max_value=200, value=val_def, step=1, key=f"l_{i}")
    fragmentos.append(val)

st.sidebar.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)
st.sidebar.header("⛏️ 2. Clasificación Superficial")

# Se renombra el parámetro a Condición Superficial según solicitud
condicion_seleccionada = st.sidebar.selectbox(
    "Condición Superficial:",
    options=["MUY BUENA (MB)", "BUENA (B)", "REGULAR (R)", "POBRE (P)", "MUY POBRE (MP)"],
    index=2
)

# Se actualizan las descripciones incluyendo textualmente el comportamiento con la picota
datos_condicion = {
    "MUY BUENA (MB)": {
        "desc": "Extremadamente resistente, fresca. Superficie de discontinuidades muy rugosas e inalteradas, cerradas. (Rc > 250 MPa).", 
        "picota": "Se astilla con golpes de picota.", 
        "color": "#38bdf8"
    },
    "BUENA (B)": {
        "desc": "Muy resistente, levemente alterada. Discontinuidades rugosas, levemente alteradas, manchas de oxidación, lig. abierta. (Rc 100 a 250 MPa).", 
        "picota": "Se rompe con varios golpes de picota.", 
        "color": "#4ade80"
    },
    "REGULAR (R)": {
        "desc": "Resistente, levemente alterada. Discontinuidades lisas, moderadamente alteradas, ligeramente abierta. (Rc 50 a 100 MPa).", 
        "picota": "Se rompe con uno o dos golpes de picota.", 
        "color": "#f59e0b"
    },
    "POBRE (P)": {
        "desc": "Moderadamente resistente, moderadamente alterada. Superficie pulida o con estriaciones, muy alterada, relleno compacto o con fragmentos de roca. (Rc 25 a 50 MPa).", 
        "picota": "Se indenta superficialmente con la picota.", 
        "color": "#f87171"
    },
    "MUY POBRE (MP)": {
        "desc": "Blanda, muy alterada. Superficie pulida y estriada, muy abierta, con relleno de arcillas blandas. (Rc < 25 MPa).", 
        "picota": "Se disgrega o indenta superficialmente con la picota.", 
        "color": "#ef4444"
    }
}

info_activa = datos_condicion[condicion_seleccionada]
st.sidebar.markdown(f"""
    <div class="panel-orientacion-oscuro" style="border-left-color: {info_activa['color']};">
        <b style="color: {info_activa['color']}; font-size: 13px;">🔬 Ensayo de Campo (Picota):</b><br>
        <b>Estado:</b> {info_activa['desc']}<br>
        <b>Comportamiento:</b> <code style='color: #ffffff; background-color:#0f172a; padding:2px 4px;'>{info_activa['picota']}</code>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# ALGORITMO GEOMECÁNICO Y CONFIGURACIÓN DE FRONTERAS (ÁBACO DE HOEK)
# ==============================================================================
fragmentos_validos = [f for f in fragmentos if f >= 10]
suma_validos = sum(fragmentos_validos)
rqd = (suma_validos / longitud_total) * 100 if longitud_total > 0 else 0.0

# Asignación de fila de Estructura según rangos de RQD oficiales de la tabla
if rqd > 75 and rqd <= 90:
    fila_activa, estructura_label = 0, "LEVEMENTE FRACTURADA (LF)"
elif rqd > 50 and rqd <= 75:
    fila_activa, estructura_label = 1, "MODERADAMENTE FRACTURADA (F)"
elif rqd > 25 and rqd <= 50:
    fila_activa, estructura_label = 2, "MUY FRACTURADA (MF)"
else:
    if num_fragmentos >= 5 and max(fragmentos) <= 35 and rqd < 25:
        fila_activa, estructura_label = 4, "TRITURADA O BRECHADA (T)"
    else:
        fila_activa, estructura_label = 3, "INTENSAMENTE FRACTURADA (IF)"

col_activa = ["MUY BUENA (MB)", "BUENA (B)", "REGULAR (R)", "POBRE (P)", "MUY POBRE (MP)"].index(condicion_seleccionada)

# Nombres correlativos de las celdas de doble entrada
matriz_letras = [
    ["LF/MB", "LF/B", "LF/R", "LF/P", "LF/MP"],
    ["F/MB",  "F/B",  "F/R",  "F/P",  "F/MP"],
    ["MF/MB", "MF/B", "MF/R", "MF/P", "MF/MP"],
    ["IF/MB", "IF/B", "IF/R", "IF/P", "IF/MP"],
    ["T/MB",  "T/B",  "T/R",  "T/P",  "T/MP"]
]

# MATRIZ HOEK REAL AUDITADA: Ajustada exactamente según el cruce de isolíneas negras de tu imagen.
# Las celdas "N/A" corresponden a zonas vacías donde no llega ninguna curva de nivel.
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
# INTERFAZ GRÁFICA: PANEL DERECHO
# ==============================================================================
st.subheader("📊 Panel de Control y Análisis Operativo")
col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.metric(label="RQD Resultante (Muestra)", value=f"{rqd:.1f} %")
    st.markdown(f"**Estructura Clasificada:** <span style='color:#38bdf8;'>{estructura_label}</span>", unsafe_allow_html=True)
    st.markdown(f"**Condición Superficial:** <span style='color:{info_activa['color']};'>{condicion_seleccionada}</span>", unsafe_allow_html=True)
    
    if valor_gsi_final == "N/A":
        st.markdown(f"""
            <div style='background-color: #7f1d1d; padding: 18px; border-radius: 8px; border: 1px solid #f87171; margin-top: 15px;'>
                <span style='color: #fca5a5; font-size: 13px; font-weight: bold;'>⚠️ CASILLA SIN CONTORNO DEFINIDO:</span><br>
                <span style='font-size: 22px; color: #ffffff; font-weight: bold;'>Valor GSI: No Existe (N/A)</span><br>
                <span style='color: #fca5a5; font-size: 12px;'>La combinación <b>{codigo_final}</b> representa una condición geomecánica vacía en el ábaco original.</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style='background-color: #1e293b; padding: 18px; border-radius: 8px; border: 1px solid #334155; margin-top: 15px;'>
                <span style='color: #94a3b8; font-size: 13px; font-weight: bold;'>🎯 INTERSECCIÓN DE ISOLÍNEA DETECTADA:</span><br>
                <span style='font-size: 28px; color: #4ade80; font-weight: bold;'>Rango GSI: {valor_gsi_final}</span><br>
                <span style='color: #cbd5e1; font-size: 12px;'>Código de Bloque Matricial: <b>{codigo_final}</b></span>
            </div>
        """, unsafe_allow_html=True)

with col_der:
    st.markdown("<b>📐 Reconstrucción Lineal Correlativa del Testigo (Sin Desfase)</b>", unsafe_allow_html=True)
    
    html_sondaje = "<div style='border: 2px solid #334155; background-color: #111827; width: 100%; height: 55px; display: table; border-collapse: collapse; border-radius: 6px; overflow: hidden;'>"
    
    for idx, frag in enumerate(fragmentos):
        if frag > 0:
            pct = (frag / longitud_total) * 100
            color = "#0284c7" if frag >= 10 else "#dc2626"
            html_sondaje += f"<div style='display: table-cell; width: {pct}%; background-color: {color}; border-right: 1px solid #0f172a; color: #ffffff; text-align: center; vertical-align: middle; font-weight: bold; font-size: 10px;'>L{idx+1}<br>{frag}cm</div>"
        else:
            html_sondaje += f"<div style='display: table-cell; width: 1.5%; background-color: #f43f5e; border-right: 1px solid #0f172a; color: #ffffff; text-align: center; vertical-align: middle; font-weight: bold; font-size: 8px;'>L{idx+1}<br>Fx</div>"
            
    suma_piezas = sum(fragmentos)
    perdida_total = longitud_total - suma_piezas
    if perdida_total > 0:
        pct_p = (perdida_total / longitud_total) * 100
        html_sondaje += f"<div style='display: table-cell; width: {pct_p}%; background-color: #334155; color: #94a3b8; text-align: center; vertical-align: middle; font-size: 10px; font-style: italic;'>Pérdida<br>{perdida_total}cm</div>"
        
    html_sondaje += "</div>"
    st.markdown(html_sondaje, unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: #334155;'>", unsafe_allow_html=True)

# ==============================================================================
# AUDITORÍA DE MATRIZ DE DOBLE ENTRADA (ESTRUCTURA vs CONDICIÓN SUPERFICIAL)
# ==============================================================================
st.subheader("🗺️ Matriz de Doble Entrada: GSI Modificado Homologado")

# Definición nítida de Filas (Estructura)
filas_tabla = [
    "<b>LEVEMENTE FRACTURADA (LF)</b><br><small style='color:#94a3b8;'>RQD 75 - 90%</small>",
    "<b>MODERADAMENTE FRACTURADA (F)</b><br><small style='color:#94a3b8;'>RQD 50 - 75%</small>",
    "<b>MUY FRACTURADA (MF)</b><br><small style='color:#94a3b8;'>RQD 25 - 50%</small>",
    "<b>INTENSAMENTE FRACTURADA (IF)</b><br><small style='color:#94a3b8;'>RQD 0 - 25%</small>",
    "<b>TRITURADA O BRECHADA (T)</b><br><small style='color:#94a3b8;'>Sin RQD</small>"
]

# Definición nítida de Columnas (Condición Superficial) con notas abreviadas de picota
headers = [
    "<th>MUY BUENA (MB)<br><small style='color:#94a3b8;'>Astilla c/ picota</small></th>", 
    "<th>BUENA (B)<br><small style='color:#94a3b8;'>Varios golpes</small></th>", 
    "<th>REGULAR (R)<br><small style='color:#94a3b8;'>1 o 2 golpes</small></th>", 
    "<th>POBRE (P)<br><small style='color:#94a3b8;'>Indenta sup.</small></th>", 
    "<th>MUY POBRE (MP)<br><small style='color:#94a3b8;'>Se disgrega</small></th>"
]

html = f"<table class='tabla-gsi-oscura'><thead><tr><th>ESTRUCTURA DEL MACIZO (Filas) ↓ / CONDICIÓN SUPERFICIAL (Columnas) →</th>{"".join(headers)}</tr></thead><tbody>"

for i, fila in enumerate(filas_tabla):
    html += f"<tr><td style='background-color: #1e293b; text-align: left; font-weight: bold; color: #ffffff; padding: 12px;'>{fila}</td>"
    for j in range(5):
        val_gsi = matriz_valores_gsi[i][j]
        cod_gsi = matriz_letras[i][j]
        
        if val_gsi == "N/A":
            if i == fila_activa and j == col_activa:
                bg = "#7f1d1d"
                color = "#f87171"
                border = "border: 3.5px solid #ef4444; font-weight: bold;"
                contenido = f"<b>{cod_gsi}</b><br><span style='font-size:11px; color:#f87171;'>Vacio Real</span>"
            else:
                bg = "#1f1616"
                border = "border: 1px dashed #453131;"
                contenido = f"<span style='color:#453131;'>{cod_gsi}</span><br><span style='font-size:12px; color:#453131;'>- - -</span>"
        else:
            if i == fila_activa and j == col_activa:
                bg = "#064e3b"
                color = "#4ade80"
                border = "border: 3.5px solid #4ade80; font-weight: bold; box-shadow: inset 0 0 8px #4ade80;"
            else:
                bg = "#111827"
                color = "#94a3b8"
                border = "border: 1px solid #334155;"
            contenido = f"<b>{cod_gsi}</b><br><span style='font-size:12px; color:#ffffff;'>Línea GSI: <b>{val_gsi}</b></span>"
            
        html += f"<td style='background-color: {bg}; {border}'>{contenido}</td>"
    html += "</tr>"
    
html += "</tbody></table>"
st.markdown(html, unsafe_allow_html=True)
