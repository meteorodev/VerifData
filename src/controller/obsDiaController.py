# -*- coding: utf-8 *-*
# Descripción
# consulta la tabla clm002 que contienen la información de las
# observaciones diarias en las tres horas de observacion 7,13 y 19 horas

from src.util import mchConect
import time as t
class ObsDiaController:

    def __init__(self,cfg):
        self.mch = mchConect.MchConect(cfg.db_host,cfg.db_user,cfg.db_pass,cfg.db_name)

    #obtine toda la informacion disponible de una estacion dado el codigo, el año y el mes
    def getObsInf(self,codigo='M0001',ai=1900,af=t.localtime()[0],mi=1,mf=t.localtime()[1]):
        """ Obtine la informacion de la tabla clm002 dado como parametros
        codigo :el codigo de la estacion -*obligatorio*- codigo de 4 digito ej: M0001
        ai: año de inicio de la consulta de datos -*opcional*- valor defecto: 1900
        af: año de fin de la consulta de datos -*opcional*- valor defecto: año del sistema
        mi: mes de inicio de la consulta de datos -*opcional*- valor defecto: 1 refiriendoce a enero
        mf: mes de fin de la consulta de datos -*opcional*- valor defecto: mes del sistema
         """
        sentencia = "select codigo, anio, mes, dia, tmax, tmin, ts07, ts13, ts19, th07, th13, th19, rr07, rr13, " \
                    "rr19, ev07, ev071, ev13, ev131, ev19, ev191, nu07, nu13, nu19, dv07, vv07, " \
                    "dv13, vv13, dv19, vv19, an07, an13, an19 from clm0002 where codigo ='"\
                    +codigo+"' and anio >= "+str(ai)+" and anio <= "\
                    +str(af)+" and mes >= "+str(mi)+ " and mes <= "+str(mf)+" ;"
        datos = self.mch.pdConsulta(sentencia)
        print(sentencia)
        return datos
