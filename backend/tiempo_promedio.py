import pandas as pd
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import calendar
import geopy.distance

def main():
    year_on_file = '2021'
    fulldfV2 = merging_files(years =[year_on_file])
    time_dataframe = median_time(timeDF=fulldfV2, year_on_file=year_on_file)


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

def median_time(timeDF=None, year_on_file=None):
    time_per_trips = timeDF.copy()
    time_per_trips["Dia"] = time_per_trips["full_date_retiro"].dt.day
    time_per_trips["Mes"] = time_per_trips["full_date_retiro"].dt.month
    time_per_trips["anio"] = time_per_trips["full_date_retiro"].dt.year.astype(str)
    median_time_trips = time_per_trips.query(f'anio == "{year_on_file}"')[['Dia','Mes','anio','time_delta']].groupby(['anio','Mes','Dia']).median().sort_values(by=["Mes","Dia"]).reset_index()
    median_time_trips.to_csv(f"./export/tiempo_promedio/{year_on_file}_time.csv")



if __name__ == '__main__':
    main()
