import pandas as pd
import geopandas as gpd
from pathlib import Path
import os
import re
import math

# Configuraciones generales
pd.set_option("display.max_columns", None)

# Diccionario de regiones unificado
region_dict = {
    'REGION DE ARICA Y PARINACOTA': 'Arica y Parinacota',
    'REGION DE TARAPACA': 'Tarapacá',
    'REGION DE ANTOFAGASTA': 'Antofagasta',
    'REGION DE ATACAMA': 'Atacama',
    'REGION DE COQUIMBO': 'Coquimbo',
    'REGION DE VALPARAISO': 'Valparaíso',
    "REGION DEL LIBERTADOR GENERAL BERNARDO O'HIGGINS": "Lib. Gral B. O'Higgins",
    'REGION DEL MAULE': 'Maule',
    'REGION DE ÑUBLE': 'Ñuble',
    'REGION DEL BIOBIO': 'Biobío',
    'REGION DE LA ARAUCANIA': 'La Araucanía',
    'REGION DE LOS RIOS': 'Los Ríos',
    'REGION DE LOS LAGOS': 'Los Lagos',
    'REGION AISEN DEL GENERAL CARLOS IBAÑEZ DEL CAMPO': 'Aysén',
    'REGION DE MAGALLANES Y DE LA ANTARTICA CHILENA': 'Magallanes',
    'REGION METROPOLITANA DE SANTIAGO': 'Metropolitana',
    'REGIÓN DE ARICA Y PARINACOTA': 'Arica y Parinacota',
    'REGIÓN DE TARAPACÁ': 'Tarapacá',
    'REGIÓN DE ANTOFAGASTA': 'Antofagasta',
    'REGIÓN DE ATACAMA': 'Atacama',
    'REGIÓN DE COQUIMBO': 'Coquimbo',
    'REGIÓN DE VALPARAÍSO': 'Valparaíso',
    'REGIÓN DEL LIBERTADOR GRAL. BERNARDO O\'HIGGINS': "Lib. Gral B. O'Higgins",
    'REGIÓN DEL MAULE': 'Maule',
    'REGIÓN DE ÑUBLE': 'Ñuble',
    'REGIÓN DEL BIOBÍO': 'Biobío',
    'REGIÓN DE LA ARAUCANÍA': 'La Araucanía',
    'REGIÓN DE LOS RÍOS': 'Los Ríos',
    'REGIÓN DE LOS LAGOS': 'Los Lagos',
    'REGIÓN DE AYSÉN DEL GRAL. CARLOS IBÁÑEZ DEL CAMPO': 'Aysén',
    'REGIÓN DE MAGALLANES Y DE LA ANTÁRTICA CHILENA': 'Magallanes',
    'REGIÓN METROPOLITANA DE SANTIAGO': 'Metropolitana'
}

# Orden de regiones para visualización
orden_regiones = [
    'Arica y Parinacota', 'Tarapacá', 'Antofagasta', 'Atacama', 'Coquimbo',
    'Valparaíso', 'Metropolitana', "Lib. Gral B. O'Higgins", 'Maule', 'Ñuble',
    'Biobío', 'La Araucanía', 'Los Ríos', 'Los Lagos', 'Aysén', 'Magallanes'
]

# Diccionario para nombres de TIPO_DEPEN
tipodepen_dict = {
    1: 'Municipal',
    2: 'Particular Subvencionado',
    3: 'Particular Pagado',
    4: 'Corp. Administración Delegada',
    5: 'Servicio Local de Educación'
}

# Mapear códigos de región para set_C
regiones_dict_inv = {
    15: 'Arica y Parinacota',
    1: 'Tarapacá',
    2: 'Antofagasta',
    3: 'Atacama',
    4: 'Coquimbo',
    5: 'Valparaíso',
    6: 'Metropolitana',
    7: "Lib. Gral B. O'Higgins",
    8: 'Maule',
    16: 'Ñuble',
    9: 'Biobío',
    10: 'La Araucanía',
    11: 'Los Ríos',
    12: 'Los Lagos',
    13: 'Aysén',
    14: 'Magallanes'
}

