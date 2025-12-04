"""
Modelo SQLAlchemy para Clientes
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Cliente(Base):
    """
    Modelo de Cliente para gestión de base de datos de clientes.
    Permite reutilizar datos de clientes en múltiples cotizaciones.
    """
    __tablename__ = "clientes"

    # Identificación
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False, index=True)
    ruc = Column(String(11), unique=True, nullable=False, index=True)

    # Datos de contacto
    direccion = Column(String(500))
    ciudad = Column(String(100))
    telefono = Column(String(20))
    email = Column(String(100))
    web = Column(String(200))

    # Contacto principal
    contacto_nombre = Column(String(200))
    contacto_cargo = Column(String(100))
    contacto_telefono = Column(String(20))
    contacto_email = Column(String(100))

    # Información adicional
    industria = Column(String(50))
    tipo_cliente = Column(String(50), default="activo")  # lead, activo, inactivo
    notas = Column(Text)

    # Logo del cliente (opcional, en base64)
    logo_base64 = Column(Text, nullable=True)

    # Metadata
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    fecha_ultima_cotizacion = Column(DateTime, nullable=True)

    # Relaciones
    cotizaciones = relationship("Cotizacion", back_populates="cliente")
    proyectos = relationship("Proyecto", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente {self.nombre} (RUC: {self.ruc})>"
