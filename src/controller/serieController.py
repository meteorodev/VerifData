# -*- coding: utf-8 *-*
# Descripción
# consulta los datos mensuales de la base para generar la normal climatologica
from builtins import type

from src.util import mchConect
import time as t
import numpy as np # importando numpy
import pandas as pd
from scipy import stats # importando scipy.stats


class SerieController:

    def __init__(self, cfg):
        self.mch = mchConect.MchConect(cfg.db_host, cfg.db_user, cfg.db_pass, cfg.db_name)

    # obtine toda la informacion disponible de una estacion dado el codigo, el año inicial y final
    def getSerie(self, codigo='M0001', ai=1900, af=t.localtime()[0], tabla='V0001'):
        """ Obtine la informacion:
        codigo :el codigo de la estacion -*obligatorio*- codigo de 4 digito ej: M0001
        ai: año de inicio de la consulta de datos -*opcional*- valor defecto: 1900
        af: año de fin de la consulta de datos -*opcional*- valor defecto: año del sistema
        tabla: tabla de consulta de datos -*obligatorio*- codigo de 4 digito ej: V0001
         """
        sentencia = "select * from " + tabla + " where codigo ='" \
                    + codigo + "' and anio >= " + str(ai) + " and anio <= " + str(af) + ";"
        datos = self.mch.pdConsulta(sentencia)
        #print(sentencia)
        return datos

        # obtine toda la informacion disponible de una estacion dado el codigo, el año y el mes
    def getSerieTrim(self, codigo='M0001', ai=1900, af=t.localtime()[0], tabla='V0001'):
        """ Obtine la informacion:
        codigo :el codigo de la estacion -*obligatorio*- codigo de 4 digito ej: M0001
        ai: año de inicio de la consulta de datos -*opcional*- valor defecto: 1900
        af: año de fin de la consulta de datos -*opcional*- valor defecto: año del sistema
        tabla: tabla de consulta de datos -*obligatorio*- codigo de 4 digito ej: V0001
        """
        sentencia = "select * from " + tabla + " where codigo ='" \
                  + codigo + "' and anio >= " + str(ai) + " and anio <= " + str(af) + ";"
        datos = self.mch.pdConsulta(sentencia)

        trim=[]
        #print(len(datos), " =>", codigo, ai, "")
        if len(datos)==0:
            trim=[np.nan,np.nan,np.nan,np.nan]
        else:
            for i in range(0, len(datos)):
                #trim=datos.iloc[i][0:2].tolist()
                trim.extend([np.round(datos.iloc[i][2:5].mean(), 1)])
                trim.extend([np.round(datos.iloc[i][5:8].mean(), 1)])
                trim.extend([np.round(datos.iloc[i][8:11].mean(), 1)])
                trim.extend([np.round(datos.iloc[i][11:14].mean(), 1)])
            #print("data i\n","T1[",np.round(datos.iloc[i][2:5].mean(),1),"]  T2[",np.round(datos.iloc[i][5:8].mean(),1),"]  T3[",np.round(datos.iloc[i][8:11].mean(),1),
            #      "]  T4[",np.round(datos.iloc[i][11:14].mean(),1),"]",sep="")
            #print(len(trim)," =>",codigo,ai, "" , trim )
        # print(sentencia)
        return trim #dt

    def getSerieDos(self, codigo='M0001', ai=1900, af=t.localtime()[0], tabla='V0009'):
        """ Obtine la informacion de tablas con dos campos:
        codigo :el codigo de la estacion -*obligatorio*- codigo de 4 digito ej: M0001
        ai: año de inicio de la consulta de datos -*opcional*- valor defecto: 1900
        af: año de fin de la consulta de datos -*opcional*- valor defecto: año del sistema
        tabla: tabla de consulta de datos -*obligatorio*- codigo de 4 digito ej: V0001
         """

        sentencia = "select codigo, anio, ene, feb, mar, abr, may, jun, jul, ago, sep, oct, nov, dic from " + tabla + " where codigo ='" \
                    + codigo + "' and anio >= " + str(ai) + " and anio <= " + str(af) + ";"
        datos = self.mch.pdConsulta(sentencia)
        #print(sentencia)
        return datos


