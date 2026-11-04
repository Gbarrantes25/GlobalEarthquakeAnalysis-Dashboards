import marimo

__generated_with = "0.25.2"
app = marimo.App(
    width="full",
    app_title="Análisis de Sismos Globales 1970 - 2026",
)


@app.cell(hide_code=True)
def _():
    import pandas as pd
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go

    @mo.persistent_cache
    def crear_df():
        dfx = pd.read_parquet(r"C:\Users\Gian\Downloads\df_sismos.parquet")
        dfx["lustro"] = (dfx["year"] // 5) * 5
        dfx = dfx.loc[dfx["Mw"] >= 5]
        dfx1 = dfx.dropna(subset=["depth"])
        dfx1["place"] = dfx1["place"].fillna("Sin registro")

        return dfx1

    df_limpio = crear_df()
    return df_limpio, go, mo, np


@app.cell(hide_code=True)
def _(mo, render_detallado, render_home, render_vistageneral):
    _router = mo.routes(
        {
            "#/": render_home,
            "#/vista_general": render_vistageneral,
            "#/analisis_detallado": render_detallado,
            mo.routes.CATCH_ALL: render_home,
        }
    )

    nav = mo.nav_menu(
        {
            "#/": "🏠 Inicio",
            "#/vista_general": "📊 Vista General",
            "#/analisis_detallado": "🔍 Análisis Detallado",
        }
    )

    mo.vstack([nav, _router])
    return


@app.cell
def _(
    carga_etl_home,
    codigo_etl_home,
    detallado1,
    detallado2,
    detallado3,
    detallado4,
    detallado5,
    detallado6,
    df_limpio,
    mo,
    objetivos_home,
    tablacontenido_home,
    titulo_home,
    vista_general,
):
    def render_home():
        return mo.vstack(
            [
                titulo_home,
                tablacontenido_home,
                objetivos_home,
                carga_etl_home,
                codigo_etl_home,
                df_limpio.head(5),
            ]
        )

    def render_vistageneral():
        resultado = vista_general
        return resultado

    def render_detallado():
        return mo.vstack(
            [
                detallado1,
                detallado2,
                detallado3,
                detallado4,
                detallado5,
                detallado6,
            ]
        )

    return render_detallado, render_home, render_vistageneral


@app.cell
def _(mo):
    titulo_home = mo.md("# Análisis de sismos globales 1970 - 2026")

    tablacontenido_home = mo.md(
        """
        ## Tabla de contenido
        <ol>
            <li>Objetivos del proyecto.</li>
            <li>Carga, limpieza y transfornamción de datos.</li>
            <li>Gráficos:</li>
                <ul>
                    <li>Vista General: Mapa de Sismos</li>
                    <li>Vista General: Mapa de Profundidad Sísmica</li>
                    <li>Análisis Detallado: Distribución y Variación de Magnitud Sísmica Anual</li>
                    <li>Análisis Detallado: Distribución de la Frecuencia y Magnitud Sísmica Mensual</li>
                    <li>Análisis Detallado: Distribución Sísmica según rango de Magnitud</li>
                    <li>Análisis Detallado: Distribución Sísmica según rango de Profundidad</li>
                    <li>Análisis Detallado: Evolución Anual de Eventos según rango de Magnitud</li>
                    <li>Análisis Detallado: Evolución Anual Acumulada de Eventos según rango de Magnitud</li>
                    <li>Análisis Detallado: Top 10 de Regiones con Sismos fuertes</li>
                    <li>Análisis Detallado: Top 10 de Países con Sismos fuertes</li>
                    <li>Análisis Detallado: Profundidad vs Magnitud Sísmica</li>
                    <li>Análisis Detallado: Top 10 Sismos más devastadores de la historia: 1970 - actualidad</li>
                </ul>
        </ol>
        """
    )
    objetivos_home = mo.md(
        """
        ## 1. Objetivos del proyecto:
        El objetivo de este proyecto es analizar la magnitud de momento y la profundidad de los sismos superiores o iguales a 5 Mw en todo el planeta desde 1970 hasta la actualidad.
        Para ello se descargó la base de datos de Kaggle 'Earthquakes_USGS_with_countries' y luego se realizó un proceso ETL limpiando y aligerando su peso (de 1.7 GB a 17.7 MB).
        Ahora lo que se busca es responder las siguientes preguntas de manera gráfica usando la librería plotly:
        <ul>
            <li>¿Dónde y con qué magnitud (Mw) y profundidad (Km) se distribuyeron los sismos a nivel mundial?</li>
            <li>¿Cómo se distribuyó y varió la magnitud de los sismos (Mw) año tras año? ¿Cuál es la distribución de la frecuencia de la profundidad y magnitud de los sismos por año/mes?</li>
            <li>¿Cuál es la frecuencia sísmica según su rango de magnitud (Mw) y Profundidad (Km) por región y país?</li>
            <li>¿Cuál es la Evolución anual de la frecuencia y acumulado de sismos registrados (Magnitud 5.0 - 10.0)?</li>
            <li>¿Cuál es la frecuencia según su rango de profundidad (Km) por región y país?</li>
            <li>¿Cuál es la Evolución anual de la frecuencia y acumulado de sismos registrados (Magnitud 5.0 - 10.0)?</li>
            <li>¿Cuáles son las regiones y países con sismos más fuertes? (>= 7 Mw)</li>
            <li>¿Cuál es la relación entre la profundidad y la magnitud de los sismos?</li>
            <li>¿Cuáles son los 10 sismos de mayor magnitud en la historia según el USGS?</li>
        </ul>
        """
    )

    carga_etl_home = mo.md(
        """
        ## 2. Carga, limpieza y transformación de datos.
        A continuación detallaré el flujo ETL aplicado a los datos globales de sismos Kaggle:
        <ul>
            <li>Carga de información desde ruta local (datos descargados en formato .csv 1.7GB</li>
            <li>Primera transformación:</li>
            <ul>
                <li>Conversión de toda la columna "status" a minúsculas</li>
                <li>Conversión de la columna "time" a tipo de dato datetime en formato mixto</li>
                <li>Filtrado de tabla por la columna "type_property" por "earthquake": esto ayuda a obtener los movimientos sísmicos de la tierra y no por explosiones u otros.</li>
                <li>Filtrado de tabla por la columna "status" por "reviewed", seleccionando las columnas necesarias.</li>
                <li>Filtrado de tabla por la columna "time" para que muestre los años desde 1970 en adelante.</li>
                <li>Quitamos espacios alrededor de los valores de la columna "magType".</li>
                <li>Creación de la columna "year".</li>
                <li>Creación de la columna "decade".</li>
            </ul>
            <li>Conversión a Magnitud de Momento (Mw):</li>
                <ul>
                    <li>Condición 1: Si "magType" = "mb" y "mag" <= 6.2, entonces Mw = 0.85 x "mag" + 1.03</li>
                    <li>Condición 2: Si "magType = ["mww", "mwc", "mwb", "mwr", "mwp", "mw"], entonces Mw = "mag"</li>
                    <li>Condición 3: Si "magType" = ["ms", "ms_20"] y ("mag" >= 3 y "mag" < 6.2), entonces Mw = 0.67 x "mag" + 2.07</li>
                    <li>Condición 4: Si "magType" = ["ms", "ms_20"] y ("mag" >= 6.2 y "mag" <= 8.2), entonces Mw = 0.99 x "mag" + 0.08</li>
                    <li>Condición 5: Si "magType" = ["ml", "Ml", "ml(texnet)"] y "mag" <= 6.5, entonces Mw = 0.722 x "mag" + 0.743</li>
                    <li>Condición 6: Si "magType" = ["md", "Md"] y "mag" <= 6.8, entonces Mw =  0.9879 x "mag" + 0.3316</li>
                    <li>Condición 7: Cualquier otra condición deberá devolver un valor NaN</li>
                </ul>
                <li>Retiramos todos los valores NaN de la columna "Mw" con un filtro a la tabla (Esos NaN representan menos del 1% de registros).</li>
                <li>Filtramos los valores >= 5.0 de la columna "Mw".</li>
                <li>Convertimos las columnas ["magType","status","country_name","region","continent"] a tipo "category".</li>
                <li>Elimino las columnas que no necesitaremos como "magType" y "status".</li>
                <li>Exportamos la tabla a formato .parquet.</li>
            </ul>
        """
    )

    codigo_etl_home = mo.accordion(
        {
            "Ver código": mo.md(
                r"""
        ```python
        @mo.cache
        def crear_df():
            dfx = pd.read_csv(r"C:\Users\Gian\Downloads\Earthquakes_USGS_with_countries.csv")
            dfx["status"] = dfx["status"].str.lower()
            dfx["time"] = pd.to_datetime(dfx["time"], format="mixed")
            dfx = dfx.loc[dfx["type_property"] == "earthquake"]
            columnas = [
                "id",
                "time",
                "latitude",
                "longitude",
                "depth",
                "mag",
                "magType",
                "status",
                "place",
                "country_name",
                "region",
                "continent",
            ]
            dfx = dfx.loc[dfx["status"] == "reviewed", columnas]
            dfx = dfx.loc[(dfx["time"].dt.year >= 1970)].reset_index(drop=True)
            dfx["magType"] = dfx["magType"].str.strip()
            dfx["year"] = dfx["time"].dt.year
            dfx["decade"] = (dfx["time"].dt.year // 10) * 10

            return dfx

        df = crear_df()



        condiciones = [
            ((df["magType"] == "mb") & (df["mag"] <= 6.2)),
            (df["magType"].isin(["mww", "mwc", "mwb", "mwr", "mwp", "mw"])),
            (df["magType"].isin(["ms", "ms_20"])& ((df["mag"] >= 3) & (df["mag"] < 6.2))),
            (df["magType"].isin(["ms", "ms_20"])& ((df["mag"] >= 6.2) & (df["mag"] <= 8.2))),
            ((df["magType"].isin(["ml", "Ml", "ml(texnet)"])) & (df["mag"] <= 6.5)),
            ((df["magType"].isin(["md", "Md"])) & (df["mag"] <= 6.8)),
        ]

        resultado = [
            0.85 * df["mag"] + 1.03,
            df["mag"],
            0.67 * df["mag"] + 2.07,
            0.99 * df["mag"] + 0.08,
            0.722 * df["mag"] + 0.743,
            0.9879 * df["mag"] + 0.3316,
        ]

        df["Mw"] = np.select(condiciones, resultado, default=np.nan).round(1)
        df_limpio = df.loc[df["Mw"].notnull()]
        df_limpio = df_limpio[(df_limpio["Mw"] >= 4.5)].reset_index(drop=True)

        columnas_categorias = [
            "magType",
            "status",
            "country_name",
            "region",
            "continent",
        ]
        df_limpio[columnas_categorias] = df_limpio[columnas_categorias].astype("category")

        df_limpio = df_limpio.drop(columns=["magType", "status"])

        df_limpio.to_parquet(r"C:\Users\Gian\Downloads\df_sismos.parquet")
        ```
        """
            )
        }
    )
    titulo_vistageneral = mo.md(
        "### ¿Dónde y con qué magnitud (Mw) y profundidad (Km) se distribuyeron los sismos a nivel mundial?"
    )
    titulo_detallado = mo.md(
        "### ¿Cómo se distribuyó y varió la magnitud de los sismos (Mw) año tras año? ¿Cuál es la distribución de la frecuencia de la profundidad y magnitud de los sismos por año/mes?"
    )
    titulo_detallado2 = mo.md(
        "### ¿Cuál es la frecuencia sísmica según su rango de magnitud (Mw) y Profundidad (Km) por región y país??"
    )
    titulo_detallado3 = mo.md(
        "### ¿Cuál es la Evolución anual de la frecuencia y acumulado de sismos registrados (Magnitud 5.0 - 10.0)?"
    )
    titulo_detallado4 = mo.md(
        "### ¿Cuál es la relación entre la profundidad y la magnitud de los sismos?"
    )
    titulo_detallado5 = mo.md(
        "### ¿Cuáles son los 10 sismos de mayor magnitud en la historia según el USGS?"
    )
    titulo_detallado6 = mo.md(
        "### ¿Cuáles son las regiones y países con sismos más fuertes? (>= 7 Mw)"
    )
    return (
        carga_etl_home,
        codigo_etl_home,
        objetivos_home,
        tablacontenido_home,
        titulo_detallado,
        titulo_detallado2,
        titulo_detallado3,
        titulo_detallado4,
        titulo_detallado5,
        titulo_detallado6,
        titulo_home,
        titulo_vistageneral,
    )


@app.cell
def _(df_limpio, mo):
    lustro_opciones = df_limpio["lustro"].unique().tolist()
    selector_lustro = mo.ui.dropdown(
        options=lustro_opciones,
        value=lustro_opciones[0],
        label="Lustro",
    )
    selector_lustro2 = mo.ui.dropdown(
        options=lustro_opciones, value=lustro_opciones[0], label="Lustro"
    )
    selector_lustro3 = mo.ui.dropdown(
        options=lustro_opciones, value=lustro_opciones[0], label="Lustro"
    )
    selector_lustro4 = mo.ui.dropdown(
        options=lustro_opciones, value=lustro_opciones[0], label="Lustro"
    )
    selector_lustro5 = mo.ui.dropdown(
        options=lustro_opciones, value=lustro_opciones[0], label="Lustro"
    )
    rango_magnitud = mo.ui.range_slider(
        start=5,
        stop=10,
        label="Magnitud de Momento (Mw)",
        full_width=True,
        value=[5, 10],
    )
    return (
        rango_magnitud,
        selector_lustro,
        selector_lustro2,
        selector_lustro3,
        selector_lustro4,
        selector_lustro5,
    )


@app.cell
def _(df_limpio, mo, selector_lustro3):
    region_opciones = (
        df_limpio.loc[df_limpio["lustro"] == selector_lustro3.value, "region"]
        .unique()
        .sort_values()
        .tolist()
    )
    selector_region = mo.ui.dropdown(
        options=region_opciones,
        value=region_opciones[0],
        label="Región",
        searchable=True,
    )
    return (selector_region,)


@app.cell
def _(df_limpio, mo, selector_lustro3, selector_region):
    paises_opciones = (
        df_limpio.loc[
            (df_limpio["lustro"] == selector_lustro3.value)
            & (df_limpio["region"] == selector_region.value),
            "country_name",
        ]
        .reset_index(drop=True)
        .sort_values()
        .unique()
        .tolist()
    )
    selector_paises = mo.ui.multiselect(
        options=paises_opciones, value=paises_opciones, label="Paises"
    )
    return (selector_paises,)


@app.cell
def _(df_limpio, mo, selector_lustro5):
    continente_opciones = (
        df_limpio.loc[
            df_limpio["lustro"] == selector_lustro5.value, "continent"
        ]
        .unique()
        .sort_values()
        .tolist()
    )
    selector_continente = mo.ui.radio(
        options=continente_opciones,
        value=continente_opciones[0],
        label="Continente:",
        inline=True,
    )
    return (selector_continente,)


@app.cell
def _(df_limpio, go, mo, np, selector_lustro, titulo_vistageneral):
    # Vista General: Mapa de magnitud y Mapa de profundidad

    # Dataframes
    def crear_df_panel(selector):
        dfx = df_limpio.loc[
            df_limpio["lustro"] == selector, ["id", "depth", "Mw", "lustro"]
        ].reset_index(drop=True)
        return dfx

    df_panel_actual = crear_df_panel(selector_lustro.value)
    df_panel_anterior = crear_df_panel((selector_lustro.value) - 5)

    def crear_df_mw_lustro(selector):
        dfx = df_limpio.loc[
            df_limpio["lustro"] == selector,
            [
                "id",
                "time",
                "latitude",
                "longitude",
                "country_name",
                "Mw",
                "lustro",
            ],
        ]
        return dfx

    df_mw_lustro = crear_df_mw_lustro(selector_lustro.value)

    def crear_df_depth_lustro(selector):
        dfx = df_limpio.loc[
            df_limpio["lustro"] == selector,
            [
                "id",
                "time",
                "latitude",
                "longitude",
                "country_name",
                "depth",
                "lustro",
                "year",
            ],
        ]
        return dfx

    df_depth_lustro = crear_df_depth_lustro(selector_lustro.value)

    # Paneles
    def crear_tarjetas():
        conteo_sismos_actual = (
            len(np.unique(df_panel_actual["id"]))
            if not df_panel_actual.empty
            else 0
        )
        conteo_sismos_anterior = (
            len(np.unique(df_panel_anterior["id"]))
            if not df_panel_anterior.empty
            else 0
        )

        if not df_panel_actual.empty:
            media_mw_actual = round(np.median(df_panel_actual["Mw"]), 1)
            max_mw_actual = round(np.max(df_panel_actual["Mw"]), 1)
            media_depth_actual = round(np.median(df_panel_actual["depth"]), 1)
            min_depth_actual = round(np.min(df_panel_actual["depth"]), 1)
        else:
            media_mw_actual = max_mw_actual = media_depth_actual = (
                min_depth_actual
            ) = 0

        if not df_panel_anterior.empty:
            media_mw_anterior = round(np.median(df_panel_anterior["Mw"]), 1)
            max_mw_anterior = round(np.max(df_panel_anterior["Mw"]), 1)
            media_depth_anterior = round(
                np.median(df_panel_anterior["depth"]), 1
            )
            min_depth_anterior = round(np.min(df_panel_anterior["depth"]), 1)
        else:
            media_mw_anterior = max_mw_anterior = media_depth_anterior = (
                min_depth_anterior
            ) = 0

        pct_sismos = (
            round((conteo_sismos_actual / conteo_sismos_anterior - 1) * 100, 1)
            if conteo_sismos_anterior
            else " - "
        )
        pct_media_mw = (
            round((media_mw_actual / media_mw_anterior - 1) * 100, 2)
            if media_mw_anterior
            else " - "
        )
        pct_max_mw = (
            round((max_mw_actual / max_mw_anterior - 1) * 100, 2)
            if max_mw_anterior
            else " - "
        )

        img = mo.image(
            src="D:/Imágenes/Logo de consultoría/VectorLogo2.svg",
            height=150,
            rounded=True,
            vmin=50,
        )
        sismos = mo.stat(
            value=conteo_sismos_actual,
            bordered=True,
            label="🌎 Total Sismos",
            caption=f"vs {conteo_sismos_anterior} | {pct_sismos}%",
        )
        mw_media = mo.stat(
            value=f"{media_mw_actual} Mw",
            bordered=True,
            label="📏 Mag. Media",
            caption=f"vs {media_mw_anterior} Mw | {pct_media_mw}%",
        )

        mw_max = mo.stat(
            value=f"{max_mw_actual} Mw",
            bordered=True,
            label="➕ Mag. Máx.",
            caption=f"vs {max_mw_anterior} Mw | {pct_max_mw}%",
        )

        depth_media = mo.stat(
            value=f"{media_depth_actual} Km",
            bordered=True,
            label="⛏ Prof. Media",
            caption=f"vs {media_depth_anterior} Km",
        )

        depth_min = mo.stat(
            value=f"{min_depth_actual} Km",
            bordered=True,
            label="➖ Prof. Mín.",
            caption=f"vs {min_depth_anterior} Km",
        )

        header = mo.hstack(
            [
                img,
                selector_lustro,
                sismos,
                mw_media,
                mw_max,
                depth_media,
                depth_min,
            ],
            widths=[0.15, 0.10, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15],
            justify="center",
            align="center",
            wrap=True,
        )
        return header

    panel = crear_tarjetas()

    # Gráficos de mapa
    def crear_mapa_mw_lustro():
        lat = df_mw_lustro["latitude"].to_numpy().round(2).astype("float32")
        lon = df_mw_lustro["longitude"].to_numpy().round(2).astype("float32")
        mw = df_mw_lustro["Mw"].to_numpy().round(1).astype("float32")
        tamaño = (mw**1.6) - 8

        fig = go.Figure()
        mapa = go.Scattermap(
            lat=lat,
            lon=lon,
            mode="markers",
            marker={
                "size": tamaño,
                "colorscale": "plasma_r",
                "color": mw,
                "showscale": True,
                "cmin": float(mw.min()),
                "cmax": float(mw.max()),
                "colorbar": {"orientation": "h"},
                "opacity": 1,
            },
            name="",
            customdata=df_mw_lustro["country_name"].to_numpy(),
            hovertemplate="<b>Magnitud: %{marker.color:.1f} Mw<br>País: %{customdata}</b>",
        )
        fig.add_trace(mapa)
        fig.update_layout(
            title={
                "text": f"<b>Mapa de Sismos, lustro: {selector_lustro.value} - {selector_lustro.value + 4}</b>"
            },
            map={
                "zoom": 1,
                "center": {"lat": 15, "lon": -90},
            },
        )
        return mo.ui.plotly(fig)

    mapa_mw_lustro = crear_mapa_mw_lustro()

    def crear_mapa_depth_lustro():
        lat = df_depth_lustro["latitude"].to_numpy().round(2).astype("float32")
        lon = (
            df_depth_lustro["longitude"].to_numpy().round(2).astype("float32")
        )
        depth = df_depth_lustro["depth"].to_numpy().astype("float32").round(1)
        colores = [
            "#800000",
            "#FF2D2D",
            "#FF5050",
            "#FF66CC",
            "#FF9900",
            "#FFCC00",
            "#FFFF00",
            "#FFFFCC",
        ]
        fig = go.Figure()
        mapa = go.Scattermap(
            lat=lat,
            lon=lon,
            mode="markers",
            name="",
            marker={
                "size": 8,
                "colorscale": "Agsunset",
                "color": depth,
                "showscale": True,
                "cmin": float(depth.min()),
                "cmax": float(depth.max()),
                "colorbar": {"orientation": "h"},
            },
            customdata=df_depth_lustro["country_name"].to_numpy(),
            hovertemplate="<b>Profundidad: %{marker.color:.1f} Km<br>País: %{customdata}</b>",
        )
        fig.add_trace(mapa)
        fig.update_layout(
            title={
                "text": f"<b>Mapa de Profundidad Sísmica, lustro: {selector_lustro.value} - {selector_lustro.value + 4}</b>"
            },
            map={
                "zoom": 1,
                "center": {"lat": 15, "lon": -90},
            },
        )
        return mo.ui.plotly(fig)

    mapa_depth_lustro = crear_mapa_depth_lustro()

    tabs_vistageneral = mo.ui.tabs(
        {
            "Magnitud de momento": mapa_mw_lustro,
            "Profundidad de sismo": mapa_depth_lustro,
        },
        lazy=True,
    )

    vista_general = mo.vstack([panel, titulo_vistageneral, tabs_vistageneral])
    return (vista_general,)


@app.cell
def _(df_limpio, go, mo, np, selector_lustro2, titulo_detallado):
    # Detallado 1: Boxplot estadístico y gráfico de dispersión frecuencia sísmica

    # Dataframes
    def crear_df_mw_lustro_anomes(selector):
        dfx = df_limpio.loc[
            df_limpio["lustro"] == selector,
            ["id", "time", "Mw", "lustro", "year"],
        ]
        dfx["year-month"] = dfx["time"].dt.strftime("%Y-%m")
        return dfx.reset_index(drop=True)

    df_mw_lustro_anomes = crear_df_mw_lustro_anomes(selector_lustro2.value)

    def crear_df_ag_mw_lustro_ano(selector):
        dfx = df_limpio.loc[
            df_limpio["lustro"] == selector,
            ["id", "time", "Mw", "lustro"],
        ]
        dfx["year-month"] = dfx["time"].dt.strftime("%Y-%m")
        dfy = dfx.groupby(["lustro", "year-month", "Mw"]).agg({"id": "count"})
        return dfy.reset_index()

    df_ag_mw_lustro_ano = crear_df_ag_mw_lustro_ano(selector_lustro2.value)

    # Gráficos
    def crear_box_mw_lustro_ano():
        mw = df_mw_lustro_anomes["Mw"].to_numpy().round(1)
        year = df_mw_lustro_anomes["year"].astype("category")

        custom = np.stack((mw, year), axis=-1)
        fig = go.Figure()
        scatter = go.Box(
            x=df_mw_lustro_anomes["year"],
            y=mw,
            name="",
            boxmean=True,
            fillcolor="lightsteelblue",
            line={"color": "slateblue"},
        )
        fig.add_traces([scatter])
        fig.update_layout(
            title={
                "text": f"<b>Distribución y Variación de Magnitud Sísmica Anual, lustro: {selector_lustro2.value} - {selector_lustro2.value + 4}</b>"
            },
            height=500,
            yaxis_title="Magnitud de Momento (Mw)",
        )
        fig.update_xaxes(type="category", categoryorder="category ascending")
        return mo.ui.plotly(fig)

    def crear_scatter_mw_lustro_anomes():
        mw = df_ag_mw_lustro_ano["Mw"].to_numpy()
        count = df_ag_mw_lustro_ano["id"].to_numpy()
        grave = int(mw[mw >= 8].sum())
        mayor = int(mw[mw >= 7].sum())
        fuerte = int(mw[mw >= 6].sum())
        year = df_ag_mw_lustro_ano["year-month"]
        custom = np.stack((mw, year, count), axis=-1)
        fig = go.Figure()
        scatter = go.Scattergl(
            x=df_ag_mw_lustro_ano["year-month"],
            y=mw,
            mode="markers",
            marker={
                "color": mw,
                "colorscale": "plasma_r",
                "showscale": True,
                "colorbar": {"orientation": "h"},
                "cmin": mw.min(),
                "cmax": mw.max(),
                "size": (count - (count * 0.90)) + 7,
            },
            customdata=custom,
            hovertemplate="<b>Año-Mes: %{customdata[1]}</b><br><b>Magnitud: %{customdata[0]} Mw (%{customdata[2]} sismos)</b>",
            name="",
        )
        fig.add_traces([scatter])
        fig.add_hline(
            y=6,
            line_dash="dot",
            line_width=1,
            annotation={"text": f"F: {fuerte}"},
        )
        fig.add_hline(
            y=7,
            line_dash="dot",
            line_width=1,
            annotation={"text": f"M: {mayor}"},
        )
        fig.add_hline(
            y=8,
            line_dash="dot",
            line_width=1,
            annotation={"text": f"G: {grave}"},
        )
        fig.update_layout(
            title={
                "text": f"<b>Distribución de la Frecuencia y Magnitud Sísmica Mensual, lustro: {selector_lustro2.value} - {selector_lustro2.value + 4}</b>"
            },
            height=450,
            yaxis_title="Magnitud de Momento (Mw)",
        )
        return mo.ui.plotly(fig)

    detallado1 = mo.vstack(
        [
            titulo_detallado,
            selector_lustro2,
            crear_box_mw_lustro_ano(),
            crear_scatter_mw_lustro_anomes(),
            mo.md(
                """
                <br>
                <hr>
                """
            ),
        ]
    )
    return (detallado1,)


@app.cell
def _(
    df_limpio,
    go,
    mo,
    selector_lustro3,
    selector_paises,
    selector_region,
    titulo_detallado2,
):
    # Detallado 2: Histograma de magnitud y profundidad sísmica

    # Selectores
    selectores_detallado2 = mo.hstack(
        [selector_lustro3, selector_region, selector_paises],
        widths=[0.1, 0.1, 0.8],
        align="center",
        justify="center",
        wrap=True,
    )

    # Dataframes
    def crear_df_lustro_region_pais(lustro, region, paises):
        dfx = df_limpio.loc[
            ((df_limpio["lustro"] == lustro) & (df_limpio["region"] == region))
            & (df_limpio["country_name"].isin(paises)),
            [
                "id",
                "depth",
                "Mw",
                "lustro",
                "year",
                "region",
                "country_name",
            ],
        ]
        return dfx.reset_index(drop=True)

    df_lustro_region_pais = crear_df_lustro_region_pais(
        selector_lustro3.value,
        selector_region.value,
        selector_paises.value,
    )

    # Gráficos
    def crear_histograma_mw_lustro():
        mw = df_lustro_region_pais["Mw"].to_numpy()
        minimo = 5.0
        maximo = 10.0
        tamaño = (maximo - minimo) / 5
        fig = go.Figure()
        histograma = go.Histogram(
            x=mw,
            xbins={"start": minimo, "end": maximo, "size": tamaño},
            autobinx=False,
            texttemplate="%{y}",
            textposition="outside",
            cliponaxis=False,
            marker={"color": "blue", "opacity": 0.4},
        )
        fig.add_traces([histograma])
        fig.update_layout(
            xaxis={"tickmode": "linear", "tick0": 5, "dtick": 1},
            title={
                "text": f"<b>Distribución Sísmica según rango de Magnitud<br>por Región y País, lustro: {selector_lustro3.value} - {(selector_lustro3.value) + 4}</b>"
            },
            xaxis_title="Magnitud de Momento (Mw)",
            yaxis_title="Frecuencia Sísmica",
            height=350,
        )
        return mo.ui.plotly(fig)

    def crear_histograma_depth_lustro():
        mw = df_lustro_region_pais["depth"].to_numpy().round(0)
        minimo = -100
        maximo = 800
        tamaño = (maximo - minimo) / 9
        fig = go.Figure()
        histograma = go.Histogram(
            x=mw,
            xbins={"start": minimo, "end": maximo, "size": tamaño},
            autobinx=False,
            texttemplate="%{y}",
            textposition="outside",
            cliponaxis=False,
            marker={"color": "blue", "opacity": 0.4},
        )
        fig.add_traces([histograma])
        fig.update_layout(
            title={
                "text": f"<b>Distribución Sísmica según rango de Profundidad<br>por Región y País, lustro: {selector_lustro3.value} - {(selector_lustro3.value) + 4}</b>"
            },
            xaxis_title="Profundidad (Km)",
            yaxis_title="Frecuencia Sísmica",
            height=350,
        )
        return mo.ui.plotly(fig)

    histograms_detallado = mo.vstack(
        [crear_histograma_mw_lustro(), crear_histograma_depth_lustro()],
    )

    detallado2 = mo.vstack(
        [
            titulo_detallado2,
            selectores_detallado2,
            mo.callout(
                value="Sin información, seleccione datos en los segmentadores",
                kind="danger",
            )
            if df_lustro_region_pais.empty
            else histograms_detallado,
            mo.md(
                """
                <hr>
                <br>
                """
            ),
        ]
    )
    return (detallado2,)


@app.cell
def _(df_limpio, go, mo, rango_magnitud, titulo_detallado3):
    # Detallado 3: Líneas temporales de sismos y acumulados

    # Dataframes
    def crear_df_ag_mw_historico(rango):
        dfx = (
            df_limpio.loc[df_limpio["Mw"].between(rango[0], rango[1])]
            .groupby("year")
            .agg({"id": "count"})
        )
        dfx["Acumulado"] = dfx["id"].cumsum()
        return dfx

    df_ag_mw_historico = crear_df_ag_mw_historico(rango_magnitud.value)

    # Gráficos
    def crear_linea_historico_mw(rango):
        count = df_ag_mw_historico["id"].to_numpy()
        fig = go.Figure()
        linea = go.Scatter(
            x=df_ag_mw_historico.index,
            y=count,
            mode="lines+markers",
            line_shape="spline",
            marker={
                "size": 6,
            },
            line={"color": "blue"},
            opacity=0.4,
        )

        fig.update_layout(
            title=f"<b>Evolución Anual de Eventos según rango de Magnitud<br>Entre {rango[0]} - {rango[1]} Mw</b>",
            yaxis_title="Cantidad de eventos",
            height=360,
        )
        fig.add_trace(linea)
        return mo.ui.plotly(fig)

    def crear_linea_historico_acumulado_mw(rango):
        acc = df_ag_mw_historico["Acumulado"].to_numpy()
        fig = go.Figure()
        linea = go.Scatter(
            x=df_ag_mw_historico.index,
            y=acc,
            mode="lines",
            line_shape="spline",
            line={"color": "blue"},
            opacity=0.3,
            fill="tozeroy",
        )

        fig.update_layout(
            title=f"<b>volución Anual Acumulada de Eventos según rango de Magnitud<br>Entre {rango[0]} - {rango[1]} Mw</b>",
            height=360,
        )
        fig.add_trace(linea)
        return mo.ui.plotly(fig)

    detallado3 = mo.vstack(
        [
            titulo_detallado3,
            rango_magnitud,
            crear_linea_historico_mw(rango_magnitud.value),
            crear_linea_historico_acumulado_mw(rango_magnitud.value),
            mo.md(
                """
                <hr>
                <br>
                """
            ),
        ]
    )
    return (detallado3,)


@app.cell
def _(df_limpio, go, mo, selector_lustro4, titulo_detallado6):
    # Detallado 4: Ranking de sismos por país y región

    # Dataframes
    def crear_df_top_sismos_pais(lustro):
        dfx = (
            df_limpio[(df_limpio["lustro"] == lustro) & (df_limpio["Mw"] >= 7)]
            .reset_index(drop=True)
            .groupby("country_name")
            .agg({"id": "count"})
            .sort_values(by="id", ascending=False)
            .head(10)
        )
        return dfx

    def crear_df_top_sismos_region(lustro):
        dfx = (
            df_limpio[(df_limpio["lustro"] == lustro) & (df_limpio["Mw"] >= 7)]
            .reset_index(drop=True)
            .groupby("region")
            .agg({"id": "count"})
            .sort_values(by="id", ascending=False)
            .head(10)
        )
        return dfx

    df_top_sismos_pais = crear_df_top_sismos_pais(selector_lustro4.value)
    df_top_sismos_region = crear_df_top_sismos_region(selector_lustro4.value)

    # Graficos
    def crear_ranking_sismos_region():
        fig = go.Figure()
        barras = go.Bar(
            x=df_top_sismos_region["id"],
            y=df_top_sismos_region.index,
            orientation="h",
            texttemplate="%{x}",
            opacity=0.7,
        )
        fig.add_trace(barras)
        fig.update_layout(
            yaxis={"categoryorder": "total ascending"},
            title="<b>Top 10 de Regiones con Sismos fuertes</b>",
            height=450,
        )
        return mo.ui.plotly(fig)

    def crear_ranking_sismos_pais():
        fig = go.Figure()
        barras = go.Bar(
            x=df_top_sismos_pais["id"],
            y=df_top_sismos_pais.index,
            orientation="h",
            texttemplate="%{x}",
            opacity=0.7,
        )
        fig.add_trace(barras)
        fig.update_layout(
            yaxis={"categoryorder": "total ascending"},
            title="<b>Top 10 de Países con Sismos fuertes</b>",
            height=450,
        )
        return mo.ui.plotly(fig)

    rankings = mo.hstack(
        [crear_ranking_sismos_region(), crear_ranking_sismos_pais()],
        widths=[1, 1],
    )
    detallado4 = mo.vstack(
        [
            titulo_detallado6,
            selector_lustro4,
            rankings,
            mo.md(
                """
                <hr>
                <br>
                """
            ),
        ]
    )
    return (detallado4,)


@app.cell
def _(
    df_limpio,
    go,
    mo,
    np,
    selector_continente,
    selector_lustro5,
    titulo_detallado4,
):
    # Detallado 5: Scatter Profundidad vs Magnitud

    # Dataframes
    def crear_df_mw_depth_lustro(lustro, continente):
        dfx = df_limpio.loc[
            (df_limpio["lustro"] == lustro)
            & (df_limpio["continent"] == continente),
            ["id", "Mw", "depth", "place", "year", "country_name"],
        ]
        return dfx

    df_mw_depth_lustro = crear_df_mw_depth_lustro(
        selector_lustro5.value, selector_continente.value
    )

    # Gráfico
    def crear_scatter_mw_depth_lustro():
        depth = df_mw_depth_lustro["depth"].to_numpy().round(2)
        mw = df_mw_depth_lustro["Mw"].to_numpy()
        custom = np.stack(
            [df_mw_depth_lustro["year"], df_mw_depth_lustro["country_name"]],
            axis=-1,
        )

        fig = go.Figure()
        scatter = go.Scattergl(
            x=depth,
            y=mw,
            mode="markers",
            marker={
                "color": mw,
                "colorscale": "plasma_r",
                "size": 10 + (1 - (abs(depth) / depth.max())) * (mw),
                "opacity": 0.6,
            },
            customdata=custom,
            hovertemplate="<b>Año: %{customdata[0]}<br>País: %{customdata[1]}<br>Magnitud: %{y:.1f} Mw<br>Profundidad: %{x:.1f} Km</b>",
            name="",
        )
        fig.add_vline(
            x=70,
            line_dash="dot",
            line_width=2,
            opacity=0.7,
            annotation={"text": "<b><- Mayor prioridad de evaluación</b>"},
            annotation_position="top right",
        )
        fig.add_hline(
            y=7,
            line_dash="dot",
            line_width=2,
            opacity=0.7,
            annotation={"text": "<b>Más energía -></b>", "textangle": 270},
            annotation_position="bottom left",
        )
        fig.add_trace(scatter)
        fig.update_layout(
            title={"text": "<b>Profundidad vs Magnitud Sísmica</b>"},
            xaxis_title="Profundidad (Km)",
            yaxis_title="Magnitud de Momento (Mw)",
        )
        return mo.ui.plotly(fig)

    selectores_detallado5 = mo.hstack(
        [selector_lustro5, selector_continente], justify="start"
    )

    detallado5 = mo.vstack(
        [
            titulo_detallado4,
            selectores_detallado5,
            crear_scatter_mw_depth_lustro(),
            mo.md(
                """
                <hr>
                <br>
                """
            ),
        ]
    )
    return (detallado5,)


@app.cell
def _(df_limpio, go, mo, np, titulo_detallado5):
    # Detallado 6: Ranking de eventos más poderosos
    def crear_df_top_eventos():
        dfx = (
            df_limpio.groupby(["year", "country_name", "place"])
            .agg({"Mw": "max"})
            .sort_values(by="Mw", ascending=False)
            .reset_index()
            .head(10)
        )

        dfx["year_country"] = (
            dfx["year"].astype(str) + " - " + dfx["country_name"].astype(str)
        )
        return dfx

    df_top_eventos = crear_df_top_eventos()

    def crear_top_eventos():
        mw = df_top_eventos["Mw"].to_numpy()
        custom = np.stack(
            [
                mw,
                df_top_eventos["country_name"],
                df_top_eventos["year"],
                df_top_eventos["place"],
            ],
            axis=-1,
        )
        fig = go.Figure()
        grafico = go.Bar(
            y=mw,
            x=df_top_eventos.index,
            texttemplate="%{y}",
            customdata=custom,
            hovertemplate="<b>País/año: %{customdata[1]} - %{customdata[2]}<br>Magnitud: %{customdata[0]} Mw<br>Lugar: %{customdata[3]}</b>",
            marker={"color": "blue"},
            opacity=0.4,
            name="",
        )
        fig.add_traces([grafico])
        fig.update_layout(
            title="<b>Top 10 Sismos más devastadores de la historia: 1970 - actualidad</b>",
            xaxis_title="Evento",
            yaxis_title="Magnitud de Momento (Mw)",
            xaxis={
                "tickvals": df_top_eventos.index,
                "ticktext": df_top_eventos["year"].astype(str)
                + " - "
                + df_top_eventos["country_name"].astype(str),
                "tickangle": -45,
                "tickfont": {"size": 11},
            },
        )
        return mo.ui.plotly(fig)

    detallado6 = mo.vstack([titulo_detallado5, crear_top_eventos()])
    return (detallado6,)


if __name__ == "__main__":
    app.run()
