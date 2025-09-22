"""
Utility functions for Meghalaya Tourism Bot.
Handles error handling, logging, and common utilities.
"""

import logging
import traceback
from typing import Any, Dict, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ErrorHandler:
    """Centralized error handling for the application."""
    
    @staticmethod
    def handle_database_error(error: Exception, operation: str) -> Dict[str, Any]:
        """Handle database-related errors."""
        error_msg = f"Database error during {operation}: {str(error)}"
        logger.error(error_msg)
        
        return {
            "success": False,
            "error": "Database connection failed. Please check your MongoDB configuration.",
            "details": error_msg,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def handle_openai_error(error: Exception, operation: str) -> Dict[str, Any]:
        """Handle OpenAI API errors."""
        error_msg = f"OpenAI API error during {operation}: {str(error)}"
        logger.error(error_msg)
        
        return {
            "success": False,
            "error": "AI service temporarily unavailable. Please try again later.",
            "details": error_msg,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def handle_configuration_error(error: Exception) -> Dict[str, Any]:
        """Handle configuration errors."""
        error_msg = f"Configuration error: {str(error)}"
        logger.error(error_msg)
        
        return {
            "success": False,
            "error": "Configuration error. Please check your environment variables.",
            "details": error_msg,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def handle_general_error(error: Exception, operation: str) -> Dict[str, Any]:
        """Handle general application errors."""
        error_msg = f"Unexpected error during {operation}: {str(error)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        
        return {
            "success": False,
            "error": "An unexpected error occurred. Please try again.",
            "details": error_msg,
            "timestamp": datetime.now().isoformat()
        }

class ValidationUtils:
    """Utility functions for data validation."""
    
    @staticmethod
    def validate_mongodb_uri(uri: str) -> bool:
        """Validate MongoDB URI format."""
        if not uri:
            return False
        
        # Basic URI validation
        valid_schemes = ["mongodb://", "mongodb+srv://"]
        return any(uri.startswith(scheme) for scheme in valid_schemes)
    
    @staticmethod
    def validate_openai_key(api_key: str) -> bool:
        """Validate OpenAI API key format."""
        if not api_key:
            return False
        
        # OpenAI API keys typically start with 'sk-'
        return api_key.startswith('sk-') and len(api_key) > 20
    
    @staticmethod
    def validate_temperature(temperature: float) -> bool:
        """Validate temperature parameter."""
        return 0.0 <= temperature <= 2.0
    
    @staticmethod
    def validate_top_k(top_k: int) -> bool:
        """Validate top-k parameter."""
        return 1 <= top_k <= 20

class LoggingUtils:
    """Utility functions for logging."""
    
    @staticmethod
    def setup_logging(level: str = "INFO") -> None:
        """Setup application logging configuration."""
        log_level = getattr(logging, level.upper(), logging.INFO)
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('meghalaya_bot.log')
            ]
        )
        
        logger.info(f"Logging configured at {level} level")
    
    @staticmethod
    def log_query_metrics(query: str, response_time: float, num_documents: int, success: bool) -> None:
        """Log query performance metrics."""
        logger.info(f"Query: {query[:50]}... | "
                   f"Response Time: {response_time:.2f}s | "
                   f"Documents: {num_documents} | "
                   f"Success: {success}")

class ResponseUtils:
    """Utility functions for response formatting."""
    
    @staticmethod
    def format_error_response(error_data: Dict[str, Any]) -> str:
        """Format error data into user-friendly message."""
        base_message = error_data.get("error", "An error occurred")
        
        # Add helpful suggestions based on error type
        if "Database" in error_data.get("details", ""):
            base_message += "\n\n💡 **Troubleshooting Tips:**\n"
            base_message += "- Check your MongoDB connection string\n"
            base_message += "- Verify your network connection\n"
            base_message += "- Ensure MongoDB Atlas is accessible"
        
        elif "OpenAI" in error_data.get("details", ""):
            base_message += "\n\n💡 **Troubleshooting Tips:**\n"
            base_message += "- Check your OpenAI API key\n"
            base_message += "- Verify you have sufficient API credits\n"
            base_message += "- Check OpenAI service status"
        
        elif "Configuration" in error_data.get("details", ""):
            base_message += "\n\n💡 **Troubleshooting Tips:**\n"
            base_message += "- Check your .env file\n"
            base_message += "- Verify all required environment variables are set\n"
            base_message += "- Restart the application after configuration changes"
        
        return base_message
    
    @staticmethod
    def format_success_response(response: str, sources: list = None) -> Dict[str, Any]:
        """Format successful response with metadata."""
        return {
            "response": response,
            "success": True,
            "sources": sources or [],
            "timestamp": datetime.now().isoformat()
        }

class DataUtils:
    """Utility functions for data processing."""
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100) -> str:
        """Truncate text to specified length with ellipsis."""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    @staticmethod
    def extract_keywords(text: str) -> list:
        """Extract potential keywords from text."""
        # Simple keyword extraction (can be enhanced with NLP libraries)
        words = text.lower().split()
        # Filter out common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must'}
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return list(set(keywords))[:10]  # Return top 10 unique keywords
    
    @staticmethod
    def calculate_response_quality(response: str, query: str) -> float:
        """Calculate a simple quality score for the response."""
        if not response or not query:
            return 0.0
        
        # Simple quality metrics
        response_length = len(response)
        query_keywords = DataUtils.extract_keywords(query)
        response_keywords = DataUtils.extract_keywords(response)
        
        # Check if response contains query keywords
        keyword_match = len(set(query_keywords) & set(response_keywords)) / max(len(query_keywords), 1)
        
        # Length score (prefer responses that are not too short or too long)
        length_score = min(response_length / 500, 1.0)  # Optimal around 500 characters
        
        # Combined quality score
        quality_score = (keyword_match * 0.7 + length_score * 0.3)
        return min(quality_score, 1.0)

def safe_json_serialize(obj: Any) -> str:
    """Safely serialize object to JSON string."""
    try:
        return json.dumps(obj, default=str, indent=2)
    except Exception as e:
        logger.error(f"JSON serialization error: {str(e)}")
        return str(obj)

def format_timestamp(timestamp: str = None) -> str:
    """Format timestamp for display."""
    if not timestamp:
        timestamp = datetime.now().isoformat()
    
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return timestamp
