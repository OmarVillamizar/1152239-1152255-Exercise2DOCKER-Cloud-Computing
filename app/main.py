from fastapi import FastAPI, Request, HTTPException
import os

from nota import Nota

app = FastAPI()
DATA_FILE = "/data/notas.txt"

@app.post("/nota")
async def guardar_note(request: Request):
    datos = await request.json()
    nota = Nota(titulo=datos['titulo'], contenido=datos['contenido'])
    return nota.guardar()

@app.get("/")
def leer_notes():
    if not os.path.exists(DATA_FILE):
        return {"notas": []}
    with open(DATA_FILE, "r") as f:
        return {"notas": f.read().splitlines()}
    
@app.get("/conteo")
def contar_notes():
    if not os.path.exists(DATA_FILE):
        return {"conteo": 0}
    with open(DATA_FILE, "r") as f:
        return {"conteo": len(f.readlines())}
    
@app.get("/autor")
def obtener_autor():
    autor = os.getenv("AUTOR", "Desconocido")
    return {"autor": autor}

@app.get("/notas-db")
def obtener_notas():
    try:
        data = Nota.todas()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))