def obtener_paths_anio(path_base: Path, anio: int) -> dict:
    path_anio = path_base / str(anio)

    path_matricula = path_anio / f'20230802_Matrícula_Ed_Superior_{anio}_PUBL_MRUN.csv'
    path_puntajes = (
        path_anio / f'A_INSCRITOS_PUNTAJES_PDT_{anio}_PUB_MRUN.csv'
        if anio in [2021, 2022]
        else path_anio / f'A_INSCRITOS_PUNTAJES_{anio}_PAES_PUB_MRUN.csv'
    )
    path_ivm = path_anio / f'IVM_Establecimientos_{anio}.xlsx'

    # Paths fijos para shapefiles
    path_establecimientos = path_anio / 'establecimientos' / 'layer_establecimientos_educacion_escolar_20220309024120.shp'
    path_inmuebles = path_anio / 'inmuebles_ies' / 'layer_establecimientos_de_educacion_superior_20220309024111.shp'

    return {
        "matricula": path_matricula,
        "puntajes": path_puntajes,
        "ivm": path_ivm,
        "establecimientos": path_establecimientos,
        "inmuebles_ies": path_inmuebles
    }

def leer_conjunto_a_desde_path(path_set_A: Path, region_dict: dict) -> tuple:
    """
    Lee y transforma el set A desde un path específico.

    Parámetros:
    ----------
    path_set_A : Path
        Ruta al archivo CSV.
    region_dict : dict
        Diccionario para estandarizar nombres de región.

    Retorna:
    -------
    tuple
        DataFrame procesado y año extraído desde el nombre del archivo.
    """

    columnas_clave = [
        "mrun", "region_sede", "provincia_sede", "comuna_sede","cod_inst",
        "nomb_inst", "nomb_carrera", "tipo_inst_1","tipo_inst_2","tipo_inst_3",
        "nivel_global", "nivel_carrera_1", "anio_ing_carr_act", "anio_ing_carr_ori",
        "forma_ingreso", "rango_edad"
    ]

    df = pd.read_csv(path_set_A, sep=';', encoding='utf-8', usecols=columnas_clave)
    df['NOMBRE_REGION_INGRESO'] = df['region_sede'].replace(region_dict)

    return df


def generar_conjuntos_filtrados(df: pd.DataFrame, year_A: int) -> dict:
    """
    Genera subconjuntos filtrados desde un DataFrame base.

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame base.
    year_A : int
        Año de ingreso a utilizar en los filtros.

    Retorna:
    -------
    dict
        Conjuntos filtrados por nombre.
    """
    filtros_a = {
        "A0": {
            "anio_ing_carr_ori": year_A,
            "nivel_global": "Pregrado",
            "forma_ingreso": "1- Ingreso Directo (regular)"
        },
        "A": {
            "anio_ing_carr_ori": year_A,
            "nivel_global": "Pregrado",
            "forma_ingreso": "1- Ingreso Directo (regular)",
            "rango_edad": "15 a 19 años"
        },
        "A1": {
            "anio_ing_carr_ori": year_A,
            "nivel_global": "Pregrado",
            "forma_ingreso": "1- Ingreso Directo (regular)",
            "rango_edad": "15 a 19 años",
            "tipo_inst_1": "Universidades"
        }
    }

    def aplicar_filtro(df, condiciones):
        for columna, valor in condiciones.items():
            df = df[df[columna] == valor]
        return df

    resultados_filtrados = {
        nombre: aplicar_filtro(df, condiciones)
        for nombre, condiciones in filtros_a.items()
    }

    return resultados_filtrados


def leer_conjunto_b_desde_path(path_set_B: Path, region_dict: dict) -> tuple:
    """
    Lee y transforma el set B desde un path específico.

    Parámetros:
    ----------
    path_set_B : Path
        Ruta al archivo CSV.
    region_dict : dict
        Diccionario para estandarizar nombres de región.

    Retorna:
    -------
    tuple
        DataFrame procesado y año extraído desde el nombre del archivo.
    """
    year_B = int(re.search(r'_(\d{4})_', str(path_set_B)).group(1))

    columnas_B = [
        "MRUN", "RBD", "CODIGO_REGION_EGRESO", "NOMBRE_REGION_EGRESO",
        "PTJE_RANKING", "PTJE_NEM"
    ] + ["PROM_CM_ACTUAL" if year_B < 2023 else "PROMEDIO_CM_MAX"]

    df = pd.read_csv(
        path_set_B,
        sep=';',
        encoding='utf-8',
        dtype={'RBD': str, 'NOMBRE_REGION_EGRESO': str},
        usecols=columnas_B
    ).rename(columns={'MRUN': 'mrun', 'PROMEDIO_CM_MAX': 'PROM_CM_ACTUAL'})

    df['NOMBRE_REGION_EGRESO'] = df['NOMBRE_REGION_EGRESO'].replace(region_dict)
    df['RBD'] = pd.to_numeric(df['RBD'], errors='coerce').dropna().astype(int)

    return df


