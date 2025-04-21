import sys
import sqlite3
import os

from PyQt6.QtWidgets import QLabel, QComboBox, QLineEdit
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem


class MainWind(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.init_db()
    
    def init_db(self):
        db_file = 'physics_calculator.db'
        
        is_new_db = not os.path.exists(db_file)
        
        self.con = sqlite3.connect(db_file)
        self.cur = self.con.cursor()
            
            
        if is_new_db:
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                formula TEXT NOT NULL,
                result TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)
            self.con.commit()
            print("База данных успешно создана")
            
    def initUI(self):
        
        self.setWindowTitle("Physical calculator")
        self.setGeometry(300, 300, 500, 400)
        
        self.formuls = QComboBox(self) 
        self.formuls.addItems(["Скорость (v = s / t)",
                                      "Ускорение (a = (v2 - v1) / t)",
                                      "Сила Тяжести (F = m * a)",
                                      "Работа (A = F * s)",
                                      "Мощность (P = A / t)",
                                      "Центро-стремительное ускорение a = v^2 / R",
                                      "Энергия(Кинетическая) E = m * v^2 / 2", 
                                      "Энергия(Потенциальная) E = m * g * h",
                                      "Второй закон Ньютона a = F / m",
                                      "Импульс тела p = m * v",
                                      "Закон всемирного тяготения F = G * m1 * m2 / R^2",
                                      "Перемещение S(→) = v * t + a * t^2 / 2",
                                      "Макс. высота тела брошенного вверх h(max)=V^2/2g"])
        self.formuls.resize(350, 20)
        self.formuls.move(145, 15)

        self.label_formuls = QLabel(self)
        self.label_formuls.setText('Формула:')
        self.label_formuls.move(10, 15)

        self.res = QLabel(self)
        self.res.resize(280, 70)
        self.res.move(10, 250)
        self.res_un = QLabel(self)
        self.res_un.resize(120, 70)
        self.res_un.move(300, 250)
        
        self.use_but = QPushButton('Использовать \n формулу', self)
        self.use_but.move(410, 40)

        self.calc_but = QPushButton('Рассчитать', self)
        self.calc_but.move(5, 365)
        self.calc_but.resize(245, 30)

        self.cler_but = QPushButton("Очистить", self)
        self.cler_but.move(250, 365)
        self.cler_but.resize(123, 30)

        self.history_but = QPushButton('История', self)
        self.history_but.move(373, 365)
        self.history_but.resize(123, 30)

        self.res_lab = QLabel(self)
        self.res_lab.setText('Результат:')
        self.res_lab.move(10, 250)
        self.zs = QLabel(self)
        self.zs.setText('Единица измерения:')
        self.zs.move(300, 250)

        self.tek = QLabel(self)
        self.tek.setText('Текущая формула:')
        self.tek.move(5, 50)

        self.tekres = QLabel(self)
        self.tekres.move(110, 48)
        self.tekres.resize(300, 20)
#Создание виджетов с символом велечины
        self.label1 = QLabel(self)
        self.label1.setText('Значение S:')
        self.label1.move(5000, 5000)
        self.line1 = QLineEdit(self)
        self.line1.move(5000, 5000)
        self.line1.resize(350, 20)
        self.znach1 = QComboBox(self)
        self.znach1.move(5000, 5000)
        self.znach1.resize(60, 20)

        self.label2 = QLabel(self)
        self.label2.setText('Значение t:')
        self.label2.move(5000, 5000)
        self.line2 = QLineEdit(self)
        self.line2.move(5000, 5000)
        self.line2.resize(350, 20)
        self.znach2 = QComboBox(self)
        self.znach2.move(5000, 5000)
        self.znach2.resize(60, 20)

        self.label3 = QLabel(self)
        self.label3.setText('Значение v1:')
        self.label3.move(5000,5000)
        self.line3 = QLineEdit(self)
        self.line3.move(5000, 5000)
        self.line3.resize(350, 20)
        self.znach3 = QComboBox(self)
        self.znach3.move(5000, 5000)
        self.znach3.resize(60, 20)

        self.label4 = QLabel(self)
        self.label4.setText('Значение v2:')
        self.label4.move(5000,5000)

        self.label5 = QLabel(self)
        self.label5.setText('Значение m:')
        self.label5.move(5000,5000)

        self.label6 = QLabel(self)
        self.label6.setText('Значение a:')
        self.label6.move(5000,5000)

        self.label7 = QLabel(self)
        self.label7.setText('Значение F:')
        self.label7.move(5000,5000)

        self.label8 = QLabel(self)
        self.label8.setText('Значение A:')
        self.label8.move(5000,5000)

        self.label9 = QLabel(self)
        self.label9.setText('Значение v:')
        self.label9.move(5000,5000)

        self.label10 = QLabel(self)
        self.label10.setText('Значение R:')
        self.label10.move(5000,5000)

        self.label11 = QLabel(self)
        self.label11.setText('Значение g:')
        self.label11.move(5000,5000)

        self.label12 = QLabel(self)
        self.label12.setText('Значение h:')
        self.label12.move(5000,5000)

        self.label13 = QLabel(self)
        self.label13.setText('Значение m1:')
        self.label13.move(5000,5000)

        self.label14 = QLabel(self)
        self.label14.setText('Значение m2:')
        self.label14.move(5000,5000)
