from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import datetime
import json
import random
from functools import wraps
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'interviewai_secret_key_2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database helper functions
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_role TEXT NOT NULL,
            resume_uploaded BOOLEAN DEFAULT 0,
            questions_answered INTEGER DEFAULT 0,
            total_questions INTEGER DEFAULT 5,
            duration_minutes INTEGER DEFAULT 0,
            communication_score REAL DEFAULT 0.0,
            confidence_score REAL DEFAULT 0.0,
            relevance_score REAL DEFAULT 0.0,
            final_score REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interview_id INTEGER NOT NULL,
            question_number INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            communication TEXT NOT NULL,
            confidence TEXT NOT NULL,
            relevance INTEGER NOT NULL,
            grammar TEXT NOT NULL,
            suggestion TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (interview_id) REFERENCES interviews (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

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

# Default Feedback Templates
DEFAULT_FEEDBACKS = [
    {
        'communication': 'Good',
        'confidence': 'Medium',
        'relevance': 8,
        'grammar': 'Good',
        'suggestion': 'Great answer! Try to provide more specific examples from your experience to make it even stronger.'
    },
    {
        'communication': 'Excellent',
        'confidence': 'High',
        'relevance': 9,
        'grammar': 'Excellent',
        'suggestion': 'Excellent response! Your confidence and clarity are impressive. Keep up the great work!'
    },
    {
        'communication': 'Good',
        'confidence': 'Medium',
        'relevance': 7,
        'grammar': 'Good',
        'suggestion': 'Good answer! Consider adding more technical details or specific metrics to demonstrate your impact.'
    },
    {
        'communication': 'Excellent',
        'confidence': 'High',
        'relevance': 8,
        'grammar': 'Excellent',
        'suggestion': 'Very professional response! Your structured thinking and clear communication are valuable assets.'
    },
    {
        'communication': 'Good',
        'confidence': 'Medium',
        'relevance': 6,
        'grammar': 'Good',
        'suggestion': 'Decent answer! Try to include more concrete examples and quantify your achievements when possible.'
    },
    {
        'communication': 'Excellent',
        'confidence': 'High',
        'relevance': 10,
        'grammar': 'Excellent',
        'suggestion': 'Outstanding response! Your comprehensive answer and confident delivery are exactly what interviewers look for.'
    },
    {
        'communication': 'Good',
        'confidence': 'Medium',
        'relevance': 8,
        'grammar': 'Good',
        'suggestion': 'Well structured answer! Consider practicing your delivery to appear more confident in interviews.'
    }
]

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Fast Feedback Function
def get_fast_feedback(question, answer):
    """Get feedback quickly using default templates"""
    # Analyze answer length and content
    word_count = len(answer.split())
    
    # Select appropriate feedback based on answer quality
    if word_count < 15:
        # Short answer
        feedback = {
            'communication': 'Fair',
            'confidence': 'Low',
            'relevance': 5,
            'grammar': 'Good',
            'suggestion': 'Your answer is too brief. Provide more details and specific examples to make it stronger.'
        }
    elif word_count < 30:
        # Medium answer
        feedback = random.choice(DEFAULT_FEEDBACKS[:4])
    else:
        # Good length answer
        feedback = random.choice(DEFAULT_FEEDBACKS[3:])
    
    # Adjust relevance based on keywords
    relevant_keywords = ["experience", "project", "skill", "developed", "created", "built", "designed", "managed", "led", "implemented"]
    relevance_count = sum(1 for keyword in relevant_keywords if keyword.lower() in answer.lower())
    
    if relevance_count >= 3:
        feedback['relevance'] = min(10, feedback['relevance'] + 2)
        feedback['communication'] = 'Excellent'
        feedback['confidence'] = 'High'
    elif relevance_count >= 1:
        feedback['relevance'] = min(10, feedback['relevance'] + 1)
    
    return feedback

# Routes
@app.route('/')
def index():
    return render_template('index_conference.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
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
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash('Email already registered', 'error')
            conn.close()
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                      (name, email, hashed_password))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get user info
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    # Get user statistics
    cursor.execute('SELECT COUNT(*) as total FROM interviews WHERE user_id = ?', (user_id,))
    total_interviews = cursor.fetchone()['total']
    
    cursor.execute('SELECT SUM(questions_answered) as total FROM interviews WHERE user_id = ?', (user_id,))
    total_questions = cursor.fetchone()['total'] or 0
    
    cursor.execute('SELECT SUM(duration_minutes) as total FROM interviews WHERE user_id = ?', (user_id,))
    total_time = cursor.fetchone()['total'] or 0
    
    cursor.execute('SELECT AVG(final_score) as avg FROM interviews WHERE user_id = ?', (user_id,))
    avg_score = cursor.fetchone()['avg'] or 0
    
    # Get recent interviews
    cursor.execute('''
        SELECT * FROM interviews 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT 5
    ''', (user_id,))
    recent_interviews = cursor.fetchall()
    
    conn.close()
    
    stats = {
        'total_interviews': total_interviews,
        'total_questions': total_questions,
        'total_time': total_time,
        'average_score': round(avg_score, 1)
    }
    
    return render_template('dashboard_smart.html', user=user, stats=stats, recent_interviews=recent_interviews)

@app.route('/start_interview', methods=['GET', 'POST'])
@login_required
def start_interview():
    if request.method == 'POST':
        job_role = request.form['job_role']
        
        # Create new interview session
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO interviews (user_id, job_role, questions_answered, total_questions)
            VALUES (?, ?, ?, ?)
        ''', (session['user_id'], job_role, 0, 5))
        interview_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        session['interview_id'] = interview_id
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
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('UPDATE interviews SET resume_uploaded = 1 WHERE id = ?', (interview_id,))
            conn.commit()
            conn.close()
        
        return jsonify({'success': True, 'message': 'Resume uploaded successfully'})
    
    return jsonify({'success': False, 'message': 'Upload failed'})

@app.route('/interview')
@login_required
def interview():
    interview_id = session.get('interview_id')
    if not interview_id:
        return redirect(url_for('dashboard'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM interviews WHERE id = ?', (interview_id,))
    interview = cursor.fetchone()
    
    current_q = session.get('current_question', 0)
    
    if current_q >= len(INTERVIEW_QUESTIONS[interview['job_role']]):
        conn.close()
        return redirect(url_for('summary'))
    
    question = INTERVIEW_QUESTIONS[interview['job_role']][current_q]
    conn.close()
    
    return render_template('interview_fast.html', 
                         interview=interview, 
                         question=question, 
                         question_number=current_q + 1)

@app.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    interview_id = session.get('interview_id')
    current_q = session.get('current_question', 0)
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM interviews WHERE id = ?', (interview_id,))
    interview = cursor.fetchone()
    
    answer = request.form['answer']
    
    # Get current question
    question = INTERVIEW_QUESTIONS[interview['job_role']][current_q]
    
    # Get fast feedback
    feedback = get_fast_feedback(question, answer)
    
    # Save feedback
    cursor.execute('''
        INSERT INTO feedback (interview_id, question_number, question, answer, 
                             communication, confidence, relevance, grammar, suggestion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (interview_id, current_q + 1, question, answer,
          feedback['communication'], feedback['confidence'], 
          feedback['relevance'], feedback['grammar'], feedback['suggestion']))
    
    # Update interview
    cursor.execute('UPDATE interviews SET questions_answered = questions_answered + 1 WHERE id = ?', 
                   (interview_id,))
    
    # Calculate scores
    cursor.execute('SELECT AVG(relevance) as avg_rel FROM feedback WHERE interview_id = ?', (interview_id,))
    avg_rel = cursor.fetchone()['avg_rel'] or 0
    
    cursor.execute('UPDATE interviews SET final_score = ? WHERE id = ?', (avg_rel, interview_id))
    
    conn.commit()
    conn.close()
    
    return jsonify(feedback)

@app.route('/next_question')
@login_required
def next_question():
    current_q = session.get('current_question', 0) + 1
    session['current_question'] = current_q
    
    interview_id = session.get('interview_id')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM interviews WHERE id = ?', (interview_id,))
    interview = cursor.fetchone()
    conn.close()
    
    if current_q >= len(INTERVIEW_QUESTIONS[interview['job_role']]):
        return redirect(url_for('summary'))
    
    return redirect(url_for('interview'))

@app.route('/summary')
@login_required
def summary():
    interview_id = session.get('interview_id')
    if not interview_id:
        return redirect(url_for('dashboard'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM interviews WHERE id = ?', (interview_id,))
    interview = cursor.fetchone()
    
    cursor.execute('SELECT * FROM feedback WHERE interview_id = ? ORDER BY question_number', (interview_id,))
    feedback_list = cursor.fetchall()
    
    # Calculate duration (mock - 2 minutes per question)
    duration_minutes = len(feedback_list) * 2
    
    # Calculate scores
    if feedback_list:
        avg_comm = 7  # Mock score
        avg_conf = 7  # Mock score
        avg_rel = sum(f['relevance'] for f in feedback_list) / len(feedback_list)
        avg_final = avg_rel
        
        cursor.execute('''
            UPDATE interviews 
            SET duration_minutes = ?, communication_score = ?, confidence_score = ?, relevance_score = ?, final_score = ?
            WHERE id = ?
        ''', (duration_minutes, avg_comm, avg_conf, avg_rel, avg_final, interview_id))
        conn.commit()
    
    conn.close()
    
    # Clear session
    session.pop('interview_id', None)
    session.pop('current_question', None)
    
    return render_template('summary_fixed.html', interview=interview, feedback_list=feedback_list)

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
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO contact_messages (name, email, message) VALUES (?, ?, ?)',
                      (name, email, message))
        conn.commit()
        conn.close()
        
        flash('Message sent successfully! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

# Initialize database
init_db()

if __name__ == '__main__':
    print("🚀 InterviewAI Conference Version Starting...")
    print("⚡ Fast feedback system enabled")
    print("🎨 Modern UI with conference theme")
    print("🌐 Server starting at http://127.0.0.1:5000")
    app.run(debug=False, host='127.0.0.1', port=5000)
