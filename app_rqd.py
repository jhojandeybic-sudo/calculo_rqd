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

# 1. CONFIGURACIÓN ESTRUCTURAL Y LENGUAJE
st.set_page_config(
    page_title="GSI Modificado - Panel Geotécnico", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILOS CSS: Paleta balanceada (Ni todo oscuro ni todo claro)
st.markdown("""
    <style>
    /* Fondo general de la aplicación (Gris claro balanceado) */
    .stApp {
        background-color: #f1f5f9;
    }
    
    /* Contenedor principal de contenido */
    .block-container {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 1rem;
    }

    /* Tarjetas de Métricas */
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Cuadro de orientación del Glosario en la Barra Lateral */
    .glosario-sidebar {
        background-color: #f8fafc;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #0284c7;
        margin-top: 15px;
        font-size: 13px;
        color: #1e293b;
    }

    /* Tablas Geomecánicas de Alta Visibilidad */
    table { 
        width: 100%; 
        border-collapse: collapse; 
        text-align: center; 
        font-family: sans-serif; 
        font-size: 12px; 
        border: 1px solid #cbd5e1;
        background-color: #ffffff;
    }
    th { 
        background-color: #1e293b; 
        color: #ffffff; 
        padding: 12px; 
        border: 1px solid #cbd5e1; 
    }
    td { 
        padding: 12px; 
        border: 1px solid #cbd5e1; 
        color: #334155;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado Corporativo
st.title("💎 Sistema de Logueo Geomecánico: RQD y GSI Modificado")
st.markdown("Plataforma analítica con asistencia técnica visual en tiempo real para ingeniería de rocas.")
st.markdown("---")

# ==============================================================================
# BARRA LATERAL: ENTRADA DE DATOS Y GUÍA TÉCNICA EN VIVO
# ==============================================================================
st.sidebar.header("🛠️ 1. Parámetros del Testigo")

longitud_total = st.sidebar.number_input(
    "Longitud Total de la Corrida (cm):", 
    min_value=10, max_value=1000, value=200, step=10,
    help="Longitud del intervalo de perforación recuperado (Core Run)."
)

num_fragmentos = st.sidebar.number_input(
    "Cantidad de Fragmentos Medidos:",
    min_value=1, max_value=20, value=4, step=1
)

st.sidebar.subheader("📐 Geometría de Fragmentos (cm):")
fragmentos = []
valores_ejercicio = [25, 15, 18, 32]

for i in range(int(num_fragmentos)):
    val_defecto = valores_ejercicio[i] if i < len(valores_ejercicio) else 10
    val = st.sidebar.number_input(
        f"Pieza L{i+1}:", 
        min_value=0, max_value=200, value=val_defecto, step=1, key=f"l_{i}"
    )
    fragmentos.append(val)

st.sidebar.markdown("---")
st.sidebar.header("⛏️ 2. Condición de Discontinuidades")

condicion_seleccionada = st.sidebar.selectbox(
    "Grado de Alteración / Rugosidad:",
    options=[
        "MUY BUENA (MB)",
        "BUENA (B)",
        "REGULAR (R)",
        "POBRE (P)",
        "MUY POBRE (MP)"
    ],
    index=2,
    help="Selecciona para ver su descripción técnica detallada abajo."
)

# Diccionario analítico del Glosario para orientación en tiempo real
info_glosario = {
    "MUY BUENA (MB)": {
        "desc": "Superficies muy rugosas, frescas, cerradas e inalteradas.",
        "resistencia": "> 250 MPa (Se astilla con golpes de picota)",
        "color": "#0369a1"
    },
    "BUENA (B)": {
        "desc": "Superficies rugosas, levemente alteradas con manchas de oxidación, ligeramente abiertas.",
        "resistencia": "100 a 250 MPa (Resistencia alta en campo)",
        "color": "#15803d"
    },
    "REGULAR (R)": {
        "desc": "Superficies lisas, moderadamente alteradas, ligeramente abiertas.",
        "resistencia": "50 a 100 MPa (Rompe con 1 o 2 golpes de picota)",
        "color": "#b45309"
    },
    "POBRE (P)": {
        "desc": "Superficies pulidas o estriadas, alteradas con relleno compacto o fragmentos de roca.",
        "resistencia": "25 a 50 MPa (Se indenta superficialmente)",
        "color": "#b91c1c"
    },
    "MUY POBRE (MP)": {
        "desc": "Superficies pulidas/estriadas con rellenos potentes de arcillas blandas.",
        "resistencia": "< 25 MPa (Se disgrega con facilidad)",
        "color": "#7f1d1d"
    }
}

# Despliegue de la previsualización del Glosario en la barra lateral
glosario_activo = info_glosario[condicion_seleccionada]
st.sidebar.markdown(f"""
    <div class="glosario-sidebar" style="border-left-color: {glosario_activo['color']};">
        <b style="color: {glosario_activo['color']}; font-size: 14px;">📖 Guía de Orientación:</b><br><br>
        <b>Descripción:</b> {glosario_activo['desc']}<br><br>
        <b>Resistencia Estimada:</b> <code>{glosario_activo['resistencia']}</code>
    </div>
""", unsafe_allow_html=True)


# ==============================================================================
# PROCESAMIENTO MATEMÁTICO DE ÍNDICES CRÍTICOS
# ==============================================================================
fragmentos_validos = [f for f in fragmentos if f >= 10]
suma_validos = sum(fragmentos_validos)
rqd = (suma_validos / longitud_total) * 100 if longitud_total > 0 else 0.0

# Asignación de Fila (Estructura)
if rqd > 75 and rqd <= 90:
    fila_activa, estructura_label = 0, "LEVEMENTE FRACTURADA (LF)"
    desc_fila = "3 a menos sistemas de discontinuidades muy espaciadas."
elif rqd > 50 and rqd <= 75:
    fila_activa, estructura_label = 1, "MODERADAMENTE FRACTURADA (F)"
    desc_fila = "Bloques cúbicos bien trabados formados por 3 familias ortonormales."
elif rqd > 25 and rqd <= 50:
    fila_activa, estructura_label = 2, "MUY FRACTURADA (MF)"
    desc_fila = "Bloques angulosos formados por 4 o más familias de discontinuidades."
else:
    if suma_validos == 0 and num_fragmentos > 4:
        fila_activa, estructura_label = 4, "TRITURADA O BRECHADA (T)"
        desc_fila = "Masa rocosa extremadamente rota, fragmentos disgregables. Sin RQD analítico."
    else:
        fila_activa, estructura_label = 3, "INTENSAMENTE FRACTURADA (IF)"
        desc_fila = "Plegamiento severo con abundantes bloques irregulares."

# Asignación de Columna (Condición)
if "MUY BUENA" in condicion_seleccionada:
    col_activa = 0
elif "BUENA" in condicion_seleccionada:
    col_activa = 1
elif "REGULAR" in condicion_seleccionada:
    col_activa = 2
elif "POBRE" in condicion_seleccionada:
    col_activa = 3
else:
    col_activa = 4

# Matrices de Datos Estructurales
matriz_letras = [
    ["LF/MB", "LF/B", "LF/R", "LF/P", "LF/MP"],
    ["F/MB",  "F/B",  "F/R",  "F/P",  "F/MP"],
    ["MF/MB", "MF/B", "MF/R", "MF/P", "MF/MP"],
    ["IF/MB", "IF/B", "IF/R", "IF/P", "IF/MP"],
    ["T/MB",  "T/B",  "T/R",  "T/P",  "T/MP"]
]

matriz_valores_gsi = [
    ["95", "85", "75", "60", "45"],
    ["80", "70", "60", "50", "35"],
    ["65", "55", "45", "35", "25"],
    ["50", "40", "30", "20", "10"],
    ["35", "25", "15", "10", "5"]
]

codigo_final = matriz_letras[fila_activa][col_activa]
valor_gsi_final = matriz_valores_gsi[fila_activa][col_activa]


# ==============================================================================
# PANEL PRINCIPAL VISUAL (OUTPUT)
# ==============================================================================
tab_reporte, tab_matrices = st.tabs([
    "📊 Pestaña 1: Diagnóstico Operativo", 
    "🗺️ Pestaña 2: Auditoría y Ubicación Matricial GSI"
])

# --- PESTAÑA 1: REPORTE OPERATIVO ---
with tab_reporte:
    col_res, col_graf = st.columns([1, 1.3])
    
    with col_res:
        st.subheader("📋 Resumen Estadístico de Salida")
        st.metric(label="RQD Resultante", value=f"{rqd:.1f} %")
        
        st.markdown(f"**Estructura del Macizo:** `{estructura_label}`")
        st.caption(f"_{desc_fila}_")
        
        st.markdown(f"**Condición Superficial:** `{condicion_seleccionada}`")
        
        st.info(f"### 🎯 GSI Calculado: ~ {valor_gsi_final} (Clase: {codigo_final})")
        
    with col_graf:
        st.subheader("📐 Representación del Testigo a Escala")
        
        html_sondaje = "<div style='border: 2px solid #cbd5e1; background-color: #f8fafc; width: 100%; height: 60px; display: table; border-collapse: collapse; border-radius: 6px; overflow: hidden;'>"
        suma_piezas = sum(fragmentos)
        perdida_total = longitud_total - suma_piezas
        
        for idx, frag in enumerate(fragmentos):
            if frag > 0:
                pct = (frag / longitud_total) * 100
                color = "#2563eb" if frag >= 10 else "#dc2626" # Azul vs Rojo
                html_sondaje += f"<div style='display: table-cell; width: {pct}%; background-color: {color}; border-right: 1px solid #ffffff; color: #ffffff; text-align: center; vertical-align: middle; font-weight: bold; font-size: 11px;'>L{idx+1}<br>{frag}cm</div>"
                
        if perdida_total > 0:
            pct_p = (perdida_total / longitud_total) * 100
            html_sondaje += f"<div style='display: table-cell; width: {pct_p}%; background-color: #cbd5e1; color: #475569; text-align: center; vertical-align: middle; font-size: 11px; font-style: italic;'>Pérdida<br>{perdida_total}cm</div>"
            
        html_sondaje += "</div>"
        st.markdown(html_sondaje, unsafe_allow_html=True)
        st.markdown("<p style='font-size:12px; text-align:center; margin-top:8px;'><span style='color:#2563eb;'>■</span> Fragmento Apto (≥10cm) &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#dc2626;'>■</span> Fragmento Ignorado (<10cm) &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#cbd5e1;'>■</span> Pérdida de Muestra</p>", unsafe_allow_html=True)
        
        st.write("---")
        st.latex(rf"\text{{RQD}} = \left( \frac{{\sum \text{{L}}_{{\ge 10\,\text{{cm}}}}}}{{\text{{L}}_{{\text{{total}}}}}} \right) \times 100 = \left( \frac{{{suma_validos}\,\text{{cm}}}}{{{longitud_total}\,\text{{cm}}}} \right) \times 100 = {rqd:.1f}\%")

# --- PESTAÑA 2: AUDITORÍA DE MATRICES ---
with tab_matrices:
    st.subheader("🗺️ Matriz Estructural de Control GSI")
    st.caption("La celda resaltada en verde brillante denota la intersección geomecánica de tu diseño actual.")
    
    filas_tabla = [
        "<b>LEVEMENTE FRACTURADA (LF)</b><br><small>RQD 75-90%</small>",
        "<b>MODERADAMENTE FRACTURADA (F)</b><br><small>RQD 50-75%</small>",
        "<b>MUY FRACTURADA (MF)</b><br><small>RQD 25-50%</small>",
        "<b>INTENSAMENTE FRACTURADA (IF)</b><br><small>RQD 0-25%</small>",
        "<b>TRITURADA O BRECHADA (T)</b><br><small>Sin RQD</small>"
    ]
    headers = ["<th>MUY BUENA (MB)</th>", "<th>BUENA (B)</th>", "<th>REGULAR (R)</th>", "<th>POBRE (P)</th>", "<th>MUY POBRE (MP)</th>"]

    html = f"<table><thead><tr><th>ESTRUCTURA DEL MACIZO</th>{"".join(headers)}</tr></thead><tbody>"
    for i, fila in enumerate(filas_tabla):
        html += f"<tr><td style='background-color: #f8fafc; text-align: left; font-weight: bold;'>{fila}</td>"
        for j in range(5):
            val_gsi = matriz_valores_gsi[i][j]
            cod_gsi = matriz_letras[i][j]
            
            # Resaltado verde de alta visibilidad técnica si la celda está activa
            if i == fila_activa and j == col_activa:
                bg = "#dcfce7"
                color = "#15803d"
                border = "border: 3.5px solid #22c55e; font-weight: bold; font-size: 13px;"
            else:
                bg = "#ffffff"
                color = "#64748b"
                border = "border: 1px solid #cbd5e1;"
                
            html += f"<td style='background-color: {bg}; color: {color}; {border}'>Clase: <b>{cod_gsi}</b><br>Índice: <b>{val_gsi}</b></td>"
        html += "</tr>"
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)
