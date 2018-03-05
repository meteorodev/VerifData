# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
"""Descripción: genera archivos de datos en base a dataset de netcdf"""

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
        #print(dataset.variables)
        """longitud = X, latitud = Y Precipitacion = precipitation"""
        lat = dataset.variables['Y'][:]
        lon = dataset.variables['X'][:]
        rr = dataset.variables['precipitation'][:]
        print(len(lat))

lnc= LoadNC()
lnc.readNc()