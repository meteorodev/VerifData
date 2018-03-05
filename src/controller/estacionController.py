# -*- coding: utf-8 *-*
from src.model import estacion
from src.util import mchConect
class EstacionController:
    def __init__(self,cfg):
        self.mch = mchConect.MchConect(cfg.db_host,cfg.db_user,cfg.db_pass,cfg.db_name)

    #devuelve la informacion de una estacion dado el codigo
    def getEstationbycod(self, cod):
        station = self.mch.pdConsulta("select estacion, municipio, nombreEstacion, latitud2"+
                                    ",longitud2,altitud from estaciones where estacion= '"+ cod +"';")
        return station
    def getListCod(self, tabla="v0001",minAños=20):
        """ devuelve un listado de cosigos de la tabal que tenga minimo minAños de datos:
                tabla: tabla de consulta de datos -*opcional*- valor defect: v0001
                minaños :el numero de años minimo que debe haber en la tabla -*opcional*- valor defect: 20
                """
        codLis = self.mch.pdConsulta("select codigo, count(codigo) as datos from "+tabla+" group by codigo having"
                                    " count(codigo) > "+str(minAños)+" ;")
        return codLis