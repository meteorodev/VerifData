# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Descripción:

from src.process import unirMchDBFMen as unir, normales as norM
from src.util import openConfig as cfgdb
from src.controller import estacionController as esController, serieController as serieController
import pandas as pd
import numpy as np
import os.path as pth

class FillMounthSerie():
    """This class search into de database a estation and fill empty data firts with dbf files, and then fill whit chirps datset """


    def __init__(self,):
        """Constructor for FillMounthSerie"""
    def getSerie(self):
        print("Serie")