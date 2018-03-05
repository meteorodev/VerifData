import numpy as np
from src.util import openConfig as cfgdb
from src.controller import estacionController as st, serieController as gNor


cfg = cfgdb.configDB()

cfg.readConfig("/home/drosero/Documentos/.drvmysql.cnf")
años=[1973,1974,1975,1976,1988,1989,2004,2005,2006,2008,2009,2010,2011,2012]

normal = gNor.SerieController(cfg)
serie = normal.getSerie('M0024', 2015, 2017, 'V0001')

for i in range(0, len(años)):
    print(años[i],type(años[i]))

serieT = normal.getSerieTrim('M0024', 2015, 2017, 'V0001')
#print(serie)
print("Serie T \n",serieT)