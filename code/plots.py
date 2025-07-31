import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# Constantes para visualización 
R = 6371.0  # Radio de la Tierra en km

orden_regiones = [
    'Arica y Parinacota', 'Tarapacá', 'Antofagasta', 'Atacama', 'Coquimbo',
    'Valparaíso', 'Metropolitana', "Lib. Gral B. O'Higgins", 'Maule', 'Ñuble',
    'Biobío', 'La Araucanía', 'Los Ríos', 'Los Lagos', 'Aysén', 'Magallanes'
]

tipos_universidad = [
    'Universidades Estatales CRUCH', 
    'Universidades Privadas', 
    'Universidades Privadas CRUCH'
]

regiones_dict = {
    1: 'Región de Tarapacá',
    2: 'Región de Antofagasta',
    3: 'Región de Atacama',
    4: 'Región de Coquimbo',
    5: 'Región de Valparaíso',
    6: 'Región Metropolitana de Santiago',
    7: 'Región del Libertador Gral. Bernardo O’Higgins',
    8: 'Región del Maule',
    9: 'Región de Biobío',
    10: 'Región de La Araucanía',
    11: 'Región de Los Ríos',
    12: 'Región de Los Lagos',
    13: 'Región de Aysén del Gral. Carlos Ibáñez del Campo',
    14: 'Región de Magallanes y de la Antártica Chilena',
    15: 'Región de Arica y Parinacota',
    16: 'Región de Ñuble'
}

tipodepen_dict = {
    1: 'Municipal',
    2: 'Particular Subvencionado',
    3: 'Particular Pagado',
    4: 'Corp. Administración Delegada',
    5: 'Servicio Local de Educación'
}

index_order = [
    'Región de Arica y Parinacota',
    'Región de Tarapacá',
    'Región de Antofagasta',
    'Región de Atacama',
    'Región de Coquimbo',
    'Región de Valparaíso',
    'Región Metropolitana de Santiago',
    'Región del Libertador Gral. Bernardo O’Higgins',
    'Región del Maule',
    'Región de Ñuble',
    'Región de Biobío',
    'Región de La Araucanía',
    'Región de Los Ríos',
    'Región de Los Lagos',
    'Región de Aysén del Gral. Carlos Ibáñez del Campo',
    'Región de Magallanes y de la Antártica Chilena'
]

index_order_02 = [
    'Arica y Parinacota', 'Tarapacá', 'Antofagasta', 'Atacama', 'Coquimbo',
    'Valparaíso', 'Metropolitana', "Lib. Gral B. O'Higgins", 'Maule', 'Ñuble',
    'Biobío', 'La Araucanía', 'Los Ríos', 'Los Lagos', 'Aysén', 'Magallanes'
]

# DataFrames para visualización
def preparar_dataset_tipo_universidad(df, tipos_universidad, orden_regiones):
    """
    Prepara un DataFrame con los porcentajes de tipos de universidad por región.
    """
    df_filtered = df[df['tipo_inst_3'].isin(tipos_universidad)].copy()
    df_filtered_unique = df_filtered.drop_duplicates(subset=['cod_inst', 'region_sede', 'tipo_inst_3'])

    df_filtered_unique.loc[:, 'region_sede'] = pd.Categorical(
        df_filtered_unique['region_sede'],
        categories=orden_regiones,
        ordered=True
    )

    df_grouped = df_filtered_unique.groupby(['region_sede', 'tipo_inst_3'], observed=True).size().unstack(fill_value=0)
    df_porcentaje = df_grouped.div(df_grouped.sum(axis=1), axis=0) * 100
    df_porcentaje = df_porcentaje.reindex(orden_regiones)

    return df_porcentaje.reset_index()

