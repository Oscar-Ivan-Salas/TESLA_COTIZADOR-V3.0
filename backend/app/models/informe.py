"""
Modelo: Informe
Representa informes técnicos y ejecutivos generados por PILI
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class TipoInforme(str, enum.Enum):
    """Tipos de informe disponibles"""
    SIMPLE = "simple"
    EJECUTIVO = "ejecutivo"
    TECNICO = "tecnico"

class FormatoInforme(str, enum.Enum):
    """Formatos de salida del informe"""
    WORD = "word"
    PDF = "pdf"

class Informe(Base):
    """
    Modelo de Informe
    Representa un informe técnico o ejecutivo generado
    """
    __tablename__ = "informes"

    # Campos principales
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False, index=True)
    tipo = Column(
        Enum(TipoInforme),
        default=TipoInforme.SIMPLE,
        nullable=False
    )
    formato = Column(
        Enum(FormatoInforme),
        default=FormatoInforme.WORD,
        nullable=False
    )

    # Contenido
    contenido = Column(Text, nullable=True)
    resumen_ejecutivo = Column(Text, nullable=True)
    conclusiones = Column(Text, nullable=True)
    recomendaciones = Column(Text, nullable=True)

    # Relación con proyecto (opcional)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id", ondelete="SET NULL"), nullable=True)
    proyecto_rel = relationship("Proyecto", backref="informes")

    # Opciones de generación
    incluir_graficos = Column(JSON, default=False)
    incluir_tablas = Column(JSON, default=True)

    # Metadata adicional (JSON)
    metadata_adicional = Column(JSON, nullable=True)

    # Timestamps
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Estado
    estado = Column(String(50), default="borrador", index=True)

    def __repr__(self):
        return f"<Informe(id={self.id}, titulo='{self.titulo}', tipo={self.tipo})>"

    def to_dict(self):
        """Convertir a diccionario"""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "tipo": self.tipo.value if self.tipo else None,
            "formato": self.formato.value if self.formato else None,
            "contenido": self.contenido,
            "resumen_ejecutivo": self.resumen_ejecutivo,
            "conclusiones": self.conclusiones,
            "recomendaciones": self.recomendaciones,
            "proyecto_id": self.proyecto_id,
            "incluir_graficos": self.incluir_graficos,
            "incluir_tablas": self.incluir_tablas,
            "metadata_adicional": self.metadata_adicional,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_modificacion": self.fecha_modificacion.isoformat() if self.fecha_modificacion else None,
            "estado": self.estado
        }