#Подключение функций к кнопкам
        self.use_but.clicked.connect(self.hello)
        self.calc_but.clicked.connect(self.culc)
        self.cler_but.clicked.connect(self.clearc)
        self.history_but.clicked.connect(self.open_tab)

    def hello(self):
        self.tekres.setText('')
        self.tekres.setText(self.formuls.currentText())

        self.line1.setText('')
        self.line2.setText('')
        self.line3.setText('')
        
        self.line1.move(5000, 5000)
        self.line2.move(5000, 5000)
        self.line3.move(5000, 5000)
   
        self.label1.move(5000,5000)
        self.label2.move(5000,5000)
        self.label3.move(5000,5000)
        self.label4.move(5000,5000)
        self.label5.move(5000,5000)
        self.label6.move(5000,5000)
        self.label7.move(5000,5000)
        self.label8.move(5000,5000)
        self.label9.move(5000,5000)
        self.label10.move(5000,5000)
        self.label11.move(5000,5000)
        self.label12.move(5000,5000)
        self.label13.move(5000,5000)
        self.label14.move(5000,5000)

        self.znach1.move(5000, 5000)
        self.znach2.move(5000, 5000)
        self.znach3.move(5000, 5000)
        self.znach1.clear()
        self.znach2.clear()
        self.znach3.clear()
