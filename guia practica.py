import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from wordcloud import WordCloud
from PIL import Image
import base64
from io import BytesIO

# Título centrado
st.markdown('<h1 style="text-align:center;"> Guía Práctica</h1>', unsafe_allow_html=True)

# Cargar imagen
imagen = Image.open("descarga.png")

# Convertir imagen a base64
buffer = BytesIO()
imagen.save(buffer, format="PNG")
img_str = base64.b64encode(buffer.getvalue()).decode()

# CSS para centrar imagen
st.markdown(
    """
    <style>
    .img-center {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Mostrar imagen centrada
st.markdown(
    f"""
    <div class="img-center">
        <img src="data:image/png;base64,{img_str}" style="width:300px; height:auto;" />
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------
# Línea divisoria
# ----------------------
st.markdown("---")

# ----------------------
# Carga del archivo Excel con control de errores
# ----------------------
try:
    df = pd.read_excel("personas_registradas.xlsx")
    archivo_cargado = True

    # Crear columnas necesarias si existe 'Correo'
    if 'Correo' in df.columns:
        df['Dominio_Correo'] = df['Correo'].str.extract(r'@([\w\.-]+)')
        df['Tipo_Correo'] = df['Dominio_Correo'].apply(
            lambda x: 'Institucional' if 'edu' in str(x) else 'Personal'
        )
except Exception as e:
    st.error(f"❌ Error al cargar el archivo Excel: {e}")
    archivo_cargado = False
    df = pd.DataFrame()

# ----------------------
# Menú lateral
# ----------------------
opcion_lateral = st.sidebar.selectbox(
    "📌 Pasos que están en la Guía",
    [
        "Pasos de la Guía",
        "Análisis de personas registradas",
        "Registros por Instituto",
        "Conclusion"
    ]
)

# ----------------------
# Sección 1: Pasos de la Guía
# ----------------------
if opcion_lateral == "Pasos de la Guía":
    st.markdown("## 👋 Bienvenido a la Guía Práctica")
    st.markdown("""
    Bienvenido a la Guía Práctica para el análisis de datos de personas registradas. Aquí podrás cargar y analizar datos desde un archivo Excel con diferentes herramientas interactivas.  

    Cada sección incluye un botón para ejecutar el análisis correspondiente cuando tú lo desees.
    """)

    st.markdown("### 📥 Carga de archivo Excel")
    st.markdown("Aquí se podrá visualizar la información de los estudiantes registrados (datos personales).")

    if archivo_cargado:
        if st.button("📚 Mostrar datos cargados"):
            st.markdown("### Paso 1: Visualización del DataFrame original")
            st.dataframe(df)
    else:
        st.warning("No se pudo cargar el archivo.")

# ----------------------
# Sección 2: Análisis de personas registradas
# ----------------------
elif opcion_lateral == "Análisis de personas registradas":
    st.markdown("## 📊 Análisis de personas registradas")
    st.markdown("""
    En esta parte se analizarán los pasos para ver el archivo xls, pero para eso debemos importar la librería **pandas** y **matplotlib**.  

    De ahí cargamos el archivo xls y lo guardamos en un **DataFrame**.
    """)
    if archivo_cargado:
        if st.button("📄 Mostrar primeras filas e info del DataFrame"):
            st.markdown("### 📊 Visualización del DataFrame")
            st.markdown("```python\n df.head() \n df.info() \n```")
            st.markdown("### 🧾 Primeras filas del DataFrame")
            st.dataframe(df.head())

            st.markdown("### 🧠 Información del DataFrame")
            buffer = io.StringIO()
            df.info(buf=buffer)
            st.text(buffer.getvalue())
        else:
            st.info("Haz clic para mostrar las primeras filas y la info del DataFrame.")
    else:
        st.warning("No se pudo cargar el archivo para mostrar los datos.")

# ----------------------
# Sección 3: Registros por Instituto
# ----------------------
elif opcion_lateral == "Registros por Instituto":
    st.markdown("## 🏫 Registros por Instituto")
    st.markdown("En esta sección se realiza un análisis detallado de los registros de personas según la institución a la que pertenecen, así como otros aspectos relacionados con su información de contacto y nombres."
    
    "Esta sección te ayudará a comprender mejor la distribución de los datos y a detectar tendencias o agrupaciones dentro del conjunto de registros.")

    if not archivo_cargado:
        st.warning("No se pudo cargar el archivo.")
    else:
        if 'Institución' in df.columns:
            if st.button("📊 Mostrar gráfico de registros por institución"):
                st.subheader("1. Registros por Institución")
                fig1, ax1 = plt.subplots()
                df["Institución"].value_counts().plot(kind="bar", color="skyblue", ax=ax1)
                ax1.set_title("Registros por Institución", fontsize=10)
                ax1.set_xlabel("Institución", fontsize=6)
                ax1.set_ylabel("Cantidad", fontsize=6)
                ax1.tick_params(axis='x', rotation=90, labelsize=4)
                ax1.tick_params(axis='y', labelsize=5)
                st.pyplot(fig1)
        else:
            st.warning("La columna 'Institución' no está en el archivo.")

        if 'Dominio_Correo' in df.columns:
            if st.button("🥧 Mostrar distribución de dominios de correo (Top 5)"):
                st.subheader("2. Distribución de Dominios de Correo (Top 5)")
                fig2, ax2 = plt.subplots()
                df["Dominio_Correo"].value_counts().head(5).plot(
                    kind="pie", autopct='%1.1f%%', shadow=True, ax=ax2,
                    textprops={'fontsize': 6})
                ax2.set_ylabel("")
                ax2.set_title("Dominios más comunes", fontsize=8)
                st.pyplot(fig2)
        else:
            st.warning("La columna 'Dominio_Correo' no está en el archivo.")

        if 'Nombres' in df.columns:
            if st.button("📈 Mostrar Top 10 nombres más comunes"):
                st.subheader("3. Top 10 Nombres más Comunes")
                fig3, ax3 = plt.subplots()
                df["Nombres"].value_counts().head(10).plot(kind="barh", color="lightgreen", ax=ax3)
                ax3.set_title("Nombres más comunes", fontsize=10)
                ax3.set_xlabel("Frecuencia", fontsize=6)
                ax3.set_ylabel("Nombre", fontsize=6)
                ax3.tick_params(axis='x', labelsize=5)
                ax3.tick_params(axis='y', labelsize=5)
                ax3.invert_yaxis()
                st.pyplot(fig3)
        else:
            st.warning("La columna 'Nombres' no está en el archivo.")

        if {'Institución', 'Tipo_Correo'}.issubset(df.columns):
            if st.button("📬 Mostrar gráfico de tipo de correo por institución"):
                st.subheader("4. Tipo de Correo por Institución")
                agrupado = df.groupby(["Institución", "Tipo_Correo"]).size().unstack().fillna(0)
                fig4, ax4 = plt.subplots()
                agrupado.plot(kind="bar", stacked=False, ax=ax4)
                ax4.set_title("Correos Institucionales vs Personales", fontsize=10)
                ax4.set_ylabel("Cantidad", fontsize=6)
                ax4.tick_params(axis='x', rotation=90, labelsize=5)
                ax4.tick_params(axis='y', labelsize=5)
                st.pyplot(fig4)
        else:
            st.warning("Faltan las columnas 'Institución' o 'Tipo_Correo' para esta gráfica.")

        if {'Nombres', 'Apellidos'}.issubset(df.columns):
            if st.button("🧠 Mostrar mapa de palabras de nombres y apellidos"):
                st.subheader("5. Mapa de Palabras de Nombres y Apellidos")
                texto = ' '.join(df['Nombres'].astype(str)) + ' ' + ' '.join(df['Apellidos'].astype(str))
                wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(texto)
                fig5, ax5 = plt.subplots(figsize=(12, 6))
                ax5.imshow(wordcloud, interpolation='bilinear')
                ax5.axis('off')
                st.pyplot(fig5)
        else:
            st.warning("Faltan las columnas 'Nombres' o 'Apellidos' para el mapa de palabras.")

# ----------------------
# Sección 4: Conclusiones
# ----------------------
elif opcion_lateral == "Conclusion":
    st.markdown("## Conclusión:")
    st.markdown("###### 👨‍💻 Desarrollado por: Byron Mendieta") 
    st.markdown("###### 📅 FECHA: 22/05/2025")