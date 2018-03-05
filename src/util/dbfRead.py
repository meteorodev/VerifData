# -*- coding: utf-8 *-*
# Read dbf file an make a matrix with the data
from builtins import range

import pysal as ps
import pandas as pd
import numpy as np

class DbfRead:
    def __init__(self):
        pass

    def dbf2DFMensual(dbfile, upper=True):  # Reads in DBF files and returns Pandas DF
        db = ps.open(dbfile)  # Pysal to open DBF
        d = {col: db.by_col(col) for col in db.header}  # Convert dbf to dictionary
        # pandasDF = pd.DataFrame(db[:]) #Convert to Pandas DF
        pandasDF = pd.DataFrame(d)  # Convert to Pandas DF
        if upper == True:  # Make columns uppercase if wanted
            pandasDF.columns = map(str.upper, db.header)
        db.close()
        return pandasDF

    def cleanMatrixMensual(dbfile):
        matrixdbf = DbfRead.dbf2DFMensual(dbfile)
        #print(matrixdbf.columns.values)
        # Cambia las cabeceras
        headers = ['ANNO', 'CODIGO','ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']
        #matrixdbf.columns = headers

        value = matrixdbf.iloc[:, 14:]
        flags = matrixdbf.iloc[:, 2:14].apply(lambda y:y.apply(lambda x:x.upper()))
        codi = matrixdbf.iloc[:,0:2]
        for i in range(0,12):
            tempv = value.iloc[:, i]
            tempf = flags.iloc[:, i]
            tempv[(tempf == 'N')] = tempv[(tempf == 'N')].apply(lambda x: np.nan)
            value.iloc[:, i] = tempv

        #print(codi)
        #print(value)
        #print(flags)
        matrixdbf = codi.join(value)
        matrixdbf.columns = headers
        return matrixdbf


#rdbf = "/home/drosero/Documentos/Boletin/2018/BASES/T0001.DBF"
# matrixdbf = DbfRead.dbf2DF(rdbf)
#mt = DbfRead.cleanMatrixMensual(rdbf)

#print(".......................................")
#print(mt)
