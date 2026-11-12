# 🌎 Global Earthquake Analysis Dashboard

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![marimo](https://img.shields.io/badge/marimo-FFD700?style=flat&logo=python&logoColor=black)](https://marimo.io/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0-blue.svg)]()

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Características Principales](#-características-principales)
- [Contenido del Proyecto](#-contenido-del-proyecto)
- [Herramientas y Tecnologías](#️-herramientas-y-tecnologías-utilizadas)
- [Configuración del Entorno](#️-configuración-del-entorno)
- [Estructura del Repositorio](#-estructura-del-repositorio)
- [Proceso ETL y Lógica de Negocio](#️-proceso-etl-y-lógica-de-negocio)
- [Vistas Previas](#️-vistas-previas-del-proyecto)
- [Autor](#-autor)
- [Licencia](#-licencia)

---

## 📃 Descripción General

Proyecto de análisis y visualización de sismos a nivel mundial entre **1970 y 2026**, desarrollado en Python con **marimo** y **Plotly**. Está diseñado para explorar la distribución geográfica, la magnitud de momento (Mw), la profundidad y la evolución histórica de los eventos sísmicos de magnitud igual o superior a 5 Mw.

Este proyecto transforma el dataset de Kaggle `Earthquakes_USGS_with_countries` (originalmente 1.7 GB en `.csv`) en un archivo `.parquet` optimizado (17.7 MB) y lo expone como una aplicación interactiva mediante:

- 🧹 **Limpieza y Transformación de Datos (ETL):** Conversión de tipos, filtrado por evento (`earthquake`) y estado (`reviewed`), estandarización a **Magnitud de Momento (Mw)**, y tipado `category` para optimizar la memoria.
- 📈 **Agrupaciones y Métricas:** Conteo de eventos por año, mes, región y país, acumulados históricos, medianas, máximos de magnitud/profundidad y variación porcentual entre lustros.
- 📊 **Visualizaciones Estadísticas:** Mapas de dispersión geográfica (`Scattermap`), boxplots, histogramas, líneas de tiempo con acumulados, rankings Top N y gráficos de dispersión profundidad vs. magnitud.
- 🖱️ **Filtros Interactivos:** Selectores de lustro, región, países, continente y rango de magnitud mediante widgets reactivos de marimo, con tarjetas de métricas (`mo.stat`) comparativas.
- 🧭 **Navegación Multipágina:** Menú de navegación (`mo.nav_menu`) y enrutamiento (`mo.routes`) con tres secciones claramente diferenciadas.

---

## ✨ Características Principales

### 🔄 Aplicación Reactiva y Multipágina
- Navegación fluida entre secciones (Inicio, Vista General, Análisis Detallado) sin recargar la aplicación completa.
- Pestañas con carga diferida (`lazy=True`) para optimizar el renderizado de mapas pesados.

### 🚀 Optimización de Rendimiento
- Uso de `@mo.persistent_cache` para evitar reprocesar el dataset en cada ejecución.
- Uso de `Scattergl` (WebGL) y tipos de datos `float32` para renderizar grandes volúmenes de puntos geográficos sin lag.
- Funciones modulares por gráfico que se recalculan únicamente cuando cambian sus filtros dependientes.

### 🎨 Diseño Interactivo y Contextual
- Filtros en cascada: las opciones de región y países se actualizan dinámicamente según el lustro seleccionado.
- Manejo elegante de casos sin datos mediante mensajes de alerta (`mo.callout`).
- Umbrales visuales de magnitud (sismo fuerte ≥ 6, mayor ≥ 7, grave ≥ 8) y de profundidad (70 km) integrados en los gráficos.

---

## 📊 Contenido del Proyecto

La aplicación está organizada en tres secciones principales que responden a preguntas clave de análisis sísmico:

### 🏠 Inicio
- Presentación del proyecto, objetivos y alcance.
- Detalle del flujo ETL (con el código fuente desplegable en un acordeón).
- Vista previa interactiva de la tabla de datos limpia.

### 📊 Vista General
1. **¿Dónde y con qué magnitud (Mw) y profundidad (km) se distribuyeron los sismos a nivel mundial?**
   - **Mapa de Sismos:** Distribución por lustro (color y tamaño según magnitud).
   - **Mapa de Profundidad Sísmica:** Distribución por lustro.
   - **Tarjetas de Métricas:** Comparación contra el lustro anterior (total de sismos, magnitud media/máxima, profundidad media/mínima).

### 🔍 Análisis Detallado
2. **¿Cómo se distribuyó y varió la magnitud de los sismos año tras año?**
   - Boxplots de distribución anual y scatter de frecuencia mensual con umbrales de severidad.
3. **¿Cuál es la frecuencia sísmica según su rango de magnitud y profundidad por región y país?**
   - Histogramas interactivos de magnitud y profundidad.
4. **¿Cuál es la evolución anual de la frecuencia y el acumulado de sismos registrados (Mw 5.0 - 10.0)?**
   - Gráfico de líneas de eventos por año con área acumulada.
5. **¿Cuáles son las regiones y países con sismos más fuertes (>= 7 Mw)?**
   - Rankings Top 10 de regiones y países por lustro.
6. **¿Cuál es la relación entre la profundidad y la magnitud de los sismos?**
   - Gráfico de dispersión (Scatter) profundidad vs. magnitud por lustro y continente.
7. **¿Cuáles son los 10 sismos de mayor magnitud en la historia según el USGS?**
   - Ranking histórico de los eventos más fuertes desde 1970.

---

## 🛠️ Herramientas y Tecnologías Utilizadas

### Software y Lenguajes
- **Python 3.10+** - Lenguaje de programación principal.
- **marimo** - Notebook reactivo de Python que se ejecuta como una aplicación web multipágina.

### Librerías Principales
- 🐼 **Pandas** y **NumPy** - Manipulación, limpieza, agregación y optimización de tipos de datos.
- 📊 **Plotly** (`graph_objects`) - Gráficos interactivos avanzados (`Scattermap`, `Scattergl`, `Box`, `Histogram`, `Bar`, `Scatter`).
- 📦 **pyarrow** - Motor de lectura/escritura eficiente para archivos `.parquet`.

### Fuente de Datos
- 🌍 **Earthquakes USGS with Countries:** Dataset original de Kaggle, basado en el catálogo del Servicio Geológico de los Estados Unidos (USGS), preprocesado y almacenado en formato `.parquet` para máxima eficiencia.

---

## ⚙️ Configuración del Entorno

### Prerequisitos
1. Tener instalado **Python 3.10** o superior.
2. Tener instalado `pip` o un gestor de entornos como `uv` o `conda`.

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/Gbarrantes25/GlobalEarthquakeAnalysis-Dashboards.git
cd GlobalEarthquakeAnalysis-Dashboards
```

### Paso 2: Instalar Dependencias

```bash
pip install marimo pandas numpy plotly pyarrow
```

(Opcional: si usas uv, ejecuta uv sync)

### Paso 3: Ejecutar el Proyecto
Puedes ejecutar el proyecto de dos maneras:
Como aplicación web interactiva (Modo Producción):

```bash
marimo run app.py
```

Como notebook editable (Modo Desarrollo):

```bash
marimo edit app.py
```

La aplicación se abrirá automáticamente en tu navegador predeterminado (generalmente en http://localhost:2718).

> ⚠️ Nota: Asegúrate de que la ruta del archivo df_sismos.parquet en el código apunte a una ubicación válida en tu sistema local.

---

## 📂 Estructura del Repositorio

```
.
├── app.py                    # Aplicación marimo con el análisis, lógica y visualizaciones
├── df_sismos.parquet         # Dataset procesado y optimizado de sismos (Mw >= 5)
├── pyproject.toml            # Configuración de dependencias del proyecto
├── .gitignore                # Archivo de configuración Git
└── README.md                 # Este archivo de documentación
```

---

## ⚙️ Proceso ETL y Lógica de Negocio

Una de las fortalezas del proyecto es su pipeline de datos, que convierte diversas escalas de magnitud a una estándar (Magnitud de Momento, Mw) para garantizar la comparabilidad histórica:

<details>
<summary>📄 Ver Reglas de Conversión a Magnitud de Momento (Mw)</summary>

| Tipo de magnitud (`magType`) | Condición sobre `mag` | Fórmula |
|---|---|---|
| `mb` | `mag <= 6.2` | `Mw = 0.85 × mag + 1.03` |
| `mww`, `mwc`, `mwb`, `mwr`, `mwp`, `mw` | — | `Mw = mag` |
| `ms`, `ms_20` | `3 <= mag < 6.2` | `Mw = 0.67 × mag + 2.07` |
| `ms`, `ms_20` | `6.2 <= mag <= 8.2` | `Mw = 0.99 × mag + 0.08` |
| `ml`, `Ml`, `ml(texnet)` | `mag <= 6.5` | `Mw = 0.722 × mag + 0.743` |
| `md`, `Md` | `mag <= 6.8` | `Mw = 0.9879 × mag + 0.3316` |
| Cualquier otro caso | — | `NaN` (menos del 1% de registros, se eliminan) |

</details>

El pipeline final filtra eventos desde 1970, elimina valores nulos de profundidad, rellena ubicaciones desconocidas con "Sin registro" y convierte columnas categóricas para reducir el tamaño del archivo en un ~99% (de 1.7 GB a 17.7 MB).

---

## 🖼️ Vistas Previas del Proyecto
<details>
<summary>📸 Ver Capturas de Pantalla</summary>

  <img width="2136" height="984" alt="image" src="https://github.com/user-attachments/assets/5b9dcc41-ff0b-44fd-aef5-adceb7c4844c" />
  <img width="2178" height="892" alt="image" src="https://github.com/user-attachments/assets/c41132ff-dadc-4b3c-aa5f-705e4e9761a7" />

</details>

<details>
<summary>🎥 Ver Video Demostrativo</summary>

   
   Ver en YouTube: https://youtu.be/WlyiYUq-yAQ?si=uZg7TLCDTZ2_z5AD
</details>

---

## 👤 Autor
Giancarlo Barrantes

Business Intelligence Developer | Power BI Specialist


<a href="https://www.linkedin.com/in/gb25"><img width="70" height="20" alt="image" src="https://github.com/user-attachments/assets/e0d69586-c6f9-4f66-9a3d-bc8dfa146463" /></a>
<a href="https://www.instagram.com/gbarrantes25"><img width="70" height="20" alt="image" src="https://github.com/user-attachments/assets/68773029-5e0f-49da-92e9-fb93a223dd09" />
</a>
<a href="https://www.tiktok.com/@gbarrantes25"><img width="65" height="20" alt="image" src="https://github.com/user-attachments/assets/349c87c0-1f3a-4368-8517-64a6012565c0" /></a>
<a href="https://www.youtube.com/@gbarrantes25"><img width="70" height="20" alt="image" src="https://github.com/user-attachments/assets/d9e2cb69-29ec-47fc-93ae-30896a7b533d" />
</a>

---

## 📝 Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo <a href="https://mit-license.org/">LICENSE</a> para más detalles.

---

## ⭐ Agradecimientos
Si este proyecto te resultó útil, considera darle una ⭐ en GitHub y compartirlo con otros profesionales de Business Intelligence.

<div align="center">
   Hecho por <a href="https://gbarrantes25.github.io/">Giancarlo Barrantes</a>
</div>
===============================================================================================================================
# Global Earthquake Analysis Dashboard 🌎

## 📃 Descripción General
Proyecto de análisis y visualización de sismos a nivel mundial entre **1970 y 2026**, desarrollado en Python con **marimo** y **Plotly**, diseñado para explorar la distribución geográfica, la magnitud de momento (Mw), la profundidad y la evolución histórica de los eventos sísmicos de magnitud igual o superior a 5 Mw.

Este proyecto transforma el dataset de Kaggle `Earthquakes_USGS_with_countries` (1.7 GB en `.csv`) en un archivo `.parquet` aligerado (17.7 MB) y lo expone como una aplicación interactiva mediante:
- 🧹 **Limpieza y Transformación de Datos (ETL)**: conversión de tipos de datos, filtrado por tipo de evento (`earthquake`) y estado (`reviewed`), selección de columnas relevantes, filtrado desde 1970, conversión de distintas escalas de magnitud a **Magnitud de Momento (Mw)**, eliminación de valores nulos y tipado `category` para variables categóricas.
- 📈 **Agrupaciones y Métricas**: conteo de eventos por año, mes, región y país, acumulados históricos, medianas y máximos de magnitud/profundidad, y variación porcentual entre lustros (periodos de 5 años).
- 📊 **Visualizaciones Estadísticas**: mapas de dispersión geográfica, boxplots, histogramas, líneas de tiempo con acumulados, rankings Top N y gráficos de dispersión profundidad vs magnitud.
- 🖱️ **Filtros Interactivos**: selectores de lustro, región, países, continente y rango de magnitud mediante widgets de marimo (`mo.ui.dropdown`, `mo.ui.multiselect`, `mo.ui.radio`, `mo.ui.range_slider`) con tarjetas de métricas (`mo.stat`).
- 🧭 **Navegación Multipágina**: menú de navegación (`mo.nav_menu`) y enrutamiento (`mo.routes`) con tres secciones: Inicio, Vista General y Análisis Detallado.

## 📊 Contenido del proyecto
La aplicación está organizada en tres secciones y responde a las siguientes preguntas de negocio:

### 🏠 Inicio
Presenta la tabla de contenido, los objetivos del proyecto, el detalle del flujo ETL (con el código desplegable en un acordeón) y una vista previa de la tabla limpia.

### 📊 Vista General
1. ¿Dónde y con qué magnitud (Mw) y profundidad (Km) se distribuyeron los sismos a nivel mundial?
   - **Mapa de Sismos** por lustro (color y tamaño según magnitud).
   - **Mapa de Profundidad Sísmica** por lustro.
   - Tarjetas de métricas con comparación contra el lustro anterior: total de sismos, magnitud media, magnitud máxima, profundidad media y profundidad mínima.

### 🔍 Análisis Detallado
2. ¿Cómo se distribuyó y varió la magnitud de los sismos año tras año? ¿Cuál es la distribución de la frecuencia por año/mes?
   - Distribución y variación de la magnitud sísmica anual (boxplot).
   - Distribución de la frecuencia y magnitud sísmica mensual (scatter con umbrales de sismo fuerte, mayor y grave).
3. ¿Cuál es la frecuencia sísmica según su rango de magnitud (Mw) y profundidad (Km) por región y país?
   - Histogramas de magnitud y de profundidad filtrados por lustro, región y países.
4. ¿Cuál es la evolución anual de la frecuencia y el acumulado de sismos registrados (Mw 5.0 - 10.0)?
   - Línea de eventos por año y área acumulada, filtrables por rango de magnitud.
5. ¿Cuáles son las regiones y países con sismos más fuertes (>= 7 Mw)?
   - Top 10 de regiones y Top 10 de países por lustro.
6. ¿Cuál es la relación entre la profundidad y la magnitud de los sismos?
   - Scatter profundidad vs magnitud por lustro y continente.
7. ¿Cuáles son los 10 sismos de mayor magnitud en la historia según el USGS?
   - Ranking de los 10 eventos más fuertes desde 1970.

## 🔄 Proceso ETL
1. **Carga** del archivo `Earthquakes_USGS_with_countries.csv` descargado de Kaggle.
2. **Primera transformación**:
   - Conversión de `status` a minúsculas.
   - Conversión de `time` a `datetime` (formato mixto).
   - Filtro `type_property == "earthquake"` para excluir explosiones y otros eventos.
   - Filtro `status == "reviewed"` y selección de columnas necesarias.
   - Filtro de fechas desde 1970.
   - Limpieza de espacios en `magType` y creación de las columnas `year` y `decade`.
3. **Conversión a Magnitud de Momento (Mw)** según el tipo de magnitud original:

| Tipo de magnitud (`magType`) | Condición sobre `mag` | Fórmula |
|---|---|---|
| `mb` | `mag <= 6.2` | `Mw = 0.85 × mag + 1.03` |
| `mww`, `mwc`, `mwb`, `mwr`, `mwp`, `mw` | — | `Mw = mag` |
| `ms`, `ms_20` | `3 <= mag < 6.2` | `Mw = 0.67 × mag + 2.07` |
| `ms`, `ms_20` | `6.2 <= mag <= 8.2` | `Mw = 0.99 × mag + 0.08` |
| `ml`, `Ml`, `ml(texnet)` | `mag <= 6.5` | `Mw = 0.722 × mag + 0.743` |
| `md`, `Md` | `mag <= 6.8` | `Mw = 0.9879 × mag + 0.3316` |
| Cualquier otro caso | — | `NaN` (menos del 1% de registros, se eliminan) |

4. **Filtrado final** por magnitud mínima, conversión de `magType`, `status`, `country_name`, `region` y `continent` a tipo `category`, eliminación de columnas innecesarias y exportación a `.parquet`.
5. **Carga en la app**: se lee el `.parquet`, se crea la columna `lustro` (`(year // 5) * 5`), se filtra `Mw >= 5` y se eliminan los registros sin `depth`; los valores nulos de `place` se rellenan con `"Sin registro"`.

## 🛠️ Herramientas y Tecnologías Utilizadas
- Desarrollo y Visualización: Python, marimo, Plotly.
- Librerías:
  - `pandas` y `numpy` para manipulación, limpieza y agregación de datos.
  - `plotly` (`graph_objects`) para gráficos interactivos (`Scattermap`, `Scattergl`, `Box`, `Histogram`, `Bar`, `Scatter`).
  - `marimo` para el notebook reactivo, widgets, navegación y despliegue como app.
- Fuente de Datos: [Earthquakes_USGS_with_countries (Kaggle)](https://www.kaggle.com/), basado en el catálogo del USGS.
- Formato de datos: `.parquet`.
- Despliegue: _(agregar enlace de molab / hosting)_.

## ⚙️ Configuración del Entorno
- Software Necesario: Python 3.10+ y las librerías `marimo`, `pandas`, `numpy`, `plotly` y `pyarrow` (para leer `.parquet`).
- Instalación:
  - Clonar el repositorio:
    ```bash
    git clone https://github.com/Gbarrantes25/GlobalEarthquakeAnalysis-Dashboards.git
    cd GlobalEarthquakeAnalysis-Dashboards
    ```
  - Instalar dependencias:
    ```bash
    pip install marimo pandas numpy plotly pyarrow
    ```
  - Ejecutar como aplicación: `marimo run app.py`
  - Editar el notebook: `marimo edit app.py`
- ⚠️ **Rutas de archivos**: asegúrate de que la ruta del archivo `df_sismos.parquet` (y la del logo, si se usa) en el código apunte a una ubicación válida en tu equipo.

## 📂 Estructura del Repositorio
```text
.
├── app.py              # Aplicación marimo con el análisis y las visualizaciones
├── README.md           # Este archivo
├── df_sismos.parquet   # Dataset procesado de sismos (Mw >= 5)
└── pyproject.toml      # Configuración de dependencias (si aplica)
```
> Ajusta esta estructura a los archivos reales del repositorio.

## ✅ Características Principales
- Aplicación reactiva con marimo y navegación multipágina (Inicio, Vista General, Análisis Detallado).
- Optimización de Rendimiento:
  - `@mo.persistent_cache` para evitar reprocesar el dataset en cada ejecución.
  - Pestañas con carga diferida (`lazy=True`) para los mapas.
  - Uso de `Scattergl` y tipos `float32` para renderizar grandes volúmenes de puntos.
  - Funciones modulares por gráfico que se recalculan solo cuando cambia su filtro.
- Filtros dependientes: las opciones de región y países se actualizan según el lustro seleccionado.
- Tarjetas de métricas con comparación contra el lustro anterior.
- Manejo de casos sin datos mediante mensajes de alerta (`mo.callout`).
- Umbrales visuales de magnitud (sismo fuerte ≥ 6, mayor ≥ 7, grave ≥ 8) y de profundidad (70 Km) en los gráficos.

## 🔎 Algunos Hallazgos
- _(Completar con los hallazgos obtenidos del análisis, por ejemplo: regiones con mayor número de sismos ≥ 7 Mw, tendencia de eventos por lustro, relación entre profundidad y magnitud, etc.)_

## 🖼️ Vistas Previas del proyecto
<details>
  <summary>Dashboard</summary>

  <img width="2136" height="984" alt="image" src="https://github.com/user-attachments/assets/5b9dcc41-ff0b-44fd-aef5-adceb7c4844c" />
  <img width="2178" height="892" alt="image" src="https://github.com/user-attachments/assets/c41132ff-dadc-4b3c-aa5f-705e4e9761a7" />

</details>

## 👤 Autor
- Giancarlo Barrantes
- Lima, Perú
- [linkedin.com/in/gb25](https://www.linkedin.com/in/gb25/)
- [instagram.com/gbarrantes25](https://www.instagram.com/gbarrantes25/)
- [tiktok.com/@gbarrantes25](https://www.tiktok.com/@gbarrantes25)
- [youtube.com/@gbarrantes25](https://www.youtube.com/@gbarrantes25)
