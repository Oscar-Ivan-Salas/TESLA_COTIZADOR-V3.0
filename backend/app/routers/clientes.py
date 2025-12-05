"""
Router de Clientes - Gestión de base de datos de clientes
"""
from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Optional
from datetime import datetime
import logging

from app.core.database import get_db
from app.models.cliente import Cliente
from app.models.cotizacion import Cotizacion
from app.schemas.cliente import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
    ClienteResumen
)

# Configurar logging
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(
    prefix="/api/clientes",
    tags=["clientes"],
    responses={404: {"description": "Cliente no encontrado"}}
)


@router.get("/search", response_model=List[ClienteResumen])
async def buscar_clientes(
    q: str = Query(..., min_length=2, description="Texto de búsqueda (mínimo 2 caracteres)"),
    limit: int = Query(10, le=50, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """
    Buscar clientes por nombre o RUC (autocompletado).

    - **q**: Texto de búsqueda (nombre o RUC)
    - **limit**: Número máximo de resultados (default: 10, max: 50)

    Retorna lista de clientes que coinciden con la búsqueda.
    """
    try:
        logger.info(f"Buscando clientes con query: {q}")

        # Buscar por nombre o RUC (case-insensitive)
        clientes = db.query(Cliente).filter(
            or_(
                Cliente.nombre.ilike(f"%{q}%"),
                Cliente.ruc.ilike(f"%{q}%")
            )
        ).limit(limit).all()

        # Agregar conteo de cotizaciones
        resultados = []
        for cliente in clientes:
            cliente_dict = {
                "id": cliente.id,
                "nombre": cliente.nombre,
                "ruc": cliente.ruc,
                "telefono": cliente.telefono,
                "email": cliente.email,
                "industria": cliente.industria,
                "total_cotizaciones": len(cliente.cotizaciones) if cliente.cotizaciones else 0
            }
            resultados.append(cliente_dict)

        logger.info(f"Se encontraron {len(resultados)} clientes")
        return resultados

    except Exception as e:
        logger.error(f"Error en búsqueda de clientes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar clientes: {str(e)}"
        )


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def crear_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    """
    Registrar un nuevo cliente en la base de datos.

    - **nombre**: Nombre o razón social del cliente
    - **ruc**: RUC de 11 dígitos (único)
    - **direccion**, **ciudad**, **telefono**, **email**: Datos de contacto (opcionales)
    - **industria**: Sector del cliente (opcional)
    - **logo_base64**: Logo del cliente en base64 (opcional)

    Retorna el cliente creado con su ID.
    """
    try:
        # Verificar que no exista un cliente con el mismo RUC
        existe = db.query(Cliente).filter(Cliente.ruc == cliente.ruc).first()
        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un cliente con RUC {cliente.ruc}"
            )

        # Crear nuevo cliente
        nuevo_cliente = Cliente(**cliente.dict())
        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)

        logger.info(f"Cliente creado: {nuevo_cliente.nombre} (ID: {nuevo_cliente.id})")

        # Preparar respuesta
        respuesta = ClienteResponse(
            **nuevo_cliente.__dict__,
            total_cotizaciones=0,
            monto_total_cotizaciones=0.0
        )

        return respuesta

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear cliente: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cliente: {str(e)}"
        )