def leer_conjunto_c_desde_path(path_set_C: Path) -> gpd.GeoDataFrame:
    """
    Lee y transforma el set C (establecimientos escolares) desde un archivo shapefile.

    Parámetros:
    ----------
    path_set_C : Path
        Ruta al archivo `.shp`.

    Retorna:
    -------
    GeoDataFrame
        GeoDataFrame con las columnas procesadas.
    """
    columnas_C = ["RBD", "NOM_RBD", "COD_REG_RB", "TIPO_DEPEN", "LATITUD", "LONGITUD"]

    df = gpd.read_file(path_set_C)[columnas_C].rename(
        columns={'LATITUD': 'LATITUD_COL', 'LONGITUD': 'LONGITUD_COL'}
    )

    df['RBD'] = pd.to_numeric(df['RBD'], errors='coerce').dropna().astype(int)
    df['COD_REG_RB'] = pd.to_numeric(df['COD_REG_RB'], errors='coerce')

    return df


def leer_conjunto_d_desde_path(path_set_D: Path, region_dict: dict) -> gpd.GeoDataFrame:
    """
    Lee y transforma el set D (inmuebles de educación superior) desde un archivo shapefile.

    Parámetros:
    ----------
    path_set_D : Path
        Ruta al archivo `.shp`.
    region_dict : dict
        Diccionario de estandarización de regiones.

    Retorna:
    -------
    GeoDataFrame
        GeoDataFrame procesado.
    """
    columnas_D = ["NOMBRE_INS", "REGIÓN", "COMUNA", "LATITUD", "LONGITUD", "TIPO_INST"]

    df = gpd.read_file(path_set_D)[columnas_D].rename(
        columns={'LATITUD': 'LATITUD_UNI', 'LONGITUD': 'LONGITUD_UNI'}
    )

    df['TIPO_INST'] = df['TIPO_INST'].str.capitalize()
    df['REGIÓN'] = df['REGIÓN'].replace(region_dict)

    df = df.drop_duplicates(subset=['NOMBRE_INS', 'REGIÓN', 'COMUNA'], keep='first')

    return df


def leer_conjunto_e_desde_path(path_set_E: Path) -> pd.DataFrame:
    """
    Lee y transforma el set E (IVM) desde un archivo Excel.

    Parámetros:
    ----------
    path_set_E : Path
        Ruta al archivo `.xlsx`.

    Retorna:
    -------
    pd.DataFrame
        DataFrame procesado con columnas agrupadas y valor de corte por año.
    """
    # Extraer año del nombre del archivo
    year_E = int(re.search(r'Establecimientos_(\d{4})', str(path_set_E)).group(1))

    # Leer hoja "Media"
    df = pd.read_excel(path_set_E, sheet_name='Media')

    # Calcular IVM_Establecimiento antes del groupby si es necesario
    if "IVM Establecimiento" not in df.columns and "IVM Ponderado" in df.columns:
        df["IVM Establecimiento"] = df["IVM Ponderado"]

    # Agrupar
    df = (
        df.groupby("ID_RBD", as_index=False)
        .agg({
            "N EVALUADO": "sum",
            "IVM Bajo": "sum",
            "IVM Medio": "sum",
            "IVM Alto": "sum",
            "IVM Muy Alto": "sum",
            "IVM Establecimiento": lambda x: (x * df.loc[x.index, "N EVALUADO"]).sum() / df.loc[x.index, "N EVALUADO"].sum()
        })
    )

    # Definir alta vulnerabilidad por año
    filtros_e = {
        2020: 21.42601,
        2021: 20.03805,
        2022: 20.03805,
        2023: 18.33834,
        2024: 19.35458
    }

    df['valor_corte'] = filtros_e.get(year_E, None)
    df.rename(columns={"IVM Establecimiento": "IVM_Establecimiento"}, inplace=True)

    return df



