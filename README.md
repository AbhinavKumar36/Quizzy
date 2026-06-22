# Online Quiz Platform

A premium, modern online quiz platform built with Python, Flask, and SQLite. Features a beautiful glassmorphism UI, dynamic animations, and a responsive design.

## Features

- **Dynamic UI**: Built with vanilla CSS/JS for maximum flexibility, featuring glassmorphism, dark mode, and smooth micro-animations.
- **Backend Logic**: Flask backend handling routing and quiz logic.
- **Database**: SQLite database with SQLAlchemy ORM for storing quizzes, questions, options, and user scores.
- **Leaderboard**: Real-time scoring and tracking of top scores for each quiz.

## Requirements

- Python 3.8+

## Setup Guide

Follow these steps to set up and run the application locally:

### 1. Install Dependencies

Open a terminal in this directory and install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Initialize the Database

Run the initialization script to create the database tables and populate them with sample quizzes:

```bash
python init_db.py
```

### 3. Run the Application

Start the Flask development server:

```bash
python app.py
```

### 4. Access the Application

Open your web browser and navigate to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

Enjoy testing your knowledge!
