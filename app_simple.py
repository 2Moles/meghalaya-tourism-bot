"""
Meghalaya Tourism Bot - Simplified Streamlit Application
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

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_config():
    """Get configuration from environment variables or Streamlit secrets."""
    try:
        # Try Streamlit secrets first
        return {
            "mongodb_uri": st.secrets["mongodb"]["uri"],
            "mongodb_database": st.secrets["mongodb"]["database"],
            "mongodb_collection": st.secrets["mongodb"]["collection"],
            "openai_api_key": st.secrets["openai"]["api_key"],
            "openai_model": st.secrets["openai"]["model"],
            "openai_embedding_model": st.secrets["openai"]["embedding_model"],
            "top_k_documents": int(st.secrets["retrieval"]["top_k_documents"]),
            "temperature": float(st.secrets["retrieval"]["temperature"]),
            "max_tokens": int(st.secrets["retrieval"]["max_tokens"])
        }
    except:
        # Fallback to environment variables
        return {
            "mongodb_uri": os.getenv("MONGODB_URI"),
            "mongodb_database": os.getenv("MONGODB_DATABASE", "meghalaya_tourism"),
            "mongodb_collection": os.getenv("MONGODB_COLLECTION", "tourism_documents"),
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "openai_model": os.getenv("OPENAI_MODEL", "gpt-4"),
            "openai_embedding_model": os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large"),
            "top_k_documents": int(os.getenv("TOP_K_DOCUMENTS", "5")),
            "temperature": float(os.getenv("TEMPERATURE", "0.7")),
            "max_tokens": int(os.getenv("MAX_TOKENS", "1000"))
        }

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
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
    """Initialize components with error handling."""
    try:
        if not st.session_state.initialized:
            with st.spinner("🌄 Initializing Meghalaya Tourism Assistant..."):
                # Get configuration
                config = get_config()
                st.session_state.config = config
                
                # Validate required fields
                if not config["mongodb_uri"] or not config["openai_api_key"]:
                    raise ValueError("Missing required configuration")
                
                st.session_state.initialized = True
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
        <div class="chat-message bot-message">
            <h3>Welcome to Meghalaya Tourism Bot! 🏔️</h3>
            <p>I'm here to help you discover the beautiful state of Meghalaya. You can ask me about:</p>
            <ul>
                <li>🏞️ Tourist attractions and places to visit</li>
                <li>🎭 Cultural festivals and traditions</li>
                <li>🏨 Accommodation and travel tips</li>
                <li>🍽️ Local cuisine and dining</li>
                <li>🚗 Transportation and getting around</li>
                <li>📅 Best times to visit</li>
                <li>🎒 Adventure activities and trekking</li>
            </ul>
            <p><strong>What would you like to know about Meghalaya?</strong></p>
        </div>
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

def generate_simple_response(user_input: str):
    """Generate a simple response without RAG for now."""
    # Update session stats
    st.session_state.session_stats["total_queries"] += 1
    
    # Simple response for testing
    response = f"""
    Thank you for your question: "{user_input}"
    
    I'm the Meghalaya Tourism Bot! While I'm still connecting to my knowledge base, I can tell you that Meghalaya is a beautiful state in Northeast India known for:
    
    🏔️ **Living Root Bridges** - Unique natural bridges made from tree roots
    💧 **Cherrapunji** - One of the wettest places on Earth
    🌿 **Lush Green Landscapes** - Rolling hills and pristine nature
    🎭 **Rich Culture** - Home to Khasi, Garo, and Jaintia tribes
    🎒 **Adventure Activities** - Trekking, caving, and river rafting
    
    Please check back in a few minutes as I connect to my full knowledge base!
    """
    
    # Update session stats
    st.session_state.session_stats["successful_queries"] += 1
    st.session_state.session_stats["total_response_time"] += 1.0
    
    return response

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
        with st.chat_message("assistant"):
            response = generate_simple_response(prompt)
            st.markdown(response)
            
            # Add to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat()
            })
    
    # Footer
    st.markdown("""
        <div class="footer">
            <p>🏔️ Meghalaya Tourism Bot | Powered by AI</p>
            <p>Built with ❤️ for travelers exploring the beautiful state of Meghalaya</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
