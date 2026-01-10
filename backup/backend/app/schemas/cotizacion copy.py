"""
Schemas de Cotización
"""
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

# ============================================
# SCHEMAS DE ITEM
# ============================================

class ItemBase(BaseModel):
    """Schema base de Item"""
    descripcion: str = Field(..., min_length=1, description="Descripción del item")
    cantidad: Decimal = Field(..., gt=0, description="Cantidad")
    precio_unitario: Decimal = Field(..., ge=0, description="Precio unitario")

class ItemCreate(ItemBase):
    """Schema para crear un item"""
    pass

class ItemResponse(ItemBase):
    """Schema de respuesta de Item"""
    id: int
    total: Decimal
    cotizacion_id: int
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# SCHEMAS DE COTIZACIÓN
# ============================================

class CotizacionBase(BaseModel):
    """Schema base de Cotización"""
    cliente: str = Field(..., min_length=3, max_length=200, description="Nombre del cliente")
    proyecto: str = Field(..., min_length=3, max_length=200, description="Nombre del proyecto")
    descripcion: Optional[str] = Field(None, description="Descripción de la cotización")

class CotizacionCreate(CotizacionBase):
    """Schema para crear una cotización"""
    items: Optional[List[Dict[str, Any]]] = Field(None, description="Items de la cotización")
    proyecto_id: Optional[int] = Field(None, description="ID del proyecto relacionado")
    estado: Optional[str] = Field("borrador", description="Estado de la cotización")
    
    @field_validator('items')
    @classmethod
    def validar_items(cls, v):
        """Validar que los items tengan la estructura correcta"""
        if v is not None:
            for item in v:
                if not isinstance(item, dict):
                    raise ValueError("Cada item debe ser un diccionario")
                
                required_fields = ["descripcion", "cantidad", "precio_unitario"]
                for field in required_fields:
                    if field not in item:
                        raise ValueError(f"El item debe tener el campo '{field}'")
                
                # Validar tipos
                if not isinstance(item["descripcion"], str) or len(item["descripcion"]) < 1:
                    raise ValueError("La descripción debe ser un texto no vacío")
                
                try:
                    cantidad = float(item["cantidad"])
                    if cantidad <= 0:
                        raise ValueError("La cantidad debe ser mayor a 0")
                except (ValueError, TypeError):
                    raise ValueError("La cantidad debe ser un número válido")
                
                try:
                    precio = float(item["precio_unitario"])
                    if precio < 0:
                        raise ValueError("El precio debe ser mayor o igual a 0")
                except (ValueError, TypeError):
                    raise ValueError("El precio debe ser un número válido")
        
        return v

class CotizacionUpdate(BaseModel):
    """Schema para actualizar una cotización"""
    cliente: Optional[str] = Field(None, min_length=3, max_length=200)
    proyecto: Optional[str] = Field(None, min_length=3, max_length=200)
    descripcion: Optional[str] = None
    items: Optional[List[Dict[str, Any]]] = None
    estado: Optional[str] = None
    metadata_adicional: Optional[Dict[str, Any]] = None
    
    @field_validator('items')
    @classmethod
    def validar_items(cls, v):
        """Validar que los items tengan la estructura correcta"""
        if v is not None:
            for item in v:
                if not isinstance(item, dict):
                    raise ValueError("Cada item debe ser un diccionario")
                
                required_fields = ["descripcion", "cantidad", "precio_unitario"]
                for field in required_fields:
                    if field not in item:
                        raise ValueError(f"El item debe tener el campo '{field}'")
        
        return v

class CotizacionResponse(CotizacionBase):
    """Schema de respuesta de Cotización"""
    id: int
    numero: str
    subtotal: Decimal
    igv: Decimal
    total: Decimal
    estado: str
    items: Optional[List[Dict[str, Any]]] = None
    metadata_adicional: Optional[Dict[str, Any]] = None
    fecha_creacion: datetime
    fecha_modificacion: datetime
    proyecto_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# SCHEMAS ESPECIALES PARA CHAT IA
# ============================================

class CotizacionRapidaRequest(BaseModel):
    """Schema para generar cotización rápida con IA"""
    descripcion_proyecto: str = Field(
        ...,
        min_length=10,
        description="Descripción del proyecto para generar la cotización"
    )
    cliente: str = Field(..., min_length=3, description="Nombre del cliente")
    proyecto: Optional[str] = Field(None, description="Nombre del proyecto")

class ChatMessage(BaseModel):
    """Schema para mensaje de chat"""
    role: str = Field(..., description="Rol del mensaje: 'user' o 'assistant'")
    content: str = Field(..., min_length=1, description="Contenido del mensaje")

class ChatRequest(BaseModel):
    """Schema para request de chat conversacional"""
    mensaje: str = Field(..., min_length=1, description="Mensaje del usuario")
    cotizacion_id: Optional[int] = Field(None, description="ID de cotización existente")
    contexto: Optional[List[ChatMessage]] = Field(None, description="Historial de chat")
    cliente: Optional[str] = Field(None, description="Nombre del cliente")
    proyecto: Optional[str] = Field(None, description="Nombre del proyecto")

class ChatResponse(BaseModel):
    """Schema de respuesta del chat"""
    respuesta: str = Field(..., description="Respuesta del asistente")
    cotizacion: Optional[CotizacionResponse] = Field(None, description="Cotización generada/actualizada")
    sugerencias: Optional[List[str]] = Field(None, description="Sugerencias de seguimiento")