@router.get("/", response_model=dict)
async def listar_clientes(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(50, ge=1, le=100, description="Número de registros a retornar"),
    industria: Optional[str] = Query(None, description="Filtrar por industria"),
    tipo_cliente: Optional[str] = Query(None, description="Filtrar por tipo de cliente"),
    db: Session = Depends(get_db)
):
    """
    Listar todos los clientes con paginación.

    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Número máximo de registros a retornar
    - **industria**: Filtrar por industria (opcional)
    - **tipo_cliente**: Filtrar por tipo de cliente (opcional)

    Retorna lista de clientes y total de registros.
    """
    try:
        # Query base
        query = db.query(Cliente)

        # Aplicar filtros si existen
        if industria:
            query = query.filter(Cliente.industria == industria)
        if tipo_cliente:
            query = query.filter(Cliente.tipo_cliente == tipo_cliente)

        # Total de registros
        total = query.count()

        # Obtener clientes con paginación
        clientes = query.offset(skip).limit(limit).all()

        # Agregar estadísticas
        clientes_con_stats = []
        for cliente in clientes:
            total_cots = len(cliente.cotizaciones) if cliente.cotizaciones else 0
            monto_total = sum(float(c.total) if c.total else 0 for c in cliente.cotizaciones) if cliente.cotizaciones else 0

            cliente_dict = ClienteResponse(
                **cliente.__dict__,
                total_cotizaciones=total_cots,
                monto_total_cotizaciones=monto_total
            )
            clientes_con_stats.append(cliente_dict)

        return {
            "clientes": clientes_con_stats,
            "total": total,
            "skip": skip,
            "limit": limit
        }

    except Exception as e:
        logger.error(f"Error al listar clientes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar clientes: {str(e)}"
        )


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def obtener_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener datos completos de un cliente específico.

    - **cliente_id**: ID del cliente

    Retorna todos los datos del cliente incluyendo estadísticas.
    """
    try:
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado"
            )

        # Calcular estadísticas
        total_cots = len(cliente.cotizaciones) if cliente.cotizaciones else 0
        monto_total = sum(float(c.total) if c.total else 0 for c in cliente.cotizaciones) if cliente.cotizaciones else 0

        respuesta = ClienteResponse(
            **cliente.__dict__,
            total_cotizaciones=total_cots,
            monto_total_cotizaciones=monto_total
        )

        return respuesta

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener cliente: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente: {str(e)}"
        )


@router.put("/{cliente_id}", response_model=ClienteResponse)
async def actualizar_cliente(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar datos de un cliente existente.

    - **cliente_id**: ID del cliente a actualizar
    - Solo se actualizan los campos proporcionados (actualización parcial)

    Retorna el cliente actualizado.
    """
    try:
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado"
            )

        # Actualizar solo los campos proporcionados
        update_data = cliente_update.dict(exclude_unset=True)
        for campo, valor in update_data.items():
            setattr(cliente, campo, valor)

        db.commit()
        db.refresh(cliente)

        logger.info(f"Cliente actualizado: {cliente.nombre} (ID: {cliente.id})")

        # Calcular estadísticas
        total_cots = len(cliente.cotizaciones) if cliente.cotizaciones else 0
        monto_total = sum(float(c.total) if c.total else 0 for c in cliente.cotizaciones) if cliente.cotizaciones else 0

        respuesta = ClienteResponse(
            **cliente.__dict__,
            total_cotizaciones=total_cots,
            monto_total_cotizaciones=monto_total
        )

        return respuesta

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar cliente: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cliente: {str(e)}"
        )


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un cliente de la base de datos.

    - **cliente_id**: ID del cliente a eliminar

    NOTA: Las cotizaciones asociadas NO se eliminan, solo se desvinculan (cliente_id = NULL).
    """
    try:
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado"
            )

        # Eliminar cliente (las cotizaciones quedan con cliente_id=NULL por ondelete="SET NULL")
        db.delete(cliente)
        db.commit()

        logger.info(f"Cliente eliminado: {cliente.nombre} (ID: {cliente.id})")

        return None

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar cliente: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cliente: {str(e)}"
        )


@router.get("/{cliente_id}/cotizaciones", response_model=dict)
async def listar_cotizaciones_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """
    Listar todas las cotizaciones de un cliente específico.

    - **cliente_id**: ID del cliente

    Retorna información del cliente y todas sus cotizaciones con estadísticas.
    """
    try:
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado"
            )

        # Obtener cotizaciones
        cotizaciones = cliente.cotizaciones if cliente.cotizaciones else []

        # Calcular estadísticas
        total_cotizaciones = len(cotizaciones)
        monto_total = sum(float(c.total) if c.total else 0 for c in cotizaciones)

        # Preparar cotizaciones para respuesta
        cotizaciones_dict = [c.to_dict() for c in cotizaciones]

        return {
            "cliente": {
                "id": cliente.id,
                "nombre": cliente.nombre,
                "ruc": cliente.ruc,
                "email": cliente.email,
                "telefono": cliente.telefono
            },
            "cotizaciones": cotizaciones_dict,
            "total_cotizaciones": total_cotizaciones,
            "monto_total": monto_total
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al listar cotizaciones de cliente: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar cotizaciones: {str(e)}"
        )
