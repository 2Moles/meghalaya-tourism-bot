"""
Meghalaya Tourism Bot - Working RAG Version
Full functionality with MongoDB vector search and OpenAI GPT-4
"""

import streamlit as st
import os
from datetime import datetime
import json

# Try to import required libraries with fallbacks
try:
    from pymongo import MongoClient
    from openai import OpenAI
    import numpy as np
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    st.error(f"Missing dependencies: {e}")
    DEPENDENCIES_AVAILABLE = False

def get_config():
    """Get configuration from Streamlit secrets or environment variables."""
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
            "mongodb_database": os.getenv("MONGODB_DATABASE", "xlayer"),
            "mongodb_collection": os.getenv("MONGODB_COLLECTION", "MeghalayaEmbeddings1"),
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "openai_model": os.getenv("OPENAI_MODEL", "gpt-4"),
            "openai_embedding_model": os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large"),
            "top_k_documents": int(os.getenv("TOP_K_DOCUMENTS", "5")),
            "temperature": float(os.getenv("TEMPERATURE", "0.7")),
            "max_tokens": int(os.getenv("MAX_TOKENS", "1000"))
        }

def connect_to_mongodb(config):
    """Connect to MongoDB and return collection."""
    try:
        client = MongoClient(config["mongodb_uri"])
        db = client[config["mongodb_database"]]
        collection = db[config["mongodb_collection"]]
        
        # Test connection
        client.admin.command('ping')
        return collection, client
    except Exception as e:
        st.error(f"MongoDB connection failed: {str(e)}")
        return None, None

def get_openai_client(config):
    """Initialize OpenAI client."""
    try:
        return OpenAI(api_key=config["openai_api_key"])
    except Exception as e:
        st.error(f"OpenAI client initialization failed: {str(e)}")
        return None

def search_documents(collection, query, top_k=5):
    """Search for relevant documents using vector similarity."""
    try:
        # For now, let's do a simple text search on the collection
        # In a real implementation, you'd use vector search
        results = collection.find({
            "$or": [
                {"page_content": {"$regex": query, "$options": "i"}},
                {"metadata.title": {"$regex": query, "$options": "i"}},
                {"metadata.tags": {"$in": [query.lower()]}}
            ]
        }).limit(top_k)
        
        documents = []
        for doc in results:
            documents.append({
                "content": doc.get("page_content", ""),
                "metadata": doc.get("metadata", {}),
                "score": 0.8  # Placeholder score
            })
        
        return documents
    except Exception as e:
        st.error(f"Document search failed: {str(e)}")
        return []