#Отображение в окне виджетов для ввода данных в зависимости от формулы
        if self.formuls.currentText() == 'Скорость (v = s / t)':
            self.label1.move(5, 100)
            self.line1.move(80, 100)
            self.znach1.move(435, 100)
            self.znach1.addItems(['км', 'м', 'см', 'мм', 'дм'])
            
            self.label2.move(5, 135)
            self.line2.move(80, 135)
            self.znach2.move(435, 135)
            self.znach2.addItems(['c', 'мин', 'ч', 'мс'])
        elif self.formuls.currentText() == 'Ускорение (a = (v2 - v1) / t)':
            self.label3.move(5, 100)
            self.line1.move(80, 100)
            self.znach1.move(435, 100)
            self.znach1.addItems(['м/c', 'км/ч', 'м/ч'])
            
            self.label4.move(5, 135)
            self.line2.move(80, 135)
            self.znach2.move(435, 135)
            self.znach2.addItems(['м/c', 'км/ч', 'м/ч'])
            
            self.label2.move(5, 170)
            self.line3.move(80, 170)
            self.znach3.move(435, 170)
            self.znach3.addItems(['c', 'мин', 'ч', 'мс'])
        elif self.formuls.currentText() == 'Сила Тяжести (F = m * a)':
            self.label5.move(5, 100)
            self.line1.move(80, 100)
            self.znach1.move(435, 100)
            self.znach1.addItems(['кг', 'г', 'т', 'ц'])
            
            self.label6.move(5, 135)
            self.line2.move(80, 135)
            self.znach2.move(435, 135)
            self.znach2.addItems(['м/c^2', 'км/с^2'])
        elif self.formuls.currentText() == 'Работа (A = F * s)':
            self.label7.move(5, 100)
            self.line1.move(80, 100)
            self.znach1.move(435, 100)
            self.znach1.addItems(['кН', 'мН', 'МН', 'нН', 'Н'])
            
            
            self.label1.move(5, 135)
            self.line2.move(80, 135)
            self.znach2.move(435, 135)
            self.znach2.addItems(['км', 'м', 'см', 'мм', 'дм'])
        elif self.formuls.currentText() == 'Мощность (P = A / t)':
            self.label8.move(5, 100)
            self.line1.move(80, 100)
            self.znach1.move(435, 100)
            self.znach1.addItems(['кДж', 'мДж', 'МДж', 'Дж'])
            
            self.label2.move(5, 135)
            self.line2.move(80, 135)
            self.znach2.move(435, 135)
            self.znach2.addItems(['c', 'мин', 'ч', 'мс'])
        elif self.formuls.currentText() == 'Центро-стремительное ускорение a = v^2 / R':
            self.label9.move(5, 100)
            self.line1.move(80, 100)
            self.znach1.move(435, 100)
            self.znach1.addItems(['м/c', 'км/ч', 'м/ч'])
            
            self.label10.move(5, 135)
            self.line2.move(80, 135)
            self.znach2.move(435, 135)
            self.znach2.addItems(['км', 'м', 'см', 'мм', 'дм'])
            
        elif self.formuls.currentText() == 'Энергия(Кинетическая) E = m * v^2 / 2':
            self.label5.move(5, 100)
            self.line1.move(80, 100)
            self.znach1.move(435, 100)
            self.znach1.addItems(['кг', 'г', 'т', 'ц'])

            self.label9.move(5, 135)
            self.line2.move(80, 135)
            self.znach2.move(435, 135)
            self.znach2.addItems(['м/c', 'км/ч', 'м/ч'])
        
        elif self.formuls.currentText() == 'Энергия(Потенциальная) E = m * g * h':
            self.label5.move(5, 100)
            self.line1.move(80, 100)
            self.znach1.move(435, 100)
            self.znach1.addItems(['кг', 'г', 'т', 'ц'])

            self.label11.move(5, 135)
            self.line2.move(80, 135)
            self.znach2.move(435, 135)
            self.znach2.addItems(['м/c^2', 'км/с^2'])
            
            self.label12.move(5, 170)
            self.line3.move(80, 170)
            self.znach3.move(435, 170)
            self.znach3.addItems(['км', 'м', 'см', 'мм', 'дм'])
        elif self.formuls.currentText() == "Второй закон Ньютона a = F / m":
            self.label7.move(5, 100)
            self.line1.move(80, 100)
            self.znach1.move(435, 100)
            self.znach1.addItems(['кН', 'мН', 'МН', 'нН', 'Н'])

            self.label5.move(5, 135)
            self.line2.move(80, 135)
            self.znach2.move(435, 135)
            self.znach2.addItems(['кг', 'г', 'т', 'ц'])
        elif self.formuls.currentText() == "Импульс тела p = m * v":
            self.label5.move(5, 100)
            self.line1.move(80, 100)
            self.znach1.move(435, 100)
            self.znach1.addItems(['кг', 'г', 'т', 'ц'])

            self.label9.move(5, 135)
            self.line2.move(80, 135)
            self.znach2.move(435, 135)
            self.znach2.addItems(['м/c', 'км/ч', 'м/ч'])
        elif self.formuls.currentText() == "Закон всемирного тяготения F = G * m1 * m2 / R^2":
            self.label13.move(5, 100)
            self.line1.move(80, 100)
            self.znach1.move(435, 100)
            self.znach1.addItems(['кг', 'г', 'т', 'ц'])

            self.label14.move(5, 135)
            self.line2.move(80, 135)
            self.znach2.move(435, 135)
            self.znach2.addItems(['кг', 'г', 'т', 'ц'])

            self.label10.move(5, 170)
            self.line3.move(80, 170)
            self.znach3.move(435, 170)
            self.znach3.addItems(['км', 'м', 'см', 'мм', 'дм'])
        elif self.formuls.currentText() == "Перемещение S(→) = v * t + a * t^2 / 2":
            self.label9.move(5, 100)
            self.line1.move(80, 100)
            self.znach1.move(435, 100)
            self.znach1.addItems(['м/c', 'км/ч', 'м/ч'])

            self.label2.move(5, 135)
            self.line2.move(80, 135)
            self.znach2.move(435, 135)
            self.znach2.addItems(['c', 'мин', 'ч', 'мс'])

            self.label6.move(5, 170)
            self.line3.move(80, 170)
            self.znach3.move(435, 170)
            self.znach3.addItems(['м/c^2', 'км/с^2'])
        elif self.formuls.currentText() == "Макс. высота тела брошенного вверх h(max)=V^2/2g":
            self.label9.move(5, 100)
            self.line1.move(80, 100)
            self.znach1.move(435, 100)
            self.znach1.addItems(['м/c', 'км/ч', 'м/ч'])

            self.label11.move(5, 135)
            self.line2.move(80, 135)
            self.znach2.move(435, 135)
            self.znach2.addItems(['м/c^2', 'км/с^2'])
          
    def convert(self):
        self.res.setText('')
        block, arg = [], []
        res_si = []
        # Добавление введенных велечин в список
        if self.tekres.text() == "Перемещение S(→) = v * t + a * t^2 / 2" or self.tekres.text() == "Закон всемирного тяготения F = G * m1 * m2 / R^2" or self.tekres.text() == 'Энергия(Потенциальная) E = m * g * h' or self.tekres.text() == 'Ускорение (a = (v2 - v1) / t)':
            try:
                block.append(float(self.line1.text()))
                block.append(float(self.line2.text()))
                block.append(float(self.line3.text()))
            except ValueError:
                self.res.setText("Введите число!")
                self.res.setStyleSheet(''' font-size: 24px; ''')
                self.res_un.setText('Error')
                self.res_un.setStyleSheet(''' font-size: 24px; ''')
            arg.append(self.znach1.currentText())
            arg.append(self.znach2.currentText())
            arg.append(self.znach3.currentText())        
        else:
            try:
                block.append(float(self.line1.text()))
                block.append(float(self.line2.text()))
            except ValueError:
                self.res.setText("Введите число!")
                self.res.setStyleSheet(''' font-size: 24px; ''')
                self.res_un.setText('Error')
                self.res_un.setStyleSheet(''' font-size: 24px; ''')
            arg.append(self.znach1.currentText())
            arg.append(self.znach2.currentText())
