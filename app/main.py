from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.infrastructure.api.routes import usuarios, parcelas, cultivos, productos, aplicaciones, recordatorios
from app.infrastructure.api.auth import auth

app = FastAPI(
    title="AgroControl API",
    description="API para la gestión de productos fitosanitarios en cultivos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(parcelas.router, prefix="/api/parcelas", tags=["Parcelas"])
app.include_router(cultivos.router, prefix="/api/cultivos", tags=["Cultivos"])
app.include_router(productos.router, prefix="/api/productos", tags=["Productos Fitosanitarios"])
app.include_router(aplicaciones.router, prefix="/api/aplicaciones", tags=["Aplicaciones"])
app.include_router(recordatorios.router, prefix="/api/recordatorios", tags=["Recordatorios"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de AgroControl"}

lambda_handler = Mangum(app=app)