def fill_university_coordinates(df, universities_db):
    """
    Llena coordenadas de universidades faltantes usando matching jerárquico.
    """

    na_rows = df[df['LATITUD_UNI'].isna()]
    if na_rows.empty:
        print("No hay valores NA en las coordenadas universitarias")
        return df

    print(f"\nFilling coordinates for {len(na_rows)} missing entries...")
    fill_count = 0

    for index, row in na_rows.iterrows():
        match = universities_db[
            (universities_db['NOMBRE_INS'] == row['nomb_inst']) &
            (universities_db['REGIÓN'] == row['NOMBRE_REGION_INGRESO']) &
            (universities_db['COMUNA'] == row['comuna_sede'])
        ]

        if match.empty:
            match = universities_db[
                (universities_db['NOMBRE_INS'] == row['nomb_inst']) &
                (universities_db['REGIÓN'] == row['NOMBRE_REGION_INGRESO'])
            ]

        if match.empty:
            match = universities_db[
                (universities_db['NOMBRE_INS'] == row['nomb_inst']) &
                (universities_db['COMUNA'] == row['comuna_sede'])
            ]

        if match.empty:
            match = universities_db[
                (universities_db['REGIÓN'] == row['NOMBRE_REGION_INGRESO']) &
                (universities_db['COMUNA'] == row['comuna_sede'])
            ]

        if not match.empty:
            df.at[index, 'LATITUD_UNI'] = match['LATITUD'].iloc[0]
            df.at[index, 'LONGITUD_UNI'] = match['LONGITUD'].iloc[0]
            fill_count += 1

    print(f"Successfully filled {fill_count} missing coordinates")
    print(f"Remaining NA values: {df['LATITUD_UNI'].isna().sum()}")
    return df


def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia Haversine entre dos puntos.
    """
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371.0 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def generar_conjuntos_abcde(set_a: pd.DataFrame,
                             set_b: pd.DataFrame,
                             set_c: pd.DataFrame,
                             set_d: pd.DataFrame,
                             set_e: pd.DataFrame,
                             output_path: str) -> None:
    """
    Junta y guarda los conjuntos AB, ABC, ABCD y ABCDE.
    """

    os.makedirs(output_path, exist_ok=True)

    # AB
    set_ab = pd.merge(set_b, set_a, on="mrun", how="inner").loc[lambda x: x['NOMBRE_REGION_EGRESO'] != ' ']

    # ABC
    set_abc = pd.merge(set_ab, set_c, on='RBD', how='inner')

    # ABCD
    set_abcd = pd.merge(
        set_abc.rename(columns={'LATITUD': 'LATITUD_COL', 'LONGITUD': 'LONGITUD_COL'}),
        set_d.rename(columns={'LATITUD': 'LATITUD_UNI', 'LONGITUD': 'LONGITUD_UNI'}),
        left_on=['nomb_inst', 'NOMBRE_REGION_INGRESO', 'comuna_sede'],
        right_on=['NOMBRE_INS', 'REGIÓN', 'COMUNA'],
        how='left'
    )

    set_abcd2 = fill_university_coordinates(
        set_abcd,
        set_d.rename(columns={'LATITUD_UNI': 'LATITUD', 'LONGITUD_UNI': 'LONGITUD'})
    )

    # ABCDE
    set_abcde = pd.merge(set_abcd2, set_e, left_on='RBD', right_on='ID_RBD', how='left')

    valor_corte = set_e['valor_corte'].iloc[0]
    set_abcde.loc[
        (set_abcde["IVM_Establecimiento"].isnull()) & (set_abcde["TIPO_DEPEN"] == 3),
        "IVM_Establecimiento"
    ] = valor_corte - 1

    set_abcde['DISTANCIA'] = set_abcde.apply(
        lambda row: haversine(row['LATITUD_COL'], row['LONGITUD_COL'], row['LATITUD_UNI'], row['LONGITUD_UNI']),
        axis=1
    )

    print(f"Cantidad de observaciones: {set_abcde.shape[0]}")

    set_ab.to_csv(f"{output_path}/set_ab.csv", index=False)
    set_abc.to_csv(f"{output_path}/set_abc.csv", index=False)
    set_abcd.to_csv(f"{output_path}/set_abcd.csv", index=False)
    set_abcde.to_csv(f"{output_path}/set_abcde.csv", index=False)
