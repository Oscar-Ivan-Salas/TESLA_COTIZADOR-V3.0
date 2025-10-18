"""
Routers de la API
"""
from app.routers.cotizaciones import router as cotizaciones_router
from app.routers.proyectos import router as proyectos_router
from app.routers.chat import router as chat_router
from app.routers.documentos import router as documentos_router

__all__ = [
    "cotizaciones_router",
    "proyectos_router",
    "chat_router",
    "documentos_router",
]