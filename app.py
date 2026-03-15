from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import datetime
import json
import requests
from functools import wraps
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'interviewai_secret_key_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    interviews = db.relationship('Interview', backref='user', lazy=True)

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_role = db.Column(db.String(100), nullable=False)
    resume_uploaded = db.Column(db.Boolean, default=False)
    questions_answered = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, default=5)
    duration_minutes = db.Column(db.Integer, default=0)
    communication_score = db.Column(db.Float, default=0.0)
    confidence_score = db.Column(db.Float, default=0.0)
    relevance_score = db.Column(db.Float, default=0.0)
    final_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    feedback = db.relationship('Feedback', backref='interview', lazy=True)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interview.id'), nullable=False)
    question_number = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    communication = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.String(50), nullable=False)
    relevance = db.Column(db.Integer, nullable=False)
    grammar = db.Column(db.String(50), nullable=False)
    suggestion = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Interview Questions Database
INTERVIEW_QUESTIONS = {
    'Software Developer': [
        "Tell me about yourself and your programming experience.",
        "What programming languages are you most comfortable with?",
        "Describe a challenging bug you fixed in your code.",
        "How do you ensure code quality in your projects?",
        "Where do you see yourself in 5 years as a developer?"
    ],
    'Data Analyst': [
        "Tell me about your experience with data analysis.",
        "What data analysis tools are you most proficient with?",
        "Describe a complex data project you worked on.",
        "How do you handle missing or inconsistent data?",
        "What makes you a good data analyst?"
    ],
    'AI Engineer': [
        "Tell me about your AI and machine learning experience.",
        "What ML frameworks have you worked with?",
        "Describe an AI project you're proud of.",
        "How do you approach model optimization?",
        "What excites you about AI engineering?"
    ],
    'Web Developer': [
        "Tell me about your web development experience.",
        "What web technologies do you specialize in?",
        "Describe a website you built from scratch.",
        "How do you ensure responsive design?",
        "What makes you passionate about web development?"
    ]
}

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# AI Analysis Function
def analyze_answer(question, answer):
    """Analyze answer using AI or fallback logic"""
    try:
        # Try AI API (placeholder - replace with actual API call)
        # For demo, we'll use fallback logic
        return generate_fallback_feedback(question, answer)
    except:
        return generate_fallback_feedback(question, answer)

def generate_fallback_feedback(question, answer):
    """Generate fallback feedback when AI API fails"""
    answer_length = len(answer.split())
    word_count = len(answer.split())
    
    # Communication analysis
    if word_count < 20:
        communication = "Short"
        comm_score = 5
    elif word_count < 50:
        communication = "Good"
        comm_score = 7
    else:
        communication = "Excellent"
        comm_score = 9
    
    # Confidence analysis
    if "I think" in answer or "maybe" in answer.lower():
        confidence = "Low"
        conf_score = 5
    elif "I believe" in answer or "I'm confident" in answer:
        confidence = "High"
        conf_score = 9
    else:
        confidence = "Medium"
        conf_score = 7
    
    # Relevance analysis
    relevant_keywords = ["experience", "project", "skill", "developed", "created", "built", "designed"]
    relevance_count = sum(1 for keyword in relevant_keywords if keyword.lower() in answer.lower())
    relevance = min(10, relevance_count + 5)
    
    # Grammar analysis
    if answer.count('.') >= answer.count(','):
        grammar = "Good"
    else:
        grammar = "Needs Improvement"
    
    # Generate suggestion
    if relevance < 7:
        suggestion = "Try to provide more specific examples from your experience."
    elif comm_score < 7:
        suggestion = "Consider elaborating more on your answer."
    else:
        suggestion = "Good answer! Try to be more confident in your delivery."
    
    return {
        'communication': communication,
        'confidence': confidence,
        'relevance': relevance,
        'grammar': grammar,
        'suggestion': suggestion
    }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    # Get user statistics
    total_interviews = Interview.query.filter_by(user_id=user_id).count()
    total_questions = db.session.query(db.func.sum(Interview.questions_answered)).filter_by(user_id=user_id).scalar() or 0
    total_time = db.session.query(db.func.sum(Interview.duration_minutes)).filter_by(user_id=user_id).scalar() or 0
    avg_score = db.session.query(db.func.avg(Interview.final_score)).filter_by(user_id=user_id).scalar() or 0
    
    # Get recent interviews
    recent_interviews = Interview.query.filter_by(user_id=user_id).order_by(Interview.created_at.desc()).limit(5).all()
    
    stats = {
        'total_interviews': total_interviews,
        'total_questions': total_questions,
        'total_time': total_time,
        'average_score': round(avg_score, 1)
    }
    
    return render_template('dashboard.html', user=user, stats=stats, recent_interviews=recent_interviews)

