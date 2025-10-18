"""
Schemas de Proyecto
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class EstadoProyecto(str, Enum):
    """Estados posibles de un proyecto"""
    PLANIFICACION = "planificacion"
    EN_PROGRESO = "en_progreso"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"

class ProyectoBase(BaseModel):
    """Schema base de Proyecto"""
    nombre: str = Field(..., min_length=3, max_length=200, description="Nombre del proyecto")
    descripcion: Optional[str] = Field(None, description="Descripción del proyecto")
    cliente: str = Field(..., min_length=3, max_length=200, description="Nombre del cliente")
    estado: EstadoProyecto = Field(default=EstadoProyecto.PLANIFICACION, description="Estado del proyecto")
    metadata_adicional: Optional[Dict[str, Any]] = Field(None, description="Metadata adicional en formato JSON")

class ProyectoCreate(ProyectoBase):
    """Schema para crear un proyecto"""
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None

class ProyectoUpdate(BaseModel):
    """Schema para actualizar un proyecto"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=200)
    descripcion: Optional[str] = None
    cliente: Optional[str] = Field(None, min_length=3, max_length=200)
    estado: Optional[EstadoProyecto] = None
    metadata_adicional: Optional[Dict[str, Any]] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None

class ProyectoResponse(ProyectoBase):
    """Schema de respuesta de Proyecto"""
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)