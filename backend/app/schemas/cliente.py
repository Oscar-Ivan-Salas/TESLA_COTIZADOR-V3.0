"""
Schemas de Cliente
Validación de datos con Pydantic
"""
from pydantic import BaseModel, Field, ConfigDict, field_validator, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime
import re

# ============================================
# SCHEMAS DE CLIENTE
# ============================================

class ClienteBase(BaseModel):
    """Schema base de Cliente"""
    nombre: str = Field(..., min_length=3, max_length=200, description="Nombre o Razón Social")
    ruc: str = Field(..., min_length=11, max_length=11, description="RUC (11 dígitos)")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono principal")
    email: Optional[EmailStr] = Field(None, description="Email principal")
    direccion: Optional[str] = Field(None, max_length=500, description="Dirección")
    ciudad: Optional[str] = Field("Huancayo", max_length=100, description="Ciudad")
    departamento: Optional[str] = Field("Junín", max_length=100, description="Departamento")
    industria: Optional[str] = Field(None, max_length=100, description="Industria o sector")
    tipo_cliente: Optional[str] = Field("empresa", max_length=50, description="Tipo de cliente")
    persona_contacto: Optional[str] = Field(None, max_length=200, description="Persona de contacto")
    cargo_contacto: Optional[str] = Field(None, max_length=100, description="Cargo del contacto")
    telefono_contacto: Optional[str] = Field(None, max_length=20, description="Teléfono del contacto")
    email_contacto: Optional[EmailStr] = Field(None, description="Email del contacto")
    notas: Optional[str] = Field(None, description="Notas adicionales")
    activo: Optional[str] = Field("activo", description="Estado del cliente")
    metadata_adicional: Optional[Dict[str, Any]] = Field(None, description="Metadata adicional")

    @field_validator('ruc')
    @classmethod
    def validar_ruc(cls, v):
        """Validar formato de RUC peruano"""
        if not v:
            raise ValueError("RUC es obligatorio")

        # Eliminar espacios
        v = v.strip().replace(" ", "")

        # Debe ser exactamente 11 dígitos numéricos
        if not re.match(r'^\d{11}$', v):
            raise ValueError("RUC debe tener exactamente 11 dígitos numéricos")

        # Validación básica: debe empezar con 10, 15, 16, 17 o 20
        if not v.startswith(('10', '15', '16', '17', '20')):
            raise ValueError("RUC debe empezar con 10, 15, 16, 17 o 20")

        return v

    @field_validator('tipo_cliente')
    @classmethod
    def validar_tipo_cliente(cls, v):
        """Validar tipo de cliente"""
        tipos_validos = ['empresa', 'persona', 'gobierno', 'otro']
        if v and v.lower() not in tipos_validos:
            raise ValueError(f"Tipo de cliente debe ser uno de: {', '.join(tipos_validos)}")
        return v.lower() if v else 'empresa'

    @field_validator('activo')
    @classmethod
    def validar_activo(cls, v):
        """Validar estado"""
        estados_validos = ['activo', 'inactivo']
        if v and v.lower() not in estados_validos:
            raise ValueError(f"Estado debe ser uno de: {', '.join(estados_validos)}")
        return v.lower() if v else 'activo'

class ClienteCreate(ClienteBase):
    """Schema para crear un cliente"""
    pass

class ClienteUpdate(BaseModel):
    """Schema para actualizar un cliente (todos los campos opcionales)"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=200)
    ruc: Optional[str] = Field(None, min_length=11, max_length=11)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    direccion: Optional[str] = Field(None, max_length=500)
    ciudad: Optional[str] = Field(None, max_length=100)
    departamento: Optional[str] = Field(None, max_length=100)
    industria: Optional[str] = Field(None, max_length=100)
    tipo_cliente: Optional[str] = Field(None, max_length=50)
    persona_contacto: Optional[str] = Field(None, max_length=200)
    cargo_contacto: Optional[str] = Field(None, max_length=100)
    telefono_contacto: Optional[str] = Field(None, max_length=20)
    email_contacto: Optional[EmailStr] = None
    notas: Optional[str] = None
    activo: Optional[str] = None
    metadata_adicional: Optional[Dict[str, Any]] = None

    @field_validator('ruc')
    @classmethod
    def validar_ruc(cls, v):
        """Validar formato de RUC peruano"""
        if v is None:
            return v

        # Eliminar espacios
        v = v.strip().replace(" ", "")

        # Debe ser exactamente 11 dígitos numéricos
        if not re.match(r'^\d{11}$', v):
            raise ValueError("RUC debe tener exactamente 11 dígitos numéricos")

        # Validación básica: debe empezar con 10, 15, 16, 17 o 20
        if not v.startswith(('10', '15', '16', '17', '20')):
            raise ValueError("RUC debe empezar con 10, 15, 16, 17 o 20")

        return v

class ClienteResponse(ClienteBase):
    """Schema de respuesta de Cliente"""
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    model_config = ConfigDict(from_attributes=True)

class ClienteListResponse(BaseModel):
    """Schema para listar clientes"""
    id: int
    nombre: str
    ruc: str
    telefono: Optional[str]
    email: Optional[str]
    ciudad: Optional[str]
    industria: Optional[str]
    activo: str

    model_config = ConfigDict(from_attributes=True)
