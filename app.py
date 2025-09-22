"""
Meghalaya Tourism Bot - Simple Streamlit Application
A simple chatbot for Meghalaya tourism information using RAG pipeline.
"""

import os
import streamlit as st
from dotenv import load_dotenv
import logging
from typing import List, Dict, Any
import json
from datetime import datetime
import time

# Import custom modules
from config import Config
from vector_store import VectorStoreManager
from rag_pipeline import RAGPipeline
from utils import ErrorHandler, ValidationUtils, LoggingUtils

# Configure logging
LoggingUtils.setup_logging()
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize configuration with error handling
try:
    config = Config()
    logger.info("Configuration loaded successfully")
except Exception as e:
    st.error(f"Configuration error: {str(e)}")
    st.stop()

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "rag_pipeline" not in st.session_state:
        st.session_state.rag_pipeline = None
    if "initialized" not in st.session_state:
        st.session_state.initialized = False
    if "config" not in st.session_state:
        st.session_state.config = None
    if "session_stats" not in st.session_state:
        st.session_state.session_stats = {
            "total_queries": 0,
            "successful_queries": 0,
            "total_response_time": 0,
            "start_time": datetime.now()
        }

def initialize_components():
    """Initialize vector store and RAG pipeline components."""
    try:
        if not st.session_state.initialized:
            with st.spinner("🌄 Initializing Meghalaya Tourism Assistant..."):
                # Validate configuration
                if not ValidationUtils.validate_mongodb_uri(config.mongodb_uri):
                    raise ValueError("Invalid MongoDB URI format")
                
                if not ValidationUtils.validate_openai_key(config.openai_api_key):
                    raise ValueError("Invalid OpenAI API key format")
                
                # Initialize vector store
                vector_store_manager = VectorStoreManager(config)
                
                # Test database connection
                if not vector_store_manager.test_connection():
                    raise ConnectionError("Failed to connect to MongoDB")
                
                st.session_state.vector_store = vector_store_manager.get_vector_store()
                
                # Initialize RAG pipeline
                st.session_state.rag_pipeline = RAGPipeline(config, st.session_state.vector_store)
                
                st.session_state.initialized = True
                st.session_state.config = config
                logger.info("Components initialized successfully")
                
    except Exception as e:
        st.error(f"Initialization error: {str(e)}")
        st.stop()

