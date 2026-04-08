from repository import ProductoRepository

class ProductoService:
    def __init__(self):
        self.repo = ProductoRepository()

    #EL servicio procesa la peticion recibida y los direcciona al repositorio.     
    def listar_productos(self):
        return self.repo.obtener_todos()

    def buscar_por_id(self, p_id: int):
        return self.repo.obtener_por_id(p_id)

    def crear_nuevo(self, producto_data):
        # Extraemos los datos del esquema de Pydantic
        return self.repo.guardar(
            producto_data.nombre, 
            producto_data.precio, 
            producto_data.stock
        )

    def actualizar_producto(self, p_id: int, datos):
        return self.repo.actualizar(
            p_id, 
            datos.nombre, 
            datos.precio, 
            datos.stock
        )

    def borrar(self, p_id: int):
        return self.repo.eliminar(p_id)