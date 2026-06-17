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

# 1. CONFIGURACIÓN DE PLATAFORMA DE ALTA DENSIDAD
st.set_page_config(
    page_title="GSI Modificado - Analizador Geotécnico", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILOS CSS: Cromática Balanceada Profesional e Industrial
st.markdown("""
    <style>
    /* Fondo neutral de ingeniería */
    .stApp {
        background-color: #f1f5f9;
    }
    
    /* Contenedores principales limpios */
    .block-container {
        background-color: #ffffff;
        padding: 2.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(15, 23, 42, 0.05);
        margin-top: 1rem;
    }

    /* Tarjetas de Indicadores Metrológicos */
    .stMetric {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    
    /* Panel de orientación dinámica de discontinuidades */
    .panel-orientacion {
        background-color: #f8fafc;
        padding: 14px;
        border-radius: 6px;
        border-left: 4px solid #0284c7;
        margin-top: 10px;
        font-size: 12.5px;
        color: #334155;
    }

    /* Tabla de Control GSI Fusionada */
    .tabla-gsi { 
        width: 100%; 
        border-collapse: collapse; 
        text-align: center; 
        font-family: Arial, sans-serif; 
        font-size: 11.5px; 
        border: 1px solid #cbd5e1;
        background-color: #ffffff;
    }
    .tabla-gsi th { 
        background-color: #1e293b; 
        color: #ffffff; 
        padding: 10px; 
        border: 1px solid #cbd5e1; 
        font-size: 11px;
    }
    .tabla-gsi td { 
        padding: 10px; 
        border: 1px solid #cbd5e1; 
        color: #334155;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado de Ingeniería
st.title("💎 Calculadora Estructural de Campo: GSI Modificado")
st.markdown("Determinación analítica del Índice Geológico de Resistencia en base a logueo de testigos y mapeo de discontinuidades.")
st.markdown("---")

# ==============================================================================
# BARRA LATERAL: ENTRADA Y GUÍAS DE ORIENTACIÓN INTEGRADAS
# ==============================================================================
st.sidebar.header("🛠️ 1. Datos del Testigo (Core Run)")

longitud_total = st.sidebar.number_input(
    "Longitud Total del Tramo (cm):", 
    min_value=10, max_value=1000, value=200, step=10
)

num_fragmentos = st.sidebar.number_input(
    "N° de Fragmentos Recuperados:",
    min_value=1, max_value=20, value=4, step=1
)

st.sidebar.subheader("📐 Registro de Longitudes (cm):")
fragmentos = []
valores_ejercicio = [25, 15, 18, 32]

for i in range(int(num_fragmentos)):
    val_defecto = valores_ejercicio[i] if i < len(valores_ejercicio) else 10
    val = st.sidebar.number_input(
        f"Pieza L{i+1}:", min_value=0, max_value=200, value=val_defecto, step=1, key=f"l_{i}"
    )
    fragmentos.append(val)

st.sidebar.markdown("---")
st.sidebar.header("⛏️ 2. Condición del Macizo")

# --- GUÍA DE ORIENTACIÓN: ESTRUCTURA LITOLÓGICA (Basada en Imagen 2 y 3) ---
with st.sidebar.expander("📖 Guía: Estructuras del Macizo"):
    st.markdown("""
    * **LF (Levemente Fracturada):** 2-6 fracturas/metro. Bloques muy espaciados. (RQD 75-90%).
    * **F (Moderadamente Fracturada):** 6-12 fracturas/metro. Bloques cúbicos bien trabados. (RQD 50-75%).
    * **MF (Muy Fracturada):** 12-20 fracturas/metro. Bloques angulosos. (RQD 25-50%).
    * **IF (Intensamente Fracturada):** >20 fracturas/metro. Bloques irregulares por fallas. (RQD 0-25%).
    * **T (Triturada o Brechada):** Masa rota sin trabazón, disgregable. (Sin RQD).
    """)

# --- SELECCIÓN Y GUÍA DINÁMICA: CONDICIÓN SUPERFICIAL DE JUNTAS ---
condicion_seleccionada = st.sidebar.selectbox(
    "Condición Superficial de Juntas:",
    options=["MUY BUENA (MB)", "BUENA (B)", "REGULAR (R)", "POBRE (P)", "MUY POBRE (MP)"],
    index=2
)

# Diccionario técnico con los datos exactos del glosario de tus imágenes
datos_juntas = {
    "MUY BUENA (MB)": {
        "desc": "Extremadamente resistente, fresca. Superficies muy rugosas e inalteradas. Juntas cerradas.",
        "rc": "Rc > 250 MPa (Se astilla con golpes de picota)",
        "color": "#0284c7"
    },
    "BUENA (B)": {
        "desc": "Muy resistente, levemente alterada. Superficies rugosas, manchas de oxidación. Ligera apertura.",
        "rc": "Rc 100 a 250 MPa (Se rompe con varios golpes de picota)",
        "color": "#16a34a"
    },
    "REGULAR (R)": {
        "desc": "Resistente, levemente alterada. Superficies lisas, moderadamente alteradas. Ligera apertura.",
        "rc": "Rc 50 a 100 MPa (Se rompe con uno o dos golpes de picota)",
        "color": "#d97706"
    },
    "POBRE (P)": {
        "desc": "Moderadamente resistente, moderadamente alterada. Superficie pulida o con estriaciones. Relleno compacto o fragmentado.",
        "rc": "Rc 25 a 50 MPa (Se indenta superficialmente)",
        "color": "#dc2626"
    },
    "MUY POBRE (MP)": {
        "desc": "Blanda, muy alterada. Superficie pulida y estriada, muy abierta. Relleno de arcillas blandas.",
        "rc": "Rc < 25 MPa (Se disgrega o indenta superficialmente)",
        "color": "#991b1b"
    }
}

# Renderizado de la previsualización del glosario en tiempo real
info_activa = datos_juntas[condicion_seleccionada]
st.sidebar.markdown(f"""
    <div class="panel-orientacion" style="border-left-color: {info_activa['color']};">
        <b style="color: {info_activa['color']}; font-size: 13px;">🔍 Previsualización de Campo:</b><br>
        <b>Estado:</b> {info_activa['desc']}<br>
        <b>Resistencia:</b> <code>{info_activa['rc']}</code>
    </div>
""", unsafe_allow_html=True)


# ==============================================================================
# ALGORITMO GEOMECÁNICO Y CLASIFICACIÓN DE CAMPOS
# ==============================================================================
fragmentos_validos = [f for f in fragmentos if f >= 10]
suma_validos = sum(fragmentos_validos)
rqd = (suma_validos / longitud_total) * 100 if longitud_total > 0 else 0.0

# Clasificación rigurosa de fila según matriz e histórico geomecánico
if rqd > 75 and rqd <= 90:
    fila_activa, estructura_label = 0, "LEVEMENTE FRACTURADA (LF)"
    desc_fila = "Tres a menos sistemas de discontinuidades muy espaciadas entre sí."
elif rqd > 50 and rqd <= 75:
    fila_activa, estructura_label = 1, "MODERADAMENTE FRACTURADA (F)"
    desc_fila = "Muy bien trabada, no disturbada. Bloques cúbicos (3 familias ortogonales)."
elif rqd > 25 and rqd <= 50:
    fila_activa, estructura_label = 2, "MUY FRACTURADA (MF)"
    desc_fila = "Moderadamente trabada, parcialmente disturbada. Bloques angulosos."
else:
    # Verificación técnica especial: si el RQD es cero por fragmentos nulos se evalúa si es Triturada (T)
    if suma_validos == 0 and num_fragmentos > 4 and fragmentos[0] <= 5:
        fila_activa, estructura_label = 4, "TRITURADA O BRECHADA (T)"
        desc_fila = "Masa rocosa extremadamente rota. Mezcla de fragmentos sueltos disgregables."
    else:
        fila_activa, estructura_label = 3, "INTENSAMENTE FRACTURADA (IF)"
        desc_fila = "Plegamiento y fallamiento con muchas discontinuidades interceptadas. Bloques irregulares."

# Asignación de columna indexada
col_activa = ["MUY BUENA (MB)", "BUENA (B)", "REGULAR (R)", "POBRE (P)", "MUY POBRE (MP)"].index(condicion_seleccionada)

# MATRICES FUSIONADAS: Valores extraídos fielmente de tus ábacos (Imágenes 2 y 3)
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
# PANELES DE CONTROL CENTRALIZADOS (OUTPUT COMPACTO Y PRÁCTICO)
# ==============================================================================
tab_operativa, tab_matriz_unificada = st.tabs([
    "📊 Diagnóstico de Operación", 
    "🗺️ Matriz Integrada de Control Geotécnico"
])

# --- PESTAÑA 1: REPORTE MATEMÁTICO Y GRÁFICO ---
with tab_operativa:
    col_izq, col_der = st.columns([1, 1.2])
    
    with col_izq:
        st.subheader("📊 Resultados de Clasificación")
        st.metric(label="RQD del Tramo Calculado", value=f"{rqd:.1f} %")
        
        st.markdown(f"**Estructura del Macizo:** `{estructura_label}`")
        st.caption(f"_{desc_fila}_")
        
        st.markdown(f"**Condición Superficial de Juntas:** `{condicion_seleccionada}`")
        
        # Alerta corporativa de alto contraste con el resultado final
        st.info(f"### 🎯 GSI Estimado: ~ {valor_gsi_final} (Zona: {codigo_final})")
        
    with col_der:
        st.subheader("📐 Representación Estructural del Testigo")
        
        html_sondaje = "<div style='border: 2px solid #cbd5e1; background-color: #f8fafc; width: 100%; height: 55px; display: table; border-collapse: collapse; border-radius: 4px; overflow: hidden;'>"
        suma_piezas = sum(fragmentos)
        perdida_total = longitud_total - suma_piezas
        
        for idx, frag in enumerate(fragmentos):
            if frag > 0:
                pct = (frag / longitud_total) * 100
                color = "#0284c7" if frag >= 10 else "#ef4444" # Azul Competente vs Rojo Fractura
                html_sondaje += f"<div style='display: table-cell; width: {pct}%; background-color: {color}; border-right: 1px solid #ffffff; color: #ffffff; text-align: center; vertical-align: middle; font-weight: bold; font-size: 10.5px;'>L{idx+1}<br>{frag}cm</div>"
                
        if perdida_total > 0:
            pct_p = (perdida_total / longitud_total) * 100
            html_sondaje += f"<div style='display: table-cell; width: {pct_p}%; background-color: #cbd5e1; color: #475569; text-align: center; vertical-align: middle; font-size: 11px; font-style: italic;'>Pérdida<br>{perdida_total}cm</div>"
            
        html_sondaje += "</div>"
        st.markdown(html_sondaje, unsafe_allow_html=True)
        st.markdown("<p style='font-size:11.5px; text-align:center; margin-top:8px;'><span style='color:#0284c7;'>■</span> Fragmento Apto (≥10cm) &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#ef4444;'>■</span> Fragmento Descartado (<10cm) &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#cbd5e1;'>■</span> Núcleo No Recuperado</p>", unsafe_allow_html=True)
        
        st.write("---")
        st.latex(rf"\text{{RQD}} = \left( \frac{{\sum \text{{L}}_{{\ge 10\,\text{{cm}}}}}}{{\text{{L}}_{{\text{{total}}}}}} \right) \times 100 = \left( \frac{{{suma_validos}\,\text{{cm}}}}{{{longitud_total}\,\text{{cm}}}} \right) \times 100 = {rqd:.1f}\%")

# --- PESTAÑA 2: TABLA FUSIONADA (CÓDIGOS + VALORES DE CONTORNO) ---
with tab_matriz_unificada:
    st.subheader("🗺️ Tablero de Control Geomecánico Unificado (GSI Modificado)")
    st.markdown("Esta tabla unifica las características estructurales y los rangos de contornos de las tablas de campo.")
    
    filas_tabla = [
        "<b>LEVEMENTE FRACTURADA (LF)</b><br><small>RQD 75 - 90%</small>",
        "<b>MODERADAMENTE FRACTURADA (F)</b><br><small>RQD 50 - 75%</small>",
        "<b>MUY FRACTURADA (MF)</b><br><small>RQD 25 - 50%</small>",
        "<b>INTENSAMENTE FRACTURADA (IF)</b><br><small>RQD 0 - 25%</small>",
        "<b>TRITURADA O BRECHADA (T)</b><br><small>Sin RQD</small>"
    ]
    headers = [
        "<th>MUY BUENA (MB)<br><small>Rc > 250 MPa</small></th>", 
        "<th>BUENA (B)<br><small>Rc 100-250 MPa</small></th>", 
        "<th>REGULAR (R)<br><small>Rc 50-100 MPa</small></th>", 
        "<th>POBRE (P)<br><small>Rc 25-50 MPa</small></th>", 
        "<th>MUY POBRE (MP)<br><small>Rc < 25 MPa</small></th>"
    ]

    html = f"<table class='tabla-gsi'><thead><tr><th>ESTRUCTURA DEL MACIZO ROCOSO</th>{"".join(headers)}</tr></thead><tbody>"
    
    for i, fila in enumerate(filas_tabla):
        html += f"<tr><td style='background-color: #f8fafc; text-align: left; font-weight: bold; color: #1e293b; padding: 12px;'>{fila}</td>"
        for j in range(5):
            val_gsi = matriz_valores_gsi[i][j]
            cod_gsi = matriz_letras[i][j]
            
            # Resaltado verde industrial de celda activa (Intersección de diseño)
            if i == fila_activa and j == col_activa:
                bg = "#bbf7d0"
                color = "#166534"
                border = "border: 3.5px solid #22c55e; font-weight: bold; font-size: 12.5px;"
            else:
                bg = "#ffffff"
                color = "#475569"
                border = "border: 1px solid #e2e8f0;"
                
            html += f"<td style='background-color: {bg}; color: {color}; {border}'><b>{cod_gsi}</b><br><span style='font-size:13px; color:#0f172a;'>GSI: <b>{val_gsi}</b></span></td>"
        html += "</tr>"
        
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)
