# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import base64
from fpdf import FPDF

# =================================================================
# 1. CONFIGURACIÓN Y ESTILO
# =================================================================
st.set_page_config(page_title="NCh 1537:2009 | Mauricio Riquelme", layout="wide")

st.markdown("""
    <style>
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6; }
    .result-box { background-color: #e8f4ea; padding: 25px; border-left: 8px solid #28a745; border-radius: 8px; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 2. ENCABEZADO
# =================================================================
st.title("🏠 Sobrecarga de Uso en Techos (NCh 1537 Of.2009)")
st.markdown("#### **Determinación de la Carga de Diseño Lr**")
st.divider()

# =================================================================
# 3. SIDEBAR: PARÁMETROS TÉCNICOS
# =================================================================
st.sidebar.header("⚙️ Parámetros de Entrada")

with st.sidebar.expander("📐 Geometría del Techo", expanded=True):
    at = st.number_input("Área Tributaria AT (m²)", value=20.0, min_value=1.0, step=1.0)
    # Entrada en porcentaje de pendiente
    pendiente_pct = st.number_input("Pendiente del Techo (%)", value=10.0, min_value=0.0, step=1.0)

# =================================================================
# 4. MOTOR DE CÁLCULO (SECCIÓN 7.2)
# =================================================================

# Carga base según Tabla 4
Lo = 100.0  # kgf/m²

# Factor R1: Por área tributaria
if at <= 20:
    R1 = 1.0
elif at >= 60:
    R1 = 0.6
else:
    R1 = 1.2 - 0.01 * at

# Factor R2: Por pendiente
# La norma define F como mm de ascenso por cada 300 mm horizontales
F = (pendiente_pct / 100) * 300

if F <= 4:
    R2 = 1.0
elif F >= 12:
    R2 = 0.6
else:
    R2 = 1.2 - 0.05 * F

# Carga final con reducciones
lr_final = Lo * R1 * R2

# Límite inferior normativo (7.2.1)
lr_final = max(lr_final, 40.0)

# =================================================================
# 5. RESULTADOS Y MÉTRICAS
# =================================================================
st.subheader("📊 Factores de Reducción y Sobrecarga Final")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Factor R1 (Área)", f"{R1:.2f}")
with c2:
    st.metric("Factor R2 (Pendiente)", f"{R2:.2f}")
with c3:
    st.metric("Carga Inicial Lo", "100 kgf/m²")
with c4:
    st.metric("Sobrecarga Lr", f"{lr_final:.1f} kgf/m²")



st.markdown(f"""
<div class="result-box">
    <h3>✅ Especificación de Sobrecarga: {lr_final:.1f} kgf/m²</h3>
    <hr>
    <strong>Memoria de Cálculo:</strong>
    <ul>
        <li><strong>Reducción R1:</strong> Calculada para una superficie de influencia de {at} m².</li>
        <li><strong>Reducción R2:</strong> Calculada para una pendiente del {pendiente_pct}%.</li>
        <li><strong>Límite Normativo:</strong> Se cumple con el mínimo de 40 kgf/m² establecido en Chile.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# =================================================================
# 6. GRÁFICO DE SENSIBILIDAD
# =================================================================
st.subheader("📈 Sensibilidad de la Carga Lr vs Área")

at_rango = np.linspace(1, 100, 50)
lr_rango = []

for a in at_rango:
    r1_t = 1.0 if a <= 20 else 0.6 if a >= 60 else 1.2 - 0.01 * a
    val = Lo * r1_t * R2
    lr_rango.append(max(val, 40))

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(at_rango, lr_rango, color='#28a745', lw=2.5, label='Lr (Sobrecarga de Uso)')
ax.axhline(40, color='red', ls='--', label='Piso Normativo (40 kgf/m²)')
ax.set_xlabel("Área Tributaria AT (m²)")
ax.set_ylabel("Carga Lr (kgf/m²)")
ax.grid(True, alpha=0.3)
ax.legend()
st.pyplot(fig)

# =================================================================
# 7. GENERADOR DE PDF PROFESIONAL (NUEVO)
# =================================================================
def generar_pdf_techo():
    pdf = FPDF()
    pdf.add_page()
    if os.path.exists("Logo.png"):
        pdf.image("Logo.png", x=10, y=8, w=33)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Memoria de Calculo: Sobrecarga de Techo", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 7, "NCh 1537:2009 | Proyectos Estructurales", ln=True, align='C')
    pdf.ln(15)

    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, " 1. PARAMETROS DE ENTRADA", ln=True, fill=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f" Area Tributaria (AT): {at} m2", ln=True)
    pdf.cell(0, 8, f" Pendiente del Techo: {pendiente_pct} %", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, " 2. FACTORES DE REDUCCION (Seccion 7.2)", ln=True, fill=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f" Factor R1 (Area): {R1:.2f}", ln=True)
    pdf.cell(0, 8, f" Factor R2 (Pendiente): {R2:.2f}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, " 3. RESULTADO FINAL", ln=True, fill=True)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f" SOBRECARGA DE DISENO (Lr): {lr_final:.1f} kgf/m2", ln=True)
    
    pdf.set_y(-25)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, "Reporte generado por Mauricio Riquelme - Proyectos Estructurales", align='C')
    return pdf.output()

st.sidebar.markdown("---")
pdf_bytes = generar_pdf_techo()
b64 = base64.b64encode(pdf_bytes).decode()
st.sidebar.markdown(f"""
    <div style="text-align: center;">
        <a href="data:application/pdf;base64,{b64}" download="Memoria_Techo_NCh1537.pdf" 
           style="background-color: #28a745; color: white; padding: 12px 20px; text-decoration: none; 
           border-radius: 5px; font-weight: bold; display: block;">
           📥 DESCARGAR REPORTE PDF
        </a>
    </div>
""", unsafe_allow_html=True)

# =================================================================
# 8. CIERRE
# =================================================================
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center;">
        <p style="font-family: 'Georgia', serif; font-size: 1.3em; color: #333; font-style: italic;">
            "Programming is understanding"
        </p>
        <p style="font-size: 0.9em; color: #666;">Mauricio Riquelme | Proyectos Estructurales EIRL</p>
    </div>
""", unsafe_allow_html=True)