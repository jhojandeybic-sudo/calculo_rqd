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
    page_title="GSI Modificado - Versión Operativa Completa", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# ARQUITECTURA CSS: Optimización de Espacios Muertos y Paneles de Ingeniería
# ==============================================================================
st.markdown("""
    <style>
    .stApp { background-color: #090d16 !important; }
    
    .block-container {
        background-color: #0f172a;
        padding: 1.2rem 2rem !important;
        border-radius: 12px;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.5);
        margin-top: 0.3rem !important;
    }

    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    
    [data-testid="stSidebar"] .stElementContainer {
        margin-bottom: 0.3rem !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: #f8fafc !important;
    }

    /* CONTROL DE INPUTS: Cajas con texto numérico en NEGRO nítido */
    [data-testid="stSidebar"] div[data-baseweb="input"] {
        background-color: #ffffff !important; 
        border: 2px solid #38bdf8 !important;  
        border-radius: 6px !important;
        height: 38px !important;
    }
    [data-testid="stSidebar"] input {
        color: #000000 !important; 
        font-weight: bold !important;
    }
    
    [data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 6px !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: #000000 !important; 
        font-weight: bold !important;
    }
    
    h1, h2, h3, p, span, label { color: #f8fafc !important; }
    div[data-testid="stMetricValue"] { color: #38bdf8 !important; font-weight: bold; font-size: 2rem !important; }
    div[data-testid="stMetricLabel"] { color: #94a3b8 !important; }
    .stMetric { background-color: #1e293b; padding: 10px 14px; border-radius: 8px; border: 1px solid #334155; }
    
    .panel-orientacion-oscuro {
        background-color: #1e293b;
        padding: 10px 14px;
        border-radius: 6px;
        border-left: 4px solid #38bdf8;
        margin-top: 5px;
        font-size: 12px;
        color: #cbd5e1;
    }
    
    /* PANELES DE COMPORTAMIENTO GEOMECÁNICO ADICIONADOS */
    .panel-comportamiento {
        padding: 12px 16px;
        border-radius: 8px;
        margin-top: 8px;
        border: 1px solid #334155;
    }
    
    .tabla-gsi-oscura { 
        width: 100%; 
        border-collapse: collapse; 
        text-align: center; 
        font-family: sans-serif; 
        font-size: 11px; 
        border: 1px solid #334155;
        background-color: #111827;
        margin-top: 6px;
    }
    .tabla-gsi-oscura th { 
        background-color: #1e293b; 
        color: #38bdf8; 
        padding: 10px 6px; 
        border: 1px solid #334155; 
        vertical-align: top;
    }
    .tabla-gsi-oscura td { padding: 10px 6px; border: 1px solid #334155; color: #e2e8f0; }
    
    hr { margin: 0.8rem 0 !important; border-color: #334155 !important; }
    </style>
""", unsafe_allow_html=True)

