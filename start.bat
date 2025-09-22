@echo off
REM Meghalaya Tourism Bot Startup Script for Windows

echo 🏔️ Starting Meghalaya Tourism Bot...

REM Check if .env file exists
if not exist .env (
    echo ❌ .env file not found!
    echo Please copy env.example to .env and configure your settings:
    echo   copy env.example .env
    echo   REM Edit .env with your MongoDB URI and OpenAI API key
    pause
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running!
    echo Please start Docker and try again.
    pause
    exit /b 1
)

REM Build the Docker image
echo 🔨 Building Docker image...
docker build -t meghalaya-chatbot .

if errorlevel 1 (
    echo ❌ Docker build failed!
    pause
    exit /b 1
)

REM Run the container
echo 🚀 Starting the bot...
docker run -p 8501:8501 --env-file .env meghalaya-chatbot

echo ✅ Bot is running at http://localhost:8501
pause