def preparar_dataset_tipodepen(df, regiones_dict, tipodepen_dict, index_order):
    """
    Prepara el dataset con porcentajes de TIPO_DEPEN por región.

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame original con las columnas 'NOM_RBD', 'COD_REG_RB', 'TIPO_DEPEN'.
    regiones_dict : dict
        Mapea código de región a nombre.
    tipodepen_dict : dict
        Mapea códigos de dependencia a nombres legibles.
    index_order : list
        Lista de regiones ordenadas de norte a sur.

    Retorna:
    --------
    df_porcentaje : pd.DataFrame
        DataFrame con los porcentajes por tipo de dependencia y región.
    """
    df_filtered = df.drop_duplicates(subset=['NOM_RBD', 'COD_REG_RB', 'TIPO_DEPEN']).copy()

    df_grouped = df_filtered.groupby(['COD_REG_RB', 'TIPO_DEPEN'], observed=True).size().unstack(fill_value=0)
    df_porcentaje = df_grouped.div(df_grouped.sum(axis=1), axis=0) * 100

    # Mapear nombres
    df_porcentaje.index = df_porcentaje.index.map(regiones_dict)
    df_porcentaje.columns = df_porcentaje.columns.map(tipodepen_dict)

    # Reordenar de norte a sur (invertido para horizontal)
    df_porcentaje = df_porcentaje.reindex(index_order[::-1])

    return df_porcentaje.reset_index()

def preparar_dataset_ivm(df, regiones_dict, index_order, valor_corte = 20.03805):
    """
    Prepara el DataFrame con el porcentaje de establecimientos con IVM mayor o igual a un valor de corte por región.

    Parámetros:
    -----------
    df : pd.DataFrame
        Contiene columnas 'RBD', 'IVM_Establecimiento' y 'CODIGO_REGION_EGRESO'.
    regiones_dict : dict
        Diccionario para mapear código de región a nombre.
    index_order : list
        Lista ordenada de nombres de regiones.
    valor_corte : float
        Valor mínimo de IVM a considerar.

    Retorna:
    --------
    resultado : pd.DataFrame
        DataFrame con columnas 'Region_Nombre' y 'Porcentaje'.
    """
    df_filtrado = df.dropna(subset=['IVM_Establecimiento'])
    df_unico_rbd = df_filtrado.drop_duplicates(subset=['RBD'])

    filtro = df_unico_rbd[df_unico_rbd['IVM_Establecimiento'] >= valor_corte]

    conteo_filtrado = filtro.groupby('CODIGO_REGION_EGRESO').size().reset_index(name='Cumple_Condicion')
    conteo_total = df_unico_rbd.groupby('CODIGO_REGION_EGRESO').size().reset_index(name='Total_Observaciones')

    resultado = pd.merge(conteo_filtrado, conteo_total, on='CODIGO_REGION_EGRESO', how='right')
    resultado['Cumple_Condicion'] = resultado['Cumple_Condicion'].fillna(0)
    resultado['Porcentaje'] = (resultado['Cumple_Condicion'] / resultado['Total_Observaciones']) * 100

    resultado['Region_Nombre'] = resultado['CODIGO_REGION_EGRESO'].map(regiones_dict)
    resultado['Region_Nombre'] = pd.Categorical(resultado['Region_Nombre'], categories=index_order, ordered=True)
    resultado = resultado.sort_values('Region_Nombre')

    return resultado[['Region_Nombre', 'Porcentaje']]

def preparar_matriz_movilidad(df, index_order):
    """
    Prepara una matriz de movilidad entre regiones de origen y destino.

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con las columnas 'NOMBRE_REGION_EGRESO' y 'NOMBRE_REGION_INGRESO'.
    index_order : list
        Lista con el orden de las regiones de norte a sur.

    Retorna:
    --------
    matriz : pd.DataFrame
        Matriz de conteo entre regiones de origen y destino (reordenada).
    """
    matriz = pd.crosstab(
        df['NOMBRE_REGION_EGRESO'],
        df['NOMBRE_REGION_INGRESO']
    )

    matriz = matriz.reindex(index=index_order, columns=index_order, fill_value=0)
    return matriz

