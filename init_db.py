from app import app
from models import db, Quiz, Question, User
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()

        print("Populating database with sample users and quizzes...")
        
        # Sample Users
        teacher = User(username='T101', password_hash=generate_password_hash('teacherpass'), role='teacher')
        student = User(username='S2024001', password_hash=generate_password_hash('01012005'), role='student')
        db.session.add_all([teacher, student])
        db.session.commit()
        
        # Sample Quiz 1: Python Basics
        quiz1 = Quiz(title="Python Basics", description="Test your fundamental knowledge of Python programming.")
        db.session.add(quiz1)
        db.session.commit() # Commit to get quiz1.id

        questions1 = [
            Question(quiz_id=quiz1.id, text="What is the output of print(2 ** 3)?", option_a="5", option_b="6", option_c="8", option_d="9", correct_option="C"),
            Question(quiz_id=quiz1.id, text="Which of the following is a mutable data type in Python?", option_a="Tuple", option_b="List", option_c="String", option_d="Integer", correct_option="B"),
            Question(quiz_id=quiz1.id, text="How do you create a function in Python?", option_a="function myFunc()", option_b="def myFunc():", option_c="create myFunc()", option_d="void myFunc()", correct_option="B"),
            Question(quiz_id=quiz1.id, text="Which keyword is used to handle exceptions?", option_a="catch", option_b="except", option_c="error", option_d="handle", correct_option="B"),
            Question(quiz_id=quiz1.id, text="What does the 'len()' function do?", option_a="Returns the length of an object", option_b="Finds the largest item", option_c="Converts to lowercase", option_d="None of the above", correct_option="A")
        ]
        db.session.bulk_save_objects(questions1)

        # Sample Quiz 2: General Tech Knowledge
        quiz2 = Quiz(title="General Tech Knowledge", description="A quick quiz on general technology concepts.")
        db.session.add(quiz2)
        db.session.commit()

        questions2 = [
            Question(quiz_id=quiz2.id, text="What does HTML stand for?", option_a="Hyperlinks and Text Markup Language", option_b="Hyper Text Markup Language", option_c="Home Tool Markup Language", option_d="Hyper Tool Multi Language", correct_option="B"),
            Question(quiz_id=quiz2.id, text="Which protocol is used for secure web browsing?", option_a="HTTP", option_b="FTP", option_c="HTTPS", option_d="SMTP", correct_option="C"),
            Question(quiz_id=quiz2.id, text="What is the brain of the computer?", option_a="RAM", option_b="Motherboard", option_c="CPU", option_d="Hard Drive", correct_option="C")
        ]
        db.session.bulk_save_objects(questions2)

        db.session.commit()
        print("Database initialized successfully with sample users and data!")

if __name__ == '__main__':
    init_database()
