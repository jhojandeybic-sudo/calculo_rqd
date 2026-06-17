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

# 1. CONFIGURACIÓN ESTRUCTURAL DE LA PÁGINA
st.set_page_config(
    page_title="GSI Modificado - Engine Analytica", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de estilos CSS para un acabado profesional de alta densidad de datos
st.markdown("""
    <style>
    .reportview-container .main .block-container{ padding-top: 1rem; }
    .stMetric { background-color: #0f172a; padding: 15px; border-radius: 8px; border: 1px solid #1e293b; }
    div.stExpander { border: 1px solid #1e293b !important; box-sizing: border-box !important; }
    table { width:100%; border-collapse: collapse; text-align: center; font-family: sans-serif; font-size: 11px; border: 1px solid #334155; }
    th { background-color: #1e293b; color: #FFF; padding: 10px; border: 1px solid #334155; }
    td { padding: 10px; border: 1px solid #334155; }
    </style>
""", unsafe_allow_html=True)

st.title("🧮 Plataforma de Caracterización Geomecánica: GSI Modificado")
st.markdown("Determinación cuantitativa de la estructura del macizo rocoso y condiciones de discontinuidades.")
st.markdown("---")

# ==============================================================================
# ETAPA 1: CAPTURA DE PARÁMETROS DEL TESTIGO (BARRA LATERAL)
# ==============================================================================
st.sidebar.header("📋 ETAPA 1: Parámetros del Testigo")

longitud_total = st.sidebar.number_input(
    "Longitud Total de la Corrida (cm):", 
    min_value=10, max_value=1000, value=200, step=10,
    help="Longitud total de la corrida o maniobra de perforación (Core Run)."
)

num_fragmentos = st.sidebar.number_input(
    "Cantidad de Fragmentos Medidos:",
    min_value=1, max_value=20, value=4, step=1,
    help="Número de trozos o piezas físicas recuperadas a evaluar."
)

st.sidebar.subheader("📐 Logueo de Fragmentos (cm):")
fragmentos = []
# Valores predeterminados depurados (Sin ceros que alteren la lógica de conteo de piezas)
valores_ejercicio = [25, 15, 18, 32]

for i in range(int(num_fragmentos)):
    val_defecto = valores_ejercicio[i] if i < len(valores_ejercicio) else 10
    val = st.sidebar.number_input(
        f"Pieza L{i+1}:", 
        min_value=0, max_value=200, value=val_defecto, step=1, key=f"l_{i}"
    )
    fragmentos.append(val)

# ==============================================================================
# ETAPA 2: EVALUACIÓN CUANTITATIVA DE DISCONTINUIDADES (BARRA LATERAL)
# ==============================================================================
st.sidebar.markdown("---")
st.sidebar.header("⛏️ ETAPA 2: Condición de Juntas")
condicion_seleccionada = st.sidebar.selectbox(
    "Grado de Alteración / Rugosidad:",
    options=[
        "MUY BUENA (Superficies muy rugosas, inalteradas, cerradas)",
        "BUENA (Rugosa, levemente meteorizada, manchas de oxidación)",
        "REGULAR (Lisa, moderadamente alterada, abierta, rompe con 1-2 golpes)",
        "POBRE (Pulida, estriada, relleno compacto o fragmentos)",
        "MUY POBRE (Superficie pulida/estriada, relleno de arcilla blanda)"
    ],
    index=2,
    help="Evaluación empírica in situ mediante la resistencia a la picota y grado de alteración planar."
)

# ==============================================================================
# PROCESAMIENTO MATEMÁTICO AVANZADO - MATRICES TÉCNICAS
# ==============================================================================
fragmentos_validos = [f for f in fragmentos if f >= 10]
suma_validos = sum(fragmentos_validos)
rqd = (suma_validos / longitud_total) * 100 if longitud_total > 0 else 0.0

# Clasificación de Fila (Estructura Litológica)
if rqd > 75 and rqd <= 90:
    fila_activa, estructura_label = 0, "LEVEMENTE FRACTURADA"
    desc_fila = "Tres a menos sistemas de discontinuidades muy espaciadas entre sí (2 a 6 fracturas por metro)."
elif rqd > 50 and rqd <= 75:
    fila_activa, estructura_label = 1, "MODERADAMENTE FRACTURADA"
    desc_fila = "Muy bien trabada, no disturbada, bloques cúbicos formados por tres sistemas de discontinuidades ortogonales (6 a 12 fracturas por metro)."
elif rqd > 25 and rqd <= 50:
    fila_activa, estructura_label = 2, "MUY FRACTURADA"
    desc_fila = "Moderadamente trabada, parcialmente disturbada, bloques angulosos formados por 4 o más familias de discontinuidades (12 a 20 fracturas por metro)."
else:
    if suma_validos == 0 and num_fragmentos > 4:
        fila_activa, estructura_label = 4, "TRITURADA O BRECHADA"
        desc_fila = "Ligeramente trabada, masa rocosa extremadamente rota con una mezcla de fragmentos fácilmente disgregables, angulosos y redondeados (Sin RQD)."
    else:
        fila_activa, estructura_label = 3, "INTENSAMENTE FRACTURADA"
        desc_fila = "Plegamiento y fallamiento con muchas discontinuidades interceptadas formando bloques angulosos o irregulares (Más de 20 fracturas por metro)."

# Clasificación de Columna (Condición Superficial)
if "MUY BUENA" in condicion_seleccionada:
    col_activa, condicion_label = 0, "MUY BUENA"
    desc_columna = "Extremadamente resistente, fresca, superficie de las discontinuidades muy rugosas e inalteradas, cerradas. Se astilla con golpes de picota. (Rc > 250 MPa)."
elif "BUENA" in condicion_seleccionada:
    col_activa, condicion_label = 1, "BUENA"
    desc_columna = "Muy resistente, levemente alterada, discontinuidades rugosas, ligeramente alterada, manchas de oxidación, ligeramente abierta. Se rompe con varios golpes de picota. (Rc 100 a 250 MPa)."
elif "REGULAR" in condicion_seleccionada:
    col_activa, condicion_label = 2, "REGULAR"
    desc_columna = "Resistente, levemente alterada, discontinuidades lisas, moderadamente alteradas, ligeramente abierta. Se rompe con uno o dos golpes de picota. (Rc 50 a 100 MPa)."
elif "POBRE" in condicion_seleccionada:
    col_activa, condicion_label = 3, "POBRE"
    desc_columna = "Moderadamente resistente, moderadamente alterada, superficie pulida o con estriaciones, muy alterada, relleno compacto o con fragmentos de roca. Se indenta superficialmente. (Rc 25 a 50 MPa)."
else:
    col_activa, condicion_label = 4, "MUY POBRE"
    desc_columna = "Blanda, muy alterada, superficie pulida y estriada, muy abierta, con relleno de arcillas blandas. Se disgrega o indenta superficialmente. (Rc < 25 MPa)."

# Definición de Matrices Originales de Hoek
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
# ETAPA 3: INTERFAZ GRÁFICA Y REPORTABILIDAD (ORDEN LÓGICO DE PRODUCCIÓN)
# ==============================================================================
col_panel, col_diagrama = st.columns([1.1, 1.4])

with col_panel:
    st.subheader("🏁 ETAPA 3: Diagnóstico y Reporte Geomecánico")
    st.metric(label="RQD Resultante Calculado", value=f"{rqd:.1f} %")
    
    st.markdown("### 🧬 Parámetros de Diseño Clasificados:")
    st.info(f"**Estructura Dominante:** {estructura_label}\n\n*{desc_fila}*")
    st.info(f"**Estado de Discontinuidades:** {condicion_label}\n\n*{desc_columna}*")
    
    st.success(f"**Zonificación Litológica:** `{codigo_final}` &nbsp;|&nbsp; **Valor GSI Modificado:** `~ {valor_gsi_final}`")

with col_diagrama:
    st.subheader("📐 Representación del Sondaje (A Escala)")
    st.caption("Reconstrucción lineal y continua del estado físico del testigo:")

    html_sondaje = "<div style='border: 3px solid #FFF; background-color: #1e293b; width: 100%; height: 60px; display: table; border-collapse: collapse; border-radius: 6px; overflow: hidden;'>"
    
    suma_piezas = sum(fragmentos)
    perdida_total = longitud_total - suma_piezas
    
    for idx, frag in enumerate(fragmentos):
        if frag > 0:
            pct = (frag / longitud_total) * 100
            color = "#1d4ed8" if frag >= 10 else "#b91c1c"  # Azul Geomecánico vs Rojo Falla
            html_sondaje += f"<div style='display: table-cell; width: {pct}%; background-color: {color}; border-right: 2px solid #0f172a; color: #FFF; text-align: center; vertical-align: middle; font-weight: bold; font-size: 12px;'>L{idx+1}<br>{frag}cm</div>"
            
    if perdida_total > 0:
        pct_p = (perdida_total / longitud_total) * 100
        html_sondaje += f"<div style='display: table-cell; width: {pct_p}%; background-color: #020617; color: #475569; text-align: center; vertical-align: middle; font-size: 11px; font-style: italic;'>Pérdida<br>{perdida_total}cm</div>"
        
    html_sondaje += "</div>"
    st.markdown(html_sondaje, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size:12px; text-align:center;'><span style='color:#1d4ed8;'>■</span> Fragmento Apto (≥10cm) &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#b91c1c;'>■</span> Fragmento Rechazado (<10cm) &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#020617;'>■</span> Longitud No Recuperada</p>", unsafe_allow_html=True)
    
    st.write("---")
    st.write("**Ecuación Matemática Aplicada:**")
    st.latex(rf"\text{{RQD}} = \left( \frac{{\sum \text{{L}}_{{\ge 10\,\text{{cm}}}}}}{{\text{{L}}_{{\text{{total}}}}}} \right) \times 100 = \left( \frac{{{suma_validos}\,\text{{cm}}}}{{{longitud_total}\,\text{{cm}}}} \right) \times 100 = {rqd:.1f}\%")

# ==============================================================================
# 5. MATRICES INTERACTIVAS CON AUDITORÍA DE ENCABEZADOS EN TIEMPO REAL
# ==============================================================================
st.write("---")
st.subheader("🗺️ Matrices de Correlación e Índices GSI")
st.caption("Usa las pestañas para alternar entre formatos. El cuadro verde resalta la intersección de tus datos de campo.")

tab_letras, tab_valores = st.tabs(["🔤 Matriz de Códigos (Letras)", "🔢 Matriz de Valores de Contorno"])

filas_tabla = [
    "<b>LEVEMENTE FRACTURADA (LF)</b><br><small>RQD 75-90%</small>",
    "<b>MODERADAMENTE FRACTURADA (F)</b><br><small>RQD 50-75%</small>",
    "<b>MUY FRACTURADA (MF)</b><br><small>RQD 25-50%</small>",
    "<b>INTENSAMENTE FRACTURADA (IF)</b><br><small>RQD 0-25%</small>",
    "<b>TRITURADA O BRECHADA (T)</b><br><small>Sin RQD</small>"
]

headers_comunes = [
    "<th>MUY BUENA (MB)</th>", "<th>BUENA (B)</th>", "<th>REGULAR (R)</th>", "<th>POBRE (P)</th>", "<th>MUY POBRE (MP)</th>"
]

# --- TABLA DE CÓDIGOS ---
with tab_letras:
    html = f"""<table><thead><tr><th>ESTRUCTURA DEL MACIZO</th>{"".join(headers_comunes)}</tr></thead><tbody>"""
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

# --- TABLA DE CONTORNOS NUMÉRICOS ---
with tab_valores:
    html = f"""<table><thead><tr><th>ESTRUCTURA DEL MACIZO</th>{"".join(headers_comunes)}</tr></thead><tbody>"""
    for i, fila in enumerate(filas_tabla):
        html += f"<tr><td style='background-color: #0f172a; text-align: left; color: #FFF;'>{fila}</td>"
        for j in range(5):
            celda = matriz_valores_gsi[i][j]
            bg = "#155724" if (i == fila_activa and j == col_activa) else "#1e293b"
            color = "#FFF" if (i == fila_activa and j == col_activa) else "#94a3b8"
            border = "border: 3.5px solid #28a745; font-weight: bold;" if (i == fila_activa and j == col_activa) else "border: 1px solid #334155;"
            html += f"<td style='background-color: {bg}; color: {color}; {border}'>GSI:<br><b>{celda}</b></td>"
        html += "</tr>"
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# 6. CRITERIOS DESPLEGABLES DINÁMICOS Y DETALLES DE FILAS Y COLUMNAS
# ==============================================================================
st.markdown("### 🔍 Auditoría y Criterios Detallados de Filas y Columnas")

# Botón interactivo inteligente para analizar la posición actual calculada
with st.expander("🎯 VER DETALLE DE LA INTERSECCIÓN ACTUADA (Fila y Columna Actual)"):
    col_f, col_c = st.columns(2)
    with col_f:
        st.markdown(f"**Fila Evaluada: `{estructura_label}`**")
        st.caption(desc_fila)
    with col_c:
        st.markdown(f"**Columna Evaluada: `{condicion_label}`**")
        st.caption(desc_columna)

# Desplegables de glosario completo e inalterable fiel a tus láminas de control
col_gl1, col_gl2 = st.columns(2)

with col_gl1:
    with st.expander("📖 Glosario Técnico de Filas (Estructura Geológica)"):
        st.markdown("""
        * **LEVEMENTE FRACTURADA (LF):** 3 a menos sistemas de discontinuidades muy espaciadas entre sí (2 a 6 fracturas por metro). RQD: 75% a 90%.
        * **MODERADAMENTE FRACTURADA (F):** Muy bien trabada, no disturbada, bloques cúbicos formados por tres sistemas de discontinuidades ortogonales (6 a 12 fracturas por metro). RQD: 50% a 75%.
        * **MUY FRACTURADA (MF):** Moderadamente trabada, parcialmente disturbada, bloques angulosos formados por 4 o más familias de discontinuidades (12 a 20 fracturas por metro). RQD: 25% a 50%.
        * **INTENSAMENTE FRACTURADA (IF):** Plegamiento y fallamiento con muchas discontinuidades interceptadas formando bloques angulosos o irregulares (Más de 20 fracturas por metro). RQD: 0% a 25%.
        * **TRITURADA O BRECHADA (T):** Ligeramente trabada, masa rocosa extremadamente rota con una mezcla de fragmentos fácilmente disgregables, angulosos y redondeados. No posee RQD asignable.
        """)

with col_gl2:
    with st.expander("📖 Glosario Técnico de Columnas (Condición Superficial)"):
        st.markdown("""
        * **MUY BUENA (MB):** Extremadamente resistente, fresca, superficie de las discontinuidades muy rugosas e inalteradas, cerradas. Se astilla con golpes de picota. ($R_c > 250\\text{ MPa}$).
        * **BUENA (B):** Muy resistente, levemente alterada, discontinuidades rugosas, ligeramente alterada, manchas de oxidación, ligeramente abierta. Se rompe con varios golpes de picota. ($R_c\\text{ } 100\\text{ a } 250\\text{ MPa}$).
        * **REGULAR (R):** Resistente, levemente alterada, discontinuidades lisas, moderadamente alteradas, ligeramente abierta. Se rompe con uno o dos golpes de picota. ($R_c\\text{ } 50\\text{ a } 100\\text{ MPa}$).
        * **POBRE (P):** Moderadamente resistente, moderadamente alterada, superficie pulida o con estriaciones, muy alterada, relleno compacto o con fragmentos de roca. Se indenta superficialmente. ($R_c\\text{ } 25\\text{ a } 50\\text{ MPa}$).
        * **MUY POBRE (MP):** Blanda, muy alterada, superficie pulida y estriada, muy abierta, con relleno de arcillas blandas. Se disgrega o indenta superficialmente. ($R_c < 25\\text{ MPa}$).
        """)
