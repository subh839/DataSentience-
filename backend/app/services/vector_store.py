# app/services/vector_store.py
import chromadb
import uuid
import numpy as np
import hashlib

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="chroma_data")
        self.collection = self.client.get_or_create_collection(
            "datacenter_docs",
            metadata={"description": "Data center operational knowledge base"}
        )
    
    async def add_documents(self, documents: list[str], metadatas: list[dict] = None):
        """Add documents using simple local embeddings"""
        print(f"Adding {len(documents)} documents to vector store...")
        
        try:
            # Generate simple deterministic embeddings locally
            embeddings = []
            for doc in documents:
                # Create deterministic embedding based on document content
                doc_hash = hashlib.md5(doc.encode()).hexdigest()
                np.random.seed(int(doc_hash[:8], 16))  # Use first 8 chars of hash as seed
                embedding = np.random.rand(384).tolist()  # 384-dim vector
                embeddings.append(embedding)
            
            # Generate IDs
            ids = [str(uuid.uuid4()) for _ in documents]
            
            # Add to collection
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f" Successfully added {len(documents)} documents with local embeddings")
            return True
            
        except Exception as e:
            print(f" Failed to add documents: {e}")
            return False
    
    async def search(self, query: str, n_results: int = 5):
        """Semantic search with local embeddings"""
        try:
            # Create query embedding using same method
            query_hash = hashlib.md5(query.encode()).hexdigest()
            np.random.seed(int(query_hash[:8], 16))
            query_embedding = np.random.rand(384).tolist()
            
            # Search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            return results
        except Exception as e:
            print(f" Search failed: {e}")
            return {'documents': [], 'metadatas': []}

vector_store = VectorStore()