def preparar_tasas_migracion_recepcion(df, orden_regiones):
    """
    Calcula las tasas de migración y recepción por región.

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con columnas 'NOMBRE_REGION_EGRESO' y 'NOMBRE_REGION_INGRESO'.
    orden_regiones : list
        Lista con el orden de las regiones de norte a sur.

    Retorna:
    --------
    df_tasas : pd.DataFrame
        DataFrame con columnas 'Región', 'Tasa Migración (%)' y 'Tasa Recepción (%)'.
    """
    cols = ["NOMBRE_REGION_EGRESO", "NOMBRE_REGION_INGRESO"]
    df_migracion = df[cols].copy()

    total_egresados = df_migracion["NOMBRE_REGION_EGRESO"].value_counts()
    migrantes = df_migracion[df_migracion["NOMBRE_REGION_EGRESO"] != df_migracion["NOMBRE_REGION_INGRESO"]]["NOMBRE_REGION_EGRESO"].value_counts()
    tasa_migracion = (migrantes / total_egresados).fillna(0) * 100

    total_ingresados = df_migracion["NOMBRE_REGION_INGRESO"].value_counts()
    foraneos = df_migracion[df_migracion["NOMBRE_REGION_EGRESO"] != df_migracion["NOMBRE_REGION_INGRESO"]]["NOMBRE_REGION_INGRESO"].value_counts()
    tasa_recepcion = (foraneos / total_ingresados).fillna(0) * 100

    df_tasas = pd.DataFrame({
        "Tasa Migración (%)": tasa_migracion,
        "Tasa Recepción (%)": tasa_recepcion
    }).fillna(0).reset_index().rename(columns={'index': 'Región'})

    df_tasas['Región'] = pd.Categorical(df_tasas['Región'], categories=orden_regiones, ordered=True)
    df_tasas = df_tasas.sort_values('Región')

    return df_tasas

def haversine(lat1, lon1, lat2, lon2):
    """Calcula la distancia entre dos puntos geográficos."""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calcular_tasas_migracion(df):
    """Calcula tasas de migración y recepción por región."""
    df_migracion = df[['NOMBRE_REGION_EGRESO', 'NOMBRE_REGION_INGRESO']]

    total_egresados = df_migracion["NOMBRE_REGION_EGRESO"].value_counts()
    migrantes = df_migracion[df_migracion["NOMBRE_REGION_EGRESO"] != df_migracion["NOMBRE_REGION_INGRESO"]]["NOMBRE_REGION_EGRESO"].value_counts()
    tasa_migracion = (migrantes / total_egresados).fillna(0) * 100

    total_ingresados = df_migracion["NOMBRE_REGION_INGRESO"].value_counts()
    foraneos = df_migracion[df_migracion["NOMBRE_REGION_EGRESO"] != df_migracion["NOMBRE_REGION_INGRESO"]]["NOMBRE_REGION_INGRESO"].value_counts()
    tasa_recepcion = (foraneos / total_ingresados).fillna(0) * 100

    df_tasas = pd.DataFrame({
        "Tasa Migración (%)": tasa_migracion,
        "Tasa Recepción (%)": tasa_recepcion
    }).fillna(0).reset_index().rename(columns={'index': 'Región'})

    return df_tasas

def calcular_distancias(df):
    """Agrega columna DISTANCIA en base a Haversine y elimina filas NaN."""
    df['DISTANCIA'] = df.apply(
        lambda row: haversine(row['LATITUD_COL'], row['LONGITUD_COL'], row['LATITUD_UNI'], row['LONGITUD_UNI']),
        axis=1
    )
    df_filtrado = df.dropna(subset=['DISTANCIA'])
    #print(f"Cantidad de observaciones: {df_filtrado.shape[0]}")
    return df_filtrado


