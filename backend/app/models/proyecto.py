"""
Modelo: Proyecto
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class EstadoProyecto(str, enum.Enum):
    """Estados posibles de un proyecto"""
    PLANIFICACION = "planificacion"
    EN_PROGRESO = "en_progreso"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"

class Proyecto(Base):
    """
    Modelo de Proyecto
    Representa un proyecto del cliente
    """
    __tablename__ = "proyectos"
    
    # Campos principales
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    cliente = Column(String(200), nullable=False, index=True)
    estado = Column(
        Enum(EstadoProyecto),
        default=EstadoProyecto.PLANIFICACION,
        nullable=False
    )
    
    # Metadata adicional (JSON)
    metadata_adicional = Column(JSON, nullable=True)
    
    # Timestamps
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    fecha_inicio = Column(DateTime(timezone=True), nullable=True)
    fecha_fin = Column(DateTime(timezone=True), nullable=True)
    
    # Relaciones
    cotizaciones = relationship(
        "Cotizacion",
        back_populates="proyecto_rel",
        cascade="all, delete-orphan"
    )
    documentos = relationship(
        "Documento",
        back_populates="proyecto",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Proyecto(id={self.id}, nombre='{self.nombre}', cliente='{self.cliente}')>"
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "cliente": self.cliente,
            "estado": self.estado.value if self.estado else None,
            "metadata_adicional": self.metadata_adicional,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_modificacion": self.fecha_modificacion.isoformat() if self.fecha_modificacion else None,
            "fecha_inicio": self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
        }