# Encabezados principales
st.title("💎 Analizador Geotécnico GSI Modificado Real")
st.markdown("<p style='color: #94a3b8; margin-top:-10px;'>Cálculo automatizado del Índice Geológico de Resistencia mediante control de testigos e ingeniería de comportamiento in-situ.</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ==============================================================================
# BARRA LATERAL: ENTRADA DINÁMICA DE DATOS
# ==============================================================================
st.sidebar.header("🛠️ 1. Datos del Testigo (Core Run)")
longitud_total = st.sidebar.number_input("Longitud Total del Tramo (cm):", min_value=10, max_value=1000, value=200, step=10)

# El usuario puede modificar libremente la cantidad de fragmentos
num_fragmentos = st.sidebar.number_input("N° de Fragmentos Registrados:", min_value=1, max_value=30, value=4, step=1)

st.sidebar.subheader("📐 Registro de Longitudes (cm):")
valores_predeterminados = [25, 15, 18, 32]
fragmentos = []

for i in range(int(num_fragmentos)):
    val_def = valores_predeterminados[i] if i < len(valores_predeterminados) else 10
    val = st.sidebar.number_input(f"Fragmento L{i+1}:", min_value=0, max_value=200, value=val_def, step=1, key=f"l_{i}")
    fragmentos.append(val)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.header("⛏️ 2. Clasificación Superficial")

condicion_seleccionada = st.sidebar.selectbox(
    "Condición Superficial:",
    options=["MUY BUENA (MB)", "BUENA (B)", "REGULAR (R)", "POBRE (P)", "MUY POBRE (MP)"],
    index=2
)

# Textos completos recuperados del ábaco oficial
datos_condicion = {
    "MUY BUENA (MB)": {
        "desc": "Extremadamente resistente, fresca. Superficie de las discontinuidades muy rugosas e inalteradas, cerradas. (Rc > 250 MPa).", 
        "picota": "Se astilla con golpes de picota.", "color": "#38bdf8"
    },
    "BUENA (B)": {
        "desc": "Muy resistente, levemente alterada. Discontinuidades rugosas, levemente alteradas, manchas de oxidación, lig. abierta. (Rc 100 a 250 MPa).", 
        "picota": "Se rompe con varios golpes de picota.", "color": "#4ade80"
    },
    "REGULAR (R)": {
        "desc": "Resistente, levemente alterada. Discontinuidades lisas, moderadamente alteradas, ligeramente abierta. (Rc 50 a 100 MPa).", 
        "picota": "Se rompe con uno o dos golpes de picota.", "color": "#f59e0b"
    },
    "POBRE (P)": {
        "desc": "Moderadamente resistente, moderadamente alterada. Superficie pulida o con estriaciones, muy alterada, relleno compacto o con fragmentos de roca. (Rc 25 a 50 MPa).", 
        "picota": "Se indenta superficialmente con la picota.", "color": "#f87171"
    },
    "MUY POBRE (MP)": {
        "desc": "Blanda, muy alterada. Superficie pulida y estriada, muy abierta, con relleno de arcillas blandas. (Rc < 25 MPa).", 
        "picota": "Se disgrega o indenta superficialmente con la picota.", "color": "#ef4444"
    }
}

info_activa = datos_condicion[condicion_seleccionada]
st.sidebar.markdown(f"""
    <div class="panel-orientacion-oscuro" style="border-left-color: {info_activa['color']};">
        <b style="color: {info_activa['color']}; font-size: 13px;">🔬 Ensayo de Campo (Picota):</b><br>
        <b>Estado:</b> {info_activa['desc']}<br>
        <b>Comportamiento:</b> <code style='color: #000000; background-color:#ffffff; padding:2px 4px; font-weight:bold; border-radius:3px;'>{info_activa['picota']}</code>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# ALGORITMO GEOMECÁNICO COMPLETO (MALLA DE HOEK)
# ==============================================================================
fragmentos_validos = [f for f in fragmentos if f >= 10]
suma_validos = sum(fragmentos_validos)
rqd = (suma_validos / longitud_total) * 100 if longitud_total > 0 else 0.0

# Estructura del macizo según rangos oficiales de RQD
if rqd > 75 and rqd <= 90:
    fila_activa, estructura_label = 0, "LEVEMENTE FRACTURADA"
elif rqd > 50 and rqd <= 75:
    fila_activa, estructura_label = 1, "MODERADAMENTE FRACTURADA"
elif rqd > 25 and rqd <= 50:
    fila_activa, estructura_label = 2, "MUY FRACTURADA"
else:
    if num_fragmentos >= 4 and (len(fragmentos) == 0 or max(fragmentos) <= 35) and rqd < 25:
        fila_activa, estructura_label = 4, "TRITURADA O BRECHADA"
    else:
        fila_activa, estructura_label = 3, "INTENSAMENTE FRACTURADA"

col_activa = ["MUY BUENA (MB)", "BUENA (B)", "REGULAR (R)", "POBRE (P)", "MUY POBRE (MP)"].index(condicion_seleccionada)

matriz_letras = [
    ["LF/MB", "LF/B", "LF/R", "LF/P", "LF/MP"],
    ["F/MB",  "F/B",  "F/R",  "F/P",  "F/MP"],
    ["MF/MB", "MF/B", "MF/R", "MF/P", "MF/MP"],
    ["IF/MB", "IF/B", "IF/R", "IF/P", "IF/MP"],
    ["T/MB",  "T/B",  "T/R",  "T/P",  "T/MP"]
]

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
# MAPEO DEL COMPORTAMIENTO TÍPICO EN INGENIERÍA (NUEVA BASE DE DATOS)
# ==============================================================================
def obtener_comportamiento_geotecnico(rango_gsi):
    if rango_gsi == "N/A":
        return "Indeterminada", "Combinación estructural no registrada.", "#64748b"
    
    # Extraemos el valor representativo más alto para clasificar según tu tabla
    try:
        limite_superior = int(rango_gsi.split("-")[0])
    except ValueError:
        limite_superior = int(rango_gsi) # Caso del valor "5"
        
    if limite_superior > 85:
        return "Muy Buena", "Excelente autosoporte; bloques grandes y estables.", "#38bdf8"
    elif limite_superior > 65:
        return "Buena", "Buena estabilidad; requiere soporte ligero o localizado.", "#4ade80"
    elif limite_superior > 45:
        # Nota: El rango "65-60" de nuestro caso entra de forma exacta aquí (Estabilidad Media)
        return "Regular", "Estabilidad media; bloques propensos a deslizar o caer.", "#f59e0b"
    elif limite_superior > 25:
        return "Mala", "Deformaciones rápidas; requiere soporte inmediato (pernos/shocrete).", "#f87171"
    else:
        return "Muy Mala", "Comportamiento plástico o suelo; colapsos inmediatos sin soporte.", "#ef4444"

calidad_roca, comportamiento_texto, color_comportamiento = obtener_comportamiento_geotecnico(valor_gsi_final)

# ==============================================================================
# DESPLIEGUE DEL PANEL DE CONTROL E INFORME COMPACTO
# ==============================================================================
st.subheader("📊 Panel de Control y Análisis Operativo")
col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.metric(label="RQD Resultante (Muestra)", value=f"{rqd:.1f} %")
    st.markdown(f"**Estructura Clasificada:** <span style='color:#38bdf8;'>{estructura_label}</span>", unsafe_allow_html=True)
    st.markdown(f"**Condición de Discontinuidades:** <span style='color:{info_activa['color']};'>{condicion_seleccionada}</span>", unsafe_allow_html=True)
    
    if valor_gsi_final == "N/A":
        st.markdown(f"""
            <div style='background-color: #7f1d1d; padding: 12px; border-radius: 8px; border: 1px solid #ef4444; margin-top: 8px;'>
                <span style='font-size: 20px; color: #ffffff; font-weight: bold;'>Valor GSI: No Existe (N/A)</span><br>
                <span style='color: #fca5a5; font-size: 12px;'>Bloque vacío en el ábaco.</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style='background-color: #1e293b; padding: 12px; border-radius: 8px; border: 1px solid #334155; margin-top: 8px;'>
                <span style='font-size: 24px; color: #4ade80; font-weight: bold;'>Rango GSI Calculado: {valor_gsi_final}</span><br>
                <span style='color: #cbd5e1; font-size: 12px;'>Bloque de Intersección Matricial: <b>{codigo_final}</b></span>
            </div>
        """, unsafe_allow_html=True)
        
        # ¡NUEVO COMPONENTE TRASLADADO DE LA TABLA DE COMPORTAMIENTO ADJUNTADA!
        st.markdown(f"""
            <div class="panel-comportamiento" style="background-color: #111827; border-left: 5px solid {color_comportamiento};">
                <span style='color: {color_comportamiento}; font-weight: bold; font-size: 14px;'>📋 CALIDAD DE LA MASA ROCOSA: {calidad_roca.upper()}</span><br>
                <p style='margin: 4px 0px 0px 0px; font-size: 12px; color: #e2e8f0;'><b>Comportamiento Típico en Ingeniería:</b> {comportamiento_texto}</p>
            </div>
        """, unsafe_allow_html=True)

with col_der:
    st.markdown("<b>📐 Reconstrucción Lineal Correlativa del Testigo (Sin Desfase)</b>", unsafe_allow_html=True)
    
    html_sondaje = "<div style='border: 2px solid #334155; background-color: #111827; width: 100%; height: 50px; display: table; border-collapse: collapse; border-radius: 6px; overflow: hidden;'>"
    for idx, frag in enumerate(fragmentos):
        if frag > 0:
            pct = (frag / longitud_total) * 100
            color = "#0284c7" if frag >= 10 else "#dc2626"
            html_sondaje += f"<div style='display: table-cell; width: {pct}%; background-color: {color}; border-right: 1px solid #0f172a; color: #ffffff; text-align: center; vertical-align: middle; font-weight: bold; font-size: 10px;'>L{idx+1}<br>{frag}cm</div>"
            
    suma_piezas = sum(fragmentos)
    perdida_total = longitud_total - suma_piezas
    if perdida_total > 0:
        pct_p = (perdida_total / longitud_total) * 100
        html_sondaje += f"<div style='display: table-cell; width: {pct_p}%; background-color: #334155; color: #94a3b8; text-align: center; vertical-align: middle; font-size: 10px; font-style: italic;'>Pérdida<br>{perdida_total}cm</div>"
    html_sondaje += "</div>"
    st.markdown(html_sondaje, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==============================================================================
# AUDITORÍA DE MATRIZ COMPLETA
# ==============================================================================
st.subheader("🗺️ Matriz de Doble Entrada Completa: GSI Modificado")

filas_tabla = [
    "<b>LEVEMENTE FRACTURADA (LF)</b><br><small style='color:#94a3b8;'>Tres a menos sistemas muy espaciados<br><b>RQD 75 - 90%</b> (2 a 6 frac/m)</small>",
    "<b>MODERADAMENTE FRACTURADA (F)</b><br><small style='color:#94a3b8;'>Muy bien trabada, bloques cúbicos<br><b>RQD 50 - 75%</b> (6 a 12 frac/m)</small>",
    "<b>MUY FRACTURADA (MF)</b><br><small style='color:#94a3b8;'>Parcialmente disturbada, bloques angulosos<br><b>RQD 25 - 50%</b> (12 a 20 frac/m)</small>",
    "<b>INTENSAMENTE FRACTURADA (IF)</b><br><small style='color:#94a3b8;'>Plegamiento y fallamiento, bloques irregulares<br><b>RQD 0 - 25%</b> (Más de 20 frac/m)</small>",
    "<b>TRITURADA O BRECHADA (T)</b><br><small style='color:#94a3b8;'>Masa rocosa extremadamente rota<br><b>Sin RQD</b> (Fácilmente disgregable)</small>"
]

headers = [
    "<th>MUY BUENA (MB)<br><small style='color:#ec4899;'>Astilla c/ picota</small><br><small style='color:#94a3b8;'>Rc > 250 MPa</small></th>", 
    "<th>BUENA (B)<br><small style='color:#ec4899;'>Varios golpes</small><br><small style='color:#94a3b8;'>Rc 100-250 MPa</small></th>", 
    "<th>REGULAR (R)<br><small style='color:#ec4899;'>1 o 2 golpes</small><br><small style='color:#94a3b8;'>Rc 50-100 MPa</small></th>", 
    "<th>POBRE (P)<br><small style='color:#ec4899;'>Indenta sup.</small><br><small style='color:#94a3b8;'>Rc 25-50 MPa</small></th>", 
    "<th>MUY POBRE (MP)<br><small style='color:#ec4899;'>Se disgrega</small><br><small style='color:#94a3b8;'>Rc < 25 MPa</small></th>"
]

html = f"<table class='tabla-gsi-oscura'><thead><tr><th>ESTRUCTURA DEL MACIZO ↓ / CONDICIÓN SUPERFICIAL →</th>{"".join(headers)}</tr></thead><tbody>"

for i, fila in enumerate(filas_tabla):
    html += f"<tr><td style='background-color: #1e293b; text-align: left; font-weight: bold; color: #ffffff; padding: 10px; font-size:11px;'>{fila}</td>"
    for j in range(5):
        val_gsi = matriz_valores_gsi[i][j]
        cod_gsi = matriz_letras[i][j]
        
        if val_gsi == "N/A":
            if i == fila_activa and j == col_activa:
                bg = "#7f1d1d"; border = "border: 3px solid #ef4444; font-weight: bold;"
                contenido = f"<b>{cod_gsi}</b><br><span style='font-size:11px; color:#f87171;'>Vacío</span>"
            else:
                bg = "#1f1616"; border = "border: 1px dashed #453131;"
                contenido = f"<span style='color:#453131;'>{cod_gsi}</span><br><span style='font-size:11px; color:#453131;'>- - -</span>"
        else:
            if i == fila_activa and j == col_activa:
                bg = "#064e3b"; border = "border: 3px solid #4ade80; font-weight: bold; box-shadow: inset 0 0 8px #4ade80;"
            else:
                bg = "#111827"; border = "border: 1px solid #334155;"
            contenido = f"<b>{cod_gsi}</b><br><span style='font-size:12px; color:#ffffff;'>Línea: <b>{val_gsi}</b></span>"
            
        html += f"<td style='background-color: {bg}; {border}'>{contenido}</td>"
    html += "</tr>"
    
html += "</tbody></table>"
st.markdown(html, unsafe_allow_html=True)
