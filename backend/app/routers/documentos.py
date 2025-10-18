"""
Router: Documentos
Endpoints para upload, procesamiento y búsqueda de documentos
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.documento import Documento
from app.schemas.documento import (
    DocumentoResponse,
    DocumentoUploadResponse,
    BusquedaSemanticaRequest,
    ResultadoBusqueda
)
from app.services.file_processor import file_processor
from app.services.rag_service import rag_service
from app.services.gemini_service import gemini_service
from app.core.config import settings
from pathlib import Path
import shutil
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# ============================================
# ENDPOINTS DE DOCUMENTOS
# ============================================

@router.post("/upload", response_model=DocumentoUploadResponse)
async def subir_documento(
    archivo: UploadFile = File(...),
    proyecto_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Subir y procesar un documento
    
    Soporta: PDF, Word, Excel, imágenes, texto
    """
    try:
        logger.info(f"Subiendo archivo: {archivo.filename}")
        
        # Validar archivo
        es_valido, mensaje_error = file_processor.validar_archivo(
            nombre_archivo=archivo.filename,
            tamano=0  # Se validará después de leer
        )
        
        if not es_valido:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=mensaje_error
            )
        
        # Leer contenido del archivo
        contenido = await archivo.read()
        tamano = len(contenido)
        
        # Validar tamaño
        if tamano > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Archivo demasiado grande. Máximo: {settings.MAX_FILE_SIZE / (1024*1024)} MB"
            )
        
        # Generar nombre único
        extension = Path(archivo.filename).suffix
        nombre_unico = f"{uuid.uuid4()}{extension}"
        ruta_archivo = Path(settings.UPLOAD_DIR) / nombre_unico
        
        # Asegurar que el directorio existe
        ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar archivo
        with open(ruta_archivo, "wb") as buffer:
            buffer.write(contenido)
        
        # Detectar tipo MIME
        import magic
        mime = magic.Magic(mime=True)
        tipo_mime = mime.from_file(str(ruta_archivo))
        
        # Crear registro en base de datos
        documento = Documento(
            nombre=nombre_unico,
            nombre_original=archivo.filename,
            ruta_archivo=str(ruta_archivo),
            tipo_mime=tipo_mime,
            tamano=tamano,
            procesado=0,  # Pendiente
            proyecto_id=proyecto_id
        )
        
        db.add(documento)
        db.commit()
        db.refresh(documento)
        
        # Procesar archivo en segundo plano
        try:
            resultado = file_processor.procesar_archivo(str(ruta_archivo))
            
            # Actualizar documento con contenido extraído
            documento.contenido_texto = resultado.get('contenido', '')
            documento.metadata_extraida = resultado.get('metadata', {})
            documento.procesado = 1  # Procesado exitosamente
            
            # Agregar a RAG (búsqueda semántica)
            if documento.contenido_texto and len(documento.contenido_texto.strip()) > 10:
                rag_service.agregar_documento(
                    documento_id=documento.id,
                    contenido=documento.contenido_texto,
                    metadata={
                        "nombre": archivo.filename,
                        "tipo": tipo_mime,
                        "proyecto_id": proyecto_id
                    }
                )
            
            db.commit()
            db.refresh(documento)
            
            logger.info(f"Documento procesado exitosamente: {archivo.filename}")
            
            return DocumentoUploadResponse(
                success=True,
                message="Documento subido y procesado exitosamente",
                documento=documento,
                contenido_extraido=documento.contenido_texto[:500] if documento.contenido_texto else None
            )
            
        except Exception as e:
            # Marcar como error pero mantener el archivo
            documento.procesado = 2  # Error
            documento.mensaje_error = str(e)
            db.commit()
            
            logger.warning(f"Error al procesar documento {archivo.filename}: {str(e)}")
            
            return DocumentoUploadResponse(
                success=True,
                message=f"Documento subido pero hubo un error al procesarlo: {str(e)}",
                documento=documento,
                contenido_extraido=None
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al subir documento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al subir documento: {str(e)}"
        )

@router.get("/", response_model=List[DocumentoResponse])
def listar_documentos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    proyecto_id: Optional[int] = Query(None),
    procesado: Optional[int] = Query(None, ge=0, le=2),
    db: Session = Depends(get_db)
):
    """
    Listar documentos con filtros
    """
    try:
        query = db.query(Documento)
        
        if proyecto_id:
            query = query.filter(Documento.proyecto_id == proyecto_id)
        
        if procesado is not None:
            query = query.filter(Documento.procesado == procesado)
        
        documentos = query.order_by(Documento.fecha_subida.desc()).offset(skip).limit(limit).all()
        
        return documentos
        
    except Exception as e:
        logger.error(f"Error al listar documentos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar documentos: {str(e)}"
        )

