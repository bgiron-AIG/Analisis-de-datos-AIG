import streamlit as st
from google import genai
import os

# Configuración de la ventana web
st.set_page_config(
    page_title="Seguridad Operacional - Análisis de Accidentes",
    layout="wide",
    page_icon="✈️"
)

st.title("✈️ Evaluación de Recomendaciones de Seguridad Operacional")
st.caption("Sistema de análisis en tiempo real basado en investigación de accidentes aéreos")

# 1. AUTENTICACIÓN CON LA API DE GEMINI
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ No se ha detectado la Clave de API (GEMINI_API_KEY). Por favor configúrala en los secretos de la aplicación.")
    st.stop()

client = genai.Client(api_key=api_key)

# 2. INSTRUCCIONES DEL SISTEMA
# (Aquí pegas únicamente las instrucciones/instrucciones del sistema que copiaste de AI Studio)
SYSTEM_INSTRUCTION = """
Eres un experto en seguridad operacional de aviación civil y análisis de investigaciones de accidentes e incidentes aéreos.
Tu función es evaluar datos históricos, procesos en curso y recomendaciones de seguridad operacional de la AIG de El Salvador.
[Pega aquí tus instrucciones completas del sistema]
"""

# 3. BASE DE DATOS O INFORMACIÓN CENTRALIZADA
@st.cache_data(ttl=300)  # Se actualiza cada 5 minutos
def cargar_datos_centrales():
    return """
    [PEGA AQUÍ LOS DATOS HISTÓRICOS Y EN PROCESO QUE QUIERES QUE TODOS CONSULTEN]
    """

datos_compartidos = cargar_datos_centrales()

# Panel visualizable para revisar la base de datos cargada
with st.expander("📂 Ver información operacional cargada actualmente en el sistema"):
    st.text(datos_compartidos)

st.divider()

# 4. INTERFAZ DE USUARIO PARA INTERACTUAR CON LA IA
st.subheader("Hacer una consulta sobre las recomendaciones de seguridad")
pregunta_usuario = st.text_area(
    "Ingresa tu consulta o parámetro de evaluación:",
    placeholder="Ejemplo: Evalúa las recomendaciones emitidas para fallas en sensores de velocidad en el historial reciente..."
)

if st.button("🔍 Evaluar y Analizar", type="primary"):
    if not pregunta_usuario.strip():
        st.warning("Por favor ingresa una pregunta o consulta.")
    else:
        with st.spinner("Procesando consulta con la información operacional actualizada..."):
            prompt_completo = f"""
            CONSULTA DEL USUARIO:
            {pregunta_usuario}

            BASE DE DATOS Y CONTEXTO COMPARTIDO:
            ---
            {datos_compartidos}
            ---
            """

            try:
                # Llamada al modelo Gemini
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt_completo,
                    config={
                        'system_instruction': SYSTEM_INSTRUCTION
                    }
                )

                st.subheader("📌 Resultado del Análisis")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Error al procesar la solicitud: {e}")
