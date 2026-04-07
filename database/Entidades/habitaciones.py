
#Clase contenedor de ModelHabitaciones.py
class Habitaciones():

    def __init__(self, codigo, tipo, descripcion, estado, capacidad, precio, grado, url_foto):
        
        self.codigo = codigo
        self.tipo = tipo
        self.descripcion = descripcion
        self.estado = estado 
        self.capacidad = capacidad
        self.precio = precio
        self.grado = grado
        self.foto = url_foto

