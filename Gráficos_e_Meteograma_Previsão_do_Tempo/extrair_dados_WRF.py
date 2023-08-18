# O código a seguir foi desenvolvido inicialmente pelo Rafael ..., em seguida for alterado por mim e pelo Arthur Martins Lemos 

import pandas as pd
import numpy as np
from netCDF4 import Dataset
from datetime import datetime
import salem
import re
import os
import wrf
import glob

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def magnitude(a, b):
    return np.sqrt(np.power(a, 2) + np.power(b, 2))

def direction(a, b):
    return 57.3 * np.arctan2(a, b) + 180

def zero_left(num):
   if num < 10:
      nu = "0"+str(num)+""
      return nu
   else:
      nu = str(num)
      return nu

def num_days(num_d):
   if i == 1 or i == 3 or i == 5 or i == 7 or i == 8 or i == 10 or i == 12:
      num_dias = 31
      return num_dias
   elif i == 4 or i == 6 or i == 9 or i == 11:
      num_dias = 30
      return num_dias
   elif i == 2:
      if ano_bi == 1:
          num_dias = 29
          return num_dias
      else:
          num_dias = 28
          return num_dias
   else:
      num_dias = 0  # Defina um valor padrão caso nenhuma das condições anteriores seja atendida
      return num_dias

def ano_bi(ano):
   if (ano%4 == 0 and ano%100 != 0) or (ano%400 == 0):
     ano_bi = 1
   else:
     ano_bi = 0
   anos = str(ano)
   return anos

def exportData(ncFilePath, locations):

  df = salem.open_wrf_dataset(ncFilePath)
  print(df)
  for loc in locations.keys():

      latArray = df['lat'][:, 0].data
      lngArray = df['lon'][0, :].data

      timeArray = df['time'].data
      print(f'Iniciando {loc} - : {ncFilePath}')

      latPoint = find_nearest(latArray, locations[loc]['lat'])
      lngPoint = find_nearest(lngArray, locations[loc]['lng'])

      tempArray = df['T2C'][:, latPoint, lngPoint].data #- 273.16
      pressureArray = df['PRESSURE'][:, 0, latPoint, lngPoint]
      rh = wrf.rh(qv=df['QVAPOR'].data, pres=df['PRESSURE'].data * 100, tkel=df['TK'].data)
      relativeHumity = rh[:, 0, latPoint, lngPoint].data


      height = df['HGT'][0, latPoint, lngPoint].data
      so2 = df['so2'][:, 0, latPoint, lngPoint].values
      height0 = 10
      u10 = df['U10'][:, latPoint, lngPoint]
      v10 = df['V10'][:, latPoint, lngPoint]
      wind0 = magnitude(u10, v10)
      wdir0 = direction(u10, v10)

      rainc = df['RAINC'][:,latPoint, lngPoint]
      rainnc = df['RAINNC'][:,latPoint, lngPoint]
      prcp = rainc + rainnc
      #prcp_hourly = rainnc - rainnc

      # print("Tamanho dos arrays:")
      # print("timeArray:", timeArray.shape)
      # print("wind0:", wind0.shape)
      # print("wdir0:", wdir0.shape)
      # print("tempArray:", tempArray.shape)
      # print("relativeHumity:", relativeHumity.shape)
      # print("pressureArray:", pressureArray.shape)
      # print("so2:", so2.shape)
      # print("prcp_hourly:", prcp_hourly.shape)


      resultDF = pd.DataFrame(
		data = {
			'time': timeArray,
        		'windSpeed 10m': wind0,
       			'windDirection 10m': wdir0,
        		'temp': tempArray,
       			'humitity': relativeHumity,
        		'pressure': pressureArray,
        		'SO2': so2,
        		'chuva': prcp,
		}
      )

      resultDF = resultDF.round(2)
      resultDF['time'] = pd.to_datetime(resultDF['time'], format='%Y-%m-%d %H:%M:%S')
      resultDF = resultDF.sort_values(by='time', ascending=True)
      resultDF_loc = resultDF
      resultDF_loc.to_csv(os.path.join('/content/drive/MyDrive/CTJL/wrfout_previsao_teste/', f'{loc}.csv'), mode='a', header=False)

  location_items = list(locations.items())
# Define as coordenadas das localidades
locations = {
    'ESTACAO_VILA_MOEMA': {'lat': -28.4836,'lng': -49.00029},
    'ESTACAO_CAPIVARI_DE_BAIXO': {'lat': -28.4476, 'lng': -48.9591825},
    'ESTACAO_SAO_BERNARDO': {'lat': -28.4459, 'lng': -49.025829},

}

ano = int(input("Digite o ano da extração dos dados que deseja:")) # definindo o ano da extração do dados

anos = ano_bi(ano)
i = 6
while i <= 12: # Indo de mes em mes
   num_dia = num_days(i)
   mes = zero_left(i)
   l = 1
   while l <= num_dia: # Indo 	de dia em dia
      dia = zero_left(l)
      n = 0
      while n <= 23: # Indo de hora em hora
         hora = zero_left(n)
       	 for file in glob.glob('/content/drive/MyDrive/CTJL/wrfout_previsao_teste/wrfout_d03_'+anos+'-'+mes+'-'+dia+'_'+hora+':*'): # Itera sobre os arquivos e as localidades
            exportData(file, locations)
         n += 1
      l += 1
   i += 1


