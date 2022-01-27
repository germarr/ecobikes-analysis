import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import calendar
import geopy.distance

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
        current_year = os.listdir(f"D:/forecasting_trips/full_db/{x}")

        for m, file_on in enumerate(current_year):
            print(".",file_on[5:-4],"🤓", end=" | ")
            this_year = pd.read_csv(f"D:/forecasting_trips/full_db/{years_on_file[i]}/{file_on}", index_col=0, low_memory=False)
            year_df = transform_df(ene= this_year)
            data_of_all_years.append(year_df)

    fulldfV2 = pd.concat(data_of_all_years)
    return fulldfV2

def get_trips_per_year(trips_data = None, year_file = None):
    trips_data["anio"] = trips_data["full_date_arribo"].dt.year
    trips_data["dia"] = trips_data["full_date_arribo"].dt.day
    trips_data = trips_data[["anio","Mes","dia"]].groupby(["anio","Mes","dia"]).size().reset_index().rename(columns={0:"viajes"}).copy()
    trips_data["Mes"] = [calendar.month_abbr[int(i)] for i in trips_data["Mes"].to_list()]

    trips_data.to_csv(f"../raw/trips_per_year/{year_file}.csv")

    return trips_data


def estaciones_df():
   estaciones = pd.read_csv("../export/ECOBICI_Cicloestaciones.csv")
   estaciones["FID"] = [i+1 for i in estaciones["FID"].astype("int").to_list()]
   estaciones["punto_geo"] = estaciones["Y"].astype(str) +"," + estaciones["X"].astype(str)
   estaciones = estaciones.rename(columns={"FID":"id","Y":"location_lat","X":"location_lon"}).copy()
   estaciones = estaciones[["id","NOMBRE","COLONIA","location_lat","location_lon","TIPO","punto_geo"]]
   estaciones["Ciclo_Estacion_Retiro"] = estaciones["id"].astype("str").copy()
   estaciones["Ciclo_Estacion_Arribo"] = estaciones["id"].astype("str").copy()
   estaciones_retiro = estaciones.rename(columns={"NOMBRE":"name_retiro","location_lat":"location_lat_retiro","location_lon":"location_lon_retiro","punto_geo":"punto_geo_retiro"}).iloc[:,[7,1,3,4,6]].copy()
   estaciones_arribo = estaciones.rename(columns={"NOMBRE":"name_arribo","location_lat":"location_lat_arribo","location_lon":"location_lon_arribo","punto_geo":"punto_geo_arribo"}).iloc[:,[8,1,3,4,6]].copy()
   return estaciones_retiro, estaciones_arribo

def mergingfiles(month, er, ea):
   first = month.merge(er, on="Ciclo_Estacion_Retiro", how="left").merge(ea, on="Ciclo_Estacion_Arribo", how="left")
   return first


def filetoexport(first):
   first = first.drop_duplicates(subset="viaje").dropna(axis=0)
        
   location_lat_retiro = first["location_lat_retiro"].to_list()
   location_lon_retiro = first["location_lon_retiro"].to_list()
   location_lat_arribo = first["location_lat_arribo"].to_list()
   location_lon_arribo = first["location_lon_arribo"].to_list()
        
   distances = pd.DataFrame({"location_dist":[geopy.distance.distance((location_lat_retiro[i],location_lon_retiro[i]), (location_lat_arribo[i],location_lon_arribo[i])).km for i in range(len(location_lon_arribo))]})
        
   l = pd.concat([first, distances], axis=1, join="inner")[["viaje","location_dist"]]
   return l

def get_total_kms(datiosanio = None):
   merge_routes = pd.read_csv("../export/all_routes_kms.csv", index_col=0)
   get_kms = datiosanio[["full_date_retiro","Ciclo_Estacion_Retiro","Ciclo_Estacion_Arribo"]].copy()
   get_kms["Ciclo_Estacion_Retiro"] = [i[:-2] for i in get_kms["Ciclo_Estacion_Retiro"].to_list()]
   get_kms["viaje"] = get_kms["Ciclo_Estacion_Retiro"].astype(str)+"-"+get_kms["Ciclo_Estacion_Arribo"].astype(str)
   get_kms["Dia"] = get_kms["full_date_retiro"].dt.day
   get_kms["Mes"] = get_kms["full_date_retiro"].dt.month
   total_kms = get_kms.merge(merge_routes, on="viaje", how="left")
   total_kms = total_kms[["Mes","Dia","location_dist"]].groupby(["Mes","Dia"]).sum().reset_index()
   return total_kms


year_on_file = "2020"
fulldfV2 = merging_files(years =[year_on_file])
trips_per_year = get_trips_per_year(trips_data = fulldfV2, year_file = year_on_file)
fdv3 = fulldfV2.replace("", np.nan).dropna(axis=0).copy()
estaciones_retiro, estaciones_arribo = estaciones_df()
exportfileII = mergingfiles(month=fdv3, er=estaciones_retiro, ea=estaciones_arribo)
new_routes = exportfileII[["viaje","location_lat_retiro","location_lon_retiro","location_lat_arribo","location_lon_arribo"]].copy()
total_routes = filetoexport(first = new_routes)
total_routes.to_csv(f"../raw/all_routes/{year_on_file}_routes.csv")
listofroutes = [i for i in os.listdir("../raw/all_routes")]
all_routes  = pd.concat([pd.read_csv(f"../raw/all_routes/{x}", index_col=0) for i, x in enumerate(listofroutes)]).drop_duplicates(subset="viaje")
all_routes["location_dist"] = [round(i,2) for i in all_routes["location_dist"].to_list()]
all_routes.to_csv("../export/all_routes_kms.csv")
year_total_kms = get_total_kms(datiosanio=fdv3)
year_total_kms.to_csv(f"../raw/distance_per_year/{year_on_file}.csv")