#Перевод велечин из списка в систему СИ, добавляя их в список           
        for i in range(len(block)):
                if arg[i] == "г":
                    res_si.append(block[i] / 1000)
                elif arg[i] == 'т':
                    res_si.append(block[i] * 1000)
                elif arg[i] == 'ц':
                    res_si.append(block[i] * 100)   
                elif arg[i] == 'км':
                    res_si.append(block[i] * 1000)
                elif arg[i] == 'см':
                    res_si.append(block[i] / 100)
                elif arg[i] == 'мм':
                    res_si.append(block[i] / 1000)
                elif arg[i] == 'дм':
                    res_si.append(block[i] / 10)
                elif arg[i] == 'км/с^2':
                    res_si.append(block[i] * 1000)
                elif arg[i] == 'мин':
                    res_si.append(block[i] * 60)
                elif arg[i] == 'ч':
                    res_si.append(block[i] * 3600)
                elif arg[i] == 'мс':
                    res_si.append(block[i] / 1000)
                elif arg[i] == 'кДж':
                    res_si.append(block[i] * 1000)
                elif arg[i] == 'мДж':
                    res_si.append(block[i] / 1000)
                elif arg[i] == 'МДж':
                    res_si.append(block[i] * 1000000)
                elif arg[i] == 'кН':
                    res_si.append(block[i] * 1000)
                elif arg[i] == 'нН':
                    res_si.append(block[i] / 1000000)
                elif arg[i] == 'мН':
                    res_si.append(block[i] / 1000)
                elif arg[i] == 'МН':
                    res_si.append(block[i] * 1000000) 
                else:
                    res_si.append(block[i])   
        return res_si
