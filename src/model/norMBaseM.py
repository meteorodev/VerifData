# -*- coding: utf-8 *-*
#Compute the normal values base on mounthly values
from src.model import estacion as e
import numpy as np
class NorMBaseM:
    #estacion
    valores = []
    periodo = []
    def __init__(self,estacion,per,val):
        self.estacion=estacion
        self.periodo=per
        self.valores = val
        self.hayNormal = self.isNormal()

    def consulta(self):
        pass

    def isNormal(self):
        count = np.count_nonzero(np.isnan(self.valores))
        #print(count)
        if count > 4:
            return False
        else:
            return True
