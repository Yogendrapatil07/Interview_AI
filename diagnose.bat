@echo off
echo 🔍 InterviewAI Diagnostic Tool
echo.

echo Step 1: Checking Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker NOT found
    echo.
    echo Please install Docker Desktop from: https://docker.com
    echo After installation, start Docker Desktop and wait for green status
    pause
    exit /b 1
) else (
    echo ✅ Docker found
)

echo.
echo Step 2: Checking current directory...
if not exist "docker-compose.yml" (
    echo ❌ NOT in InterviewAI directory
    echo.
    echo Please navigate to: c:\Users\yogen\OneDrive\Desktop\HAryaVerse_2.0\InterviewAI
    pause
    exit /b 1
) else (
    echo ✅ In correct directory
)

echo.
echo Step 3: Checking environment files...
if not exist ".env" (
    echo 📝 Creating .env file...
    copy .env.example .env >nul
    echo ✅ Created .env
) else (
    echo ✅ .env exists
)

if not exist "backend\.env" (
    echo 📝 Creating backend\.env file...
    copy backend\.env.example backend\.env >nul
    echo ✅ Created backend\.env
) else (
    echo ✅ backend\.env exists
)

if not exist "frontend\.env" (
    echo 📝 Creating frontend\.env file...
    copy frontend\.env.example frontend\.env >nul
    echo ✅ Created frontend\.env
) else (
    echo ✅ frontend\.env exists
)

echo.
echo Step 4: Checking Docker status...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker daemon not running
    echo.
    echo Please start Docker Desktop and wait for green status
    pause
    exit /b 1
) else (
    echo ✅ Docker daemon running
)

echo.
echo Step 5: Checking for existing containers...
docker ps -a --filter "name=interviewai" --format "table {{.Names}}\t{{.Status}}"

echo.
echo Step 6: Starting services...
echo This will take 2-5 minutes on first run...
echo.

docker-compose up --build

echo.
echo 🎉 If you see this message, services are starting!
echo.
echo 🌐 Try accessing:
echo    Frontend: http://localhost:3000
echo    Backend:  http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo 💡 If still getting connection errors:
echo    1. Wait 2-3 more minutes
echo    2. Check TROUBLESHOOTING.md
echo    3. Try http://localhost:3001 (alternative port)
echo.
echo 🛑 Press Ctrl+C to stop services
