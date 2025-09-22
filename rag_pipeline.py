"""
RAG Pipeline for Meghalaya Tourism Bot.
Handles retrieval-augmented generation using MongoDB vector search and OpenAI GPT-4.
"""

import logging
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from config import Config

logger = logging.getLogger(__name__)

class RAGPipeline:
    """Retrieval-Augmented Generation pipeline for tourism information."""
    
    def __init__(self, config: Config, vector_store):
        """Initialize RAG pipeline with configuration and vector store."""
        self.config = config
        self.vector_store = vector_store
        self.openai_config = config.get_openai_config()
        self.retrieval_config = config.get_retrieval_config()
        
        # Initialize OpenAI chat model
        self.llm = ChatOpenAI(
            openai_api_key=self.openai_config["api_key"],
            model_name=self.openai_config["model"],
            temperature=self.openai_config["temperature"],
            max_tokens=self.openai_config["max_tokens"]
        )
        
        # Define system prompt for Meghalaya tourism
        self.system_prompt = self._create_system_prompt()
        
        # Create chat prompt template
        self.chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.system_prompt),
            HumanMessagePromptTemplate.from_template("{question}")
        ])
        
        logger.info("RAG Pipeline initialized successfully")
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for Meghalaya tourism bot."""
        return """You are a knowledgeable and friendly Meghalaya Tourism Bot, designed to provide comprehensive, accurate, and helpful travel-related information about Meghalaya, India. 

Your role is to:
- Provide detailed information about Meghalaya's attractions, culture, festivals, and travel tips
- Help users plan their trips with practical advice on accommodation, transportation, and activities
- Share insights about local customs, traditions, and cultural experiences
- Offer recommendations based on user preferences and interests
- Provide up-to-date information about weather, seasons, and travel conditions

Key areas of expertise:
- Natural attractions: Living Root Bridges, Cherrapunji, Mawsynram, Shillong, etc.
- Cultural heritage: Khasi, Garo, and Jaintia traditions
- Festivals: Nongkrem, Wangala, Behdienkhlam, etc.
- Adventure activities: Trekking, caving, river rafting
- Local cuisine and dining recommendations
- Accommodation options and booking tips
- Transportation and getting around
- Best times to visit and seasonal considerations

Always be:
- Accurate and up-to-date in your information
- Culturally sensitive and respectful
- Helpful and encouraging about visiting Meghalaya
- Specific with recommendations and practical details
- Ready to provide additional information when asked

Use the provided context documents to enhance your responses with specific details, but always prioritize accuracy and helpfulness. If you're unsure about something, say so and suggest how the user might find more information.

Context from tourism documents:
{context}

Please provide a helpful and informative response about Meghalaya tourism based on the user's question and the context provided above."""
    
    def retrieve_documents(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for the given query."""
        try:
            documents = self.vector_store.search_documents(
                query=query,
                k=self.retrieval_config["top_k"]
            )
            
            logger.info(f"Retrieved {len(documents)} documents for query: {query[:50]}...")
            return documents
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []
    
    def format_context(self, documents: List[Dict[str, Any]]) -> str:
        """Format retrieved documents into context string."""
        if not documents:
            return "No relevant tourism documents found for this query."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            score = doc.get("score", 0)
            
            # Extract source information
            source = metadata.get("source", "Unknown source")
            title = metadata.get("title", f"Document {i}")
            
            context_parts.append(f"""
Document {i} (Source: {source}, Title: {title}, Relevance Score: {score:.3f}):
{content}
---"""
            )
        
        return "\n".join(context_parts)
    
    def generate_response(self, query: str, context: str) -> Dict[str, Any]:
        """Generate response using retrieved context."""
        try:
            # Create messages for the chat model
            messages = [
                SystemMessage(content=self.system_prompt.format(context=context)),
                HumanMessage(content=query)
            ]
            
            # Generate response
            response = self.llm(messages)
            
            return {
                "response": response.content,
                "success": True,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                "response": f"I apologize, but I encountered an error while generating a response: {str(e)}",
                "success": False,
                "error": str(e)
            }
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a user query through the complete RAG pipeline."""
        try:
            logger.info(f"Processing query: {query[:100]}...")
            
            # Step 1: Retrieve relevant documents
            documents = self.retrieve_documents(query)
            
            # Step 2: Format context
            context = self.format_context(documents)
            
            # Step 3: Generate response
            result = self.generate_response(query, context)
            
            # Add metadata to result
            result["documents"] = documents
            result["context_length"] = len(context)
            result["num_documents"] = len(documents)
            
            logger.info(f"Query processed successfully. Generated response with {len(documents)} documents.")
            return result
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "response": f"I apologize, but I encountered an error while processing your request: {str(e)}",
                "success": False,
                "error": str(e),
                "documents": [],
                "context_length": 0,
                "num_documents": 0
            }
    
    def get_conversation_summary(self, messages: List[Dict[str, Any]]) -> str:
        """Generate a summary of the conversation for context."""
        if not messages:
            return "No previous conversation context."
        
        # Extract recent messages (last 5)
        recent_messages = messages[-5:] if len(messages) > 5 else messages
        
        summary_parts = []
        for msg in recent_messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")[:100]  # Truncate long messages
            summary_parts.append(f"{role}: {content}")
        
        return "Recent conversation:\n" + "\n".join(summary_parts)
    
    def enhance_query_with_context(self, query: str, conversation_history: List[Dict[str, Any]]) -> str:
        """Enhance query with conversation context if relevant."""
        if not conversation_history:
            return query
        
        # Simple enhancement - add context if the query seems to reference previous conversation
        context_indicators = ["that", "this", "it", "there", "those", "above", "mentioned", "earlier"]
        
        if any(indicator in query.lower() for indicator in context_indicators):
            context_summary = self.get_conversation_summary(conversation_history)
            enhanced_query = f"Context: {context_summary}\n\nCurrent question: {query}"
            return enhanced_query
        
        return query