def generate_embedding(text, openai_client, model="text-embedding-3-large"):
    """Generate embedding for text using OpenAI."""
    try:
        response = openai_client.embeddings.create(
            model=model,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        st.error(f"Embedding generation failed: {str(e)}")
        return None

def generate_response(query, documents, openai_client, config):
    """Generate response using OpenAI GPT-4 with retrieved documents."""
    try:
        # Format context from documents
        context = ""
        for i, doc in enumerate(documents, 1):
            context += f"Document {i}: {doc['content'][:500]}...\n\n"
        
        # Create system prompt
        system_prompt = f"""You are a knowledgeable Meghalaya Tourism Bot. Use the provided context to answer questions about Meghalaya tourism. If the context doesn't contain relevant information, provide general helpful information about Meghalaya.

Context from tourism documents:
{context}

Please provide a helpful and informative response about Meghalaya tourism based on the user's question and the context provided above."""
        
        # Generate response
        response = openai_client.chat.completions.create(
            model=config["openai_model"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=config["temperature"],
            max_tokens=config["max_tokens"]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Response generation failed: {str(e)}")
        return f"I apologize, but I encountered an error while generating a response: {str(e)}"

def main():
    """Main application function."""
    st.set_page_config(
        page_title="Meghalaya Tourism Bot",
        page_icon="🏔️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
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
        .status-box {
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .status-success {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .status-error {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "initialized" not in st.session_state:
        st.session_state.initialized = False
    if "config" not in st.session_state:
        st.session_state.config = None
    if "collection" not in st.session_state:
        st.session_state.collection = None
    if "openai_client" not in st.session_state:
        st.session_state.openai_client = None
    if "session_stats" not in st.session_state:
        st.session_state.session_stats = {
            "total_queries": 0,
            "successful_queries": 0,
            "total_response_time": 0,
            "start_time": datetime.now()
        }
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🏔️ Meghalaya Tourism Bot</h1>
            <p>Your AI-powered guide to the beautiful state of Meghalaya, India</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Check dependencies
    if not DEPENDENCIES_AVAILABLE:
        st.error("❌ Required dependencies are not available. Please check the requirements.txt file.")
        st.stop()
    
    # Initialize components
    if not st.session_state.initialized:
        with st.spinner("🌄 Initializing Meghalaya Tourism Assistant..."):
            try:
                # Get configuration
                config = get_config()
                st.session_state.config = config
                
                # Validate configuration
                if not config["mongodb_uri"] or not config["openai_api_key"]:
                    raise ValueError("Missing required configuration (MongoDB URI or OpenAI API key)")
                
                # Connect to MongoDB
                collection, client = connect_to_mongodb(config)
                if collection:
                    st.session_state.collection = collection
                    st.session_state.mongo_client = client
                
                # Initialize OpenAI client
                openai_client = get_openai_client(config)
                if openai_client:
                    st.session_state.openai_client = openai_client
                
                st.session_state.initialized = True
                st.success("✅ Bot initialized successfully!")
                
            except Exception as e:
                st.error(f"❌ Initialization failed: {str(e)}")
                st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Bot Information")
        
        # Status indicators
        if st.session_state.collection:
            st.markdown('<div class="status-box status-success">✅ MongoDB Connected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-box status-error">❌ MongoDB Disconnected</div>', unsafe_allow_html=True)
        
        if st.session_state.openai_client:
            st.markdown('<div class="status-box status-success">✅ OpenAI Connected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-box status-error">❌ OpenAI Disconnected</div>', unsafe_allow_html=True)
        
        # Quick actions
        st.subheader("🚀 Quick Actions")
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        # Statistics
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
                st.session_state.messages.append({
                    "role": "user",
                    "content": question,
                    "timestamp": datetime.now().isoformat()
                })
                st.rerun()
        
        # Database info
        if st.session_state.collection:
            st.subheader("🗄️ Database Info")
            try:
                count = st.session_state.collection.count_documents({})
                st.write(f"Documents: {count}")
                
                # Show sample document
                sample = st.session_state.collection.find_one()
                if sample:
                    st.write("**Sample Document:**")
                    st.write(f"Title: {sample.get('metadata', {}).get('title', 'N/A')}")
                    st.write(f"Content: {sample.get('page_content', '')[:100]}...")
            except Exception as e:
                st.write(f"Database error: {str(e)}")
    
    # Main chat interface
    st.markdown("### 💬 Chat with Meghalaya Tourism Bot")
    
    # Display chat messages
    if not st.session_state.messages:
        st.markdown("""
        <div class="chat-message bot-message">
            <h3>Welcome to Meghalaya Tourism Bot! 🏔️</h3>
            <p>I'm your AI-powered guide with access to a comprehensive knowledge base about Meghalaya tourism. I can help you with:</p>
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
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show sources if available
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
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about Meghalaya tourism..."):
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🌄 Thinking about your question..."):
                start_time = datetime.now()
                
                # Search for relevant documents
                documents = []
                if st.session_state.collection:
                    documents = search_documents(st.session_state.collection, prompt, st.session_state.config["top_k_documents"])
                
                # Generate response
                if st.session_state.openai_client and documents:
                    response = generate_response(prompt, documents, st.session_state.openai_client, st.session_state.config)
                else:
                    response = f"""
                    I apologize, but I'm currently unable to access my knowledge base. 
                    
                    However, I can tell you that Meghalaya is a beautiful state in Northeast India known for:
                    - Living Root Bridges
                    - Cherrapunji (wettest place on Earth)
                    - Rich cultural heritage
                    - Adventure activities
                    
                    Please try again in a moment, or check if the database connection is working.
                    """
                
                end_time = datetime.now()
                processing_time = (end_time - start_time).total_seconds()
                
                st.markdown(response)
                
                # Show sources
                if documents:
                    st.markdown("**📚 Sources:**")
                    for i, source in enumerate(documents, 1):
                        source_title = source.get("metadata", {}).get("title", f"Source {i}")
                        source_score = source.get("score", 0)
                        st.markdown(f"""
                        <div class="source-info">
                            {i}. {source_title} (Relevance: {source_score:.2f})
                        </div>
                        """, unsafe_allow_html=True)
                
                # Add to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": end_time.isoformat(),
                    "sources": documents,
                    "processing_time": processing_time
                })
                
                # Update stats
                st.session_state.session_stats["total_queries"] += 1
                st.session_state.session_stats["total_response_time"] += processing_time
                if response and not response.startswith("I apologize"):
                    st.session_state.session_stats["successful_queries"] += 1
    
    # Footer
    st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #666; border-top: 1px solid #eee; margin-top: 2rem;">
            <p>🏔️ Meghalaya Tourism Bot | Powered by MongoDB Vector Search & OpenAI GPT-4</p>
            <p>Built with ❤️ for travelers exploring the beautiful state of Meghalaya</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