#Функция выполняет вычисление формулы с переведенными в систему Си велечинами                    
    def culc(self):
        convert = self.convert()
        a = ''
        if self.res.text() == "Введите число!":
            pass
        else:
            result = 1
            if self.tekres.text() == 'Энергия(Потенциальная) E = m * g * h':
                if convert[0] < 0 or convert[2] < 0:
                    self.res.setText("Масса или высота < 0")
                    self.res_un.setText("Error")
                    self.res.setStyleSheet(''' font-size: 24px; ''')
                    self.res_un.setStyleSheet(''' font-size: 24px; ''')
                    return
                edin = 'Дж'
                for k in range(len(convert)):
                        result = result * convert[k]  
                result = round(result, 6)
            elif self.tekres.text() == 'Энергия(Кинетическая) E = m * v^2 / 2':
                if convert[0] < 0:
                    self.res.setText("Масса отрицательная")
                    self.res_un.setText("Error")
                    self.res.setStyleSheet(''' font-size: 24px; ''')
                    self.res_un.setStyleSheet(''' font-size: 24px; ''')
                    return
                edin = "Дж"
                result = round(convert[0] * convert[-1] ** 2 / 2, 6)
            elif self.tekres.text() == 'Центро-стремительное ускорение a = v^2 / R':
                if convert[1] <= 0:
                    self.res.setText("Радиус <= 0")
                    self.res_un.setText("Error")
                    self.res.setStyleSheet(''' font-size: 24px; ''')
                    self.res_un.setStyleSheet(''' font-size: 24px; ''')
                    return
                edin = "м/с^2"
                result = round(convert[0] ** 2 / convert[-1], 100)
            elif self.tekres.text() == 'Мощность (P = A / t)':
                if convert[1] <= 0:
                    self.res.setText("Время <= 0")
                    self.res_un.setText("Error")
                    self.res.setStyleSheet(''' font-size: 24px; ''')
                    self.res_un.setStyleSheet(''' font-size: 24px; ''')
                    return
                edin = "Вт"
                try:
                    result = round(convert[0] / convert[-1], 100)
                except ZeroDivisionError:
                    a = 'На ноль делить нельзя!'
            elif self.tekres.text() == 'Работа (A = F * s)':
                if convert[1] < 0:
                    self.res.setText("Путь < 0")
                    self.res_un.setText("Error")
                    self.res.setStyleSheet(''' font-size: 24px; ''')
                    self.res_un.setStyleSheet(''' font-size: 24px; ''')
                    return
                edin = "Дж"
                result = round(convert[0] * convert[-1], 100)
            elif self.tekres.text() == 'Сила Тяжести (F = m * a)':
                if convert[0] < 0:
                    self.res.setText("Масса отрицательная")
                    self.res_un.setText("Error")
                    self.res.setStyleSheet(''' font-size: 24px; ''')
                    self.res_un.setStyleSheet(''' font-size: 24px; ''')
                    return
                edin = "Н"
                result = round(convert[0] * convert[-1], 6)
            elif self.tekres.text() == 'Ускорение (a = (v2 - v1) / t)':
                if convert[2] <= 0:
                    self.res.setText("Время <= 0")
                    self.res_un.setText("Error")
                    self.res.setStyleSheet(''' font-size: 24px; ''')
                    self.res_un.setStyleSheet(''' font-size: 24px; ''')
                    return
                edin = "м/с^2"
                try:
                    result = round((convert[0] - convert[1]) / convert[-1], 100)
                except ZeroDivisionError:
                    a = 'На ноль делить нельзя!'
            elif self.tekres.text() == 'Скорость (v = s / t)':
                if convert[1] <= 0 or convert[0] <= 0:
                    self.res.setText("Время или путь <= 0")
                    self.res_un.setText("Error")
                    self.res.setStyleSheet(''' font-size: 24px; ''')
                    self.res_un.setStyleSheet(''' font-size: 24px; ''')
                    return
                edin = "м/с"
                try:
                    result = round(convert[0] / convert[-1], 100)
                except ZeroDivisionError:
                    a = 'На ноль делить нельзя!'
            elif self.tekres.text() == "Второй закон Ньютона a = F / m":
                if convert[1] <= 0: 
                    self.res.setText("Масса <= 0")
                    self.res_un.setText("Error")
                    self.res.setStyleSheet(''' font-size: 24px; ''')
                    self.res_un.setStyleSheet(''' font-size: 24px; ''')
                    return
                edin = "м/с^2"
                try:
                    result = round(convert[0] / convert[-1], 100)
                except ZeroDivisionError:
                    a = 'На ноль делить нельзя!'
            elif self.tekres.text() == "Импульс тела p = m * v":
                if convert[0] < 0:
                    self.res.setText("Масса отрицательная")
                    self.res_un.setText("Error")
                    self.res.setStyleSheet(''' font-size: 24px; ''')
                    self.res_un.setStyleSheet(''' font-size: 24px; ''')
                    return
                edin = "кг * м/с"
                result = round(convert[0] * convert[-1], 6)
            elif self.tekres.text() == "Закон всемирного тяготения F = G * m1 * m2 / R^2":
                if convert[0] < 0 or convert[1] < 0:
                    self.res.setText("Масса отрицательная")
                    self.res_un.setText("Error")
                    self.res.setStyleSheet(''' font-size: 24px; ''')
                    self.res_un.setStyleSheet(''' font-size: 24px; ''')
                    return
                if convert[2] <= 0:
                    self.res.setText("Расстояние < 0")
                    self.res_un.setText("Error")
                    self.res.setStyleSheet(''' font-size: 24px; ''')
                    self.res_un.setStyleSheet(''' font-size: 24px; ''')
                    return
                edin = 'Н'
                try:
                    result = round(6.67  * 10 ** -11 * convert[0] * convert[1] / convert[-1] ** 2 , 100)
                except ZeroDivisionError:
                    a = 'На ноль делить нельзя!'
            elif self.tekres.text() == "Перемещение S(→) = v * t + a * t^2 / 2":
                if convert[1] <= 0:
                    self.res.setText("Время < 0")
                    self.res_un.setText("Error")
                    self.res.setStyleSheet(''' font-size: 24px; ''')
                    self.res_un.setStyleSheet(''' font-size: 24px; ''')
                    return
                edin = 'м'
                result = round(convert[0] * convert[1] + convert[-1] * convert[1] ** 2 / 2 ,6)
            elif self.tekres.text() == "Макс. высота тела брошенного вверх h(max)=V^2/2g":
                edin = 'м'
                try:
                    result = round(convert[0] ** 2 / (2 * convert[-1]), 100)
                except ZeroDivisionError:
                    a = 'На ноль делить нельзя!'

            if a == '':
                expression = str(self.tekres.text())
                result1 = str(result) + ' ' + edin
                self.res.setText(str(result))
                self.res.setStyleSheet(''' font-size: 24px; ''')
                self.res_un.setText(edin)
                self.res_un.setStyleSheet(''' font-size: 24px; ''')
                self.cur.execute(
                "INSERT INTO calculations(formula, result) VALUES(?, ?)",
                (self.tekres.text(), f"{result} {edin}")
            )
                self.con.commit()
            else:
                self.res.setText(str(a))
                self.res.setStyleSheet(''' font-size: 24px; ''')
                self.res_un.setText('Error')
                self.res_un.setStyleSheet(''' font-size: 24px; ''')
#Очистка результата вычислений, а также введеных данных            
    def clearc(self):
        self.res.setText('')
        self.res_un.setText('')

        self.line1.setText('')
        self.line2.setText('')
        self.line3.setText('')
#Открытие окна с историей вычислений        
    def open_tab(self):
        self.wid = Hist()
        self.wid.show()
        
#Создание окна в котором находиться таблица с результатами вычислений формулы 
class Hist(QWidget):
    def __init__(self):
        super().__init__()
        
        self.con = sqlite3.connect('physics_calculator.db')
        self.cur = self.con.cursor()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('История вычислений')
        self.setGeometry(200, 200, 600, 400)
        
        self.table = QTableWidget(self)
        self.table.resize(600, 400)
        
        result = self.cur.execute('''SELECT * FROM calculations''').fetchall()
        if result:
            self.table.setRowCount(len(result))
            self.table.setColumnCount(len(result[0]))
                
            for row_idx, row in enumerate(result):
                for col_idx, value in enumerate(row):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
            
  
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWind()
    ex.show()
    sys.exit(app.exec())
