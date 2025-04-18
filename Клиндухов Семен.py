import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
 
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle('Тренировочные задания')
        self.setGeometry(100, 100, 600, 200)
 
        title = QLabel("Тренировочные задания по алгебре логики и системам счисления")
        title.setStyleSheet("font-size: 20px; margin: 20px;")
 
        login_btn = QPushButton("Войти")
        register_btn = QPushButton("Зарегистрироваться")
 
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(login_btn)
        buttons_layout.addWidget(register_btn)
 
        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(buttons_layout)
 
        self.setLayout(main_layout)
 
        login_btn.clicked.connect(self.on_login_click)
        register_btn.clicked.connect(self.on_register_click)
 
    def on_login_click(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
 
    def on_register_click(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()
 
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('quiz_db.db')
        self.create_tables()
        self.init_questions()
        
    def create_tables(self):
        tables = [
            '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                password TEXT NOT NULL,
                UNIQUE(name, surname)
            );''',
            '''CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task TEXT,
                difficulty TEXT CHECK(difficulty IN ('легко', 'средне', 'сложно')),
                score INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );''',
            '''CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                question TEXT UNIQUE NOT NULL,
                answer TEXT NOT NULL
            );'''
        ]
        self.conn.execute("PRAGMA foreign_keys = ON")
        for table in tables:
            self.conn.execute(table)
        self.conn.commit()
 
    def init_questions(self):
        questions = [
                ('Алгебра логики', 'легко', 'не(A и B) = ?', 'неA или неB'),
                ('Алгебра логики', 'легко', 'A или неA = ?', '1'),
                ('Алгебра логики', 'средне', '(A импликация B) = ?', 'неA или B'),
                ('Алгебра логики', 'сложно', '((A импликация B) и (B импликация C)) импликация (A импликация C)', 'Одно и то же'),
                ('Алгебра логики', 'средне', '(A и B) или (A и неB) = ?', 'A'),
                ('Алгебра логики', 'сложно', '(A импликация (B импликация C)) = ((A и B) импликация C)', 'Одно и то же'),
                ('Алгебра логики', 'легко', 'A или 1 = ?', '1'),
                ('Алгебра логики', 'средне', 'не(A или B) = ?', 'неA и неB'),
                ('Алгебра логики', 'сложно', '(A исключающее или B) импликация (A и B) = ?', 'не(A исключающее или B) или (A и B)'),
                ('Алгебра логики', 'средне', 'A равносильно B = ?', '(A импликация B) и (B импликация A)'),
                ('Алгебра логики', 'легко', 'A и 0 = ?', '0'),
                ('Алгебра логики', 'сложно', '((A или B) и (неA или C)) импликация (B или C)', 'Одно и то же'),
        
                ('Системы счисления', 'легко', '1010₂ = ?₁₀', '10'),
                ('Системы счисления', 'легко', '16₁₀ = ?₂', '10000'),
                ('Системы счисления', 'средне', 'FF₁₆ = ?₁₀', '255'),
                ('Системы счисления', 'сложно', '735₈ = ?₁₆', '1DD'),
                ('Системы счисления', 'средне', '1011₂ + 1101₂ = ? (в двоичной системе)', '11000'),
                ('Системы счисления', 'сложно', '1A3₁₆ переведите в восьмеричную систему', '643'),
                ('Системы счисления', 'легко', '255₁₀ переведите в шестнадцатеричную систему', 'FF'),
                ('Системы счисления', 'средне', '37₈ * 2₈ = ? (в восьмеричной системе)', '76'),
                ('Системы счисления', 'сложно', '1010₂ * 11₂ = ? (в двоичной системе)', '11110'),
                ('Системы счисления', 'средне', '1101₂ - 1011₂ = ? (в двоичной системе)', '10'),
                ('Системы счисления', 'сложно', 'DEAD₁₆ = ?₁₀', '57005')
                
        ]
        cursor = self.conn.cursor()
        cursor.executemany('''INSERT OR IGNORE INTO questions 
                            (topic, difficulty, question, answer)
                            VALUES (?, ?, ?, ?)''', questions)
        self.conn.commit()
 
    def add_user(self, name, surname, password):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO users (name, surname, password) 
                           VALUES (?, ?, ?)''', (name, surname, password))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            QMessageBox.warning(None, "Ошибка", "Пользователь уже существует!")
            return None
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Ошибка базы данных: {str(e)}")
            return None
 
    def check_user(self, name, surname, password):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT id FROM users 
                        WHERE name = ? AND surname = ? AND password = ?''',
                        (name, surname, password))
        return cursor.fetchone()
 
    def get_questions(self, topic, difficulty, limit=10):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT question, answer FROM questions 
                        WHERE topic=? AND difficulty=?
                        ORDER BY RANDOM() LIMIT ?''',
                        (topic, difficulty, limit))
        return cursor.fetchall()
 
    def add_result(self, user_id, task, difficulty, score):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        cursor.execute('''INSERT INTO results 
                        (user_id, task, difficulty, score)
                        VALUES (?, ?, ?, ?)''', 
                        (user_id, task, difficulty, score))
        self.conn.commit()
        return True
        
 
    def get_all_results(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''SELECT 
                users.name, 
                users.surname, 
                results.task, 
                results.difficulty, 
                results.score
                FROM results 
                INNER JOIN users 
                ON results.user_id = users.id
                ORDER BY users.surname, users.name''')
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Ошибка при получении результатов: {e}")
            return []
 
    def __del__(self):
        self.conn.close()
 
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.current_user = None
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle('Вход')
        self.setGeometry(200, 200, 400, 200)
 
        title = QLabel("Вход")
        title.setStyleSheet("font-size: 18px; margin: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
 
        self.name_input = QLineEdit()
        self.surname_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
 
        form_layout = QVBoxLayout()
        fields = [
            ("Имя:", self.name_input),
            ("Фамилия:", self.surname_input),
            ("Пароль:", self.password_input)
        ]
 
        for label_text, field in fields:
            row = QHBoxLayout()
            row.addWidget(QLabel(label_text), alignment=Qt.AlignmentFlag.AlignLeft)
            row.addWidget(field)
            form_layout.addLayout(row)
 
        login_btn = QPushButton("Войти")
        login_btn.clicked.connect(self.check_credentials)
        form_layout.addWidget(login_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        form_layout.insertWidget(0, title)
        self.setLayout(form_layout)
 
    def check_credentials(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        password = self.password_input.text()
 
        if not all([name, surname, password]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return
 
        user = self.db.check_user(name, surname, password)
        if user:
            self.current_user = user[0]
            self.close()
            self.welcome_window = WelcomeWindow(self.current_user)
            self.welcome_window.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверные учетные данные!")
 
class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle('Регистрация')
        self.setGeometry(200, 200, 400, 250)
 
        title = QLabel("Регистрация")
        title.setStyleSheet("font-size: 18px; margin: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
 
        self.name_input = QLineEdit()
        self.surname_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
 
        form_layout = QVBoxLayout()
        fields = [
            ("Имя:", self.name_input),
            ("Фамилия:", self.surname_input),
            ("Пароль:", self.password_input)
        ]
 
        for label_text, field in fields:
            row = QHBoxLayout()
            row.addWidget(QLabel(label_text), alignment=Qt.AlignmentFlag.AlignLeft)
            row.addWidget(field)
            form_layout.addLayout(row)
 
        register_btn = QPushButton("Зарегистрироваться")
        register_btn.clicked.connect(self.register_user)
        form_layout.addWidget(register_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        form_layout.insertWidget(0, title)
        self.setLayout(form_layout)
 
    def register_user(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        password = self.password_input.text()
    
        if not all([name, surname, password]):
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения!")
            return
        
        user_id = self.db.add_user(name, surname, password)
        if user_id:
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")
            self.close()
            self.login_window = LoginWindow()
            self.login_window.show()
 
class WelcomeWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.db = Database()
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle('Выбор задания')
        self.setGeometry(300, 300, 600, 400)
 
        welcome_label = QLabel("Добро пожаловать!")
        welcome_label.setStyleSheet("font-size: 24px;")
        
        results_btn = QPushButton("Посмотреть результаты")
        results_btn.setFixedWidth(150)
 
        task_label = QLabel("Выберите задание:")
        task_label.setStyleSheet("font-size: 20px;")
        task_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
 
        logic_btn = QPushButton("Алгебра логики")
        logic_btn.setFixedSize(150, 50)
        logic_btn.clicked.connect(lambda: self.open_difficulty_window("Алгебра логики"))
        
        system_btn = QPushButton("Системы счисления")
        system_btn.setFixedSize(150, 50)
        system_btn.clicked.connect(lambda: self.open_difficulty_window("Системы счисления"))
 
        layout = QVBoxLayout()
        layout.addWidget(welcome_label)
        layout.addWidget(results_btn, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addStretch()
        layout.addWidget(task_label)
        layout.addSpacing(20)
        layout.addWidget(logic_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(system_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
 
        results_btn.clicked.connect(self.show_results)
        self.setLayout(layout)
 
    def open_difficulty_window(self, task_type):
        self.difficulty_window = DifficultyWindow(self.user_id, task_type)
        self.difficulty_window.show()
        self.close()
        
    def show_results(self):
        self.results_window = ResultsWindow(self.db)
        self.results_window.show()
 
class DifficultyWindow(QWidget):
    def __init__(self, user_id, task_type):
        super().__init__()
        self.user_id = user_id
        self.task_type = task_type
        self.db = Database()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Выбор сложности')
        self.setGeometry(300, 300, 400, 300)
        
        title = QLabel(f"{self.task_type}\nВыберите сложность")
        title.setStyleSheet("font-size: 20px; margin: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        easy_btn = QPushButton("Легкая")
        medium_btn = QPushButton("Средняя")
        hard_btn = QPushButton("Сложная")
        
        buttons = [easy_btn, medium_btn, hard_btn]
        for btn in buttons:
            btn.setFixedSize(200, 40)
            btn.setStyleSheet("font-size: 16px;")
        
        easy_btn.clicked.connect(lambda: self.start_quiz('легко'))
        medium_btn.clicked.connect(lambda: self.start_quiz('средне'))
        hard_btn.clicked.connect(lambda: self.start_quiz('сложно'))
        
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(easy_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(medium_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hard_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def start_quiz(self, difficulty):
        questions = self.db.get_questions(self.task_type, difficulty)
        self.quiz_window = QuizWindow(self.user_id, questions, self.task_type, difficulty)
        self.quiz_window.show()
        self.close()
 
class QuizWindow(QWidget):
    def __init__(self, user_id, questions, task_type, difficulty):
        super().__init__()
        self.db = Database()
        self.user_id = user_id
        self.questions = questions
        self.task_type = task_type
        self.difficulty = difficulty
        self.current_question = 0
        self.score = 0
        self.initUI()
        self.show_question()
        
    def initUI(self):
        self.setWindowTitle('Тестирование')
        self.setGeometry(300, 300, 600, 400)
        
        self.question_label = QLabel()
        self.question_label.setStyleSheet("font-size: 18px;")
        self.question_label.setWordWrap(True)
        
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Введите ваш ответ...")
        
        self.status_label = QLabel()
        self.counter_label = QLabel()
        
        self.next_btn = QPushButton("Следующий вопрос")
        self.next_btn.clicked.connect(self.check_answer)
        
        layout = QVBoxLayout()
        layout.addWidget(self.counter_label)
        layout.addWidget(self.question_label)
        layout.addWidget(self.answer_input)
        layout.addWidget(self.status_label)
        layout.addWidget(self.next_btn)
        
        self.setLayout(layout)
        
    def show_question(self):
        if self.current_question < len(self.questions):
            self.answer_input.setDisabled(False)
            self.next_btn.setText("Следующий вопрос")
            self.next_btn.clicked.disconnect()
            self.next_btn.clicked.connect(self.check_answer)
            
            question, answer = self.questions[self.current_question]
            self.current_question += 1
            self.counter_label.setText(f"Вопрос {self.current_question}/{len(self.questions)}")
            self.question_label.setText(question)
            self.correct_answer = answer
            self.answer_input.clear()
            self.status_label.clear()
        else:
            self.finish_quiz()
 
    def check_answer(self):
        user_answer = self.answer_input.text().strip().lower()
        correct_answer = self.correct_answer.strip().lower()
        
        if user_answer == correct_answer:
            self.score += 5
            self.status_label.setText("Правильно! +5 баллов")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.status_label.setText(f"Неверно!Правильный ответ: {self.correct_answer}")
            self.status_label.setStyleSheet("color: red;")
        
        self.answer_input.setDisabled(True)
        self.next_btn.setText("Продолжить" if self.current_question < len(self.questions) else "Завершить")
        self.next_btn.clicked.disconnect()
        self.next_btn.clicked.connect(self.show_question)
 
    def finish_quiz(self):
        success = self.db.add_result(self.user_id, self.task_type, self.difficulty, self.score)
        self.close()
        
 
class ResultsWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.initUI()
        self.load_data()
 
    def initUI(self):
        self.setWindowTitle('Результаты')
        self.setGeometry(200, 200, 800, 400)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ['Имя', 'Фамилия', 'Задание', 'Сложность', 'Баллы']
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
 
    def load_data(self):
        data = self.db.get_all_results()
        if not data:
            print("База данных результатов пуста!")
        else:
            for i, row in enumerate(data):
                self.table.setRowCount(self.table.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(elem)))
            self.table.resizeColumnsToContents()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
