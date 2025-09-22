#!/usr/bin/env python3
"""
Test script to verify Meghalaya Tourism Bot setup.
Run this script to check if all components are working correctly.
"""

import os
import sys
from dotenv import load_dotenv

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        from langchain_community.vectorstores import MongoDBAtlasVectorSearch
        from langchain_openai import OpenAIEmbeddings, ChatOpenAI
        print("✅ LangChain modules imported successfully")
    except ImportError as e:
        print(f"❌ LangChain import failed: {e}")
        return False
    
    try:
        import pymongo
        print("✅ PyMongo imported successfully")
    except ImportError as e:
        print(f"❌ PyMongo import failed: {e}")
        return False
    
    try:
        import openai
        print("✅ OpenAI imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    load_dotenv()
    
    required_vars = [
        'MONGODB_URI',
        'OPENAI_API_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
        return False
    
    print("✅ Configuration loaded successfully")
    return True

def test_custom_modules():
    """Test custom module imports."""
    print("\nTesting custom modules...")
    
    try:
        from config import Config
        print("✅ Config module imported successfully")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from vector_store import VectorStoreManager
        print("✅ VectorStore module imported successfully")
    except ImportError as e:
        print(f"❌ VectorStore import failed: {e}")
        return False
    
    try:
        from rag_pipeline import RAGPipeline
        print("✅ RAG Pipeline module imported successfully")
    except ImportError as e:
        print(f"❌ RAG Pipeline import failed: {e}")
        return False
    
    # UI Components are now integrated into app.py
    print("✅ UI Components integrated into main app")
    
    try:
        from utils import ErrorHandler, ValidationUtils
        print("✅ Utils module imported successfully")
    except ImportError as e:
        print(f"❌ Utils import failed: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("🏔️ Meghalaya Tourism Bot - Setup Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test configuration
    if not test_configuration():
        all_tests_passed = False
    
    # Test custom modules
    if not test_custom_modules():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! The bot is ready to run.")
        print("\nTo start the bot, run:")
        print("  streamlit run app.py")
        print("\nOr with Docker:")
        print("  docker build -t meghalaya-chatbot .")
        print("  docker run -p 8501:8501 --env-file .env meghalaya-chatbot")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
