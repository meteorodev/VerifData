# -*- coding: utf-8 *-*

from src.util import openConfig as cfgdb
from src.controller import estacionController as st, serieController as gNor
from src.process import variacion as var
from src.model import norMBaseM as norM,estacion as estas
import pandas as pd
import numpy as np
import csv ,warnings, os, sys

cfg = cfgdb.configDB()

cfg.readConfig("/home/drosero/Documentos/.drvmysql.cnf")
#End conect
etiqueta = ["codigo","nombre","latitud","Longitud","Altitud"]
meses=["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]
años=[1973,1974,1975,1976,1988,1989,2004,2005,2006,2008,2009,2010,2011,2012]
for b in range(0,len(años)):
    for c in range(0,12):
        etiqueta.append(meses[c]+str(años[b]))


def unirVariacion(codE, añoini, añofin, tabla, norm,extr,tempe):
    normal = gNor.SerieController(cfg)
    if extr == True:
        serie = normal.getSerieDos(codE, añoini, añofin, tabla)
    else:
        serie = normal.getSerie(codE, añoini, añofin, tabla)
    tama = añofin - añoini + 1
    tamS = serie.__len__()
    varia = []
    for i in range(0, tama):
        temFram = serie.loc[serie['anio'] == (añoini + i)]
        if temFram.__len__() > 0:
            if tempe == True:
                varia.extend(var.Variacion().variacionInstant(norm, temFram.iloc[0][2:]))
            else:
                varia.extend(var.Variacion().varicionAgrega(norm, temFram.iloc[0][2:]))
        else:
            vacio = np.empty(12)
            vacio[:] = np.nan
            varia.extend(vacio)
    return varia

def totrime(vars,años):
    data=[]
    etiTrim=["codigo","nombre","latitud","Longitud","Altitud"]
    trim=["EFM","AMJ","JAS","OND"]
    for b in range(0, len(años)):
        for c in range(0, len(trim)):
            etiTrim.append(trim[c] + str(años[b]))
    data.append(etiTrim)
    for i in range(1,len(vars)):
        vtem=vars[i]
        etiTrim = vtem[0:5]
        #print(vtem)
        for j in range(5,len(vtem),3):
            vtemp = np.array(vtem[j:(j+3)])
            vtemp=vtemp[~np.isnan(vtemp)]
            with warnings.catch_warnings():
                warnings.filterwarnings('error')
                try:
                    x = np.around(np.mean(vtemp),1)
                except RuntimeWarning:
                    x = np.nan
            etiTrim.extend([x])
            #print("\ndatos......................\n mean(",vtemp,") = ",np.mean(vtemp),"  sin nan ")
        #print(len(etiTrim)," -- -- -- ",etiTrim)
        data.append(etiTrim)
    return data

def getTrimes(codE,años,tabla):
    trim=[]
    normal = gNor.SerieController(cfg)
    for i in range(0,len(años)):
        trim.extend(normal.getSerieTrim(codE, años[i], años[i], tabla))
    return trim

def totrimeOBS(vars, años, tabla):
    data=[]
    etiTrim=["codigo","nombre","latitud","Longitud","Altitud"]
    trim=["EFM-O","AMJ-O","JAS-O","OND-O"]
    for b in range(0, len(años)):
        for c in range(0, len(trim)):
            etiTrim.append(trim[c] + str(años[b]))
    data.append(etiTrim)
    for i in range(1,len(vars)):
        vtem=vars[i]
        etiTrim = vtem[0:5]
        #print(vtem)
        etiTrim.extend(getTrimes(vtem[0], años, tabla))
        #print(trim)
        conteo=0
        data.append(etiTrim)
    return data


def mergeTrimNor(data1, tabla):
    normal = gNor.SerieController(cfg)
    data = []
    etiTrim = ["codigo", "nombre", "latitud", "Longitud", "Altitud"]
    trim = ["EFM-V", "EFM-N", "AMJ-V", "AMJ-N", "JAS-V", "JAS-N", "OND-V", "OND-N"]
    for b in range(0, len(años)):
        for c in range(0, len(trim)):
            etiTrim.append(trim[c] + str(años[b]))
    data.append(etiTrim)
    añoini = 1981
    añofin = 2010
    for i in range(1, len(data1)):
        # from ENSO work
        vtmp = data1[i]
        serieRR = normal.getSerieDos(vtmp[0], añoini, añofin, tabla)
        normalRR = normal.MakeNormal(serieRR)
        #print( i, " normal de  ", vtmp[0], "\n", np.round(np.mean(normalRR.iloc[0:3]), 1), sep="")
        #print(len(vtmp)," * ",vtmp," \n",len(vtmpo), " *",vtmpo)
        etiTrim = vtmp[0:5]
        cont=0
        for j in range(5,len(vtmp)):
            if cont == 12:
                cont = 0
            etiTrim.extend([vtmp[j]])
            etiTrim.extend([np.round(np.mean(normalRR.iloc[cont:(cont+3)]), 1)])
            cont=cont+3
                #etiTrim
        data.append(etiTrim)

    return data

def toYears(vars,años):
    data = []
    etiAño = ["codigo", "nombre", "latitud", "Longitud", "Altitud"]
    etiAño.extend(años)
    data.append(etiAño)
    for i in range(1,len(vars)):
        vtem = vars[i]
        etiAño=vtem[0:5]
        for j in range(5,len(vtem),12):
            vtemp = np.array(vtem[j:(j + 12)])
            vtemp = vtemp[~np.isnan(vtemp)]
            with warnings.catch_warnings():
                warnings.filterwarnings('error')
                try:
                    x = np.around(np.mean(vtemp),1)
                except RuntimeWarning:
                    x = np.nan

            etiAño.extend([x])
            #print(len(vtemp)," <-> ",vtemp,"  ...  ",x)
        data.append(etiAño)
    return data


def writeCSV(nombrArc,d):
    with open(nombrArc, "w") as output:
        writer = csv.writer(output, lineterminator='\n', delimiter=';')
        writer.writerows(d)

def makeVarArchi(tabla,vec,extr,tempe):
    d=[vec]
    conteo = 0
    varsEsta = []
    estCon = st.EstacionController(cfg)
    lisCodRR = estCon.getListCod(tabla, 20)
    for i in range(0, lisCodRR.__len__()):
        codE = lisCodRR.iloc[i][0]
        añoini = 1981
        añofin = 2010
        # obtener un listado de estaciones de temp
        getestacion = estCon.getEstationbycod(codE)
        # from ENSO work
        normal = gNor.SerieController(cfg)
        serieRR = normal.getSerieDos(codE, añoini, añofin, tabla)
        normalRR = normal.MakeNormal(serieRR)
        estacion = estas.Estacion(getestacion["estacion"], getestacion["municipio"], getestacion["nombreEstacion"] \
                                  , getestacion["latitud2"], getestacion["longitud2"], getestacion["altitud"])
        norm = norM.NorMBaseM(estacion, [añoini, añofin], normalRR)
        if norm.hayNormal:
            varsEsta = [estacion.codigo.values[0], estacion.nombre.values[0], estacion.latitud.values[0] \
                , estacion.longitud.values[0], estacion.altitud.values[0]]
            varsEsta.extend(unirVariacion(codE, 1973, 1976, tabla, norm,extr,tempe))
            varsEsta.extend(unirVariacion(codE, 1988, 1989, tabla, norm, extr,tempe))
            varsEsta.extend(unirVariacion(codE, 2004, 2006, tabla, norm,extr,tempe))
            varsEsta.extend(unirVariacion(codE, 2008, 2009, tabla, norm,extr,tempe))
            varsEsta.extend(unirVariacion(codE, 2010, 2012, tabla, norm,extr,tempe))
            d.append(varsEsta)
            conteo = conteo + 1
        #else:
        #    print("No se puede calcular la variación para la estacion ", estacion.codigo.values[0])
    # end FOR
    print("procesados ", conteo,"\n\n")
    return d #Fin funcion del archivo variaciones de tablas de estremas

# data = makeVarArchi("V0009",etiqueta,True,True)
# writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarTXExtMen.csv",data)
# datatrim=totrime(data,años)
# writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarTXExtTrim.csv",datatrim)
# dataY=toYears(data,años)
# writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarTXExtAño.csv",dataY)
#
# data = makeVarArchi("V0010",etiqueta,True,True)
# writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarTNExtMen.csv",data)
# datatrim=totrime(data,años)
# writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarTNExtTrim.csv",datatrim)
# dataY=toYears(data,años)
# writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarTNExtAño.csv",dataY)
#
#data = makeVarArchi("V0011",etiqueta,False,True)
#writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarTXMedMen.csv",data)
#datatrim=totrime(data,años)
#writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarTXMedTrim.csv",datatrim)
#dataY=toYears(data,años)
#writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarTXMedAño.csv",dataY)
#
#data = makeVarArchi("V0012",etiqueta,False,True)
#writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarTNMedMen.csv",data)
#datatrim=totrime(data,años)
#writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarTNMedTrim.csv",datatrim)
#dataY=toYears(data,años)
#writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarTNMedAño.csv",dataY)

#data = makeVarArchi("V0001", etiqueta, False, False)
#writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarRRMen.csv",data)
#datatrim=totrime(data,años)
#writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarRRTrim.csv",datatrim)
#dataY=toYears(data,años)
#writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarRRAño.csv",dataY)



#modifocacion para generar las anomalias y datos observados
data = makeVarArchi("V0011",etiqueta,False,True)
datatrimv=totrime(data, años)
writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarTXMedTrim.csv",datatrimv)
datatrimo = totrimeOBS(data, años, "V0011")
writeCSV("/media/drosero/Datos/QGIS/Niña/datos/ObsTXMedTrim.csv",datatrimo)
datatrim=mergeTrimNor(datatrimo, "V0011")
writeCSV("/media/drosero/Datos/QGIS/Niña/datos/ObsNorTXMedTrim.csv",datatrim)

#
data = makeVarArchi("V0012",etiqueta,False,True)
datatrimv=totrime(data,años)
writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarTNMedTrim.csv",datatrimv)
datatrimo = totrimeOBS(data, años, "V0012")
writeCSV("/media/drosero/Datos/QGIS/Niña/datos/ObsTNMedTrim.csv",datatrimo)
datatrim=mergeTrimNor(datatrimo,"V0012")
writeCSV("/media/drosero/Datos/QGIS/Niña/datos/ObsNorTNMedTrim.csv",datatrim)
#
data = makeVarArchi("V0001", etiqueta, False, False)
datatrimv = totrime(data,años)
writeCSV("/media/drosero/Datos/QGIS/Niña/datos/VarRRTrim.csv",datatrimv)
datatrimo = totrimeOBS(data, años, "V0001")
writeCSV("/media/drosero/Datos/QGIS/Niña/datos/ObsRRTrim.csv",datatrimo)
datatrim = mergeTrimNor(datatrimo,"V0001")
writeCSV("/media/drosero/Datos/QGIS/Niña/datos/ObsNorRRTrim.csv",datatrim)
