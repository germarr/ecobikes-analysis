La primera parte de este proyecto consistira en descargar los datos del programa de Ecobici. Una vez descargados voy a proceder a limpiar la data utilizando Python/Pandas y finalmente voy a publicar una API con los datos para que pueda ser consumida por mi frontend.

El API lo voy a crear utilizando [FASTAPI](https://fastapi.tiangolo.com/). Este es un poderoso y moderno framework que nos permite diseñar API´s y publicarlas a una velocidad extraordinaria. Esto sumado a que tiene una de las documentaciones más completas que te puedas imaginar.

Todos los datos los vamos a alamcenar en una base de datos de PostgreSQL y para la interacción entre nuestra base y Fastapi vamos a utilizar SQLModel.

La segunda parte del proyecto consistirá en crear el Frontend. Si quiere leer esa parte da click [aquí]().

## 1. Descargando los datos.

Lo primero que tenemos que hacer es descargar los datos en formato `.csv` de la página de Ecobici. Los puedes encontrar [aqui](https://www.ecobici.cdmx.gob.mx/en/informacion-del-servicio/open-data). Algo que me gusta de este servicio es que tiene publicado datos desde el 2010, por lo que se pueden realizar muchísmos analisis de tiempo. 

En especifico, para este proyecto, voy a descargar los últimos 3 años (2019,2020,2021). Una vez descargados, podemos empezar a familiarizarnos con el archvio abriendolo en un programa como Excel o Google Sheets.

Podemos ver que el archivo tiene las siguientes columnas:

| Genero_Usuario   |   Edad_Usuario |   Bici |   Ciclo_Estacion_Retiro | Fecha_Retiro   | Hora_Retiro   |   Ciclo_EstacionArribo | Fecha Arribo   | Hora_Arribo   |
|:-----------------|---------------:|-------:|------------------------:|:---------------|:--------------|-----------------------:|:---------------|:--------------|
| M                |             41 |   6844 |                     398 | 30/11/2021     | 23:55:08      |                    427 | 01/12/2021     | 00:00:36      |
| M                |             26 |  11982 |                     121 | 30/11/2021     | 23:50:25      |                     99 | 01/12/2021     | 00:01:18      |
| M                |             57 |   9423 |                     455 | 30/11/2021     | 23:31:17      |                    430 | 01/12/2021     | 00:01:20      |
| M                |             31 |   8834 |                     326 | 30/11/2021     | 23:22:33      |                    390 | 01/12/2021     | 00:01:25      |
| M                |             32 |   2061 |                     266 | 30/11/2021     | 23:54:07      |                    183 | 01/12/2021     | 00:02:09      |

Después de analizar este documento, decidi que las metricas que quiero reflejar en mi dashboard son las siguientes:
1. Número total de viajes por mes
2. Número total de kms recorridos por mes
3. Promedio de tiempo entre viajes
4. Promedio de km's entre viajes
5. Un aproximado de ganacias por mes

Adicional, quisiera crear algunas visualizaciones para dar sentido a cierta información. Quiero realizar una visualización que muestre el promedio de viajes por hora en un determinado mes, otra visualización que muestre la distribución de viajes por genero y, finalmente, quiero una visualización que muestre los viajes totales por mes en un determinado año. 

Para finalizar, quiero agregar una tabla que muestre las rutas más populares por mes y un mapa que muestre el trayecto de dicha ruta. 

En cualquier parte de tu computadora crea una carpeta llamada `bici-proyectos`. Dentro de esta carpeta crea una carpeta adicional llamada `db`. Ubicate dentro de `db` y crea una carpeta con el titulo de cada año que quieras agregar a tu analisis. Para efectos de este tutorial, yo descargue los datos del 2021,2020 y 2019. Dentro de la carpeta con el nombre de cada año, guarda los archivos `.csv` correspondeintes a cada mes.

Así se debería ver tu estructura de archivos para este punto:

```
├── bici-proyectos
│   ├──db
│   │   ├── 2021
│   │   │   ├── jan.csv
│   │   │   ├── feb.csv
│   │   ├── 2020
│   │   ├── 2019
│   ├── viajes_totales.py
```

## 2. Limpiar los datos
Antes de empezar a manipular la data, es importante pre-planear. Para este proyecto, y debido a que el tamaño combinado de archivos que descargue es de casi 1 GB, he decidio hacer todo el cálculo y manipulación de datos utilizando Pandas. Pandas es una libreria de python que nos permite crear y manipular *dataframes*. Un *dataframe* es similar a la estructura de un archivo tipo Excel, con columnas, filas y valores, con la diferencia de que un *dataframe* utiliza de forma más eficiente la memoria de la computadora al realizar los cálculos. 

La forma más sencilla de aprender Pandas, e ir viendo como funciona, es usandolo a través de interfaces como los jupyeter notebooks. Puedes leer más sobre este tema y como descargarlo en tu equipo en [esta](https://jupyter.org/install) liga. Si tienes un editor como VSCode, tambi{en puedes acceder a las funcionalidades de un Jupyter Notebook. [Aquí](https://code.visualstudio.com/docs/datascience/jupyter-notebooks) puedes leer más al respecto. 

### 2.1 Número total de viajes por mes
Para comenzar, desplazate a la carpeta principal del proyecto `bici-proyectos` y crea una carpeta llamada `exports` y un archivo que se llame `viajes_totales.py`. Dentro de este archivo ira el siguiente códgio:

```python
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import calendar

def transform_df(ene= None):
    ene = ene.iloc[1:,:].reset_index().rename(columns={0:'Genero_Usuario',1:'Edad_Usuario',2:'Bici',3:'Ciclo_Estacion_Retiro',4:'Fecha_Retiro',5:'Hora_Retiro',6:'Ciclo_Estacion_Arribo',7:'Fecha_Arribo',8:'Hora_Arribo'})
    
    try:
        ene["full_date_retiro"] = pd.to_datetime(ene["Fecha_Retiro"] + " " + ene["Hora_Retiro"], format="%d/%m/%Y %H:%M:%S").copy()
    except:
        ene["full_date_retiro"] = pd.to_datetime("31/10/1900 23:46:40")

    try:
        ene["full_date_arribo"] = pd.to_datetime(ene["Fecha_Arribo"] + " " + ene["Hora_Arribo"], format="%d/%m/%Y %H:%M:%S").copy()
    except:
        ene["full_date_arribo"] = pd.to_datetime("31/10/1900 23:46:40")
    
    try:
        ene["Mes"] = ene["full_date_retiro"].dt.month
    except:
        ene["Mes"] = 0

    try:
        ene["Hora"] = ene["full_date_retiro"].dt.hour
    except:
        ene["Hora"] = 0

    try:
        ene["time_delta"] = round((ene["full_date_arribo"]  - ene["full_date_retiro"]) / np.timedelta64(1,"m"),2)
    except:
        ene["time_delta"] = 0
    
    ene["Ciclo_Estacion_Retiro"]= ene[["Ciclo_Estacion_Retiro"]].astype(str)
    ene["Ciclo_Estacion_Retiro"] = [i[:-2] for i in ene["Ciclo_Estacion_Retiro"]]
    ene["Bici"]= ene[["Bici"]].astype(str)
    ene["Bici"] = [i[:-2] for i in ene["Bici"]]
    ene["Ciclo_Estacion_Arribo"]= ene[["Ciclo_Estacion_Arribo"]].astype(str)
    ene["Ciclo_Estacion_Arribo"] = [i[:-2] for i in ene["Ciclo_Estacion_Arribo"]]
    ene["viaje"] = ene["Ciclo_Estacion_Retiro"].astype(str)+"-"+ene["Ciclo_Estacion_Arribo"]
    ene["Genero_Usuario"] = ene["Genero_Usuario"].fillna("X")
    ene = ene.dropna(axis=0).copy()
    return ene

def merging_files(years = None):
    years_on_file = years

    data_of_all_years = []

    for i,x in enumerate(years_on_file):
        current_year = os.listdir(f"./db/{x}")

        for m, file_on in enumerate(current_year):
            print("Now we are on file--> ",file_on,"🤓", end=" | ")
            this_year = pd.read_csv(f"./db/{years_on_file[i]}/{file_on}", index_col=0, low_memory=False, header=None)
            year_df = transform_df(ene= this_year)
            data_of_all_years.append(year_df)

    fulldfV2 = pd.concat(data_of_all_years)
    return fulldfV2

fulldfV2 = merging_files(years =["2019","2020","2021"])

def get_trips_per_year(trips_data = fulldfV2):
    trips_data["anio"] = trips_data["full_date_arribo"].dt.year
    trips_data = trips_data[["anio","Mes"]].groupby(["anio","Mes"]).size().reset_index().rename(columns={0:"viajes"}).copy()
    trips_data["Mes"] = [calendar.month_abbr[int(i)] for i in trips_data["Mes"].to_list()]

    trips_data.query("anio > 1900").to_csv("../exports/viajes_por_anio/total_viajes.csv")

    return trips_data

trips_per_year = get_trips_per_year(fulldfV2)

```

Antes de correr el script, desplazate a la carpeta `exports` y genera un nuevo archivo llamado `viajes_por_anio`.

Este código nos va a generar un archivo `.csv` que contendrá el total de viajes de cada año que guardamos en la carpeta `db` agrupado por año y mes. 

Para este punto, nuestra estructura de archivos se debe ver algo así:

```
├── bici-proyectos
│   ├──db
│   │   ├── 2021
│   │   │   ├── jan.csv
│   │   │   ├── feb.csv
│   │   ├── 2020
│   │   ├── 2019
│   ├──exports
│   │   ├── viajes_por_anio
│   ├── viajes_totales.py
```

### 2.2 Número total de kms recorridos por mes

Ahora vamos a calular el total de kms recorridos por mes. Para obtener este calculo, necestiamos un archvio que contenga la geolocalización de cada estación de Ecobici. Este archivo lo podemos descargar [**aquí**](https://datos.cdmx.gob.mx/dataset/infraestructura-vial-ciclista/resource/93e9879c-141f-4065-82f4-d9b43bbe1e13?inner_span=True).

El archvio que descargaremos es formato `.kmz`. Este tipo de archivos se utilizan mucho para analisis cartograficos, por ejemplo. Sin embargo, para este proyecto yo terecomendaría utilizar un programa que convierta este archvio a formato `.csv`. Una rápida busqueda en Google me recomendo [**esta página**](https://mygeodata.cloud/converter/kmz-to-csv), sin embargo culaquiera te puede funcionar. 

Una vez que tenemos nuestro archivo en `.csv` podemos inspeccionarlo. Se debería ver algo similar a esto:
```
|    |        X |       Y | Name    |   description | altitudeMode   |   CE_CERCA_4 |   CE_CERCA_5 |   CE_CERCA_1 | TIPO     |   CE_CERCA_3 | COLONIA            |   CE_CERCA0 |   CVE_CE |   CE_CERCA_2 |   FID | SISTEMA   | NOMBRE                        |   CP | Field_1   |
|---:|---------:|--------:|:--------|--------------:|:---------------|-------------:|-------------:|-------------:|:---------|-------------:|:-------------------|------------:|---------:|-------------:|------:|:----------|:------------------------------|-----:|:----------|
|  0 | -99.1678 | 19.4336 | ECOBICI |           nan | clampToGround  |            0 |            0 |            8 | BIKE,TPV |            0 | Cuauhtémoc         |           3 |        1 |           85 |     0 | ECOBICI   | Río Sena-Río Balsas           | 6500 | ECOBICI   |
|  1 | -99.1717 | 19.4314 | ECOBICI |           nan | clampToGround  |            0 |            0 |            5 | BIKE     |            0 | Cuauhtémoc         |           1 |        2 |            0 |     1 | ECOBICI   | Río Guadalquivir - Río Balsas | 6500 | ECOBICI   |
|  2 | -99.1587 | 19.4317 | ECOBICI |           nan | clampToGround  |            0 |            0 |           20 | BIKE,TPV |            0 | Ampliación Granada |           8 |        3 |           86 |     2 | ECOBICI   | Reforma - Insurgentes         | 6500 | ECOBICI   |
```



Ahora vamos a crear un nuevo arhivo que se llama `requirements.txt` y vamos a agregar las siguientes librerias:

```txt
fastapi
uvicorn[standard]
pandas
python-dotenv
lock
psycopg2-binary
requests
ipykernel
numpy
```



```
├── env
├── requirements.txt
├── app
│   ├── main.py
│   ├── youtube_scripts.py
│   ├── static
│   │   ├── styles.css
│   ├── templates
│   │   ├── index.html
│   │   ├── layout.html
│   │   ├── post.html
│   │   ├── input.css
│   ├── __init__.py
│   ├── .env
```