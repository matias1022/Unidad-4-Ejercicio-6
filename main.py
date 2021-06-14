from classRepositorio import RespositorioProvincias
from classVistas import ProvincesView
from controlador import ControladorProvincias
from classObjectEncoder import ObjectEncoder
def main():
    conn=ObjectEncoder('datos.json')
    repo=RespositorioProvincias(conn)
    vista=ProvincesView()
    ctrl=ControladorProvincias(repo, vista)
    vista.setControlador(ctrl)
    ctrl.start()
    ctrl.salirGrabarDatos()

if __name__ == "__main__":
    main()