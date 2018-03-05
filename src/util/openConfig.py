# -*- coding: utf-8 *-*

# read a configuration db file a put this credentias into mchclass
from distutils.command.config import config
import os.path


class configDB:
    db_host = ""
    db_user = ""
    db_pass = ""
    db_name = ""

    def __init__(self):
        pass

    # self.db_host = db_host
    # self.db_user = db_user
    # self.db_pass = db_pass
    # self.db_name = db_name

    def readConfig(self, ruta):

        if os.path.exists(ruta):
            config = open(ruta)

            while True:
                linea = config.readline()  # lee línea
                # print(linea)
                #  Muestra la línea leída
                if not linea:
                    break  # Si no hay más se rompe bucle
                else:
                    valores = linea.split("=")
                    # print(valores[0],"  ", valores[1])
                    if valores[0].strip() == "host":
                        self.db_host = valores[1].strip()
                    elif valores[0].strip() == "user":
                        self.db_user = valores[1].strip()
                    elif valores[0].strip() == "password":
                        self.db_pass = valores[1].strip()
                    elif valores[0].strip() == "database":
                        self.db_name = valores[1].strip()
            config.close
        else:
            print("No existe el archivo de configuracion ", ruta)

    def makeCfgFile(self, ruta):
        # Open a file
        ruta = ruta+".cnf"
        fo = open(ruta, "w")
        datos="database=mch\nhost=192.168.1.39\nuser=drosero\npassword=darwin"
        fo.write(datos)

        # Close opend file
        fo.close()