# _*_ coding: utf-8 *_*
# Autor: Daarwin Rosero Vaca
# Descripción: genera las graficas para le boletin

import pandas as pd
import numpy as np
from numpy.distutils.tests.test_exec_command import emulate_nonposix

from src.util.dbfRead import DbfRead
from src.controller import estacionController as estacionController, serieController as serieController


class UnirMchDBFMen():
    """Une los datos de las bases de la base MCH y los archivos BDF generados para el boletin"""


    def __init__(self, cfg):
        """Constructor for UnirMchDBFMen, une las estaciones por regiones"""
        self.cfg = cfg


        # print(self.estaBol)
    def LoadDBF(self,rdbf):
        self.matrixDBF = DbfRead.cleanMatrixMensual(rdbf)

    def mchDBFMensual(self, añoi, añof, tabla,seriedbf,es):
        """Consulta los datos a la base de datos mch para generar una serie de tiempo"""
        dataEsta = pd.DataFrame()
        year = np.arange(añoi, añof+1, 1)  # crea la lista de años para comparar
        """Recorre cada una de las estacioens para calcular consultar los datos"""
        estInfo = estacionController.EstacionController(self.cfg)
        serie = serieController.SerieController(self.cfg)
        head = ["codigo", "anio", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
        nulos = [np.nan]
        seriemch = pd.DataFrame()
        estCunsul = estInfo.getEstationbycod(es)  # consulta la informacion de la estacion por el codigo
        coddbf = estCunsul['municipio'][0]
        for i in range(0, len(year)):
            emptyRow = pd.DataFrame({"a": ["M0000"], "b": [-10],
                                     "c": nulos, "d": nulos, "e": nulos, "f": nulos, "g": nulos, "h": nulos,
                                     "i": nulos, "j": nulos, "k": nulos, "l": nulos, "m": nulos, "n": nulos})
            emptyRow.columns = head
            emptyRow.iat[0, 1] = year[i]
            emptyRow.iat[0, 0] = estCunsul.iat[0, 0]
            tempmch = serie.getSerie(estCunsul.iat[0, 0], year[i], year[i], tabla)
            #print(tempmch)
            tempdbf = seriedbf[(seriedbf['ANNO'] == year[i])]
            #print(tempdbf)
            if tempmch.empty:
                #busca dentro del dbf para completar los datos vacios
                if not tempdbf.empty:
                    for itera in range(2, 14):
                        if not np.isnan(tempdbf.iat[0,itera]):
                            emptyRow.iat[0, itera] = tempdbf.iat[0, itera]
            else:
                ########### dataframe filtrado
                #print("Tempdbf \n",tempdbf,"\nTempmch\n",tempmch,"\nEmpty row\n",emptyRow)
                for itera in range(2, 14):
                    emptyRow.iat[0, itera] = tempmch.iat[0, itera]
                    if not tempdbf.empty and np.isnan(emptyRow.iat[0,itera]) and not np.isnan(tempdbf.iat[0,itera]):
                        """print(emptyRow.iat[0,1],emptyRow.columns[itera],emptyRow.iat[0, itera] ," to ", tempdbf.iat[0,itera],
                              tempdbf.iat[0,0],tempdbf.columns[itera])"""
                        emptyRow.iat[0, itera] = tempdbf.iat[0,itera]
                            # seriemch[(seriemch['anio'] == thisYear)][seriemch.columns[2:14]]=temp[temp.columns[2:14]]
                # agrega los valores consultados al frame
            if i == 0:
                seriemch = emptyRow
                #seriemch = seriemch.append(emptyRow, ignore_index=True)
            else:
                seriemch = seriemch.append(emptyRow,ignore_index=True)
            #print(year[i]," datos agregados ",len(seriemch)," i ",i)
        #print("voy a imprimir los datos para la estacion ", estCunsul.iat[0, 0])
        return seriemch


    def filtromatrizDBF(self, coddbf, añoi, añof):

        seriedbf = self.matrixDBF[
            (self.matrixDBF['CODIGO'] == coddbf) & (self.matrixDBF['ANNO'] >= añoi) & (self.matrixDBF['ANNO'] <= añof)]
        return seriedbf




