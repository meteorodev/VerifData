# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Descripción:
import numpy as np
import pandas as pd

class Normales():
    """Esta clase genera las normales decadales mensuales trimestrales y anuales para las series dadas """

    def __init__(self,):
        """Constructor for Normales"""

    def normalMensual(self, serie, porcent=50,ai=1981,af=2010):
        """ Genera las normales dado un porcentaje de datos faltantes:
        serie: tabla de consulta de datos -*obligatorio*- codigo de 4 digito ej: V0001
        porcent :el porcentaje de datos faltantes permitido por mes -*opcional*- valor defect: 10
        ai: año de inicio -*Opcional*- valor defecto 1981
        ai: año de fin -*Opcional*- valor defecto 2010
        """
        porComp=100-porcent
        pn=af-ai +1
        tam = len(serie)
        vacioIni = 100 - int(tam*100/pn)
        naMes=serie.isnull().sum()
        #print("periodo -", pn, "- longitud serie -", tam, "- porcentaje vacio datos -", vacioIni, \
        #      " porcen comparar -", porComp)
        #print(naMes)
        ##calcula el porcentaje total de vacio por mes
        naMes=naMes[2:]
        naMes=np.around(100-(tam - naMes)*100/pn)
        #print(naMes)
        if porComp > vacioIni:
            #print(serie.iloc[0: ,[1]])
            normaCom = np.around(np.mean(serie[serie.columns[2:]]), 1)
            #print(len(normaCom))
            compr=np.where(naMes > porcent)
            normaCom.iloc[compr] = np.nan
            #print(compr)
            #print(normaCom)
            #print(np.around(normaCom,decimals=1))
        else:
            normaCom = np.empty((1, 12,))
            normaCom[:] = np.nan
        ## make dataframe
        normaCom=pd.DataFrame(normaCom).T
        return normaCom

