# -*- coding: utf-8 *-*
import MySQLdb
import pandas as pd

class MchConect:
    nombremod = __name__

    def __init__(self,db_host,db_user,db_pass,db_name):
        self.db_host = db_host
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name

    def consulta(self, sent=''):
        #print(self.db_host, self.db_user, self.db_pass, self.db_name)
        datos = [self.db_host, self.db_user, self.db_pass, self.db_name]

        conn = MySQLdb.connect(*datos)  # Conectar a la base de datos
        cursor = conn.cursor()  # Crear un cursor
        cursor.execute(sent)  # Ejecutar una consulta

        if sent.upper().startswith('SELECT'):
            data = cursor.fetchall()  # Traer los resultados de un select
        else:
            conn.commit()  # Hacer efectiva la escritura de datos
            data = None

        cursor.close()  # Cerrar el cursor
        conn.close()  # Cerrar la conexión

        return data

    def pdConsulta(self,sent=''):
        # print(self.db_host, self.db_user, self.db_pass, self.db_name)
        datos = [self.db_host, self.db_user, self.db_pass, self.db_name]

        conn = MySQLdb.connect(*datos)  # Conectar a la base de datos
        data = pd.read_sql(sent,con=conn)
        conn.close()
        return data