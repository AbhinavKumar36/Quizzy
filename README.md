# 🎓 Quizzy

A premium, modern online quiz platform built with Python, Flask, and SQLite. Features a beautiful dark-themed glassmorphism UI, dynamic micro-animations, and a responsive design tailored for both Students and Teachers.

## 🚀 Features

### For Students
- **Real-Time Quizzes**: Interactive quiz interface with dynamic highlighting.
- **Multiple Question Types**: Support for both Single Choice (radio buttons) and Multiple Answers (checkboxes).
- **Auto-Submitting Timer**: Countdown timer that automatically submits the quiz when time runs out.
- **Detailed Results**: Beautiful scorecards featuring a Top 5 Leaderboard and an itemized breakdown of correct/incorrect answers.

### For Teachers
- **Teacher Dashboard**: A centralized hub to manage quizzes, view attempts, and register new students securely.
- **Quiz Management**: Create new quizzes with custom time limits.
- **Question Editor**: A split-screen interface to add, edit, or delete questions on the fly.
- **Analytics Dashboard**: View aggregate student metrics (Total Attempts, Average Score) and an itemized table of all student scores and submission times for any given quiz.

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask
- **Database**: SQLite with Flask-SQLAlchemy ORM
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (No heavy frameworks required)
- **Styling**: Custom Design System featuring Glassmorphism, CSS Variables, Flexbox/Grid, and Dark Mode.

## ⚙️ Setup Guide

Follow these steps to set up and run the application locally:

### 1. Install Dependencies
Open a terminal in the project directory and install the required Python packages:
```bash
pip install -r requirements.txt
```

### 2. Initialize the Database
Run the initialization script to create the database tables, seed initial users, and populate sample quizzes:
```bash
python init_db.py
```

### 3. Run the Application
Start the Flask development server:
```bash
python app.py
```

### 4. Access the Platform
Open your web browser and navigate to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🔑 Default User Roles

After running `init_db.py`, the following accounts are pre-configured:

**Teacher Account**
- **Teacher ID**: `T101`
- **Password**: `teacherpass`

**Student Account**
- **Registration No**: `S2024001`
- **Password**: `01012005` *(DOB format DDMMYYYY)*
