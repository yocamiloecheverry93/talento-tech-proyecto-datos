import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Viabilidad Energía Solar", page_icon="☀️", layout="wide")

# --- CARGA DE DATOS DESDE CSV ---
# El decorador @st.cache_data hace que el CSV se lea una sola vez y la app sea más rápida
@st.cache_data
def load_data():
    # Asegúrate de que tu archivo se llame exactamente así y esté en la misma carpeta
    try:
        df = pd.read_csv('datos_solares.csv', sep=";", encoding='latin-1')
        return df
    except FileNotFoundError:
        st.error("⚠️ No se encontró el archivo 'datos_solares.csv'. Asegúrate de subirlo a tu repositorio.")
        return pd.DataFrame()

# --- MENÚ LATERAL (NAVEGACIÓN) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3254/3254061.png", width=100)
st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Ir a:", ["Landing Page", "Dashboard Analítico"])

# --- SECCIÓN 1: LANDING PAGE ---
if opcion == "Landing Page":
    st.title("☀️ Proyecto Final: Viabilidad de Energía Solar a Gran Escala")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Descripción del Proyecto")
        st.write("""
        Este proyecto analiza la viabilidad y el despliegue global de la energía solar 
        a gran escala (Utility-Scale). Utilizando datos de instalaciones operativas, 
        buscamos identificar tendencias de crecimiento, países líderes y el impacto 
        tecnológico en la transición energética justa.
        """)
        st.write("**Línea de investigación:** Transición energética justa y democratización.")
    
    with col2:
        st.subheader("👥 Equipo de Trabajo")
        st.write("""
        * **[Tu Nombre]** - Arquitecto de Datos / Analista SQL
        * **[Integrante 2]** - Especialista en Python y Pandas
        * **[Integrante 3]** - Desarrollador BI (Streamlit)
        * **[Integrante 4]** - Especialista de Dominio
        * **[Integrante 5]** - Documentación y QA
        * **[Integrante 6]** - Apoyo Analítico
        """)
    
    st.info("👈 Selecciona 'Dashboard Analítico' en el menú lateral para interactuar con los datos.")

# --- SECCIÓN 2: DASHBOARD INTERACTIVO ---
elif opcion == "Dashboard Analítico":
    st.title("📊 Dashboard de Capacidad Solar Operativa")
    st.markdown("Análisis interactivo de las plantas solares a nivel global.")
    
    # Cargar los datos
    df = load_data()
    
    if not df.empty:
        # Pre-procesamiento básico: Filtramos solo los proyectos operativos
        df_operativos = df[df['Status'] == 'operating']
        
        # 1. KPIs Principales (Tarjetas de métricas)
        total_proyectos = len(df_operativos)
        capacidad_total_mw = df_operativos['Capacity (MW)'].sum()
        promedio_planta = capacidad_total_mw / total_proyectos if total_proyectos > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Proyectos Operativos", f"{total_proyectos:,.0f}")
        col2.metric("Capacidad Total (MW)", f"{capacidad_total_mw:,.0f}")
        col3.metric("Promedio por Planta (MW)", f"{promedio_planta:,.1f}")
        
        st.markdown("---")
        
        # 2. Gráfico: Top 10 Países
        st.subheader("Top 10 Países por Capacidad Instalada (MW)")
        
        # Agrupamos por país y sumamos la capacidad
        top_paises = df_operativos.groupby('Country/Area')['Capacity (MW)'].sum().reset_index()
        top_paises = top_paises.sort_values(by='Capacity (MW)', ascending=False).head(10)
        
        fig_barras = px.bar(top_paises, x='Country/Area', y='Capacity (MW)', 
                            color='Capacity (MW)', color_continuous_scale='YlOrRd',
                            labels={'Country/Area': 'País', 'Capacity (MW)': 'Capacidad (MW)'})
        st.plotly_chart(fig_barras, use_container_width=True)

        # 3. Gráfico: Evolución temporal
        st.subheader("Evolución Histórica de Instalaciones (A partir de 2010)")
        
        # Limpiamos los años nulos y filtramos desde 2010
        df_evolucion = df.dropna(subset=['Start year'])
        df_evolucion = df_evolucion[(df_evolucion['Start year'] >= 2010) & (df_evolucion['Start year'] <= 2024)]
        
        # Agrupamos por año de inicio y sumamos la capacidad
        evolucion_agrupada = df_evolucion.groupby('Start year')['Capacity (MW)'].sum().reset_index()
        
        fig_linea = px.line(evolucion_agrupada, x='Start year', y='Capacity (MW)', 
                            markers=True, line_shape='spline',
                            labels={'Start year': 'Año de Inicio', 'Capacity (MW)': 'Nueva Capacidad (MW)'})
        fig_linea.update_traces(line_color='#FF8C00')
        st.plotly_chart(fig_linea, use_container_width=True)
