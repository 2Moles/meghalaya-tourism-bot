"""
MongoDB Vector Store Manager for Meghalaya Tourism Bot.
Handles vector search operations using MongoDB Atlas Vector Search.
"""

import logging
from typing import List, Dict, Any, Optional
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient
from config import Config

logger = logging.getLogger(__name__)

class VectorStoreManager:
    """Manages MongoDB vector store operations."""
    
    def __init__(self, config: Config):
        """Initialize vector store manager with configuration."""
        self.config = config
        self.mongodb_config = config.get_mongodb_config()
        self.openai_config = config.get_openai_config()
        
        # Initialize MongoDB client
        self.client = MongoClient(self.mongodb_config["uri"])
        self.database = self.client[self.mongodb_config["database"]]
        self.collection = self.database[self.mongodb_config["collection"]]
        
        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=self.openai_config["api_key"],
            model=self.openai_config["embedding_model"]
        )
        
        logger.info("VectorStoreManager initialized successfully")
    
    def get_vector_store(self) -> MongoDBAtlasVectorSearch:
        """Get MongoDB Atlas Vector Search instance."""
        try:
            vector_store = MongoDBAtlasVectorSearch(
                collection=self.collection,
                embedding=self.embeddings,
                index_name="vector_index"  # Default index name
            )
            
            logger.info("Vector store connection established")
            return vector_store
            
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise
    
    def search_documents(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant documents using vector similarity."""
        try:
            vector_store = self.get_vector_store()
            
            # Perform vector search
            results = vector_store.similarity_search_with_score(
                query=query,
                k=k
            )
            
            # Format results
            documents = []
            for doc, score in results:
                documents.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": score
                })
            
            logger.info(f"Found {len(documents)} relevant documents for query: {query[:50]}...")
            return documents
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific document by ID."""
        try:
            document = self.collection.find_one({"_id": doc_id})
            if document:
                return {
                    "content": document.get("page_content", ""),
                    "metadata": document.get("metadata", {}),
                    "id": str(document["_id"])
                }
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving document {doc_id}: {str(e)}")
            return None
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics."""
        try:
            total_docs = self.collection.count_documents({})
            
            # Get sample of documents to analyze content
            sample_docs = list(self.collection.find().limit(10))
            
            stats = {
                "total_documents": total_docs,
                "collection_name": self.mongodb_config["collection"],
                "database_name": self.mongodb_config["database"],
                "sample_documents": len(sample_docs)
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {"error": str(e)}
    
    def test_connection(self) -> bool:
        """Test MongoDB connection."""
        try:
            # Test basic connection
            self.client.admin.command('ping')
            
            # Test collection access
            self.collection.find_one()
            
            logger.info("MongoDB connection test successful")
            return True
            
        except Exception as e:
            logger.error(f"MongoDB connection test failed: {str(e)}")
            return False
    
    def close_connection(self):
        """Close MongoDB connection."""
        try:
            self.client.close()
            logger.info("MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {str(e)}")
