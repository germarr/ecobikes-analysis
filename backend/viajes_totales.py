import pandas as pd
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import calendar
import geopy.distance

def main():
    year_on_file = "2021"
    fulldfV2 = merging_files(years =[year_on_file])
    print("fulldf is ready!")
    trips_per_year = get_trips_per_year(trips_data = fulldfV2, year_file = year_on_file)

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

def get_trips_per_year(trips_data = None, year_file = None):
    trips_data["anio"] = trips_data["full_date_arribo"].dt.year
    trips_data["dia"] = trips_data["full_date_arribo"].dt.day
    trips_data = trips_data[["anio","Mes","dia"]].groupby(["anio","Mes","dia"]).size().reset_index().rename(columns={0:"viajes"}).copy()
    # trips_data["Mes"] = [calendar.month_abbr[int(i)] for i in trips_data["Mes"].to_list()]
    

    trips_data.to_csv(f"./export/viajes_por_dia/{year_file}.csv")

    return trips_data

if __name__ == '__main__':
    main()
