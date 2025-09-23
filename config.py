"""
Configuration management for Meghalaya Tourism Bot.
Handles environment variables and application settings.
"""

import os
from typing import Optional
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

class Config:
    """Configuration class for managing application settings."""
    
    def __init__(self):
        """Initialize configuration from environment variables or Streamlit secrets."""
        load_dotenv()
        
        # Try to get configuration from Streamlit secrets first, then environment variables
        try:
            import streamlit as st
            # MongoDB Configuration
            self.mongodb_uri = st.secrets.get("mongodb", {}).get("uri") or self._get_env_var("MONGODB_URI", required=True)
            self.mongodb_database = st.secrets.get("mongodb", {}).get("database") or self._get_env_var("MONGODB_DATABASE", default="meghalaya_tourism")
            self.mongodb_collection = st.secrets.get("mongodb", {}).get("collection") or self._get_env_var("MONGODB_COLLECTION", default="tourism_documents")
            
            # OpenAI Configuration
            self.openai_api_key = st.secrets.get("openai", {}).get("api_key") or self._get_env_var("OPENAI_API_KEY", required=True)
            self.openai_model = st.secrets.get("openai", {}).get("model") or self._get_env_var("OPENAI_MODEL", default="gpt-4")
            self.openai_embedding_model = st.secrets.get("openai", {}).get("embedding_model") or self._get_env_var("OPENAI_EMBEDDING_MODEL", default="text-embedding-3-large")
            
            # Retrieval Parameters
            self.top_k_documents = int(st.secrets.get("retrieval", {}).get("top_k_documents") or self._get_env_var("TOP_K_DOCUMENTS", default="5"))
            self.temperature = float(st.secrets.get("retrieval", {}).get("temperature") or self._get_env_var("TEMPERATURE", default="0.7"))
            self.max_tokens = int(st.secrets.get("retrieval", {}).get("max_tokens") or self._get_env_var("MAX_TOKENS", default="1000"))
            
        except Exception:
            # Fallback to environment variables only
            # MongoDB Configuration
            self.mongodb_uri = self._get_env_var("MONGODB_URI", required=True)
            self.mongodb_database = self._get_env_var("MONGODB_DATABASE", default="meghalaya_tourism")
            self.mongodb_collection = self._get_env_var("MONGODB_COLLECTION", default="tourism_documents")
            
            # OpenAI Configuration
            self.openai_api_key = self._get_env_var("OPENAI_API_KEY", required=True)
            self.openai_model = self._get_env_var("OPENAI_MODEL", default="gpt-4")
            self.openai_embedding_model = self._get_env_var("OPENAI_EMBEDDING_MODEL", default="text-embedding-3-large")
            
            # Retrieval Parameters
            self.top_k_documents = int(self._get_env_var("TOP_K_DOCUMENTS", default="5"))
            self.temperature = float(self._get_env_var("TEMPERATURE", default="0.7"))
            self.max_tokens = int(self._get_env_var("MAX_TOKENS", default="1000"))
        
        # Streamlit Configuration
        self.streamlit_port = int(self._get_env_var("STREAMLIT_SERVER_PORT", default="8501"))
        self.streamlit_address = self._get_env_var("STREAMLIT_SERVER_ADDRESS", default="0.0.0.0")
        
        # Validate configuration
        self._validate_config()
    
    def _get_env_var(self, key: str, default: Optional[str] = None, required: bool = False) -> str:
        """Get environment variable with optional default value."""
        value = os.getenv(key, default)
        
        if required and not value:
            raise ValueError(f"Required environment variable '{key}' is not set. Please set it in Railway dashboard under Variables tab or in secrets.toml file.")
        
        return value
    
    def _validate_config(self):
        """Validate configuration values."""
        if self.top_k_documents <= 0:
            raise ValueError("TOP_K_DOCUMENTS must be a positive integer")
        
        if not 0 <= self.temperature <= 2:
            raise ValueError("TEMPERATURE must be between 0 and 2")
        
        if self.max_tokens <= 0:
            raise ValueError("MAX_TOKENS must be a positive integer")
        
        logger.info("Configuration validated successfully")
    
    def get_mongodb_config(self) -> dict:
        """Get MongoDB configuration as dictionary."""
        return {
            "uri": self.mongodb_uri,
            "database": self.mongodb_database,
            "collection": self.mongodb_collection
        }
    
    def get_openai_config(self) -> dict:
        """Get OpenAI configuration as dictionary."""
        return {
            "api_key": self.openai_api_key,
            "model": self.openai_model,
            "embedding_model": self.openai_embedding_model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
    
    def get_retrieval_config(self) -> dict:
        """Get retrieval configuration as dictionary."""
        return {
            "top_k": self.top_k_documents,
            "temperature": self.temperature
        }