@app.route('/start_interview', methods=['GET', 'POST'])
@login_required
def start_interview():
    if request.method == 'POST':
        job_role = request.form['job_role']
        
        # Create new interview session
        new_interview = Interview(
            user_id=session['user_id'],
            job_role=job_role,
            questions_answered=0,
            total_questions=5
        )
        db.session.add(new_interview)
        db.session.commit()
        
        session['interview_id'] = new_interview.id
        session['current_question'] = 0
        
        return redirect(url_for('interview'))
    
    return render_template('start_interview.html')

@app.route('/upload_resume', methods=['POST'])
@login_required
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'})
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Update interview record
        interview_id = session.get('interview_id')
        if interview_id:
            interview = Interview.query.get(interview_id)
            interview.resume_uploaded = True
            db.session.commit()
        
        return jsonify({'success': True, 'message': 'Resume uploaded successfully'})
    
    return jsonify({'success': False, 'message': 'Upload failed'})

@app.route('/interview')
@login_required
def interview():
    interview_id = session.get('interview_id')
    if not interview_id:
        return redirect(url_for('dashboard'))
    
    interview = Interview.query.get(interview_id)
    current_q = session.get('current_question', 0)
    
    if current_q >= len(INTERVIEW_QUESTIONS[interview.job_role]):
        return redirect(url_for('summary'))
    
    question = INTERVIEW_QUESTIONS[interview.job_role][current_q]
    
    return render_template('interview.html', 
                         interview=interview, 
                         question=question, 
                         question_number=current_q + 1)

@app.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    interview_id = session.get('interview_id')
    current_q = session.get('current_question', 0)
    
    interview = Interview.query.get(interview_id)
    answer = request.form['answer']
    
    # Get current question
    question = INTERVIEW_QUESTIONS[interview.job_role][current_q]
    
    # Analyze answer
    feedback = analyze_answer(question, answer)
    
    # Save feedback
    feedback_record = Feedback(
        interview_id=interview_id,
        question_number=current_q + 1,
        question=question,
        answer=answer,
        communication=feedback['communication'],
        confidence=feedback['confidence'],
        relevance=feedback['relevance'],
        grammar=feedback['grammar'],
        suggestion=feedback['suggestion']
    )
    db.session.add(feedback_record)
    
    # Update interview
    interview.questions_answered += 1
    
    # Calculate scores
    all_feedback = Feedback.query.filter_by(interview_id=interview_id).all()
    if all_feedback:
        avg_comm = sum(f.relevance for f in all_feedback) / len(all_feedback)
        interview.final_score = avg_comm
    
    db.session.commit()
    
    return jsonify(feedback)

@app.route('/next_question')
@login_required
def next_question():
    current_q = session.get('current_question', 0) + 1
    session['current_question'] = current_q
    
    interview_id = session.get('interview_id')
    interview = Interview.query.get(interview_id)
    
    if current_q >= len(INTERVIEW_QUESTIONS[interview.job_role]):
        return redirect(url_for('summary'))
    
    return redirect(url_for('interview'))

@app.route('/summary')
@login_required
def summary():
    interview_id = session.get('interview_id')
    if not interview_id:
        return redirect(url_for('dashboard'))
    
    interview = Interview.query.get(interview_id)
    feedback_list = Feedback.query.filter_by(interview_id=interview_id).all()
    
    # Calculate duration (mock - in real app, track actual time)
    interview.duration_minutes = len(feedback_list) * 2  # 2 minutes per question
    
    # Calculate scores
    if feedback_list:
        interview.communication_score = sum(7 for f in feedback_list) / len(feedback_list)
        interview.confidence_score = sum(7 for f in feedback_list) / len(feedback_list)
        interview.relevance_score = sum(f.relevance for f in feedback_list) / len(feedback_list)
        interview.final_score = interview.relevance_score
    
    db.session.commit()
    
    # Clear session
    session.pop('interview_id', None)
    session.pop('current_question', None)
    
    return render_template('summary.html', interview=interview, feedback_list=feedback_list)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        contact_msg = ContactMessage(name=name, email=email, message=message)
        db.session.add(contact_msg)
        db.session.commit()
        
        flash('Message sent successfully! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

# Create database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
