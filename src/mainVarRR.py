# -*- coding: utf-8 *-*
from src.util import openConfig as cfgdb
from src.controller import estacionController as st, serieController as gNor
from src.process import variacion as var
from src.model import norMBaseM as norM,estacion as estas
import pandas as pd
import numpy as np
import csv
cfg = cfgdb.configDB()
cfg.readConfig("/home/drosero/Documentos/.drvmysql.cnf")
#End conect
tabla="v0001"
framaVariacion = pd.DataFrame
estCon  = st.EstacionController(cfg)
#obtener un listado de estaciones de precipitacion
lisCodRR = estCon.getListCod("V0001",20)
print(type(lisCodRR))
conteo =0
index=[]
d=[]
varsEsta=[]
for i in range(0,lisCodRR.__len__()):
    varsA = []
    varsB = []
    varsC = []
    varsD = []
    codE = lisCodRR.iloc[i][0]
    añoini = 1981
    añofin = 2010
    getestacion = estCon.getEstationbycod(codE)
    #from ENSO work
    normal = gNor.SerieController(cfg)
    serieRR = normal.getSerie(codE,añoini,añofin,tabla)
    normalRR = normal.MakeNormal(serieRR)
    estacion = estas.Estacion(getestacion["estacion"],getestacion["municipio"],getestacion["nombreEstacion"]\
                             ,getestacion["latitud2"],getestacion["longitud2"],getestacion["altitud"])
    ##Normal en base a la tabla mensual
    #print(estacion.codigo)
    #print(normalRR)
    norm = norM.NorMBaseM(estacion,[añoini,añofin],normalRR)

    #periodo de la niña a analizar
    if norm.hayNormal:
        #Variacion para el periodo 1973 - 1976
        añoini = 1973
        añofin = 1976
        serieA = normal.getSerie(codE,añoini,añofin,tabla)
        #print(str(añofin-añoini),"lon ",len(serieA),"type ",type(serieA),"Serie ........\n")#,serieA)
        tama = añofin-añoini+1
        tamS = serieA.__len__()

        for i in range(0, tama):
            temFram = serieA.loc[serieA['anio'] == (añoini + i)]
            if temFram.__len__() > 0:
                #print("el año existe ", temFram.iloc[0][2:])
                varsA.extend(var.Variacion().varicionAgrega(norm, temFram.iloc[0][2:]))
            else:
                #print("El año no existe llenar con nan ")
                vacio = np.empty(12)
                vacio[:] = np.nan
                varsA.extend(vacio)
        #print(varsA)
        #print(norm.valores)
        #print(serieA)
        #print(varsA)
        #Variacion para el periodo 2005 - 2006
        añoini = 2005
        añofin = 2006
        serieB = normal.getSerie(codE,añoini,añofin,tabla)
        tama = añofin - añoini + 1
        tamS = serieB.__len__()
        for i in range(0, tama):
            temFram = serieB.loc[serieB['anio'] == (añoini + i)]
            if temFram.__len__() > 0:
                # print("el año existe ", temFram.iloc[0][2:])
                varsB.extend(var.Variacion().varicionAgrega(norm, temFram.iloc[0][2:]))
            else:
                # print("El año no existe llenar con nan ")
                vacio = np.empty(12)
                vacio[:] = np.nan
                varsB.extend(vacio)
        #varsB=var.Variacion().varicionAgrega(norm,serieB.iloc[0][2:])
        #print(serieB)
        #print(varsB)
        #Variacion para el periodo 2008 - 2009
        añoini = 2008
        añofin = 2009
        serieC = normal.getSerie(codE,añoini,añofin,tabla)
        tama = añofin - añoini + 1
        tamS = serieC.__len__()

        for i in range(0, tama):
            temFram = serieC.loc[serieC['anio'] == (añoini + i)]
            if temFram.__len__() > 0:
                # print("el año existe ", temFram.iloc[0][2:])
                varsC.extend(var.Variacion().varicionAgrega(norm, temFram.iloc[0][2:]))
            else:
                # print("El año no existe llenar con nan ")
                vacio = np.empty(12)
                vacio[:] = np.nan
                varsC.extend(vacio)
        #varsC=var.Variacion().varicionAgrega(norm,serieC.iloc[0][2:])
        #print(serieC)
        #print(varsC)
        #Variacion para el periodo 2010 - 2012
        añoini = 2010
        añofin = 2012
        serieD = normal.getSerie(codE,añoini,añofin,tabla)
        tama = añofin - añoini + 1
        tamS = serieD.__len__()
        for i in range(0, tama):
            temFram = serieD.loc[serieD['anio'] == (añoini + i)]
            if temFram.__len__() > 0:
                # print("el año existe ", temFram.iloc[0][2:])
                varsD.extend(var.Variacion().varicionAgrega(norm, temFram.iloc[0][2:]))
            else:
                # print("El año no existe llenar con nan ")
                vacio = np.empty(12)
                vacio[:] = np.nan
                varsD.extend(vacio)
        #varsD=var.Variacion().varicionAgrega(norm,serieD.iloc[0][2:])
        #print(serieD)
        #print(varsD)


        index.append(codE)
        varsEsta=[estacion.codigo.values[0],estacion.nombre.values[0],estacion.latitud.values[0]\
                  ,estacion.longitud.values[0],estacion.altitud.values[0]]
        varsEsta.extend(varsA)
        varsEsta.extend(varsB)
        varsEsta.extend(varsC)
        varsEsta.extend(varsD)
        #print(len(varsA),len(varsB),len(varsC),len(varsD)," longitud total ",str(len(varsA)+len(varsB)+len(varsC)+len(varsD)))
        d.append(varsEsta)


        #print(d)
        conteo = conteo+1
    else:
        print("No se puede calcular la variación para la estacion ", estacion.codigo.values[0])
#end FOR

print("procesados ",conteo)

#wirte like a file
#print(type(d),len(d),"\n",d)

for i in range(0,len(d)):
    print(d[i])

with open("VarRRniña1.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in d:
        writer.writerow(val)

with open("VarRRniña.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n',delimiter=';')
    writer.writerows(d)