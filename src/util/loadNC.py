# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca

"""Descripción: genera archivos de datos en base a dataset de netcdf

descarga de datos modo experto

 SOURCES .UCSB .CHIRPS .v2p0 .monthly .global .precipitation
  X (81.5W) (74E) RANGEEDGES
  T (Jan 1981) (Jan 2017) RANGEEDGES
  Y (3N) (6S) RANGEEDGES
  X (81.5W) (74w) RANGEEDGES

link de descarga

https://iridl.ldeo.columbia.edu/SOURCES/.UCSB/.CHIRPS/.v2p0/.monthly/.global/.precipitation/X/%2881.5W%29%2874E%29RANGEEDGES/T/%28Jan%201981%29%28Jan%202017%29RANGEEDGES/Y/%283N%29%286S%29RANGEEDGES/X/%2881.5W%29%2874w%29RANGEEDGES/data.nc

"""

import numpy as np
import netCDF4 as nc
import pandas as pd
class LoadNC():
    """"""

    def __init__(self,):
        """Constructor for LoadNC"""
    def readNc(self):

        dataset=nc.Dataset("/home/drosero/Descargas/rrchirps.nc")
        print("leyendo el netcdf\n imprimiendo el metadato")
        print(dataset.file_format)
        print(dataset.dimensions.keys())
        print(dataset.dimensions['T'])
        print(dataset.variables.keys())
        print(dataset.variables['precipitation'])
        #print(dataset.variables)
        """longitud = X, latitud = Y Precipitacion = precipitation"""
        lat = dataset.variables['Y'][:]
        lon = dataset.variables['X'][:]
        rr = dataset.variables['precipitation'][:,:,:]
        print(rr)


    def findLatLong(self):
        pass


lnc= LoadNC()
lnc.readNc()