# -*- coding: utf-8 *-*

from src.util import openConfig as cfgdb
from src.controller import estacionController as st, serieController as gNor
#from src.controller import obsDiaController as thd
from src.process import variacion as var
from src.model import norMBaseM as norM,estacion as estas
import pandas as pd
from IPython.display import display, HTML
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
varsA=[]
varsB=[]
varsC=[]
varsD=[]
for i in range(0,lisCodRR.__len__()):
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
        serieA = normal.getSerie(codE,1973,1976,tabla)
        varsA=var.Variacion().varicionAgrega(norm, serieA)
        #print(norm.valores)
        #print(serieA)
        #print(varsA)
        #Variacion para el periodo 2005 - 2006
        serieB = normal.getSerie(codE,2005,2006,tabla)
        varsB=var.Variacion().varicionAgrega(norm, serieB)
        #print(serieB)
        #print(varsB)
        #Variacion para el periodo 2008 - 2009
        serieC = normal.getSerie(codE,2008,2009,tabla)
        varsC=var.Variacion().varicionAgrega(norm, serieC)
        #print(serieC)
        #print(varsC)
        #Variacion para el periodo 2010 - 2012
        serieD = normal.getSerie(codE,2010,2012,tabla)
        varsD=var.Variacion().varicionAgrega(norm, serieD)
        #print(serieD)
        #print(varsD)
        ##
        ## cambiar esto a lista. ojo
        ##
        ##
        index.append(codE)
        varsEsta=[getestacion["estacion"].values[0],getestacion["municipio"].values,getestacion["nombreEstacion"].values\
                             ,getestacion["latitud2"].values,getestacion["longitud2"].values,getestacion["altitud"].values]
        varsEsta.extend(varsA)
        varsEsta.extend(varsB)
        varsEsta.extend(varsC)
        varsEsta.extend(varsD)
        d.append(varsEsta)
        #print(d)
        conteo = conteo+1
    else:
        print("No se puede calcular la variación para la estacion ", estacion.codigo)
#end FOR

print("procesados ",conteo)

#wirte like a file
print(type(d),len(d),"\n",d)

data=d
print(data)
out = csv.writer(open("VarRRniña.csv","w"), delimiter=';',quoting=csv.QUOTE_ALL)
out.writerow(data)