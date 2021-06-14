import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk, font
from classProvincia import Provincia
import requests
class ProvinceList(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master)
        self.lb = tk.Listbox(self, **kwargs)
        scroll = tk.Scrollbar(self, command=self.lb.yview)
        self.lb.config(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    def insertar(self, provincia, index=tk.END):
        text = "{}".format(provincia.getNombre())
        self.lb.insert(index, text)
    def borrar(self, index):
        self.lb.delete(index, index)
    def modificar(self, provincia, index):
        self.borrar(index)
        self.insertar(provincia, index)
    def bind_doble_click(self, callback):
        handler = lambda _: callback(self.lb.curselection()[0])
        self.lb.bind("<Double-Button-1>", handler)

class ProvinceForm(tk.LabelFrame):
    fields = ("Nombre", "Capital", "Cantidad de Habitantes", "Cantidad de departamentos/partidos")
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Provincia", padx=10, pady=10, **kwargs)
        self.frame = tk.Frame(self)
        self.entries = list(map(self.crearCampo, enumerate(self.fields)))
        self.frame.pack()
    def crearCampo(self, field):
        position, text = field
        label = tk.Label(self.frame, text=text)
        entry = tk.Entry(self.frame, width=25)
        label.grid(row=position, column=0, pady=5)
        entry.grid(row=position, column=1, pady=5)
        return entry
    def crearProvinciaDesdeFormulario(self):
        #obtiene los valores de los campos del formulario
        #para crear un nuevo paciente
        values = [e.get() for e in self.entries]
        provincia=None
        try:
            provincia = Provincia(*values)
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e), parent=self)
        return provincia
    def limpiar(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

class UpdateProvinceForm(tk.LabelFrame):
    fields = ("Nombre", "Capital", "Cantidad de Habitantes",
    "Cantidad de departamentos/partidos","Temperatura",
    "Sensación Termica",'Humedad')
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Provincia", padx=10, pady=10, **kwargs)
        self.frame = tk.Frame(self)
        self.entries = list(map(self.crearCampo, enumerate(self.fields)))
        self.btn_delete = tk.Button(self, text="Borrar")
        self.btn_delete.pack(side=tk.BOTTOM, ipadx=5, padx=5, pady=5)
        self.frame.pack()
    def crearCampo(self, field):
        position, text = field
        label = tk.Label(self.frame, text=text)
        entry = tk.Entry(self.frame, width=25)
        label.grid(row=position, column=0, pady=5)
        entry.grid(row=position, column=1, pady=5)
        return entry
    def bind_delete(self, callback):
        self.btn_delete.config(command=callback)
    def mostrarEstadoProvinciaEnFormulario(self, provincia):
        # a partir de un paciente, obtiene el estado
        # y establece en los valores en el formulario de entrada
        datosApi=self.cargaDatos(provincia)
        values = (provincia.getNombre(), provincia.getCapital(), 
                    provincia.getHab(),provincia.getDep(),datosApi[0],datosApi[1],datosApi[2])
        for entry, value in zip(self.entries, values):
            entry.delete(0, tk.END)
            entry.insert(0, value)
    def limpiar(self):
        for entry in self.entries:
            entry.delete(0, tk.END)
    def cargaDatos(self,provincia):
        complete_url = ('http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=b319b301cdc069464b37daa716905189'.format(provincia.getNombre()))
        r = requests.get(complete_url)
        re = r.json()
        lista=["SIN DATOS","SIN DATOS","SIN DATOS"]
        if r.status_code==200 and re["sys"]["country"]=='AR':
            print(complete_url)
            lista = ['{} °C'.format(re["main"]["temp"]),
                    '{} °C'.format(re["main"]["feels_like"]),
                    '{} %'.format(re["main"]["humidity"])]
        else:
            complete_url2 = ('http://api.openweathermap.org/data/2.5/weather?q={},ar&units=metric&appid=b319b301cdc069464b37daa716905189'.format(provincia.getCapital()))
            print(complete_url2)
            r2 = requests.get(complete_url2)
            re2 = r2.json()
            if r2.status_code==200 and re2["sys"]["country"]=='AR':
                    lista = ['{} °C'.format(re2["main"]["temp"]),
                            '{} °C'.format(re2["main"]["feels_like"]),
                            '{} %'.format(re2["main"]["humidity"])]
        return lista

class NewProvince(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.provincia = None
        self.form = ProvinceForm(self)
        self.btn_add = tk.Button(self, text="Confirmar", command=self.confirmar)
        self.form.pack(padx=10, pady=10)
        self.btn_add.pack(pady=10)
    def confirmar(self):
        self.provincia = self.form.crearProvinciaDesdeFormulario()
        if self.provincia:
            self.destroy()
    def show(self):
        self.grab_set()
        self.wait_window()
        return self.provincia

class ProvincesView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lista de Provincias")
        self.list = ProvinceList(self, height=15)
        self.form = UpdateProvinceForm(self)
        self.btn_new = tk.Button(self, text="Agregar provincia")
        self.list.pack(side=tk.LEFT, padx=10, pady=10)
        self.form.pack(padx=10, pady=10)
        self.btn_new.pack(side=tk.BOTTOM, pady=5)
    def setControlador(self, ctrl):
        #vincula la vista con el controlador
        self.btn_new.config(command=ctrl.crearProvincia)
        self.form.bind_delete(ctrl.borrarProvincia)
        self.list.bind_doble_click(ctrl.seleccionarProvincia)
    def agregarProvincia(self, provincia):
        self.list.insertar(provincia)
    def modificarProvincia(self, provincia, index):
        self.list.modificar(provincia, index)
    def borrarProvincia(self, index):
        self.form.limpiar()
        self.list.borrar(index)
    #Ver estado de Paciente en formulario de pacientes
    def verProvinciaEnForm(self, provincia):
        self.form.mostrarEstadoProvinciaEnFormulario(provincia)