def calcular_distancias_promedio(df_distancias, df_tasas):
    """Calcula distancia promedio de migración y recepción por región."""
    df_resultado = df_tasas.copy()
    df_resultado['DISTANCIA_PROMEDIO_MIGRACIÓN'] = 0.0
    df_resultado['DISTANCIA_PROMEDIO_RECEPCIÓN'] = 0.0

    migracion_count = {region: 0 for region in df_resultado['Región']}
    recepcion_count = {region: 0 for region in df_resultado['Región']}

    for _, row in df_distancias.iterrows():
        egreso = row['NOMBRE_REGION_EGRESO']
        ingreso = row['NOMBRE_REGION_INGRESO']
        distancia = row['DISTANCIA']

        if egreso != ingreso:
            if egreso in migracion_count:
                df_resultado.loc[df_resultado['Región'] == egreso, 'DISTANCIA_PROMEDIO_MIGRACIÓN'] += distancia
                migracion_count[egreso] += 1
            if ingreso in recepcion_count:
                df_resultado.loc[df_resultado['Región'] == ingreso, 'DISTANCIA_PROMEDIO_RECEPCIÓN'] += distancia
                recepcion_count[ingreso] += 1

    df_resultado['DISTANCIA_PROMEDIO_MIGRACIÓN'] = df_resultado.apply(
        lambda row: row['DISTANCIA_PROMEDIO_MIGRACIÓN'] / max(migracion_count.get(row['Región'], 1), 1), axis=1
    )

    df_resultado['DISTANCIA_PROMEDIO_RECEPCIÓN'] = df_resultado.apply(
        lambda row: row['DISTANCIA_PROMEDIO_RECEPCIÓN'] / max(recepcion_count.get(row['Región'], 1), 1), axis=1
    )

    return df_resultado

# Gráficos para visualización
def plotly_tipo_universidad_por_region(df_porcentaje):
    """
    Gráfico de barras horizontales apiladas: tipos de universidad por región.
    """
    fig = go.Figure()

    for tipo in df_porcentaje.columns[1:]:
        fig.add_trace(go.Bar(
            y=df_porcentaje['region_sede'],
            x=df_porcentaje[tipo],
            name=tipo,
            orientation='h',
            text=df_porcentaje[tipo].round(1).astype(str) + '%',
            textposition='inside'
        ))

    fig.update_layout(
        barmode='stack',
        title='Porcentaje Tipo Universidad por Región',
        xaxis_title='Porcentaje',
        yaxis_title='Región',
        height=600,
        legend_title='Tipo de Universidad'
    )
    fig.update_yaxes(autorange='reversed')
    fig.update_traces(insidetextanchor='middle', textfont_size=11)
    return fig

def plotly_tipodepen_por_region(df_porcentaje):
    """
    Gráfico de barras horizontales apiladas: tipo de dependencia por región.
    """
    fig = go.Figure()

    for tipo in df_porcentaje.columns[1:]:
        fig.add_trace(go.Bar(
            y=df_porcentaje[df_porcentaje.columns[0]],
            x=df_porcentaje[tipo],
            name=tipo,
            orientation='h',
            text=df_porcentaje[tipo].round(1).astype(str) + '%',
            textposition='inside'
        ))

    fig.update_layout(
        barmode='stack',
        title='Porcentaje de TIPO_DEPEN para cada región',
        xaxis_title='Porcentaje (%)',
        yaxis_title='Región',
        height=700,
        legend_title='Tipo de Dependencia'
    )
    fig.update_yaxes(autorange='reversed')
    fig.update_traces(insidetextanchor='middle', textfont_size=10)
    return fig


