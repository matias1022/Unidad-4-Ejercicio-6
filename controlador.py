from classProvincia import Provincia
from classVistas import ProvincesView, NewProvince
from classManejador import ManejadorProvincias
class ControladorProvincias(object):
    def __init__(self, repo, vista):
        self.repo = repo
        self.vista = vista
        self.seleccion = -1
        self.provincias = list(repo.obtenerListaProvincias())
    # comandos de que se ejecutan a través de la vista
    def crearProvincia(self):
        nuevaProvincia= NewProvince(self.vista).show()
        if nuevaProvincia:
            provincia = self.repo.agregarProvincia(nuevaProvincia)
            self.provincias.append(provincia)
            self.vista.agregarProvincia(provincia)
    def seleccionarProvincia(self, index):
        self.seleccion = index
        provincia = self.provincias[index]
        self.vista.verProvinciaEnForm(provincia)
    def borrarProvincia(self):
        if self.seleccion==-1:
            return
        provincia = self.provincias[self.seleccion]
        self.repo.borrarProvincia(provincia)
        self.provincias.pop(self.seleccion)
        self.vista.borrarProvincia(self.seleccion)
        self.seleccion=-1
    def start(self):
        for c in self.provincias:
            self.vista.agregarProvincia(c)
        self.vista.mainloop()
    def salirGrabarDatos(self):
        self.repo.grabarDatos()