def setup_custom_css():
    """Setup custom CSS for better UI styling."""
    st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        
        .chat-message {
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border-left: 4px solid #2a5298;
        }
        
        .user-message {
            background-color: #e3f2fd;
            margin-left: 20%;
        }
        
        .bot-message {
            background-color: #f5f5f5;
            margin-right: 20%;
        }
        
        .source-info {
            background-color: #fff3e0;
            padding: 0.5rem;
            border-radius: 5px;
            margin-top: 0.5rem;
            font-size: 0.8rem;
            border-left: 3px solid #ff9800;
        }
        
        .stats-container {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        .footer {
            text-align: center;
            padding: 2rem;
            color: #666;
            border-top: 1px solid #eee;
            margin-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the main header section."""
    st.markdown("""
        <div class="main-header">
            <h1>🏔️ Meghalaya Tourism Bot</h1>
            <p>Your virtual guide to the beautiful state of Meghalaya, India</p>
        </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with information and controls."""
    with st.sidebar:
        st.header("📋 Bot Information")
        
        # Bot status
        if st.session_state.get("initialized", False):
            st.success("✅ Bot is ready!")
        else:
            st.error("❌ Bot is initializing...")
        
        # Quick actions
        st.subheader("🚀 Quick Actions")
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        # Statistics
        if st.session_state.get("initialized", False):
            st.subheader("📊 Session Statistics")
            stats = st.session_state.session_stats
            
            st.metric("Total Queries", stats["total_queries"])
            st.metric("Success Rate", f"{(stats['successful_queries']/max(stats['total_queries'], 1)*100):.1f}%")
            
            if stats["total_queries"] > 0:
                avg_time = stats["total_response_time"] / stats["total_queries"]
                st.metric("Avg Response Time", f"{avg_time:.2f}s")
        
        # Quick questions
        st.subheader("💡 Quick Questions")
        quick_questions = [
            "Tell me about living root bridges",
            "What festivals are in Meghalaya?",
            "Best places to visit in Shillong",
            "What to do in Cherrapunji?",
            "Adventure activities in Meghalaya"
        ]
        
        for question in quick_questions:
            if st.button(f"❓ {question}", use_container_width=True):
                # Add question to chat
                st.session_state.messages.append({
                    "role": "user",
                    "content": question,
                    "timestamp": datetime.now().isoformat()
                })
                st.rerun()
        
        # About section
        st.subheader("ℹ️ About")
        st.info("""
        **Meghalaya Tourism Bot** is your AI-powered guide to explore the beautiful state of Meghalaya.
        
        Ask me about:
        • Tourist attractions
        • Cultural festivals
        • Travel tips
        • Local cuisine
        • Adventure activities
        """)

def render_chat_messages():
    """Render chat messages in the conversation."""
    if not st.session_state.messages:
        # Welcome message
        st.markdown("""
       
        """, unsafe_allow_html=True)
        return
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show source attribution if available
            if message.get("sources"):
                st.markdown("**📚 Sources:**")
                for i, source in enumerate(message["sources"], 1):
                    source_title = source.get("metadata", {}).get("title", f"Source {i}")
                    source_score = source.get("score", 0)
                    st.markdown(f"""
                    <div class="source-info">
                        {i}. {source_title} (Relevance: {source_score:.2f})
                    </div>
                    """, unsafe_allow_html=True)

def generate_and_display_response(user_input: str):
    """Generate and display bot response."""
    if not st.session_state.get("rag_pipeline"):
        st.error("RAG pipeline not initialized. Please refresh the page.")
        return
    
    # Update session stats
    st.session_state.session_stats["total_queries"] += 1
    
    # Show loading spinner
    with st.spinner("🌄 Thinking about your question..."):
        start_time = datetime.now()
        
        # Process query through RAG pipeline
        result = st.session_state.rag_pipeline.process_query(user_input)
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
    
    # Update session stats
    st.session_state.session_stats["total_response_time"] += processing_time
    if result["success"]:
        st.session_state.session_stats["successful_queries"] += 1
    
    # Prepare response data
    response_data = {
        "role": "assistant",
        "content": result["response"],
        "timestamp": end_time.isoformat(),
        "metadata": {
            "processing_time": processing_time,
            "success": result["success"],
            "num_documents": result.get("num_documents", 0),
            "context_length": result.get("context_length", 0)
        }
    }
    
    # Add sources if available
    if result.get("documents"):
        response_data["sources"] = result["documents"]
    
    # Add to chat history
    st.session_state.messages.append(response_data)
    
    # Display bot response
    with st.chat_message("assistant"):
        st.markdown(result["response"])
        
        # Show source attribution
        if result.get("documents"):
            st.markdown("**📚 Sources:**")
            for i, source in enumerate(result["documents"], 1):
                source_title = source.get("metadata", {}).get("title", f"Source {i}")
                source_score = source.get("score", 0)
                st.markdown(f"""
                <div class="source-info">
                    {i}. {source_title} (Relevance: {source_score:.2f})
                </div>
                """, unsafe_allow_html=True)

def main():
    """Main application function."""
    # Page configuration
    st.set_page_config(
        page_title="Meghalaya Tourism Bot",
        page_icon="🏔️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Setup custom CSS
    setup_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Initialize components
    initialize_components()
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Main chat interface
    st.markdown("### 💬 Chat with Meghalaya Tourism Bot")
    
    # Display chat messages
    render_chat_messages()
    
    # Chat input - outside of any columns
    if prompt := st.chat_input("Ask me anything about Meghalaya tourism..."):
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate bot response
        generate_and_display_response(prompt)
    
    # Footer
    st.markdown("""
        <div class="footer">
            <p>🏔️ Meghalaya Tourism Bot | Powered by LangChain, MongoDB, and OpenAI</p>
            <p>Built with ❤️ for travelers exploring the beautiful state of Meghalaya</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()