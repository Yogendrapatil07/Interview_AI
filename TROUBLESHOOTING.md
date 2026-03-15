# 🔧 InterviewAI Troubleshooting Guide

## ❌ "localhost refused to connect" - Common Solutions

### Step 1: Check if Docker is Running

**Open Command Prompt and run:**
```bash
docker --version
```

If you see an error, Docker is not installed or not running.

**Solution:**
1. Install Docker Desktop from https://docker.com
2. Start Docker Desktop
3. Wait for it to fully start (green icon in system tray)

### Step 2: Check Current Directory

**Make sure you're in the right folder:**
```bash
cd c:\Users\yogen\OneDrive\Desktop\HAryaVerse_2.0\InterviewAI
dir
```

You should see files like:
- start.bat
- docker-compose.yml
- backend/
- frontend/

### Step 3: Setup Environment Files

**Create necessary environment files:**
```bash
copy .env.example .env
copy backend\.env.example backend\.env
copy frontend\.env.example frontend\.env
```

### Step 4: Add Your OpenAI API Key

**Edit backend\.env file:**
1. Right-click on `backend\.env`
2. Select "Edit"
3. Add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_openai_api_key_here
MONGODB_URL=mongodb://localhost:27017/interviewai
JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
APP_NAME=InterviewAI
VERSION=1.0.0
```

### Step 5: Start Services

**Option A: Use the startup script**
```bash
start.bat
```

**Option B: Manual Docker start**
```bash
docker-compose up --build
```

### Step 6: Wait for Services to Start

**This takes 2-5 minutes on first run!**

You should see output like:
```
[+] Building 0.0s (0/0)  
[+] Running 3/3
 ⠧ Container interviewai-mongodb  Starting
 ⠧ Container interviewai-backend   Starting
 ⠧ Container interviewai-frontend  Starting
```

Wait until you see:
```
Container interviewai-frontend  Started
```

### Step 7: Verify Services are Running

**Check Docker containers:**
```bash
docker ps
```

You should see 3 containers running:
- interviewai-mongodb
- interviewai-backend  
- interviewai-frontend

### Step 8: Test Connection

**Test backend health:**
```bash
curl http://localhost:8000/health
```

Should return: `{"status": "healthy", "service": "InterviewAI API"}`

**Test frontend:**
Open http://localhost:3000 in browser

---

## 🚨 Common Issues & Solutions

### Issue 1: "Docker daemon is not running"
**Solution:**
1. Start Docker Desktop
2. Wait for green status
3. Try again

### Issue 2: "Port 3000 is already in use"
**Solution:**
```bash
# Stop other services using port 3000
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F
```

Or change port in docker-compose.yml:
```yaml
frontend:
  ports:
    - "3001:3000"  # Use 3001 instead
```

### Issue 3: "OpenAI API key invalid"
**Solution:**
1. Check your OpenAI API key is correct
2. Ensure you have credits in your OpenAI account
3. Verify the key format (starts with sk-)

### Issue 4: "MongoDB connection failed"
**Solution:**
1. Ensure MongoDB container is running
2. Check the MongoDB URL in backend\.env
3. Restart containers: `docker-compose down && docker-compose up`

### Issue 5: "Permission denied" errors
**Solution:**
1. Run Command Prompt as Administrator
2. Or use PowerShell instead of Command Prompt

---

## 🔧 Manual Setup (If Docker Fails)

### Install MongoDB Locally
1. Download MongoDB Community Server
2. Install with default settings
3. Start MongoDB service

### Setup Backend (Manual)
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Setup Frontend (Manual)
```bash
cd frontend
npm install
npm start
```

---

## 📱 Alternative Ports

If 3000 doesn't work, try:
- http://localhost:3001
- http://localhost:3002
- http://127.0.0.1:3000
- http://127.0.0.1:3001

---

## 🆘 Get Help

### Check Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mongodb
```

### Reset Everything
```bash
docker-compose down -v
docker system prune -f
docker-compose up --build
```

### Contact Support
- Check the browser console (F12) for errors
- Look at Command Prompt output for error messages
- Ensure all environment variables are set correctly

---

## ✅ Success Indicators

You know it's working when:
1. Docker shows 3 running containers
2. Backend health check returns success
3. Frontend loads without errors
4. You can create an account
5. The dashboard appears

**Still stuck?** Try the manual setup or check if your system meets the requirements.
