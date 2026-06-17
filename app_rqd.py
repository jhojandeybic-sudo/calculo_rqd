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

# 1. CONFIGURACIÓN ESTRUCTURAL DE ALTA DENSIDAD
st.set_page_config(
    page_title="GSI Modificado - Engine Analytica", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Corporativos para Tablas Geomecánicas e Indicadores
st.markdown("""
    <style>
    .reportview-container .main .block-container{ padding-top: 1rem; }
    .stMetric { background-color: #0f172a; padding: 18px; border-radius: 8px; border: 1px solid #1e293b; }
    div.stExpander { border: 1px solid #1e293b !important; }
    table { width:100%; border-collapse: collapse; text-align: center; font-family: sans-serif; font-size: 11.5px; border: 1px solid #334155; }
    th { background-color: #1e293b; color: #FFF; padding: 12px; border: 1px solid #334155; }
    td { padding: 12px; border: 1px solid #334155; }
    </style>
""", unsafe_allow_html=True)

# Encabezado Ejecutivo
st.title("💎 Sistema de Logueo Geomecánico: RQD y GSI Modificado")
st.markdown("Plataforma analítica para la clasificación estructural de macizos rocosos en ingeniería de minas y túneles.")
st.markdown("---")

# ==============================================================================
# BARRA LATERAL: ENTRADA DE DATOS UNIFICADA (INPUT)
# ==============================================================================
st.sidebar.header("🛠️ 1. Parámetros del Testigo")

longitud_total = st.sidebar.number_input(
    "Longitud Total de la Corrida (cm):", 
    min_value=10, max_value=1000, value=200, step=10,
    help="Longitud total del intervalo de perforación recuperado (Core Run)."
)

num_fragmentos = st.sidebar.number_input(
    "Cantidad de Fragmentos Medidos:",
    min_value=1, max_value=20, value=4, step=1,
    help="Número de piezas físicas de testigo a registrar."
)

st.sidebar.subheader("📐 Geometría de Fragmentos (cm):")
fragmentos = []
# Datos predeterminados depurados (Sin ceros analíticos para mantener el RQD base limpio)
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
    "Grado de Alteración / Rugosidad de Juntas:",
    options=[
        "MUY BUENA (Superficies muy rugosas, inalteradas, cerradas)",
        "BUENA (Rugosa, levemente meteorizada, manchas de oxidación)",
        "REGULAR (Lisa, moderadamente alterada, abierta, rompe con 1-2 golpes)",
        "POBRE (Pulida, estriada, relleno compacto o fragmentos)",
        "MUY POBRE (Superficie pulida/estriada, relleno de arcilla blanda)"
    ],
    index=2,
    help="Evaluación geomecánica in situ mediante resistencia a la picota y estado planar."
)

# ==============================================================================
# PROCESAMIENTO LOGICO-MATEMÁTICO (CÁLCULO DE ÍNDICES CRÍTICOS)
# ==============================================================================
fragmentos_validos = [f for f in fragmentos if f >= 10]
suma_validos = sum(fragmentos_validos)
rqd = (suma_validos / longitud_total) * 100 if longitud_total > 0 else 0.0

# Asignación de Fila (Estructura del Macizo según RQD)
if rqd > 75 and rqd <= 90:
    fila_activa, estructura_label = 0, "LEVEMENTE FRACTURADA (LF)"
    desc_fila = "3 a menos sistemas de discontinuidades muy espaciadas (2-6 fracturas/metro)."
elif rqd > 50 and rqd <= 75:
    fila_activa, estructura_label = 1, "MODERADAMENTE FRACTURADA (F)"
    desc_fila = "Bloques cúbicos bien trabados formados por 3 familias ortogonales (6-12 fracturas/metro)."
elif rqd > 25 and rqd <= 50:
    fila_activa, estructura_label = 2, "MUY FRACTURADA (MF)"
    desc_fila = "Bloques angulosos formados por 4 o más familias de discontinuidades (12-20 fracturas/metro)."
else:
    if suma_validos == 0 and num_fragmentos > 4:
        fila_activa, estructura_label = 4, "TRITURADA O BRECHADA (T)"
        desc_fila = "Masa rocosa extremadamente rota, fragmentos fácilmente disgregables. Sin RQD."
    else:
        fila_activa, estructura_label = 3, "INTENSAMENTE FRACTURADA (IF)"
        desc_fila = "Plegamiento/fallamiento severo con bloques irregulares (Más de 20 fracturas/metro)."

# Asignación de Columna (Condición Superficial)
if "MUY BUENA" in condicion_seleccionada:
    col_activa, condicion_label = 0, "MUY BUENA (MB)"
    desc_columna = "Superficies inalteradas, cerradas. Se astilla con picota (Rc > 250 MPa)."
elif "BUENA" in condicion_seleccionada:
    col_activa, condicion_label = 1, "BUENA (B)"
    desc_columna = "Levemente alterada con manchas de oxidación, ligeramente abierta (Rc 100-250 MPa)."
