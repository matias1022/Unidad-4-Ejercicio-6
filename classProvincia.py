import re

class Provincia:
    __nombre=None
    __capital=None
    __habitantes=None
    __depart=None
    def __init__(self,nombre,capital,habitantes,depart) -> None:
        self.__nombre=self.requerido(nombre, 'Nombre de Provincia es un valor requerido')
        self.__capital=self.requerido(capital, 'Capital es un valor requerido')
        self.__habitantes=self.formatoValidoNum(habitantes, 'Cantidad de Habitantes no tiene formato numerico')
        self.__depart=self.formatoValidoNum(depart, 'Cantidad de Departamentos/Partidos no tiene formato numerico')
    def getNombre(self):
        return self.__nombre
    def getCapital(self):
        return self.__capital
    def getHab(self):
        return self.__habitantes
    def getDep(self):
        return self.__depart
    def requerido(self,atributo,mensaje):
        if not atributo:
            raise ValueError(mensaje)
        return atributo
    def formatoValidoNum(self, valor, mensaje):
        if not valor or not valor.isnumeric():
            raise ValueError(mensaje)
        return valor
    def __gt__(self,otro):
        return (self.getNombre().upper()>otro.getNombre().upper())
    def toJSON(self):
        d = dict(
            __class__=self.__class__.__name__,
            __atributos__=dict(
                        nombre=self.__nombre,
                        capital=self.__capital,
                        habitantes=self.__habitantes,
                        depart=self.__depart
                        )
                )
        return d