# Quick Start Guide - InterviewAI

## 🚀 Get InterviewAI Running in Minutes

### Prerequisites
- Node.js 18+ 
- Python 3.9+
- MongoDB (or Docker)
- OpenAI API Key

### Option 1: Docker (Recommended - Easiest)

1. **Clone and Navigate**
```bash
cd InterviewAI
```

2. **Setup Environment Variables**
```bash
# Copy environment files
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit .env files with your API keys
# Add your OpenAI API key to backend/.env
# Add your backend URL to frontend/.env
```

3. **Run with Docker**
```bash
docker-compose up --build
```

4. **Access the App**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your OpenAI API key
# OPENAI_API_KEY=your_key_here
# MONGODB_URL=mongodb://localhost:27017/interviewai
# JWT_SECRET_KEY=your_secret_key

# Start the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Edit .env if needed (default should work)
# REACT_APP_API_URL=http://localhost:8000

# Start the frontend
npm start
```

#### Database Setup
```bash
# Start MongoDB (if not using Docker)
mongod

# Or run with Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### 🔑 Default Admin Account
- Email: admin@interviewai.com
- Password: admin123

### 🧪 Test the Setup

1. **Check Backend Health**
```bash
curl http://localhost:8000/health
```

2. **Check Frontend**
Open http://localhost:3000 in your browser

3. **Create Account**
- Sign up as a new user
- Upload a resume
- Generate interview questions
- Start a mock interview

### 🐛 Common Issues

#### Backend Issues
- **Port 8000 in use**: Change port in uvicorn command
- **MongoDB connection**: Check MongoDB is running
- **OpenAI API key**: Verify your API key is valid

#### Frontend Issues
- **Port 3000 in use**: npm start will suggest alternative port
- **API connection**: Check backend is running
- **Environment variables**: Verify .env file is correct

#### Docker Issues
- **Port conflicts**: Check ports 3000, 8000, 27017 are free
- **Permission issues**: Run with sudo if needed (Linux/Mac)
- **Docker not running**: Start Docker Desktop

### 📱 Access Points

- **Main App**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Admin Panel**: http://localhost:3000/admin (after login)
- **Health Check**: http://localhost:8000/health

### 🛠️ Development Tips

- **Backend logs**: Check terminal where uvicorn is running
- **Frontend logs**: Check browser console
- **Database**: Use MongoDB Compass to view data
- **API Testing**: Use Postman or curl

### 🎯 Next Steps

1. Create an account
2. Upload your resume
3. Generate interview questions
4. Practice with mock interviews
5. View your feedback and progress

---

**Need help?** Check the full README.md or open an issue on GitHub.