elif "REGULAR" in condicion_seleccionada:
    col_activa, condicion_label = 2, "REGULAR (R)"
    desc_columna = "Superficie lisa, moderadamente alterada. Rompe con 1 o 2 golpes de picota (Rc 50-100 MPa)."
elif "POBRE" in condicion_seleccionada:
    col_activa, condicion_label = 3, "POBRE (P)"
    desc_columna = "Superficie pulida/estriada, relleno compacto o fragmentado (Rc 25-50 MPa)."
else:
    col_activa, condicion_label = 4, "MUY POBRE (MP)"
    desc_columna = "Muy alterada, abierta con rellenos de arcillas blandas, se disgrega (Rc < 25 MPa)."

# Definición de Estructura de Matrices Originales
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
# PANEL PRINCIPAL: DISTRIBUCIÓN LOGICA EN PESTAÑAS (OUTPUT)
# ==============================================================================
tab_reporte, tab_matrices, tab_glosario = st.tabs([
    "📊 Pestaña 1: Diagnóstico Operativo", 
    "🗺️ Pestaña 2: Auditoría de Matrices GSI", 
    "📖 Pestaña 3: Glosario de Ingeniería"
])

# --- PESTAÑA 1: REPORTE DE CÁLCULO Y GRÁFICO DEL SONDAJE ---
with tab_reporte:
    col_res, col_graf = st.columns([1, 1.4])
    
    with col_res:
        st.subheader("📋 Resumen Geotécnico de Salida")
        st.metric(label="RQD Resultante Computado", value=f"{rqd:.1f} %")
        
        st.markdown(f"**Estructura del Macizo:** `{estructura_label}`")
        st.caption(f"_{desc_fila}_")
        
        st.markdown(f"**Condición Superficial:** `{condicion_label}`")
        st.caption(f"_{desc_columna}_")
        
        st.success(f"### 🎯 GSI Estimado: ~ {valor_gsi_final} (Clase: {codigo_final})")
        
    with col_graf:
        st.subheader("📐 Reconstrucción Estructural a Escala Real")
        st.caption("Mapeo lineal continuo del core run recuperado:")
        
        html_sondaje = "<div style='border: 3px solid #FFF; background-color: #1e293b; width: 100%; height: 65px; display: table; border-collapse: collapse; border-radius: 6px; overflow: hidden;'>"
        suma_piezas = sum(fragmentos)
        perdida_total = longitud_total - suma_piezas
        
        for idx, frag in enumerate(fragmentos):
            if frag > 0:
                pct = (frag / longitud_total) * 100
                color = "#1d4ed8" if frag >= 10 else "#b91c1c" # Azul ISRM (Apto) vs Rojo Falla
                html_sondaje += f"<div style='display: table-cell; width: {pct}%; background-color: {color}; border-right: 2px solid #0f172a; color: #FFF; text-align: center; vertical-align: middle; font-weight: bold; font-size: 11px;'>L{idx+1}<br>{frag}cm</div>"
                
        if perdida_total > 0:
            pct_p = (perdida_total / longitud_total) * 100
            html_sondaje += f"<div style='display: table-cell; width: {pct_p}%; background-color: #020617; color: #475569; text-align: center; vertical-align: middle; font-size: 11px; font-style: italic;'>Pérdida<br>{perdida_total}cm</div>"
            
        html_sondaje += "</div>"
        st.markdown(html_sondaje, unsafe_allow_html=True)
        st.markdown("<p style='font-size:12px; text-align:center; margin-top:8px;'><span style='color:#1d4ed8;'>■</span> Fragmento Apto (≥10cm) &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#b91c1c;'>■</span> Fragmento Descartado (<10cm) &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#020617;'>■</span> Zona No Recuperada</p>", unsafe_allow_html=True)
        
        st.write("---")
        st.latex(rf"\text{{RQD}} = \left( \frac{{\sum \text{{L}}_{{\ge 10\,\text{{cm}}}}}}{{\text{{L}}_{{\text{{total}}}}}} \right) \times 100 = \left( \frac{{{suma_validos}\,\text{{cm}}}}{{{longitud_total}\,\text{{cm}}}} \right) \times 100 = {rqd:.1f}\%")

