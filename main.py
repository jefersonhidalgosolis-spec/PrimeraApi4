from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from service import ProductoService

app = FastAPI()
_service = ProductoService()

# Esquema para validar los datos que entran por JSON
class ProductoSchema(BaseModel):
    nombre: str
    precio: float
    stock: int

#5.GET 5555555555555555555555555555555555555555555555555555 
#rama path 
#Calcular la suma de precio de todos los productos 
@app.get("/productos/resumen")
def get_summary():
    return {"valor_inventario": _service.calcular_valor_total()}
    
#GET (leer)
#Esta peticion responde al endpoint Get que utliza la ruta /productos para activar esta funcion. La funcion debe mostrar 
#la lista de productos llevando esta peticion al servicio para obtner los datos. 
@app.get("/productos")
def get_all():
    return _service.listar_productos() 

#GET (leer)
#Esta peticion responde al endpoint GET que utiliza la ruta /productos/{p_id} para buscar los datos de un id especifico. 
# 
@app.get("/productos/{p_id}") 
def get_by_id(p_id: int):
    res = _service.buscar_por_id(p_id)
    if not res:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return res 

#"Cuando alguien me envíe datos de un nuevo producto, usa el servicio para guardarlo".
#POST (CREAR)
@app.post("/productos", status_code=201)
def create(producto: ProductoSchema):
    return _service.crear_nuevo(producto)

#PUT(ACTUALIZAR)
@app.put("/productos/{p_id}")
def update(p_id: int, producto: ProductoSchema):
    exito = _service.actualizar_producto(p_id, producto)
    if not exito:
        raise HTTPException(status_code=404, detail="No se encontró para actualizar")
    return {"mensaje": "Actualizado correctamente"}

#DELETE
@app.delete("/productos/{p_id}")
def delete(p_id: int):
    if _service.borrar(p_id):
        return {"mensaje": "Eliminado correctamente"}
    raise HTTPException(status_code=404, detail="ID no existente")
