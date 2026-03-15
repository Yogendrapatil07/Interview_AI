# InterviewAI – Smart Interview Preparation Assistant

An AI-powered platform that helps students and job seekers prepare for interviews through resume analysis, AI-generated interview questions, mock interviews, and feedback.

## Features

- 🤖 **AI Interview Questions**: Generate personalized interview questions based on job role, experience level, and industry
- 📄 **Resume Analysis**: Upload and analyze resumes with AI-powered feedback
- 🎭 **Mock Interview Practice**: Interactive AI chatbot for realistic interview simulation
- 📊 **Performance Analytics**: Detailed feedback and scoring system
- 🌙 **Modern UI**: Dark/Light mode with smooth animations
- 📱 **Mobile Responsive**: Works seamlessly on all devices

## Tech Stack

### Frontend
- React.js
- Tailwind CSS
- Framer Motion
- Axios

### Backend
- Python FastAPI
- MongoDB
- JWT Authentication
- OpenAI API

### Deployment
- Docker
- Docker Compose

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- MongoDB
- OpenAI API Key

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd InterviewAI
```

2. **Set up environment variables**
```bash
# Backend
cd backend
cp .env.example .env
# Edit .env with your API keys

# Frontend
cd ../frontend
cp .env.example .env
# Edit .env with your backend URL
```

3. **Run with Docker (Recommended)**
```bash
docker-compose up --build
```

4. **Or run locally**

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

### Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Environment Variables

### Backend (.env)
```
MONGODB_URL=mongodb://localhost:27017/interviewai
OPENAI_API_KEY=your_openai_api_key
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_BASE_URL=http://localhost:8000/api/v1
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout

### Resume
- `POST /api/v1/resume/upload` - Upload resume
- `GET /api/v1/resume/analyze/{resume_id}` - Analyze resume

### Interview
- `POST /api/v1/interview/generate-questions` - Generate interview questions
- `POST /api/v1/interview/start-session` - Start mock interview
- `POST /api/v1/interview/submit-answer` - Submit interview answer

### Feedback
- `GET /api/v1/feedback/session/{session_id}` - Get session feedback
- `GET /api/v1/feedback/user/{user_id}` - Get user feedback history

## Project Structure

```
InterviewAI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