@router.get("/{documento_id}", response_model=DocumentoResponse)
def obtener_documento(
    documento_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener documento por ID
    """
    documento = db.query(Documento).filter(Documento.id == documento_id).first()
    
    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documento con ID {documento_id} no encontrado"
        )
    
    return documento

@router.delete("/{documento_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_documento(
    documento_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar documento
    """
    documento = db.query(Documento).filter(Documento.id == documento_id).first()
    
    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documento con ID {documento_id} no encontrado"
        )
    
    try:
        # Eliminar archivo físico
        ruta_archivo = Path(documento.ruta_archivo)
        if ruta_archivo.exists():
            ruta_archivo.unlink()
        
        # Eliminar de RAG
        rag_service.eliminar_documento(documento_id)
        
        # Eliminar de base de datos
        db.delete(documento)
        db.commit()
        
        logger.info(f"Documento eliminado: {documento.nombre_original}")
        
        return None
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar documento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar documento: {str(e)}"
        )

@router.post("/buscar-semantica")
def buscar_semantica(
    request: BusquedaSemanticaRequest,
    db: Session = Depends(get_db)
):
    """
    Búsqueda semántica en documentos usando RAG
    
    Encuentra documentos relevantes basándose en el significado,
    no solo palabras clave
    """
    try:
        logger.info(f"Búsqueda semántica: {request.query}")
        
        # Buscar en RAG
        filtro = None
        if request.proyecto_id:
            filtro = {"proyecto_id": request.proyecto_id}
        
        resultados = rag_service.buscar_similar(
            query=request.query,
            limite=request.limite,
            filtro_metadata=filtro
        )
        
        # Enriquecer resultados con información de documento
        resultados_enriquecidos = []
        
        for resultado in resultados:
            documento_id = resultado['metadata'].get('documento_id')
            
            if documento_id:
                documento = db.query(Documento).filter(Documento.id == documento_id).first()
                
                if documento:
                    resultados_enriquecidos.append(ResultadoBusqueda(
                        documento_id=documento.id,
                        nombre_documento=documento.nombre_original,
                        fragmento=resultado['contenido'][:300],
                        score=resultado['score'],
                        metadata=resultado['metadata']
                    ))
        
        return {
            "query": request.query,
            "total_resultados": len(resultados_enriquecidos),
            "resultados": resultados_enriquecidos
        }
        
    except Exception as e:
        logger.error(f"Error en búsqueda semántica: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en búsqueda: {str(e)}"
        )

@router.post("/{documento_id}/reprocesar")
def reprocesar_documento(
    documento_id: int,
    db: Session = Depends(get_db)
):
    """
    Reprocesar un documento (útil si falló el procesamiento inicial)
    """
    documento = db.query(Documento).filter(Documento.id == documento_id).first()
    
    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documento con ID {documento_id} no encontrado"
        )
    
    try:
        logger.info(f"Reprocesando documento: {documento.nombre_original}")
        
        # Procesar archivo
        resultado = file_processor.procesar_archivo(documento.ruta_archivo)
        
        # Actualizar documento
        documento.contenido_texto = resultado.get('contenido', '')
        documento.metadata_extraida = resultado.get('metadata', {})
        documento.procesado = 1
        documento.mensaje_error = None
        
        # Actualizar en RAG
        if documento.contenido_texto and len(documento.contenido_texto.strip()) > 10:
            # Eliminar anterior
            rag_service.eliminar_documento(documento_id)
            
            # Agregar nuevo
            rag_service.agregar_documento(
                documento_id=documento.id,
                contenido=documento.contenido_texto,
                metadata={
                    "nombre": documento.nombre_original,
                    "tipo": documento.tipo_mime,
                    "proyecto_id": documento.proyecto_id
                }
            )
        
        db.commit()
        db.refresh(documento)
        
        return {
            "success": True,
            "message": "Documento reprocesado exitosamente",
            "documento": documento
        }
        
    except Exception as e:
        documento.procesado = 2
        documento.mensaje_error = str(e)
        db.commit()
        
        logger.error(f"Error al reprocesar documento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al reprocesar: {str(e)}"
        )

@router.post("/{documento_id}/analizar-con-ia")
def analizar_documento_con_ia(
    documento_id: int,
    db: Session = Depends(get_db)
):
    """
    Analizar documento con IA para extraer información relevante
    """
    documento = db.query(Documento).filter(Documento.id == documento_id).first()
    
    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documento con ID {documento_id} no encontrado"
        )
    
    if not documento.contenido_texto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El documento no tiene contenido de texto procesado"
        )
    
    try:
        logger.info(f"Analizando documento con IA: {documento.nombre_original}")
        
        # Analizar con Gemini
        analisis = gemini_service.analizar_documento(
            texto_documento=documento.contenido_texto,
            tipo_analisis="general"
        )
        
        return {
            "success": True,
            "documento_id": documento_id,
            "nombre_documento": documento.nombre_original,
            "analisis": analisis
        }
        
    except Exception as e:
        logger.error(f"Error al analizar documento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al analizar: {str(e)}"
        )

@router.get("/estadisticas/rag")
def estadisticas_rag():
    """
    Obtener estadísticas del sistema RAG
    """
    try:
        estadisticas = rag_service.estadisticas()
        
        return estadisticas
        
    except Exception as e:
        logger.error(f"Error al obtener estadísticas RAG: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )