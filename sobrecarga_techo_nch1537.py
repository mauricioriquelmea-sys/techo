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
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6; }
    .result-box { background-color: #e8f4ea; padding: 25px; border-left: 8px solid #28a745; border-radius: 8px; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 2. ENCABEZADO
# =================================================================
st.title("🏠 Sobrecarga de Uso en Techos (NCh 1537:2009)")
st.markdown("#### **Cálculo de Sobrecarga Reducida Lr**")
st.divider()

# =================================================================
# 3. SIDEBAR: PARÁMETROS TÉCNICOS
# =================================================================
st.sidebar.header("⚙️ Parámetros de Entrada")

with st.sidebar.expander("📐 Geometría del Techo", expanded=True):
    at = st.number_input("Área Tributaria AT (m²)", value=20.0, min_value=1.0, step=1.0)
    # Pendiente en porcentaje (ej: 10% = 10)
    pendiente_pct = st.number_input("Pendiente del Techo (%)", value=10.0, min_value=0.0, step=1.0)

# =================================================================
# 4. MOTOR DE CÁLCULO (SECCIÓN 7.2)
# =================================================================

# Sobrecarga base nominal Lo (Tabla 4)
Lo = 100.0  # kgf/m²

# Factor R1: Por área tributaria
if at <= 20:
    R1 = 1.0
elif at >= 60:
    R1 = 0.6
else:
    R1 = 1.2 - 0.01 * at

# Factor R2: Por pendiente (F = aumento de elevación en mm por cada 300mm)
# F = (pendiente_pct / 100) * 300
F = (pendiente_pct / 100) * 300

if F <= 4:
    R2 = 1.0
elif F >= 12:
    R2 = 0.6
else:
    R2 = 1.2 - 0.05 * F

# Cálculo de la sobrecarga final
lr_final = Lo * R1 * R2

# Mínimo normativo infranqueable para techos
lr_final = max(lr_final, 40.0)

# =================================================================
# 5. RESULTADOS Y MÉTRICAS
# =================================================================
st.subheader("📊 Factores de Reducción y Carga Final")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Factor R1 (Área)", f"{R1:.2f}")
with c2:
    st.metric("Factor R2 (Pendiente)", f"{R2:.2f}")
with c3:
    st.metric("Carga Base Lo", "100 kgf/m²")
with c4:
    st.metric("Carga Final Lr", f"{lr_final:.1f} kgf/m²")

[Image of roof live load reduction factors R1 and R2 chart from ASCE 7 or NCh 1537]

st.markdown(f"""
<div class="result-box">
    <h3>✅ Sobrecarga de Diseño: {lr_final:.1f} kgf/m²</h3>
    <hr>
    <strong>Memoria de Verificación:</strong>
    <ul>
        <li><strong>Reducción por Área (R1):</strong> Aplicado para {at} m².</li>
        <li><strong>Reducción por Pendiente (R2):</strong> Aplicado para {pendiente_pct}% de inclinación.</li>
        <li><strong>Validación Mínima:</strong> Se asegura el cumplimiento del límite de 40 kgf/m² (NCh 1537, 7.2.1).</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# =================================================================
# 6. GRÁFICO DE SENSIBILIDAD
# =================================================================
st.subheader("📈 Sensibilidad de la Carga Lr")

at_rango = np.linspace(1, 100, 50)
lr_rango = []

for a in at_rango:
    r1_temp = 1.0 if a <= 20 else 0.6 if a >= 60 else 1.2 - 0.01 * a
    val = Lo * r1_temp * R2
    lr_rango.append(max(val, 40))

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(at_rango, lr_rango, color='#28a745', lw=2.5, label='Sobrecarga Lr')
ax.axhline(40, color='red', ls='--', label='Mínimo Normativo')
ax.set_xlabel("Área Tributaria AT (m²)")
ax.set_ylabel("Carga Lr (kgf/m²)")
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