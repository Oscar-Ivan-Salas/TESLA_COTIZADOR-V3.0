"""
RAG Service - Retrieval Augmented Generation
Compatible con ChromaDB 0.4.x+
"""

import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings

logger = logging.getLogger(__name__)


class RAGService:
    """
    Servicio de RAG usando ChromaDB para almacenamiento vectorial
    """
    
    def __init__(self):
        """Inicializar el servicio RAG con manejo de errores"""
        self.collection_name = "tesla_cotizador_docs"
        self.client = None
        self.collection = None
        
        try:
            # Usar PersistentClient (API nueva de ChromaDB)
            self.client = chromadb.PersistentClient(
                path="./chroma_db"
            )
            
            logger.info("✅ ChromaDB client inicializado")
            
            # Obtener o crear colección
            self.collection = self._get_or_create_collection()
            
            logger.info(f"✅ RAGService inicializado con colección '{self.collection_name}'")
            
        except Exception as e:
            logger.error(f"❌ Error al inicializar RAGService: {str(e)}")
            logger.warning("⚠️ RAG Service funcionará en modo degradado")
            self.client = None
            self.collection = None
    
    def _get_or_create_collection(self):
        """
        Obtener o crear la colección de ChromaDB
        """
        if not self.client:
            return None
            
        try:
            # Intentar obtener colección existente
            collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Documentos de cotizaciones Tesla"}
            )
            
            logger.info(f"Colección '{self.collection_name}' lista")
            return collection
            
        except Exception as e:
            logger.error(f"Error al crear/obtener colección: {str(e)}")
            return None
    
    def is_available(self) -> bool:
        """Verificar si el servicio está disponible"""
        return self.client is not None and self.collection is not None
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> bool:
        """
        Agregar documentos a la colección
        
        Args:
            documents: Lista de textos a agregar
            metadatas: Metadatos opcionales para cada documento
            ids: IDs opcionales para cada documento
            
        Returns:
            True si se agregaron exitosamente
        """
        if not self.is_available():
            logger.warning("RAG Service no disponible")
            return False
        
        try:
            # Generar IDs si no se proporcionan
            if not ids:
                import uuid
                ids = [str(uuid.uuid4()) for _ in documents]
            
            # Preparar metadatos
            if not metadatas:
                metadatas = [{} for _ in documents]
            
            # Agregar a la colección
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"✅ {len(documents)} documentos agregados a ChromaDB")
            return True
            
        except Exception as e:
            logger.error(f"Error al agregar documentos: {str(e)}")
            return False
    
    def query(
        self,
        query_text: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Buscar documentos relevantes
        
        Args:
            query_text: Texto de búsqueda
            n_results: Número de resultados
            where: Filtros opcionales
            
        Returns:
            Lista de documentos relevantes con metadatos
        """
        if not self.is_available():
            logger.warning("RAG Service no disponible")
            return []
        
        try:
            # Realizar búsqueda
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where
            )
            
            # Formatear resultados
            formatted_results = []
            
            if results and "documents" in results:
                for i, doc in enumerate(results["documents"][0]):
                    result = {
                        "document": doc,
                        "metadata": results["metadatas"][0][i] if "metadatas" in results else {},
                        "distance": results["distances"][0][i] if "distances" in results else None
                    }
                    formatted_results.append(result)
            
            logger.info(f"✅ Búsqueda retornó {len(formatted_results)} resultados")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error al buscar documentos: {str(e)}")
            return []
    
    def delete_documents(self, ids: List[str]) -> bool:
        """
        Eliminar documentos por ID
        
        Args:
            ids: Lista de IDs a eliminar
            
        Returns:
            True si se eliminaron exitosamente
        """
        if not self.is_available():
            logger.warning("RAG Service no disponible")
            return False
        
        try:
            self.collection.delete(ids=ids)
            logger.info(f"✅ {len(ids)} documentos eliminados")
            return True
            
        except Exception as e:
            logger.error(f"Error al eliminar documentos: {str(e)}")
            return False
    
    def get_collection_count(self) -> int:
        """Obtener número de documentos en la colección"""
        if not self.is_available():
            return 0
        
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Error al contar documentos: {str(e)}")
            return 0
    
    def reset_collection(self) -> bool:
        """
        Resetear la colección (eliminar todos los documentos)
        
        Returns:
            True si se reseteó exitosamente
        """
        if not self.client:
            logger.warning("RAG Service no disponible")
            return False
        
        try:
            # Eliminar colección existente
            self.client.delete_collection(name=self.collection_name)
            
            # Recrear colección
            self.collection = self._get_or_create_collection()
            
            logger.info("✅ Colección reseteada")
            return True
            
        except Exception as e:
            logger.error(f"Error al resetear colección: {str(e)}")
            return False


# Crear instancia global
try:
    rag_service = RAGService()
except Exception as e:
    logger.error(f"Error crítico al inicializar RAGService: {str(e)}")
    rag_service = None