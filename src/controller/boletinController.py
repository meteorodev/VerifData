# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Descripción:

from src.process import unirMchDBFMen as unir, normales as norM
from src.util import openConfig as cfgdb
from src.controller import estacionController as esController, serieController as serieController
import pandas as pd
import numpy as np
import os.path as pth


class BoletinController():
    """ Genera estadisticas de las estaciones del boletin a manera mensual"""

    estaBolCosta = ['M0058', 'M0025', 'M0026', 'M0005', 'M0006', 'M0037', 'M0056', 'M0183']
    estaBolSierra = ['M0103', 'M0001', 'M1094', 'M0024', 'M0002', 'M0003', 'M0064', 'M0123', 'M0004', 'M0066', 'M0258',
                     'M0031', 'M0067', 'M0033', 'M0060']
    estaBolOriente = ['M0061', 'M0052', 'M0007', 'M0063', 'M0008', 'M0062']
    estaBolGalapagos = ['M0221']
    estaBol = []
    udb = None
    mchConsul = None

    def __init__(self,):
        """Constructor for BoletinController"""
        cfg = cfgdb.configDB()
        cfg.readConfig("/home/drosero/Documentos/.drvmysql.cnf")
        self.cfg = cfg
        self.uneEstaciones()
        self.udb = unir.UnirMchDBFMen(self.cfg)
        self.esConexion = esController.EstacionController(self.cfg)
        self.conecmch = serieController.SerieController(self.cfg)

    def uneEstaciones(self):
        self.estaBol.extend(self.estaBolCosta)
        self.estaBol.extend(self.estaBolSierra)
        self.estaBol.extend(self.estaBolOriente)
        self.estaBol.extend(self.estaBolGalapagos)


    def normalMensual(self,añoiN,añofN,codEsta = estaBol, rutadbf="/" ,tabla="V0001"):
        """Genramos las normales para cada estacion del boletin
            y las almacena en un dataframe
            @parametros
            añoiN= año de inicio para el calculo de la normal
            añofN= año de fin para el calculo de la normal
            estaciones = listado de estaciones para procesar
            rutadbf = ruta del archivo dbf para completar la consulta de la base mch
            tabla = tabla para realizar la consulta de la base de datos
        """
        getNormal = norM.Normales()
        if pth.exists(rutadbf):
            self.udb.LoadDBF(rutadbf)

        else:
            print("Archivo .DBF no encontrado......")
            print("Necesito el archivo DBF para completar \n",
                  "solo se consultara la base de datos MCH")

        ##recorre cada estacion para consultar los valores
        normalesdf= pd.DataFrame()
        for es in codEsta:
            estaConsul = self.esConexion.getEstationbycod(es)
            if pth.exists(rutadbf):
                # generar la serie desde el dbf
                seriedbf = self.udb.filtromatrizDBF(estaConsul.iat[0, 1], añoiN, añofN)
                # crear serie base
                serie = self.udb.mchDBFMensual(añoiN, añofN, tabla, seriedbf, estaConsul.iat[0, 0])
            else:
                serie = self.conecmch.getSerie( estaConsul.iat[0, 0], añoiN, añofN, tabla)
            #serie.iloc[:,2:14].plot()
            #plt.show()
            #generar normal de la serie base
            normal=getNormal.normalMensual(serie)
            estaConsul = pd.concat([estaConsul,normal],axis=1)
            #staked = pd.concat(estaConsul,normal)
            normalesdf=normalesdf.append(estaConsul)
        #print("fin del metodo.....")
        return normalesdf


    def getVariacionMensual(self,añoCom,normales ,tabla,completarDbf = True, agregada=True):
        """Genramos genera la variación las normales para cada estacion del boletin
                    y las almacena en un dataframe
                    @parametros
                    añoiN = año de inicio para el calculo de la normal
                    añofN = año de fin para el calculo de la normal
                    estaciones = listado de estaciones para procesar
                    rutadbf = ruta del archivo dbf para completar la consulta de la base mch
                    tabla = tabla para realizar la consulta de la base de datos
                    añoCom = año para comparar con la normal
                    completarDbf = True Para buscar datos dentro de la matrizDBF
                    aggragada = True  Variables de agracacion como precipitacion
                """
        #recorre el listado de estaciones
        conteo=0
        tempHead=["codigo", "anio", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
        varHead = ["codigo", "anio", "s_ene", "s_feb", "s_mar", "s_abr", "s_may", "s_jun", "s_jul", "s_ago", "s_sep", "s_oct", "s_nov", "s_dic"
            , "v_ene", "v_feb", "v_mar", "v_abr", "v_may", "v_jun", "v_jul", "v_ago", "v_sep", "v_oct", "v_nov", "v_dic"]
        nlis=map(lambda x: "a"+x,tempHead)
        tablaVaria = pd.DataFrame()
        nuevo = True
        for i in range(0,len(normales)):
            serieVar = None
            for ac in añoCom:
                #print(ac,normales.iat[i,1])
                serieComp = self.conecmch.getSerie(normales.iat[i,0], ac, ac, tabla)
                if (completarDbf): ## busca dentro de las tablas de dbf
                    seriedbf = self.udb.matrixDBF[(self.udb.matrixDBF['ANNO'] == ac) & (self.udb.matrixDBF['CODIGO'] == normales.iat[i,1])]
                    if serieComp.empty:
                        seriedbf.columns=tempHead
                        serieComp = pd.concat([serieComp,seriedbf])
                        serieComp.iat[0, 0] = normales.iat[i,0]
                        serieComp.iat[0, 1] = ac
                    else:
                        for j in range(2,14):
                            serieComp.iat[0,j]=seriedbf.iat[0,j]

            #calcula la anomalia para variables de agregacion mediante
                #self.printDF(serieComp,"serieComp")
                if agregada:
                    serieVar = ((serieComp.iloc[0,2:14]*100)/normales.iloc[i,6:18])-100
                    serieVar = np.round(serieVar.astype(np.double), 1)
                else:
                    serieVar = normales.iloc[i, 6:18] - serieComp.iloc[0, 2:14]
                    serieVar = np.round(serieVar.astype(np.double), 1)

                serieVar = pd.DataFrame(serieVar,index=tempHead[2:14]).T
                #self.printDF(serieVar, "serieVar")
                data = np.append(serieComp.values,serieVar.values)
                #self.printDF(data, "data")
                varDf = pd.DataFrame(data,index=varHead).T
                if nuevo:
                    tablaVaria = varDf
                    nuevo = False
                else:
                    tablaVaria = tablaVaria.append(varDf, ignore_index=True)

        #self.printDF(tablaVaria,"tablavaria")

        return tablaVaria

    def printDF(self,df,nombre):
        print("##########",nombre,"##########\n",
              "#############################\n",
              type(df), "\n", df, sep="")

"""####ejecucion principal"""
#ruta de archivos
#rs = "/media/drosero/Datos/INAMHI/2018/Información/CIFFEN/"
rs = "/home/drosero/Escritorio/"
bc= BoletinController()
#listado = bc.estaBol

##Para precipitacion
#rdbf = "/home/drosero/Documentos/Boletin/2018/BASES/T0001.DBF"
#listado=["M0103","M0002","M0258","M0006","M0024","M1094","M0025"]
#nc=bc.normalMensual(1981,2010,listado,rdbf,tabla="V0001")
#nc.to_csv((rs+"RRNormal"), sep=';', encoding='utf-8')
#vc=bc.getVariacionMensual([2017], nc, tabla="V0001")
#vc.to_csv((rs+"RRVaria"), sep=';', encoding='utf-8')


##Para Temperatura maxima
#rdbf = "/home/drosero/Documentos/Boletin/2018/BASES/T0011.DBF"

#nc=bc.normalMensual(1981,2010,listado,rdbf,tabla="V0008")
#nc.to_csv((rs+"TMedNormal"), sep=';', encoding='utf-8')
##vc=bc.getVariacionMensual([2017], nc, tabla="V0008",agregada=False)
##vc.to_csv((rs+"TmaxVaria"), sep=';', encoding='utf-8')


##Para Temperatura maxima
"""rdbf = "/home/drosero/Documentos/Boletin/2018/BASES/T0011.DBF"

nc=bc.normalMensual(1981,2010,listado,rdbf,tabla="V0011")
nc.to_csv((rs+"TmaxNormal"), sep=';', encoding='utf-8')
vc=bc.getVariacionMensual([2017], nc, tabla="V0011",agregada=False)
vc.to_csv((rs+"TmaxVaria"), sep=';', encoding='utf-8')

##Para Temperatura minima
rdbf = "/home/drosero/Documentos/Boletin/2018/BASES/T0012.DBF"

nc=bc.normalMensual(1981,2010,listado,rdbf,tabla="V0012")
nc.to_csv((rs+"TminNormal"), sep=';', encoding='utf-8')
vc=bc.getVariacionMensual([2017], nc, tabla="V0012",agregada=False)
vc.to_csv((rs+"TminVaria"), sep=';', encoding='utf-8')

print("##########Normal calculada ##########\n",
      "#####################################\n",nc,sep="")
print("##########variacion calculada ##########\n",
      "#####################################\n",vc,sep="")"""


########estaciones de pedro mocayo

listado=["M0001", "M0009", "M0021", "M0023", "M0024", "M0105", "M0310", "M0318", "M0321", "M0328", "M0337", "M0343", "M0344",
             "M0345", "M0346", "M0357", "M0358", "M0359", "M0909", "M0910", "M1094", "M1183", "M1240", "M5021", "M5044", "M0010",
             "M0011", "M0022", "M0053", "M0055", "M0098", "M0108", "M0109", "M0110", "M0111", "M0115", "M0210", "M0211", "M0214",
             "M0264", "M0265", "M0267", "M0282", "M0285", "M0299", "M0316", "M0317", "M0319", "M0320", "M0322", "M0323", "M0329",
             "M0330", "M0331", "M0332", "M0333", "M0334", "M0338", "M0341", "M0342", "M0347", "M0356", "M0525", "M0526", "M0561",
             "M0566", "M0572", "M0573", "M0574", "M0604", "M0605", "M0618", "M0628", "M0701", "M0705", "M0714", "M0734", "M0833",
             "M0834", "M0872", "M0873", "M0874", "M0875", "M0880", "M0886", "M0911", "M0912", "M0913", "M0915", "M0939", "M0940",
             "M0941", "M0942", "M0943", "M0944", "M0945", "M0946", "M0947", "M0948", "M0949", "M0950", "M0951", "M0952", "M0953",
             "M0954", "M0955", "M0956", "M0957", "M1002", "M1012", "M1016", "M1017", "M1056", "M1057", "M1061", "M1200", "M1211",
             "M5003", "M5031", "M5035", "M5036", "M5037", "M5042", "M5043", "M5054", "M5055", "M5074", "M5088", "M5104", "M1156",
             "M1002", "M1016"]


rdbf = "/home/drosero/Documentos/Boletin/2018/BASES/T0011.DBF"
rs = "/home/drosero/Escritorio/chirps/"
nc=bc.normalMensual(1981,2010,listado,rdbf,tabla="V0011")
nc.to_csv((rs+"TmaxNormal.csv"), sep=';', encoding='utf-8')
#vc=bc.getVariacionMensual(list(range(1981,2018)), nc, tabla="V0011",agregada=False)
#vc.to_csv((rs+"TmaxVaria.csv"), sep=';', encoding='utf-8')

##Para Temperatura minima
rdbf = "/home/drosero/Documentos/Boletin/2018/BASES/T0012.DBF"

nc=bc.normalMensual(1981,2010,listado,rdbf,tabla="V0012")
nc.to_csv((rs+"TminNormal.csv"), sep=';', encoding='utf-8')
#vc=bc.getVariacionMensual(list(range(1981,2018)), nc, tabla="V0012",agregada=False)
#vc.to_csv((rs+"TminVaria.csv"), sep=';', encoding='utf-8')