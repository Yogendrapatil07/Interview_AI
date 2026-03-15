# 🚀 Run InterviewAI NOW - Step by Step

## Method 1: Docker (Easiest)

### Step 1: Open Command Prompt/Terminal
Navigate to the InterviewAI folder:
```bash
cd c:\Users\yogen\OneDrive\Desktop\HAryaVerse_2.0\InterviewAI
```

### Step 2: Run the Startup Script
```bash
start.bat
```

That's it! The script will:
- Check for Docker
- Create necessary .env files
- Start all services
- Open the app at http://localhost:3000

---

## Method 2: Manual Docker Setup

### Step 1: Setup Environment Files
```bash
cd c:\Users\yogen\OneDrive\Desktop\HAryaVerse_2.0\InterviewAI

# Create environment files
copy .env.example .env
copy backend\.env.example backend\.env
copy frontend\.env.example frontend\.env
```

### Step 2: Edit Environment Files
Open `backend\.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
MONGODB_URL=mongodb://localhost:27017/interviewai
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Step 3: Run Docker Compose
```bash
docker-compose up --build
```

---

## Method 3: Manual Setup (No Docker)

### Step 1: Start MongoDB
```bash
# Option A: Install MongoDB locally
# Download from https://www.mongodb.com/try/download/community

# Option B: Use Docker for MongoDB only
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### Step 2: Setup Backend
```bash
cd c:\Users\yogen\OneDrive\Desktop\HAryaVerse_2.0\InterviewAI\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env file with your OpenAI API key
# OPENAI_API_KEY=your_key_here

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Setup Frontend (New Terminal)
```bash
cd c:\Users\yogen\OneDrive\Desktop\HAryaVerse_2.0\InterviewAI\frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env

# Start frontend
npm start
```

---

## 🔑 Access the Application

Once running, access:
- **Main App**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 👤 Default Login
- Email: admin@interviewai.com
- Password: admin123

## 🧪 Quick Test

1. Open http://localhost:3000
2. Click "Sign Up"
3. Create a new account
4. Upload a PDF resume
5. Generate interview questions
6. Start a mock interview

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change frontend port
npm start -- --port=3001

# Change backend port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### MongoDB Connection Error
```bash
# Check if MongoDB is running
docker ps | grep mongodb

# Or check if local MongoDB is installed
mongod --version
```

### OpenAI API Error
- Verify your API key is valid
- Check you have credits in your OpenAI account
- Ensure the key is correctly set in backend\.env

### Frontend Not Connecting to Backend
- Check backend is running on port 8000
- Verify REACT_APP_API_URL in frontend\.env
- Check browser console for errors

---

## 📱 What to Expect

1. **Modern UI**: Clean, responsive interface with dark/light themes
2. **AI Features**: Resume analysis, question generation, mock interviews
3. **Real-time Feedback**: Instant AI analysis of your interview answers
4. **Progress Tracking**: Detailed analytics and performance metrics
5. **Admin Panel**: Complete platform management tools

## 🎯 First Steps

1. **Create Account**: Sign up as a student or job seeker
2. **Upload Resume**: Get AI analysis of your resume
3. **Generate Questions**: Create custom interview questions
4. **Practice Interview**: Try a mock interview session
5. **View Feedback**: Check your performance and improvement areas

---

**Need Help?** Check QUICK_START.md or open an issue on GitHub.

**Happy Interviewing!** 🎉
