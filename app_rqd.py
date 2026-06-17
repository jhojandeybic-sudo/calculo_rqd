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

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Calculadora GSI Modificado Profesional", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💎 Sistema de Logueo Geomecánico: RQD y GSI Modificado")
st.markdown("Clasificación dinámica y visualización a escala de testigos de perforación para ingeniería de rocas.")
st.markdown("---")

# 2. BARRA LATERAL - ENTRADA DE DATOS DINÁMICOS
st.sidebar.header("🛠️ 1. Datos del Testigo (Entrada)")

longitud_total = st.sidebar.number_input(
    "Longitud total de la muestra (cm):", 
    min_value=10, max_value=1000, value=200, step=10
)

num_fragmentos = st.sidebar.number_input(
    "Número de fragmentos medidos:",
    min_value=1, max_value=20, value=6, step=1
)

st.sidebar.subheader("Longitudes de fragmentos (cm):")
fragmentos = []
valores_ejercicio = [25, 15, 0, 18, 32, 0]

for i in range(int(num_fragmentos)):
    val_defecto = valores_ejercicio[i] if i < len(valores_ejercicio) else 0
    val = st.sidebar.number_input(
        f"Fragmento L{i+1}:", 
        min_value=0, max_value=200, value=val_defecto, step=1, key=f"l_{i}"
    )
    fragmentos.append(val)

st.sidebar.header("⛏️ 2. Evaluación de Campo (Entrada)")
condicion_seleccionada = st.sidebar.selectbox(
    "Selecciona la condición superficial observada:",
    options=[
        "MUY BUENA (Extremadamente resistente, fresca, Rc > 250 MPa)",
        "BUENA (Muy resistente, levemente alterada, Rc 100-250 MPa)",
        "REGULAR (Resistente, rompe con 1 o 2 golpes de picota, Rc 50-100 MPa)",
        "POBRE (Moderadamente resistente, se indenta superficialmente, Rc 25-50 MPa)",
        "MUY POBRE (Blanda, se disgrega con la mano, Rc < 25 MPa)"
    ],
    index=2  # Predeterminado del ejercicio actual
)

# 3. PROCESAMIENTO MATEMÁTICO (LÓGICA SEGÚN LAS TABLAS SUMINISTRADAS)
fragmentos_validos = [f for f in fragmentos if f >= 10]
suma_validos = sum(fragmentos_validos)
rqd = (suma_validos / longitud_total) * 100 if longitud_total > 0 else 0.0

# Clasificación de Fila (Estructura de la roca según rangos de RQD)
if rqd > 75 and rqd <= 90:
    fila_activa = 0
    estructura_label = "LEVEMENTE FRACTURADA"
    desc_fila = "Tres a menos sistemas de discontinuidades muy espaciadas entre sí (2 a 6 fracturas por metro)."
elif rqd > 50 and rqd <= 75:
    fila_activa = 1
    estructura_label = "MODERADAMENTE FRACTURADA"
    desc_fila = "Muy bien trabada, no disturbada, bloques cúbicos formados por tres sistemas de discontinuidades (6 a 12 fracturas por metro)."
elif rqd > 25 and rqd <= 50:
    fila_activa = 2
    estructura_label = "MUY FRACTURADA"
    desc_fila = "Moderadamente trabada, parcialmente disturbada, bloques angulosos por 4 o más familias (12 a 20 fracturas por metro)."
else:
    if suma_validos == 0 and num_fragmentos > 4:
        fila_activa = 4
        estructura_label = "TRITURADA O BRECHADA"
        desc_fila = "Ligeramente trabada, masa rocosa extremadamente rota. Fragmentos fácilmente disgregables. (Sin RQD)."
    else:
        fila_activa = 3
        estructura_label = "INTENSAMENTE FRACTURADA"
        desc_fila = "Plegamiento y fallamiento con muchas discontinuidades interceptadas formando bloques irregulares (Más de 20 fracturas por metro)."

# Clasificación de Columna (Condición superficial)
if "MUY BUENA" in condicion_seleccionada:
    col_activa = 0
    condicion_label = "MUY BUENA"
    desc_columna = "Extremadamente resistente, fresca, superficie de las discontinuidades muy rugosas e inalteradas, cerradas. Se astilla con golpes de picota. (Rc > 250 MPa)."
elif "BUENA" in condicion_seleccionada:
    col_activa = 1
    condicion_label = "BUENA"
    desc_columna = "Muy resistente, levemente alterada, discontinuidades rugosas, ligeramente alterada, manchas de oxidación, ligeramente abierta. Se rompe con varios golpes de picota. (Rc 100 a 250 MPa)."
elif "REGULAR" in condicion_seleccionada:
    col_activa = 2
    condicion_label = "REGULAR"
    desc_columna = "Resistente, levemente alterada, discontinuidades lisas, moderadamente alteradas, ligeramente abierta. Se rompe con uno o dos golpes de picota. (Rc 50 a 100 MPa)."