def plotly_ivm_por_region(df_ivm, valor_corte = 20.03805):
    """
    Genera un gráfico de barras horizontales con Plotly para mostrar el porcentaje de IVM >= valor_corte por región.

    Parámetros:
    -----------
    df_ivm : pd.DataFrame
        DataFrame con columnas 'Region_Nombre' y 'Porcentaje'.
    valor_corte : float
        Valor mínimo de IVM para título del gráfico.
    """
    fig = px.bar(
        df_ivm,
        x='Porcentaje',
        y='Region_Nombre',
        orientation='h',
        text=df_ivm['Porcentaje'].round(2).astype(str) + '%',
        title=f'Porcentaje de Establecimientos con IVM ≥ {valor_corte} por Región',
        labels={'Region_Nombre': 'Región', 'Porcentaje': 'Porcentaje (%)'},
        color_discrete_sequence=['skyblue']
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(
        yaxis=dict(categoryorder='array', categoryarray=df_ivm['Region_Nombre'][::-1]),
        height=600,
        margin=dict(l=80, r=40, t=60, b=40)
    )

    return fig

def plotly_matriz_movilidad(matriz):
    """
    Genera un heatmap interactivo con Plotly usando log1p para la escala.

    Parámetros:
    -----------
    matriz : pd.DataFrame
        Matriz de conteo de estudiantes por región (output de preparar_matriz_movilidad).
    """
    matriz_log = np.log1p(matriz)  # Escala logarítmica suave
    fig = px.imshow(
        matriz_log,
        labels=dict(x="Región Destino Educación Superior", y="Región Origen Educación Media", color="log(1 + estudiantes)"),
        x=matriz.columns,
        y=matriz.index,
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        title="Mapa de Calor: Cantidad de Estudiantes por Región de Origen y Destino",
        xaxis_title="Destino",
        yaxis_title="Origen",
        height=700
    )
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(autorange="reversed")
    return fig

def plotly_tasas_migracion_recepcion(df_tasas):
    """
    Genera un gráfico de barras horizontales con Plotly para tasas de migración y recepción por región.

    Parámetros:
    -----------
    df_tasas : pd.DataFrame
        DataFrame con columnas 'Región', 'Tasa Migración (%)' y 'Tasa Recepción (%)'.
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=df_tasas['Región'],
        x=df_tasas['Tasa Migración (%)'],
        name='Tasa de Migración',
        orientation='h',
        marker_color='#1f78b4',
        text=df_tasas['Tasa Migración (%)'].round(1).astype(str) + '%',
        textposition='auto'
    ))

    fig.add_trace(go.Bar(
        y=df_tasas['Región'],
        x=df_tasas['Tasa Recepción (%)'],
        name='Tasa de Recepción',
        orientation='h',
        marker_color='#ff7f0e',
        text=df_tasas['Tasa Recepción (%)'].round(1).astype(str) + '%',
        textposition='auto'
    ))

    fig.update_layout(
        barmode='group',
        title='Tasas de Migración y Recepción por Región',
        xaxis_title='Tasa (%)',
        yaxis_title='Región',
        height=700,
        legend_title='Tipo de Tasa',
        margin=dict(l=100, r=40, t=60, b=40)
    )

    fig.update_yaxes(autorange="reversed")
    return fig

def plotly_migracion_vs_distancia(df):
    """
    Gráfico interactivo de tasa de migración vs distancia promedio de migración por región.
    """
    fig = px.scatter(
        df,
        x='DISTANCIA_PROMEDIO_MIGRACIÓN',
        y='Tasa Migración (%)',
        text='Región',
        color_discrete_sequence=['blue'],
        labels={
            'DISTANCIA_PROMEDIO_MIGRACIÓN': 'Distancia Promedio de Migración (km)',
            'Tasa Migración (%)': 'Tasa de Migración (%)'
        },
        title='Tasa de Migración vs Distancia Promedio de Migración (km)',
        width=800,
        height=500
    )

    fig.update_traces(textposition='top center', marker=dict(size=10, line=dict(width=1, color='black')))
    fig.update_layout(
        margin=dict(l=60, r=40, t=60, b=40)
    )
    return fig


def plotly_tasa_vs_distancia(df, col_x, col_y, titulo, color='blue'):
    """
    Gráfico interactivo genérico de tasa vs distancia usando Plotly.

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con las columnas para x e y y 'Región'.
    col_x : str
        Nombre de la columna del eje X (distancia).
    col_y : str
        Nombre de la columna del eje Y (tasa).
    titulo : str
        Título del gráfico.
    color : str
        Color de los puntos.
    """
    fig = px.scatter(
        df,
        x=col_x,
        y=col_y,
        text='Región',
        color_discrete_sequence=[color],
        labels={
            col_x: col_x.replace('_', ' '),
            col_y: col_y
        },
        title=titulo,
        width=800,
        height=500
    )

    fig.update_traces(textposition='top center', marker=dict(size=10, line=dict(width=1, color='black')))
    fig.update_layout(
        margin=dict(l=60, r=40, t=60, b=40)
    )
    return fig
    