# --- PESTAÑA 2: AUDITORÍA VISUAL DE MATRICES ---
with tab_matrices:
    st.subheader("🗺️ Verificación de Posicionamiento en Matrices de Hoek")
    st.caption("El recuadro verde con fondo resaltado indica la posición exacta de las coordenadas ingresadas.")
    
    sub_tab_letras, sub_tab_valores = st.tabs(["🔤 Matriz de Códigos Litológicos", "🔢 Matriz de Índices GSI"])
    
    filas_tabla = [
        "<b>LEVEMENTE FRACTURADA (LF)</b><br><small>RQD 75-90%</small>",
        "<b>MODERADAMENTE FRACTURADA (F)</b><br><small>RQD 50-75%</small>",
        "<b>MUY FRACTURADA (MF)</b><br><small>RQD 25-50%</small>",
        "<b>INTENSAMENTE FRACTURADA (IF)</b><br><small>RQD 0-25%</small>",
        "<b>TRITURADA O BRECHADA (T)</b><br><small>Sin RQD</small>"
    ]
    headers_comunes = ["<th>MUY BUENA (MB)</th>", "<th>BUENA (B)</th>", "<th>REGULAR (R)</th>", "<th>POBRE (P)</th>", "<th>MUY POBRE (MP)</th>"]

    with sub_tab_letras:
        html = f"<table><thead><tr><th>ESTRUCTURA DEL MACIZO</th>{"".join(headers_comunes)}</tr></thead><tbody>"
        for i, fila in enumerate(filas_tabla):
            html += f"<tr><td style='background-color: #0f172a; text-align: left; color: #FFF;'>{fila}</td>"
            for j in range(5):
                celda = matriz_letras[i][j]
                bg = "#155724" if (i == fila_activa and j == col_activa) else "#1e293b"
                color = "#FFF" if (i == fila_activa and j == col_activa) else "#94a3b8"
                border = "border: 3.5px solid #28a745; font-weight: bold;" if (i == fila_activa and j == col_activa) else "border: 1px solid #334155;"
                html += f"<td style='background-color: {bg}; color: {color}; {border}'><b>{celda}</b></td>"
            html += "</tr>"
        html += "</tbody></table>"
        st.markdown(html, unsafe_allow_html=True)

    with sub_tab_valores:
        html = f"<table><thead><tr><th>ESTRUCTURA DEL MACIZO</th>{"".join(headers_comunes)}</tr></thead><tbody>"
        for i, fila in enumerate(filas_tabla):
            html += f"<tr><td style='background-color: #0f172a; text-align: left; color: #FFF;'>{fila}</td>"
            for j in range(5):
                celda = matriz_valores_gsi[i][j]
                bg = "#155724" if (i == fila_activa and j == col_activa) else "#1e293b"
                color = "#FFF" if (i == fila_activa and j == col_activa) else "#94a3b8"
                border = "border: 3.5px solid #28a745; font-weight: bold;" if (i == fila_activa and j == col_activa) else "border: 1px solid #334155;"
                html += f"<td style='background-color: {bg}; color: {color}; {border}'>Índice GSI:<br><b>{celda}</b></td>"
            html += "</tr>"
        html += "</tbody></table>"
        st.markdown(html, unsafe_allow_html=True)

# --- PESTAÑA 3: GLOSARIO TÉCNICO INALTERABLE ---
with tab_glosario:
    st.subheader("📖 Sustento y Criterios Técnicos de Clasificación")
    col_gl1, col_gl2 = st.columns(2)
    
    with col_gl1:
        with st.expander("🔬 Estructuras Litológicas (Filas) - Detalle Completo", expanded=True):
            st.markdown("""
            * **LEVEMENTE FRACTURADA (LF):** 3 a menos familias de discontinuidades muy espaciadas (2 a 6 fracturas por metro). RQD del 75% al 90%.
            * **MODERADAMENTE FRACTURADA (F):** Muy bien trabada, bloques cúbicos formados por 3 familias ortogonales (6 a 12 fracturas por metro). RQD del 50% al 75%.
            * **MUY FRACTURADA (MF):** Moderadamente trabada, parcialmente disturbada, bloques angulosos por 4 o más familias (12 a 20 fracturas por metro). RQD del 25% al 50%.
            * **INTENSAMENTE FRACTURADA (IF):** Macizo severamente plegado/fallado con bloques irregulares (Más de 20 fracturas por metro). RQD del 0% al 25%.
            * **TRITURADA O BRECHADA (T):** Masa rocosa rota, fragmentos fácilmente disgregables mezclados (Sin RQD asignable).
            """)
            
    with col_gl2:
        with st.expander("🔍 Condición Superficial de Juntas (Columnas) - Detalle Completo", expanded=True):
            st.markdown("""
            * **MUY BUENA (MB):** Superficies muy rugosas, frescas, cerradas e inalteradas. Se astilla con golpes de picota ($R_c > 250\\text{ MPa}$).
            * **BUENA (B):** Superficies rugosas, levemente alteradas con manchas de oxidación, ligeramente abiertas ($R_c\\text{ } 100\\text{ a } 250\\text{ MPa}$).
            * **REGULAR (R):** Superficies lisas, moderadamente alteradas, ligeramente abiertas. Rompe con 1 o 2 golpes de picota ($R_c\\text{ } 50\\text{ a } 100\\text{ MPa}$).
            * **POBRE (P):** Superficies pulidas o estriadas, alteradas con relleno compacto o fragmentos de roca ($R_c\\text{ } 25\\text{ a } 50\\text{ MPa}$).
            * **MUY POBRE (MP):** Superficies pulidas/estriadas con rellenos potentes de arcillas blandas, se disgrega con facilidad ($R_c < 25\\text{ MPa}$).
            """)