elif "POBRE" in condicion_seleccionada:
    col_activa = 3
    condicion_label = "POBRE"
    desc_columna = "Moderadamente resistente, moderadamente alterada, superficie pulida o con estriaciones, muy alterada, relleno compacto o con fragmentos de roca. Se indenta superficialmente. (Rc 25 a 50 MPa)."
else:
    col_activa = 4
    condicion_label = "MUY POBRE"
    desc_columna = "Blanda, muy alterada, superficie pulida y estriada, muy abierta, con relleno de arcillas blandas. Se disgrega o indenta superficialmente. (Rc < 25 MPa)."

# Definición de Matrices
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

# 4. ORDEN LÓGICO DE VISUALIZACIÓN EN LA INTERFAZ
col_izq, col_der = st.columns([1, 1.4])

with col_izq:
    st.subheader("📊 Resumen del Análisis de Entrada")
    
    # Mostrar datos que ingresó el usuario de manera ejecutiva
    st.markdown(f"• **Longitud de Testigo Analizada:** `{longitud_total} cm`")
    st.markdown(f"• **Condición Superficial de Campo Elegida:** `{condicion_label}`")
    st.write(f"*{desc_columna}*")
    
    st.write("---")
    st.subheader("🎯 Diagnóstico Final de Salida")
    st.metric(label="RQD Resultante", value=f"{rqd:.1f} %")
    
    st.markdown(f"• **Estructura Asignada:** `{estructura_label}`")
    st.caption(f"*{desc_fila}*")
    st.markdown(f"• **Combinación Litológica:** `{codigo_final}`")
    
    st.success(f"### 🎯 Índice GSI Modificado Estimado: ~ {valor_gsi_final}")

with col_der:
    st.subheader("📐 Diagrama Esquemático del Sondaje (A Escala)")
    st.caption("Reconstrucción visual interactiva de la muestra en base a las longitudes registradas:")

    # Renderizado CSS robusto en formato de tabla para garantizar visualización
    html_sondaje = "<div style='border: 3px solid #FFF; background-color: #222; width: 100%; height: 60px; display: table; border-collapse: collapse; border-radius: 6px; overflow: hidden;'>"
    
    suma_piezas = sum(fragmentos)
    perdida_total = longitud_total - suma_piezas
    
    for idx, frag in enumerate(fragmentos):
        if frag > 0:
            pct = (frag / longitud_total) * 100
            color = "#1E40AF" if frag >= 10 else "#B91C1C"
            html_sondaje += f"<div style='display: table-cell; width: {pct}%; background-color: {color}; border-right: 2px solid #111; color: #FFF; text-align: center; vertical-align: middle; font-weight: bold; font-size: 12px;'>L{idx+1}<br>({frag}cm)</div>"
            
    if perdida_total > 0:
        pct_p = (perdida_total / longitud_total) * 100
        html_sondaje += f"<div style='display: table-cell; width: {pct_p}%; background-color: #111; color: #555; text-align: center; vertical-align: middle; font-size: 11px; font-style: italic;'>Pérdida<br>({perdida_total}cm)</div>"
        
    html_sondaje += "</div>"
    st.markdown(html_sondaje, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size:13px;'><span style='color:#1E40AF;'>■</span> Fragmentos aptos (≥10cm) &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#B91C1C;'>■</span> Fragmentos ignorados (<10cm) &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#111; border: 1px solid #555; padding: 1px 4px;'>■</span> Pérdida / No Recuperado</p>", unsafe_allow_html=True)
    
    st.write("---")
    st.write("**Ecuación Aplicada:**")
    st.latex(rf"\text{{RQD}} = \left( \frac{{\sum \text{{Longitudes}} \ge 10\,\text{{cm}}}}{{\text{{Longitud Total del Corrido}}}} \right) \times 100 = {rqd:.1f}\%")

# 5. MATRICES INTERACTIVAS CON BOTÓN DE DETALLES TÉCNICOS
st.write("---")
st.subheader("🗺️ Matriz GSI Modificado Interactiva")
st.caption("Usa las pestañas para cambiar la visualización y expande las cajas inferiores para estudiar las descripciones completas de tus láminas.")

tab_letras, tab_valores = st.tabs(["🔤 Ver Códigos (Letras)", "🔢 Ver Contornos (Valores Numéricos)"])

filas_tabla = [
    "<b>LEVEMENTE FRACTURADA</b><br><small>RQD 75-90%</small>",
    "<b>MODERADAMENTE FRACTURADA</b><br><small>RQD 50-75%</small>",
    "<b>MUY FRACTURADA</b><br><small>RQD 25-50%</small>",
    "<b>INTENSAMENTE FRACTURADA</b><br><small>RQD 0-25%</small>",
    "<b>TRITURADA O BRECHADA</b><br><small>Sin RQD</small>"
]

headers_comunes = [
    "<th>MUY BUENA (MB)</th>", "<th>BUENA (B)</th>", "<th>REGULAR (R)</th>", "<th>POBRE (P)</th>", "<th>MUY POBRE (MP)</th>"
]

# --- TABLA DE LETRAS ---
with tab_letras:
    html = f"""<table style='width:100%; border-collapse: collapse; text-align: center; font-family: sans-serif; font-size: 12px; border: 1px solid #555;'>
        <thead><tr style='background-color: #1E293B; color: #FFF;'><th style='padding: 10px;'>ESTRUCTURA</th>{"".join(headers_comunes)}</tr></thead><tbody>"""
    for i, fila in enumerate(filas_tabla):
        html += f"<tr><td style='padding: 10px; background-color: #0F172A; text-align: left; color: #FFF; border: 1px solid #444;'>{fila}</td>"
        for j in range(5):
            celda = matriz_letras[i][j]
            bg = "#16A34A" if (i == fila_activa and j == col_activa) else "#1E293B"
            color = "#FFF" if (i == fila_activa and j == col_activa) else "#94A3B8"
            border = "border: 3.5px solid #4ADE80; font-weight: bold;" if (i == fila_activa and j == col_activa) else "border: 1px solid #334155;"
            html += f"<td style='background-color: {bg}; color: {color}; {border} padding: 10px;'><b>{celda}</b></td>"
        html += "</tr>"
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)

