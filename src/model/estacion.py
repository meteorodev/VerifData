# -*- coding: utf-8 *-*
class Estacion:

    def __init__(self,codigo,codV,nombre,latitud,longitud,
                 altitud):
        self.codigo = codigo
        self.codV=codV
        self.nombre = nombre
        self.latitud = latitud
        self.longitud=longitud
        self.altitud=altitud
        self.infra="S/N"
        self.estado="S/N"