# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Descripción:
#striming API token: p7wjs231co
#api key: hjS0GbiygSn15V8wF0UK

import plotly as py
#from plotly.graph_objs import *
import plotly.graph_objs as go
import numpy as np
class PlotyUse():
    """"""

    def __init__(self,):
        """Constructor for PlotyUse"""
        py.tools.set_credentials_file(username='darwin11rv',api_key='hjS0GbiygSn15V8wF0UK')
    def saludo(self,nombre):
        print("Hola ",nombre)

    def plotyOnline(self):
        trace0 = go.Scatter(
            x=[1, 2, 3, 4],
            y=[10, 15, 13, 17]
        )
        trace1 = go.Scatter(
            x=[1, 2, 3, 4],
            y=[16, 5, 11, 9]
        )
        data = go.Data([trace0, trace1])

        py.plotly.plot(data, filename='basic-line')
    def plotyOffline(self):
        print(py.__version__)
        py.offline.plot({
            "data": [go.Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
            "layout": go.Layout(title="hello world")
        })
        #basic histogram
        x = np.random.randn(500)
        data = [go.Histogram(x=x)]
        py.offline.plot(data)
    def boxplot(self):
        y0 = np.random.randn(50)-1
        y1 = np.random.randn(50)+1

        enero = go.Box(
            y=y0
        )
        febrero = go.Box(
            y=y1
        )
        print(enero)
        data = [enero, febrero]
        py.offline.plot(data)


p=PlotyUse()
p.saludo("Darwin")
#p.plotyOnline()
#p.plotyOffline()
p.boxplot()