# --- TABLA DE VALORES ---
with tab_valores:
    html = f"""<table style='width:100%; border-collapse: collapse; text-align: center; font-family: sans-serif; font-size: 12px; border: 1px solid #555;'>
        <thead><tr style='background-color: #1E293B; color: #FFF;'><th style='padding: 10px;'>ESTRUCTURA</th>{"".join(headers_comunes)}</tr></thead><tbody>"""
    for i, fila in enumerate(filas_tabla):
        html += f"<tr><td style='padding: 10px; background-color: #0F172A; text-align: left; color: #FFF; border: 1px solid #444;'>{fila}</td>"
        for j in range(5):
            celda = matriz_valores_gsi[i][j]
            bg = "#155724" if (i == fila_activa and j == col_activa) else "#1E293B"
            color = "#FFF" if (i == fila_activa and j == col_activa) else "#94A3B8"
            border = "border: 3.5px solid #28A745; font-weight: bold;" if (i == fila_activa and j == col_activa) else "border: 1px solid #334155;"
            html += f"<td style='background-color: {bg}; color: {color}; {border} padding: 10px;'>GSI: <b>{celda}</b></td>"
        html += "</tr>"
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)

# --- SECCIÓN DE BOTONES DESPLEGABLES CON DETALLES COMPLETOS (Fiel a tus imágenes) ---
st.markdown("### 🔍 4. Detalle Técnico de Categorías (Botones Desplegables)")

with st.expander("📖 Ver detalles completos de las FILAS (Estructura del Macizo)"):
    st.markdown("""
    * **LEVEMENTE FRACTURADA (LF):** Tres a menos sistemas de discontinuidades muy espaciadas entre sí (2 a 6 fracturas por metro).
    * **MODERADAMENTE FRACTURADA (F):** Muy bien trabada, no disturbada, bloques cúbicos formados por tres sistemas de discontinuidades ortogonales (6 a 12 fracturas por metro).
    * **MUY FRACTURADA (MF):** Moderadamente trabada, parcialmente disturbada, bloques angulosos formados por cuatro o más sistemas de discontinuidades (12 a 20 fracturas por metro).
    * **INTENSAMENTE FRACTURADA (IF):** Plegamiento y fallamiento con muchas discontinuidades interceptadas formando bloques angulosos o irregulares (Más de 20 fracturas por metro).
    * **TRITURADA O BRECHADA (T):** Ligeramente trabada, masa rocosa extremadamente rota con una mezcla de fragmentos fácilmente disgregables, angulosos y redondeados (Sin RQD).
    """)

with st.expander("📖 Ver detalles completos de las COLUMNAS (Condición Superficial)"):
    st.markdown("""
    * **MUY BUENA (MB):** Extremadamente resistente, fresca. Superficie de las discontinuidades muy rugosas e inalteradas, cerradas. Se astilla con golpes de picota ($R_c > 250\\text{ MPa}$).
    * **BUENA (B):** Muy resistente, levemente alterada. Discontinuidades rugosas, levemente alteradas, manchas de oxidación, ligeramente abierta. Se rompe con varios golpes de picota ($R_c\\text{ } 100\\text{ a } 250\\text{ MPa}$).
    * **REGULAR (R):** Resistente, levemente alterada. Discontinuidades lisas, moderadamente alteradas, ligeramente abierta. Se rompe con uno o dos golpes de picota ($R_c\\text{ } 50\\text{ a } 100\\text{ MPa}$).
    * **POBRE (P):** Moderadamente resistente, moderadamente alterada. Superficie pulida o con estriaciones, muy alterada, relleno compacto o con fragmentos de roca. Se indenta superficialmente ($R_c\\text{ } 25\\text{ a } 50\\text{ MPa}$).
    * **MUY POBRE (MP):** Blanda, muy alterada. Superficie pulida y estriada, muy abierta, con relleno de arcillas blandas. Se disgrega o indenta superficialmente ($R_c < 25\\text{ MPa}$).
    """)