import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
from app.core.config import settings
import uuid

class RAGService:
    """
    Servicio de Retrieval-Augmented Generation (RAG)
    para búsqueda semántica en documentos
    """
    
    def __init__(self):
        # Inicializar ChromaDB
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=settings.CHROMA_PERSIST_DIRECTORY
        ))
        
        # Modelo de embeddings
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # Colección principal
        self.collection_name = "documentos_cotizaciones"
        self.collection = self._get_or_create_collection()
    
    def _get_or_create_collection(self):
        """
        Obtiene o crea la colección de documentos
        """
        try:
            return self.client.get_collection(name=self.collection_name)
        except:
            return self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Documentos para cotizaciones"}
            )
    
    async def agregar_documento(
        self,
        texto: str,
        metadata: Dict[str, Any],
        documento_id: Optional[int] = None
    ) -> str:
        """
        Agrega un documento a la base vectorial
        """
        
        # Dividir texto en chunks si es muy largo
        chunks = self._dividir_en_chunks(texto, max_length=500)
        
        ids = []
        for i, chunk in enumerate(chunks):
            chunk_id = f"doc_{documento_id or uuid.uuid4()}_{i}"
            
            # Generar embedding
            embedding = self.model.encode(chunk).tolist()
            
            # Agregar a ChromaDB
            self.collection.add(
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{
                    **metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }],
                ids=[chunk_id]
            )
            
            ids.append(chunk_id)
        
        return f"Agregados {len(ids)} chunks del documento"
    
    async def buscar_similar(
        self,
        query: str,
        n_resultados: int = 5,
        filtros: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Busca documentos similares usando búsqueda semántica
        """
        
        # Generar embedding de la query
        query_embedding = self.model.encode(query).tolist()
        
        # Buscar en ChromaDB
        resultados = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_resultados,
            where=filtros
        )
        
        # Formatear resultados
        docs = []
        for i in range(len(resultados['ids'][0])):
            docs.append({
                "id": resultados['ids'][0][i],
                "texto": resultados['documents'][0][i],
                "metadata": resultados['metadatas'][0][i],
                "distancia": resultados['distances'][0][i] if 'distances' in resultados else None
            })
        
        return docs
    
    async def buscar_por_proyecto(
        self,
        query: str,
        proyecto_id: int,
        n_resultados: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Busca documentos relacionados a un proyecto específico
        """
        
        filtros = {"proyecto_id": str(proyecto_id)}
        return await self.buscar_similar(query, n_resultados, filtros)
    
    async def obtener_contexto_para_ia(
        self,
        query: str,
        proyecto_id: Optional[int] = None,
        max_tokens: int = 2000
    ) -> str:
        """
        Obtiene contexto relevante para alimentar a la IA
        """
        
        # Buscar documentos relevantes
        if proyecto_id:
            resultados = await self.buscar_por_proyecto(query, proyecto_id, n_resultados=10)
        else:
            resultados = await self.buscar_similar(query, n_resultados=10)
        
        # Construir contexto
        contexto_partes = []
        tokens_actuales = 0
        
        for doc in resultados:
            texto = doc['texto']
            tokens_estimados = len(texto.split())
            
            if tokens_actuales + tokens_estimados > max_tokens:
                break
            
            contexto_partes.append(f"--- Documento: {doc['metadata'].get('nombre', 'Sin nombre')} ---")
            contexto_partes.append(texto)
            contexto_partes.append("")
            
            tokens_actuales += tokens_estimados
        
        return '\n'.join(contexto_partes)
    
    def _dividir_en_chunks(self, texto: str, max_length: int = 500) -> List[str]:
        """
        Divide un texto largo en chunks manejables
        """
        
        palabras = texto.split()
        chunks = []
        chunk_actual = []
        longitud_actual = 0
        
        for palabra in palabras:
            chunk_actual.append(palabra)
            longitud_actual += len(palabra) + 1
            
            if longitud_actual >= max_length:
                chunks.append(' '.join(chunk_actual))
                chunk_actual = []
                longitud_actual = 0
        
        if chunk_actual:
            chunks.append(' '.join(chunk_actual))
        
        return chunks
    
    async def eliminar_documento(self, documento_id: int) -> bool:
        """
        Elimina todos los chunks de un documento
        """
        
        try:
            # Buscar todos los IDs que empiecen con doc_{documento_id}_
            prefix = f"doc_{documento_id}_"
            
            # ChromaDB no tiene filtro directo por prefijo, así que obtenemos todos
            all_ids = self.collection.get()['ids']
            ids_to_delete = [id for id in all_ids if id.startswith(prefix)]
            
            if ids_to_delete:
                self.collection.delete(ids=ids_to_delete)
            
            return True
        except Exception as e:
            print(f"Error al eliminar documento: {e}")
            return False
    
    async def limpiar_coleccion(self) -> bool:
        """
        Limpia toda la colección (usar con cuidado)
        """
        
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self._get_or_create_collection()
            return True
        except Exception as e:
            print(f"Error al limpiar colección: {e}")
            return False

# Instancia global
rag_service = RAGService()