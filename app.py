import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from code import plots  # Importa las funciones de visualización desde el módulo 'code.plots'

# Configuración de la página
st.set_page_config(
    page_title="GeoEdu Chile: Exploración Territorial Universitaria",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class SidebarText:
    introduccion = """
    <h4>🌎 GeoEdu Chile</h4>
    Plataforma interactiva basada en el <b>Estudio de Contextualización Territorial Universitaria</b>, 
    desarrollado en el marco del proyecto <b>RED20993</b>.

    Esta aplicación permite explorar y analizar:
    <ul>
        <li>📊 La distribución territorial de instituciones educativas.</li>
        <li>🌍 La movilidad interregional de los estudiantes.</li>
        <li>📈 Las desigualdades regionales en puntajes, distancias y vulnerabilidad.</li>
    </ul>

    Todo con el propósito de fortalecer la toma de decisiones en educación superior con un enfoque territorial.
    """

    objetivos = """
    <h5>🎯 Objetivos del estudio</h5>
    <ul>
        <li>📌 Desarrollar un instrumento de contextualización territorial del ingreso universitario.</li>
        <li>📌 Analizar movilidad, puntajes, distancia y vulnerabilidad desde una perspectiva regional.</li>
        <li>📌 Apoyar la formulación de estrategias institucionales y políticas públicas.</li>
    </ul>
    """

    autores = """
    <h5>📄 Equipo de trabajo:</h5>
    <p>Esta aplicación ha sido anonimizada para revisión por pares.</p>
    """


class BodyText:
    tab1_tabla1 = """
    Según el *Informe Estadístico del Sistema Educacional con enfoque de género* (MINEDUC, 2021), en 2019, de un total de 251.706 estudiantes egresados de educación escolar,
    un 41,7% ingresó a la educación superior. Un 58,1% de quienes ingresan lo hacen a universidades, mientras el resto opta por el subsistema técnico profesional.

    """
    tab1_tabla2 = """
    La diferencia entre la tabla anterior y las nuevas matrículas de 2021 puede deberse a estudiantes reincorporados, movilidad entre instituciones o rezagos. La siguiente tabla, extraída desde SIES 2021, lo detalla:
    """
    tab1_tabla3 = """
    Para complementar este análisis, se cruzaron datos de matrícula con registros de PSU:
    """
    tab1_tabla4 = """
    Finalmente, se construyó una muestra robusta para el análisis utilizando fuentes como SIES, DEMRE y JUNAEB. La siguiente tabla resume las variables clave y su cobertura:
    """
    tab1_fuentes1 = """
Se utilizaron fuentes públicas oficiales del sistema educativo chileno, disponibles para libre acceso:

- **📌 [Matrícula en Educación Superior (SIES)](https://datosabiertos.mineduc.cl/matricula-en-educacion-superior/):** Registro anual de matrícula de estudiantes en instituciones de educación superior, incluyendo carrera, tipo de ingreso e institución.
- **📌 [Puntajes de Admisión (DEMRE)](https://datosabiertos.mineduc.cl/pruebas-de-admision-a-la-educacion-superior/):** Resultados de las pruebas PSU/PAES y antecedentes de postulación, incluyendo dirección de egreso y tipo de establecimiento.
- **📌 [Establecimientos Educacionales (MINEDUC)](https://www.geoportal.cl/geoportal/catalog/35408/Establecimientos%20Educaci%C3%B3n%20Escolar):** Información georreferenciada de colegios y liceos, junto con su matrícula vigente al 30 de agosto de cada año.
- **📌 [Inmuebles de Educación Superior (MINEDUC)](https://www.geoportal.cl/geoportal/catalog/35408/Establecimientos%20Educaci%C3%B3n%20Escolar):** Coordenadas y localización de las sedes de instituciones de educación superior.
- **📌 [Índice de Vulnerabilidad Multidimensional (IVM – JUNAEB)](https://www.junaeb.cl/medicion-la-vulnerabilidad-ivm/):** Indicador que estima el nivel de vulnerabilidad socioeducativa de los estudiantes, con valores entre 0 y 100.
"""
    tab1_fuentes2 = """
Se definieron tres conjuntos iniciales de datos según criterios de edad, nivel educativo e institución:

- **🧾 A0:** Estudiantes de primer año en educación superior, ingreso regular, sin carrera previa.
- **🧾 A:** A0 filtrado por estudiantes de entre 15 y 19 años.
- **🧾 A1:** A filtrado por estudiantes matriculados exclusivamente en universidades.

Estos conjuntos se complementaron con información adicional proveniente de otras bases de datos:

- **🧾 B:** Puntajes PSU, vinculados mediante RUN enmascarado (MRUN), correspondientes a los procesos de admisión 2019, 2020 y 2021.
- **🧾 C:** Establecimientos escolares georreferenciados (11.285 RBDs), incluyendo datos de vulnerabilidad (IVM).
- **🧾 D:** Inmuebles de instituciones de educación superior georreferenciados (1.297 sedes).
- **🧾 E:** Índice de Vulnerabilidad Multidimensional (IVM) de los establecimientos de enseñanza media.

"""

    tab1_fuentes3 = """
Cada conjunto fue enriquecido con nuevas variables mediante cruces de datos:

- **🧾 A1B:** Puntaje PSU, dependencia y región de egreso.
- **🧾 A1BCD:** + Distancia geográfica entre comuna de egreso y sede universitaria.
- **🧾 A1BCDE:** + Índice de Vulnerabilidad Multidimensional (IVM).

Estas combinaciones permitieron analizar movilidad, desigualdades y condiciones de ingreso de forma georreferenciada.
    """
    tab2_fig1 = """
La oferta académica universitaria en Chile, vigente al año 2021, estaba compuesta por un total de **56 universidades**, clasificadas en tres tipos institucionales:

- **18 Universidades Estatales pertenecientes al CRUCH**
- **12 Universidades Privadas adscritas al CRUCH**
- **26 Universidades Privadas no adscritas al CRUCH**

El **CRUCH** (Consejo de Rectores de las Universidades Chilenas) agrupa a instituciones que participan en el sistema común de admisión y en instancias de coordinación académica a nivel nacional.  
*Fuente: SIES, Ministerio de Educación, 2021.*
    """
    tab2_fig2 = """
La distribución de establecimientos de educación media según su dependencia administrativa varía significativamente entre regiones.

Esta clasificación considera establecimientos **municipales**, **particulares subvencionados** y **particulares pagados**, lo que permite observar diferencias territoriales que influyen en el origen escolar de quienes ingresan a la educación superior.  
*Fuente: CEM, Ministerio de Educación, 2021.*
    """
    tab2_fig3 = """
    A continuación se examina el **Índice de Vulnerabilidad Multidimensional (IVM)** provisto por **JUNAEB** para establecimientos de educación media. Este índice permite conocer la **condición de vulnerabilidad de la población estudiantil** a nivel territorial e institucional, y se clasifica en cuatro categorías:

- IVM Bajo
- IVM Medio
- IVM Alto
- IVM Muy Alto

Esta clasificación es útil para identificar contextos educativos más desfavorecidos y orientar políticas de equidad educativa.  
*Fuente: JUNAEB, 2021.*
"""
    tab3_fig1 = """
La matriz de movilidad muestra los flujos de estudiantes desde su región de egreso hacia la región donde ingresan a la universidad. En general, los estudiantes prefieren matricularse en regiones cercanas.

Las regiones más preferidas como destino son **Metropolitana**, **Valparaíso**, **Biobío**, **La Araucanía** y **Maule**. En cambio, **O’Higgins**, **Aysén** y **Magallanes** presentan menor atracción.

Estudiantes del sur del país rara vez se desplazan hacia el norte, especialmente más allá de Coquimbo.

    """

    tab3_fig2 = """
A partir de la matriz de movilidad se calcularon dos tasas: la **tasa de migración**, que mide el porcentaje de estudiantes que estudian fuera de su región de origen, y la **tasa de recepción**, que indica cuántos estudiantes provienen de otras regiones.

Las regiones con mayor migración son **Tarapacá (96%)** y **Aysén (94%)**, mientras que las de menor migración son **Metropolitana (4%)** y **Biobío (9,5%)**.

En cuanto a recepción, destacan **Los Ríos (52,7%)**, **Valparaíso (27,9%)** y **Biobío (25,7%)** como las regiones que más reciben estudiantes desde otras zonas. Por el contrario, **O’Higgins (4,6%)** y **Aysén (7,4%)** tienen baja recepción.

Respecto a las distancias promedio, **Tarapacá** registra los desplazamientos más extensos, mientras que la **Región Metropolitana** muestra las distancias más cortas.

    """

    tab4_fig1 = """
Se analizaron variables como **movilidad**, **tasa IVM**, **puntaje PSU**, **ranking** y **distancia** de desplazamiento, agrupadas por región.

Se usó el método de detección de anomalías **Isolation Forest**, identificando cinco regiones con características particulares:

- **Atacama**: Puntajes bajos, segunda menor distancia, baja recepción.  
- **Región Metropolitana**: Puntajes más altos, menor migración, alta vulnerabilidad.  
- **O’Higgins**: Mayor migración, menor recepción, alto ranking.  
- **Los Ríos**: Alta recepción, gran distancia, buen ranking.  
- **Aysén**: Puntajes más bajos, mayor distancia, menor tasa IVM.
    """

    tab4_fig2 = """
    Se aplicó **k-Means (k=3)** para agrupar regiones no anómalas.  
    Agrupación resultante:

    - **Grupo X**: Arica, Tarapacá, Antofagasta, Magallanes  
    - **Grupo Y**: Coquimbo, Ñuble, La Araucanía, Los Lagos  
    - **Grupo Z**: Valparaíso, Maule, Biobío
    """

    tab4_fig3 = """
Respecto al puntaje en pruebas obligatorias de los matriculados en una universidad de la región, es posible notar que los tres grupos son distintos entre sí: el **grupo Z** es el que evidencia el mayor valor (548), seguido del **grupo Y** (522) y finalmente el **grupo X** (512). Las regiones de O’Higgins (548) y Los Ríos (553) no evidencian diferencia significativa respecto al grupo Z. De igual forma, los pares Atacama-Aysén (494-488) y O’Higgins-Los Ríos (548-553) tampoco evidencian diferencias significativas. La región Metropolitana (576) tiene el mayor puntaje y es el único outlier con diferencia significativa respecto a todos los demás grupos y regiones anómalas.
    """

    tab4_fig4 = """
Respecto al puntaje en las pruebas obligatorias de los egresados/as de la región que ingresan a alguna universidad en el país, es posible notar que los tres grupos son distintos entre sí: el **grupo Z** es el que evidencia el mayor valor (548), seguido del **grupo Y** (538) y finalmente el **grupo X** (528). Las regiones Los Ríos (533) y Aysén (538) no evidencian diferencia significativa respecto a los grupos Y y Z (pero éstos sí son distintos entre sí). De igual forma, el par Los Ríos-Aysén tampoco evidencia diferencia significativa.
    """

    tab4_fig5 = """
Respecto al puntaje ranking de los matriculados/as en una universidad de la región, es posible notar que los tres grupos son distintos entre sí: el **grupo Z** es el que evidencia el mayor valor (675), seguido del **grupo X** (664) y finalmente el **grupo Y** (649). Los pares Atacama-Aysén (615-613) y O’Higgins-Los Ríos (704-695) no evidencian diferencia significativa.
    """

    tab4_fig6 = """
Respecto al puntaje ranking de los egresados/as de la región que ingresan a alguna universidad en el país, el tamaño del efecto resulta ser insignificante (𝜀 < 0.01).
    """

    tab4_fig7 = """
Con respecto a la distancia de desplazamiento de los matriculados en una universidad de la región, se evidencia diferencia significativa entre los **grupos X, Y y Z** (4, 15 y 30 km respectivamente). No se evidencia diferencia significativa entre la Región Metropolitana (14 km) y el grupo Y, tampoco entre la región de O’Higgins (6 km) y el grupo X. El par O’Higgins-Aysén (ambos con 6 km) no muestran diferencia significativa. Es relevante mencionar que el grupo X muestra un comportamiento bimodal debido a su baja concentración en distancias del orden de las decenas de kilómetros, pero alta concentración en distancias menores y mayores.
    """

    tab4_fig8 = """
Con respecto a la distancia de desplazamiento de los egresados/as de la región que ingresan a alguna universidad en el país, se evidencia diferencia significativa entre los **grupos X, Y y Z** (8, 46 y 23 km respectivamente). No se evidencia diferencia significativa entre la región Atacama (112 km) y el grupo Y. Es relevante mencionar que el grupo X muestra un comportamiento bimodal debido a su baja concentración en distancias del orden de las decenas de kilómetros, pero alta concentración en distancias menores y mayores.
    """

    tab4_fig9 = """
La región de Los Ríos exhibe la tasa de recepción más alta (52.6%), siendo el único caso con mayoría de estudiantes jóvenes foráneos ingresando en 2021 a alguna región, y le siguen el **grupo Z** (25.6%), **grupo Y** (19.6%) y **grupo X** (11.3%). La región Metropolitana tiene una tasa de recepción de un 11.3%, por lo que es mayor respecto al grupo X, pero no respecto a los grupos Y y Z. Las regiones con menor tasa de recepción son O’Higgins (6.2%), Aysén (7.4%) y Atacama (9.1%).
    """

    tab4_fig10 = """
Las regiones con mayor tasa de migración son O’Higgins (81.7%) y Aysén (74%). La región Metropolitana tiene el valor más bajo (4%). El porcentaje de migración del **grupo Z** (16.1%) es menor a los **grupos X e Y** (35.4% y 35.3% respectivamente).
    """

    tab4_fig11 = """
Con respecto al porcentaje de pertenencia a establecimientos de alta vulnerabilidad por región de origen, es posible observar que de manera conjunta los **grupos X, Y y Z** muestran porcentajes decrecientes (12.9%, 7.7% y 4.3%). Las regiones Metropolitana (12%) y Atacama (9.6%) exhiben porcentajes mayores respecto a los grupos X y Z pero no respecto al grupo Z. Finalmente las regiones O’Higgins (4.3%), Los Ríos (4.3%) y Aysén (2%) tienen tasas menores o iguales respecto al grupo Z.
    """

class ImagesPath:
    logo = Path("images/logo.png")
    logo2 = Path("images/logo2.png")
    figura1 = Path("images/figuras/15.png")
    figura2 = Path("images/figuras/16.png")
    figura3 = Path("images/figuras/17.png")
    figura4 = Path("images/figuras/18.png")
    figura5 = Path("images/figuras/19.png")
    figura6 = Path("images/figuras/20.png")
    figura7 = Path("images/figuras/21.png")
    figura8 = Path("images/figuras/22.png")
    figura9 = Path("images/figuras/23.png")
    figura10 = Path("images/figuras/24.png")
def mostrar_sidebar():
    """
    Carga el contenido del panel lateral de la aplicación.
    """

    st.sidebar.image(ImagesPath.logo2, width=200)

    st.sidebar.title('🗺️ GeoEdu Chile: Exploración Territorial Universitaria')
    with st.sidebar:
        with st.expander("📘 Acerca de GeoEdu Chile"):
            st.markdown(SidebarText.introduccion, unsafe_allow_html=True)
            st.markdown(SidebarText.objetivos, unsafe_allow_html=True)
            st.markdown(SidebarText.autores, unsafe_allow_html=True)

def mostrar_cuerpo():
    """
    Cuerpo principal con tabs de navegación para GeoEdu Chile.
    """

    st.title("🗺️ GeoEdu Chile: Exploración Territorial Universitaria")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Población Objetivo",
        "🏛️ Contexto Institucional",
        "🌍 Movilidad Interregional",
        "📊 Ingreso Juvenil Regional"
    ])

    with tab1:
        st.header("Población Objetivo")

        st.markdown(BodyText.tab1_tabla1, unsafe_allow_html=True)
        tabla1 = pd.read_csv("data/plots/tabla1.csv")
        st.dataframe(tabla1, use_container_width=False)

        st.markdown(BodyText.tab1_tabla2, unsafe_allow_html=True)
        tabla2 = pd.read_csv("data/plots/tabla2.csv")
        st.dataframe(tabla2, use_container_width=False)

        st.header("Fuentes de Datos Utilizadas")
        st.markdown(BodyText.tab1_fuentes1, unsafe_allow_html=True)

        st.header("Conjuntos de Datos Iniciales y Complementarios")
        st.markdown(BodyText.tab1_fuentes2, unsafe_allow_html=True)


        st.markdown(BodyText.tab1_tabla4, unsafe_allow_html=True)
        tabla4 = pd.read_csv("data/plots/tabla4.csv")
        st.dataframe(tabla4, use_container_width=False)

    with tab2:
        st.header("Contexto Institucional")
        st.markdown("Explora la distribución de instituciones universitarias por tipo y dependencia.")

        df_tipo = pd.read_csv("data/plots/df_tipo_universidad.csv")
        df_dep = pd.read_csv("data/plots/df_tipodepen.csv")

        
        st.markdown(BodyText.tab2_fig1, unsafe_allow_html=True)

        st.plotly_chart(plots.plotly_tipo_universidad_por_region(df_tipo), use_container_width=False)

        st.markdown(BodyText.tab2_fig2, unsafe_allow_html=True)

        st.plotly_chart(plots.plotly_tipodepen_por_region(df_dep), use_container_width=True)

        st.markdown(BodyText.tab2_fig3, unsafe_allow_html=True)

        df_ivm = pd.read_csv("data/plots/df_ivm.csv")
        st.plotly_chart(plots.plotly_ivm_por_region(df_ivm), use_container_width=True)

    with tab3:
        st.header("Movilidad Interregional")

        matriz = pd.read_csv("data/plots/df_matriz_movilidad.csv", index_col=0)
        df_tasas = pd.read_csv("data/plots/df_tasas_migracion.csv")
        df_dist = pd.read_csv("data/plots/df_migracion_distancia.csv")


        st.markdown(BodyText.tab3_fig1, unsafe_allow_html=True)
        st.plotly_chart(plots.plotly_matriz_movilidad(matriz), use_container_width=True)

        st.markdown(BodyText.tab3_fig2, unsafe_allow_html=True)
        st.plotly_chart(plots.plotly_tasas_migracion_recepcion(df_tasas), use_container_width=True)
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(plots.plotly_migracion_vs_distancia(df_dist), use_container_width=True)

        with col2:
            st.plotly_chart(plots.plotly_tasa_vs_distancia(
                df_dist,
                col_x="DISTANCIA_PROMEDIO_RECEPCIÓN",
                col_y="Tasa Recepción (%)",
                titulo="Tasa de Recepción vs Distancia Promedio de Recepción",
                color="orange"
            ), use_container_width=True)

    with tab4:
        st.header("Ingreso Juvenil Regional")

        st.markdown(BodyText.tab4_fig1)
        st.markdown(BodyText.tab4_fig2)
        st.image(ImagesPath.figura1, caption="Agrupación de regiones por características similares",width=800)

        with st.expander("📈 Puntajes de pruebas y ranking"):
          st.markdown(BodyText.tab4_fig4)
          st.image(ImagesPath.figura3, caption="Puntaje pruebas obligatorias (egresados/as)",width=800)

          st.markdown(BodyText.tab4_fig5)
          st.image(ImagesPath.figura4, caption="Puntaje ranking (matriculados/as)",width=800)

          st.markdown(BodyText.tab4_fig6)
          st.image(ImagesPath.figura5, caption="Puntaje ranking (egresados/as)",width=800)

        with st.expander("📍 Distancia de desplazamiento"):
            st.markdown(BodyText.tab4_fig7)
            st.image(ImagesPath.figura6, caption="Distancia de desplazamiento (matriculados/as)",width=800)

            st.markdown(BodyText.tab4_fig8)
            st.image(ImagesPath.figura7, caption="Distancia de desplazamiento (egresados/as)",width=800)

        with st.expander("🏫 Tasa Recepción, migración y vulnerabilidad"):
            st.markdown(BodyText.tab4_fig9)
            st.image(ImagesPath.figura8, caption="Tasa de recepción por región",width=800)

            st.markdown(BodyText.tab4_fig10)
            st.image(ImagesPath.figura9, caption="Tasa de migración por región",width=800)

            st.markdown(BodyText.tab4_fig11)
            st.image(ImagesPath.figura10, caption="Porcentaje de alta vulnerabilidad por región",width=800)




    # Estilos visuales
    estilos_css = '''
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.3rem;
        }
    </style>
    '''
    st.markdown(estilos_css, unsafe_allow_html=True)

def main():
    """
    Función principal que organiza la estructura de la aplicación.
    """
    mostrar_sidebar()
    mostrar_cuerpo()

# Ejecutar la aplicación si se llama directamente
if __name__ == "__main__":
    main()
