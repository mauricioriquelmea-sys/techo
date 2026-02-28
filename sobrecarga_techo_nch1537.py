# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# =================================================================
# 1. CONFIGURACIÓN Y ESTILO
# =================================================================
st.set_page_config(page_title="NCh 1537:2009 | Mauricio Riquelme", layout="wide")

st.markdown("""
    <style>
    .main > div { padding-left: 2.5rem; padding-right: 2.5rem; }
    .stMetric { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border: 1px solid #d1d3d4; }
    .result-box { background-color: #e8f4ea; padding: 25px; border-left: 8px solid #28a745; border-radius: 8px; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 2. ENCABEZADO
# =================================================================
st.title("🏠 Sobrecarga de Uso en Techos (NCh 1537:2009)")
st.markdown("#### **Determinación de Lr según Área Tributaria y Pendiente**")
st.divider()

# =================================================================
# 3. SIDEBAR: PARÁMETROS DE DISEÑO
# =================================================================
st.sidebar.header("⚙️ Parámetros de Entrada")

with st.sidebar.expander("📐 Geometría y Uso", expanded=True):
    at = st.number_input("Área Tributaria AT (m²)", value=20.0, min_value=1.0, step=1.0)
    pendiente_pct = st.number_input("Pendiente del Techo (%)", value=10.0, min_value=0.0, step=1.0)
    
    tipo_techo = st.sidebar.selectbox(
        "Tipo de Techo",
        ["Techos corrientes (incapacidad de retener agua)", "Techos para jardines", "Techos para reuniones"]
    )

# =================================================================
# 4. MOTOR DE CÁLCULO (LÓGICA DE REDUCCIÓN)
# =================================================================

# Sobrecarga nominal base (Tabla 4 NCh 1537)
if tipo_techo == "Techos corrientes (incapacidad de retener agua)":
    Lo = 100 # kgf/m2 (valor base para techos no accesibles)
    
    # Factores de Reducción (Sección 7.2)
    # R1: Por área tributaria
    if at <= 20: R1 = 1.0
    elif at >= 60: R1 = 0.6
    else: R1 = 1.2 - 0.01 * at
    
    # R2: Por pendiente
    # F = 0.12 * pendiente (%)
    F = 0.12 * pendiente_pct
    if F <= 4: R2 = 1.0
    elif F >= 12: R2 = 0.6
    else: R2 = 1.2 - 0.05 * F
    
    lr_final = Lo * R1 * R2
    
    # La norma establece un mínimo de 40 kgf/m2 para techos
    lr_final = max(lr_final, 40)

elif tipo_techo == "Techos para jardines":
    Lo = 100 # Según especificación paisajismo, pero mín 100
    lr_final = Lo # No aplica reducción de área usualmente
    R1, R2 = 1.0, 1.0

else: # Techos para reuniones
    Lo = 500 # kgf/m2
    lr_final = Lo
    R1, R2 = 1.0, 1.0

# =================================================================
# 5. RESULTADOS
# =================================================================
st.subheader("📊 Resultados de Sobrecarga de Diseño")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Sobrecarga Base (Lo)", f"{Lo} kgf/m²")
with c2:
    st.metric("Factor Reducción (R1xR2)", f"{R1*R2:.2f}")
with c3:
    st.metric("Sobrecarga Final (Lr)", f"{lr_final:.1f} kgf/m²")



st.markdown(f"""
<div class="result-box">
    <h3>✅ Sobrecarga de Uso Calculada: {lr_final:.1f} kgf/m²</h3>
    <hr>
    <strong>Memoria de Cálculo:</strong>
    <ul>
        <li><strong>Factor R1 (Área):</strong> {R1:.2f} (AT = {at} m²)</li>
        <li><strong>Factor R2 (Pendiente):</strong> {R2:.2f} (Pendiente = {pendiente_pct} %)</li>
        <li><strong>Criterio Normativo:</strong> Se ha aplicado el límite inferior de 40 kgf/m² según Cláusula 7.2.1.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# =================================================================
# 6. GRÁFICO DE SENSIBILIDAD
# =================================================================
st.subheader("📈 Sensibilidad: Sobrecarga vs Área Tributaria")

at_rango = np.linspace(1, 100, 50)
lr_rango = []

for a in at_rango:
    # Lógica de R1 dinámica
    r1_temp = 1.0 if a <= 20 else 0.6 if a >= 60 else 1.2 - 0.01 * a
    # R2 constante para este gráfico
    val = Lo * r1_temp * R2
    lr_rango.append(max(val, 40))

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(at_rango, lr_rango, color='#28a745', lw=2, label='Lr calculada')
ax.axhline(40, color='red', ls='--', label='Mínimo Normativo (40 kgf/m²)')
ax.set_xlabel("Área Tributaria (m²)")
ax.set_ylabel("Sobrecarga Lr (kgf/m²)")
ax.grid(True, alpha=0.3)
ax.legend()
st.pyplot(fig)

# =================================================================
# 7. CIERRE
# =================================================================
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center;">
        <p style="font-family: 'Georgia', serif; font-size: 1.2em; color: #333; font-style: italic;">
            "Programming is understanding"
        </p>
        <p style="font-size: 0.8em; color: #666;">Mauricio Riquelme | Proyectos Estructurales EIRL | NCh 1537 Of.2009</p>
    </div>
""", unsafe_allow_html=True)