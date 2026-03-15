@echo off
echo 🚀 Starting InterviewAI...
echo.

REM Check if Docker is available
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker not found. Please install Docker first.
    echo.
    echo Option 1: Install Docker Desktop from https://docker.com
    echo Option 2: Run manual setup (see QUICK_START.md)
    pause
    exit /b 1
)

echo ✅ Docker found
echo.

REM Check if environment files exist
if not exist ".env" (
    echo 📝 Creating .env file...
    copy .env.example .env
    echo.
    echo ⚠️  Please edit .env file with your OpenAI API key
    echo    OPENAI_API_KEY=your_key_here
    echo.
)

if not exist "backend\.env" (
    echo 📝 Creating backend\.env file...
    copy backend\.env.example backend\.env
)

if not exist "frontend\.env" (
    echo 📝 Creating frontend\.env file...
    copy frontend\.env.example frontend\.env
)

echo 🐳 Starting services with Docker...
echo.
echo This will take a few minutes on first run...
echo.

REM Start Docker Compose
docker-compose up --build

echo.
echo 🛑 Press Ctrl+C to stop all services
echo 🌐 Access the app at http://localhost:3000
echo 📚 API docs at http://localhost:8000/docs
