import os
import random
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Quiz, Question, Score, User, StudentAnswer

app = Flask(__name__)
# Basic config for SQLite and sessions
app.config['SECRET_KEY'] = 'super-secret-quiz-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        user = User.query.filter_by(username=username, role=role).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully.')
            if user.role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            else:
                return redirect(url_for('index'))
        flash('Invalid Registration No/Teacher ID or Password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

@app.route('/')
def index():
    # Fetch all available quizzes
    quizzes = Quiz.query.all()
    return render_template('index.html', quizzes=quizzes)

@app.route('/quiz/<int:quiz_id>', methods=['GET'])
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Phase 2: Randomize questions for anti-cheating
    random.shuffle(questions)
    
    return render_template('quiz.html', quiz=quiz, questions=questions)

@app.route('/submit/<int:quiz_id>', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    score_val = 0
    total_questions = len(questions)

    # Create the score attempt
    new_score = Score(quiz_id=quiz.id, user_id=current_user.id, score=0, total_questions=total_questions)
    db.session.add(new_score)
    db.session.flush() # Get ID without full commit

    # Process individual answers
    for question in questions:
        # Form field names will be q_<question_id>
        selected_options = request.form.getlist(f'q_{question.id}')
        
        if not selected_options:
            selected_option_str = ""
        else:
            selected_option_str = ",".join(sorted(selected_options))
            
        correct_opts = sorted(question.correct_option.split(','))
        correct_opt_str = ",".join(correct_opts)
        
        is_correct = False
        
        if selected_option_str and selected_option_str.upper() == correct_opt_str.upper():
            score_val += 1
            is_correct = True
            
        answer_record = StudentAnswer(
            score_id=new_score.id,
            question_id=question.id,
            selected_option=selected_option_str,
            is_correct=is_correct
        )
        db.session.add(answer_record)

    new_score.score = score_val
    db.session.commit()

    return redirect(url_for('result', score_id=new_score.id))

@app.route('/result/<int:score_id>')
@login_required
def result(score_id):
    score_record = Score.query.get_or_404(score_id)
    quiz = Quiz.query.get(score_record.quiz_id)
    
    # Get top 5 scores for this quiz to show leaderboard
    top_scores = Score.query.filter_by(quiz_id=quiz.id).order_by(Score.score.desc(), Score.timestamp.asc()).limit(5).all()

    # Get student answers for detailed view
    student_answers = StudentAnswer.query.filter_by(score_id=score_id).all()

    return render_template('result.html', score=score_record, quiz=quiz, top_scores=top_scores, student_answers=student_answers)

# --- Teacher Routes ---

@app.route('/teacher')
@login_required
def teacher_dashboard():
    if current_user.role != 'teacher':
        flash('Access denied. Teacher portal only.')
        return redirect(url_for('index'))
    quizzes = Quiz.query.order_by(Quiz.id.desc()).all()
    return render_template('teacher_dashboard.html', quizzes=quizzes)

@app.route('/teacher/quiz/<int:quiz_id>/analytics')
@login_required
def teacher_quiz_analytics(quiz_id):
    if current_user.role != 'teacher':
        flash('Access denied. Teacher portal only.')
        return redirect(url_for('index'))
        
    quiz = Quiz.query.get_or_404(quiz_id)
    
    results = db.session.query(Score, User).join(User, Score.user_id == User.id)\
        .filter(Score.quiz_id == quiz.id)\
        .order_by(Score.score.desc(), Score.timestamp.desc()).all()
        
    total_attempts = len(results)
    avg_score = 0
    if total_attempts > 0:
        avg_score = sum([r.Score.score for r in results]) / total_attempts
        
    return render_template('teacher_quiz_analytics.html', quiz=quiz, results=results, total_attempts=total_attempts, avg_score=avg_score)

@app.route('/teacher/register_student', methods=['GET', 'POST'])
@login_required
def teacher_register_student():
    if current_user.role != 'teacher':
        flash('Access denied. Teacher portal only.')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        reg_no = request.form.get('reg_no')
        dob = request.form.get('dob') # password
        
        if reg_no and dob:
            if User.query.filter_by(username=reg_no).first():
                flash('Student with this Registration No already exists.')
            else:
                new_student = User(
                    username=reg_no,
                    password_hash=generate_password_hash(dob),
                    role='student'
                )
                db.session.add(new_student)
                db.session.commit()
                flash(f'Student {reg_no} registered successfully!')
                return redirect(url_for('teacher_dashboard'))
                
    return render_template('register_student.html')

@app.route('/teacher/quiz/new', methods=['GET', 'POST'])
@login_required
def teacher_create_quiz():
    if current_user.role != 'teacher':
        flash('Access denied. Teacher portal only.')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        time_limit_str = request.form.get('time_limit', '0')
        
        time_limit = int(time_limit_str) if time_limit_str.isdigit() else 0
        
        if title:
            new_quiz = Quiz(title=title, description=description, time_limit=time_limit)
            db.session.add(new_quiz)
            db.session.commit()
            return redirect(url_for('teacher_add_question', quiz_id=new_quiz.id))
            
    return render_template('teacher_create_quiz.html')

@app.route('/teacher/quiz/<int:quiz_id>/add_question', methods=['GET', 'POST'])
@login_required
def teacher_add_question(quiz_id):
    if current_user.role != 'teacher':
        flash('Access denied. Teacher portal only.')
        return redirect(url_for('index'))

    quiz = Quiz.query.get_or_404(quiz_id)
    
    if request.method == 'POST':
        text = request.form.get('text')
        option_a = request.form.get('option_a')
        option_b = request.form.get('option_b')
        option_c = request.form.get('option_c')
        option_d = request.form.get('option_d')
        
        correct_options = request.form.getlist('correct_option')
        is_multiple_choice = request.form.get('is_multiple_choice') == '1'
        
        if not correct_options:
            flash('You must select at least one correct option.', 'error')
            return redirect(url_for('teacher_add_question', quiz_id=quiz.id))
            
        correct_option_str = ",".join(correct_options)
        
        if all([text, option_a, option_b, option_c, option_d]):
            new_question = Question(
                quiz_id=quiz.id,
                text=text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_option=correct_option_str,
                is_multiple_choice=is_multiple_choice
            )
            db.session.add(new_question)
            db.session.commit()
            flash('Question added successfully!')
            return redirect(url_for('teacher_add_question', quiz_id=quiz.id))

    # Fetch existing questions to display them
    existing_questions = Question.query.filter_by(quiz_id=quiz.id).all()
    return render_template('teacher_add_question.html', quiz=quiz, existing_questions=existing_questions)

@app.route('/teacher/question/<int:question_id>/edit', methods=['GET', 'POST'])
@login_required
def teacher_edit_question(question_id):
    if current_user.role != 'teacher':
        flash('Access denied. Teacher portal only.')
        return redirect(url_for('index'))
        
    question = Question.query.get_or_404(question_id)
    
    if request.method == 'POST':
        question.text = request.form.get('text')
        question.option_a = request.form.get('option_a')
        question.option_b = request.form.get('option_b')
        question.option_c = request.form.get('option_c')
        question.option_d = request.form.get('option_d')
        
        correct_options = request.form.getlist('correct_option')
        if not correct_options:
            flash('You must select at least one correct option.', 'error')
            return redirect(url_for('teacher_edit_question', question_id=question.id))
            
        question.correct_option = ",".join(correct_options)
        question.is_multiple_choice = request.form.get('is_multiple_choice') == '1'
        
        db.session.commit()
        flash('Question updated successfully!')
        return redirect(url_for('teacher_add_question', quiz_id=question.quiz_id))
        
    return render_template('teacher_edit_question.html', question=question)

@app.route('/teacher/question/<int:question_id>/delete', methods=['POST'])
@login_required
def teacher_delete_question(question_id):
    if current_user.role != 'teacher':
        flash('Access denied. Teacher portal only.')
        return redirect(url_for('index'))
        
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully!')
    return redirect(url_for('teacher_add_question', quiz_id=quiz_id))

if __name__ == '__main__':
    os.makedirs(app.instance_path, exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
