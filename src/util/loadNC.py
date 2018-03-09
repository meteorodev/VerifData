# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca

"""Descripción: genera archivos de datos en base a dataset de netcdf

descarga de datos modo experto

  SOURCES .UCSB .CHIRPS .v2p0 .monthly .global .precipitation
  X (82W) (74W) RANGEEDGES
  Y (3N) (6S) RANGEEDGES
  T (Jan 1981) (Feb 2018) RANGEEDGES
link de descarga

https://iridl.ldeo.columbia.edu/SOURCES/.UCSB/.CHIRPS/.v2p0/.monthly/.global/.precipitation/X/%2881.5W%29%2874E%29RANGEEDGES/T/%28Jan%201981%29%28Jan%202017%29RANGEEDGES/Y/%283N%29%286S%29RANGEEDGES/X/%2881.5W%29%2874w%29RANGEEDGES/data.nc

"""

import numpy as np
import netCDF4 as nc
import pandas as pd
from django.template.defaulttags import verbatim


class LoadNC():
    """"""

    def __init__(self,):
        """Constructor for LoadNC"""
    def readNc(self, rutaNC,añoIn):

        dataset=nc.Dataset(rutaNC)
        #print("leyendo el netcdf\n imprimiendo el metadato")
        print(dataset.file_format)
        print(dataset.dimensions.keys())
        #print(dataset.dimensions['T'])
        print(dataset.variables.keys())
        #print(dataset.variables['precipitation'])
        #print(dataset.variables)
        """longitud = X, latitud = Y Precipitacion = precipitation"""
        #dataset.
        lat = dataset.variables['Y'][:]
        lon = dataset.variables['X'][:]
        #rr = dataset.variables['precipitation'][:]
        #rr = rr.filled(np.nan)
        #rr_units = dataset.variables['precipitation'].units
        #print("lat : ",len(lat),"lon: ",len(lon))
        #print("units" ,rr_units)
        #print("rr length ",len(rr))

        ##time serie
        cadena = str(añoIn)+"-01-01"
        fechas = pd.date_range(start=cadena,periods=len(dataset.variables['T']),freq="MS")
        print(fechas)
        print("tipo de datos ", type(lon))
        cordNC = self.findCoor(lat,lon,lonp=-78.17830278,latp=0.1783027778)
        print(cordNC.items())
        print("coordenadas encontradas  ==> ",cordNC["coor"], " posiciones ==> ", cordNC["pos"])
        #get all values for this lat and lon
        rr=dataset.variables["precipitation"][:,cordNC["pos"][0],cordNC["pos"][1]]
        print("rr length ",len(rr),"\n valores de RR \n",rr)
        #self.getDataAsfile(rr, lat, lon)
        valores=pd.Series(rr,index=fechas)


        dataset.close();

        return valores


    def findCoor(self,latnc, lonnc, latp, lonp):
        """Retorna un serie de tiempo desde el netcdf dada un latitud y longitug"""

        print(latp," ", lonp)
        ncmx = np.where(latnc >= latp)
        mx=len(ncmx[0])
        latncb =[latnc[mx-1],latnc[mx]]
        print("latitudes ", latncb)
        a = abs(latncb[0]) - abs(latp)
        b = abs(latp) - abs(latncb[1])
        corfin=[]
        pos=[]
        if a > b:
            corfin.append(latncb[1])
            pos.append(mx)
        else:
            corfin.append(latncb[0])
            pos.append(mx-1)
        ncmx = np.where(lonnc <= lonp)
        mx = len(ncmx[0])
        lonncb = [lonnc[mx-1], lonnc[mx]]
        a = abs(lonncb[0]) - abs(lonp)
        b = abs(lonp) - abs(lonncb[1])
        if a > b:
            corfin.append(lonncb[1])
            pos.append(mx)
        else:
            corfin.append(lonncb[0])
            pos.append(mx-1)
        # A CUAL CORDENADA ESTA MAS PROXIMO EL PUNTO
        # ENTONCES  x >= lonnc
        # y >= latnc
        print("longitudes ",lonncb)
        print("############################################")
        return {"coor":corfin,"pos":pos}




    def getDataAsfile(self, varible, lat, lon):

        for t in range(0,5):
        #print("t : ",t," ",lat[0], " {", 0, ":", 74, "} ", lon[74], " : ", varible[t, 0, 74])
            sLat=[]
            sLon=[]
            v1=[]
            v2=[]
            v3=[]
            v4=[]
            v5 = []
            to=0
            for i in range(0,len(lat)):
                for j in range(0, len(lon)):
                    #print(lat[i], " {", i, ":", j, "} ", lon[j], " : ", varible[0, 0, 74])
                    sLat.append(lat[i])
                    sLon.append(lon[j])
                    v1.append(varible[0, i, j])
                    v2.append(varible[1, i, j])
                    v3.append(varible[2, i, j])
                    v4.append(varible[3, i, j])
                    v5.append(varible[4, i, j])
        print(len(sLat),len(sLon))
        #data={"lon":sLon,"lat":sLat,"1981-01":v1,"1981-02":v2,"1981-03":v3,"1981-04":v4,"1981-05":v5}
        dataF=pd.DataFrame({"lon":sLon,"lat":sLat,"1981-01":v1,"1981-02":v2,"1981-03":v3,"1981-04":v4,"1981-05":v5})
        dataF.to_csv("/home/darwin/Escritorio/chirps.csv",sep=";")
        ##datos=pd.DataFrame(sLat,sLon,v1,v2,v3,v4,v5)


lonp=78.17830278
latp=0.1783027778

lnc= LoadNC()
print(lnc.readNc("/home/darwin/Descargas/rrchirps.nc",1981))