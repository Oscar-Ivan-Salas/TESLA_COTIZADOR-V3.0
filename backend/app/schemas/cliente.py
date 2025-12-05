"""
Schemas Pydantic para Cliente
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class ClienteBase(BaseModel):
    """Schema base para Cliente"""
    nombre: str = Field(..., min_length=1, max_length=200, description="Nombre o razón social")
    ruc: str = Field(..., min_length=11, max_length=11, description="RUC de 11 dígitos")
    direccion: Optional[str] = Field(None, max_length=500)
    ciudad: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    web: Optional[str] = Field(None, max_length=200)
    contacto_nombre: Optional[str] = Field(None, max_length=200)
    contacto_cargo: Optional[str] = Field(None, max_length=100)
    contacto_telefono: Optional[str] = Field(None, max_length=20)
    contacto_email: Optional[str] = Field(None, max_length=100)
    industria: Optional[str] = Field(None, max_length=50)
    tipo_cliente: Optional[str] = Field("activo", max_length=50)
    notas: Optional[str] = None
    logo_base64: Optional[str] = None

    @validator('ruc')
    def validar_ruc(cls, v):
        """Validar que RUC sea numérico y tenga 11 dígitos"""
        if not v.isdigit():
            raise ValueError('RUC debe contener solo dígitos')
        if len(v) != 11:
            raise ValueError('RUC debe tener exactamente 11 dígitos')
        return v


class ClienteCreate(ClienteBase):
    """Schema para crear un cliente"""
    pass


class ClienteUpdate(BaseModel):
    """Schema para actualizar un cliente"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=200)
    ruc: Optional[str] = Field(None, min_length=11, max_length=11)
    direccion: Optional[str] = Field(None, max_length=500)
    ciudad: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    web: Optional[str] = Field(None, max_length=200)
    contacto_nombre: Optional[str] = Field(None, max_length=200)
    contacto_cargo: Optional[str] = Field(None, max_length=100)
    contacto_telefono: Optional[str] = Field(None, max_length=20)
    contacto_email: Optional[str] = Field(None, max_length=100)
    industria: Optional[str] = Field(None, max_length=50)
    tipo_cliente: Optional[str] = Field(None, max_length=50)
    notas: Optional[str] = None
    logo_base64: Optional[str] = None


class ClienteResponse(ClienteBase):
    """Schema para respuesta de cliente"""
    id: int
    fecha_registro: datetime
    fecha_ultima_cotizacion: Optional[datetime] = None

    # Estadísticas calculadas (opcionales)
    total_cotizaciones: Optional[int] = 0
    monto_total_cotizaciones: Optional[float] = 0.0

    class Config:
        from_attributes = True


class ClienteResumen(BaseModel):
    """Schema resumido para búsquedas y listas"""
    id: int
    nombre: str
    ruc: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    industria: Optional[str] = None
    total_cotizaciones: Optional[int] = 0

    class Config:
        from_attributes = True
