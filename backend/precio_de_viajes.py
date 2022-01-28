import pandas as pd
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import calendar
import geopy.distance

def main():
    year_on_file = '2019'
    fulldfV2 = merging_files(years =[year_on_file])
    ppt = obtener_precio(timeDF = fulldfV2)
    ppt.to_csv(f"./export/precio_por_viajes/precios_{year_on_file}.csv")

def transform_df(ene= None):
    ene = ene.iloc[:,0:8].reset_index().query('Fecha_Arribo != "10"').query('Hora_Retiro != "18::"').copy()
    ene["full_date_retiro"] = pd.to_datetime(ene["Fecha_Retiro"] + " " + ene["Hora_Retiro"], format="%d/%m/%Y %H:%M:%S")
    ene["full_date_arribo"] = pd.to_datetime(ene["Fecha_Arribo"] + " " + ene["Hora_Arribo"], format="%d/%m/%Y %H:%M:%S")
    ene["Mes"] = ene["full_date_retiro"].dt.month
    ene["Hora"] = ene["full_date_retiro"].dt.hour
    ene["time_delta"] = round((ene["full_date_arribo"]  - ene["full_date_retiro"]) / np.timedelta64(1,"m"),2)
    ene["Ciclo_Estacion_Retiro"]= ene["Ciclo_Estacion_Retiro"].astype(str)
    ene["Bici"]= ene[["Bici"]].astype(str)
    ene["Bici"] = [i[:-2] for i in ene["Bici"]]
    ene["Ciclo_Estacion_Arribo"]= ene["Ciclo_Estacion_Arribo"].astype(str)
    ene["viaje"] = ene["Ciclo_Estacion_Retiro"].astype(str)+"-"+ene["Ciclo_Estacion_Arribo"].astype(str)
    ene["Genero_Usuario"] = ene["Genero_Usuario"].fillna("X")
    ene = ene.dropna(axis=0).copy()
    return ene

def merging_files(years = None):
    years_on_file = years

    data_of_all_years = []

    for i,x in enumerate(years_on_file):
        current_year = os.listdir(f"./db/{x}")

        for m, file_on in enumerate(current_year):
            print(".",file_on[5:-4],"🤓", end=" | ")
            this_year = pd.read_csv(f"./db/{years_on_file[i]}/{file_on}", index_col=0, low_memory=False)
            year_df = transform_df(ene= this_year)
            data_of_all_years.append(year_df)

    fulldfV2 = pd.concat(data_of_all_years)
    return fulldfV2

def obtener_precio(timeDF = None):
    price_per_trip = timeDF.copy()
    price_per_trip["Dia"] = price_per_trip["full_date_retiro"].dt.day
    price_per_trip["Mes"] = price_per_trip["full_date_retiro"].dt.month
    price_per_trip["anio"] = price_per_trip["full_date_retiro"].dt.year.astype(str)

    listadeprecios = price_per_trip['time_delta'].to_list()
    precios = []

    for i,x in enumerate(listadeprecios):
        if x > 15 and x < 60:
            precios.append(14.67)
        elif x > 60:
            time = round(x/60)
            precios.append(44*time)
        else:
            precios.append(0)

    price_per_trip["precio_viaje"] = precios
    ppt = price_per_trip[['Dia','Mes','anio', 'precio_viaje']].groupby(['Dia','Mes','anio']).sum().reset_index()
    return ppt



if __name__ == '__main__':
    main()