# -*- coding: utf-8 *-*
# make a variation of precipitation and temp base on the normal

#from src.model import norMBaseM as nor
#from src.controller import estacionController as st, norMbasMController as gNor
import numpy as np
import pandas as pd
class Variacion:


    def __init__(self):
        pass

    def varicionAgrega(self, nor, serie):

        datatem = serie*100

        datatem = pd.Series(((datatem )/nor.valores)-100)
        datatem = np.round(datatem.astype(np.double),0)
        return datatem.tolist()

    def variacionInstant(self, nor, serie):
        datatem = pd.Series(nor.valores - serie)
        datatem = np.round(datatem.astype(np.double), 1)
        return datatem.tolist()
