#!/usr/bin/env python3
"""
Deployment helper script for Meghalaya Tourism Bot
"""

import os
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if all required files exist."""
    required_files = [
        'app.py',
        'config.py',
        'vector_store.py',
        'rag_pipeline.py',
        'utils.py',
        'requirements.txt',
        '.streamlit/secrets.toml'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files present")
    return True

def check_git_status():
    """Check git status and provide deployment instructions."""
    try:
        # Check if git is initialized
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Git not initialized. Run 'git init' first.")
            return False
        
        # Check for uncommitted changes
        if "nothing to commit" not in result.stdout:
            print("⚠️  You have uncommitted changes. Consider committing them first.")
            print("   Run: git add . && git commit -m 'Your commit message'")
        
        print("✅ Git repository ready")
        return True
        
    except FileNotFoundError:
        print("❌ Git not installed. Please install Git first.")
        return False

def create_deployment_checklist():
    """Create a deployment checklist."""
    checklist = """
🚀 DEPLOYMENT CHECKLIST

Before deploying to Streamlit Cloud:

1. ✅ Code is ready
   - All files are present
   - App runs locally without errors
   - Dependencies are in requirements.txt

2. 🔐 Secrets configured
   - MongoDB URI is correct
   - OpenAI API key is valid
   - All environment variables are set

3. 📁 Repository ready
   - Code is committed to Git
   - Repository is pushed to GitHub
   - .gitignore excludes sensitive files

4. 🌐 Streamlit Cloud setup
   - Account created at https://share.streamlit.io/
   - Repository connected
   - Secrets configured in Streamlit Cloud

5. 🧪 Testing
   - App loads successfully
   - Database connection works
   - Chat functionality works
   - Error handling works

NEXT STEPS:
1. Go to https://share.streamlit.io/
2. Click "New app"
3. Select your GitHub repository
4. Set main file to "app.py"
5. Configure secrets
6. Deploy!

Your app will be available at:
https://your-app-name.streamlit.app/
"""
    print(checklist)

def main():
    """Main deployment helper function."""
    print("🏔️ Meghalaya Tourism Bot - Deployment Helper")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please fix missing files before deploying.")
        return
    
    # Check git status
    if not check_git_status():
        print("\n❌ Please fix git issues before deploying.")
        return
    
    # Show deployment checklist
    create_deployment_checklist()

if __name__ == "__main__":
    main()
