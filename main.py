import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QPlainTextEdit, QWidget,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
)
from PyQt5.QtCore import pyqtSignal, Qt


class StandardCalc:

    def __init__(self, win):
        """Base class method to initialise class object. All methods and fields are public"""
        self.answer_status = True
        self.err_status = False
        self.prev = ''
        if not hasattr(self, 'widgets'):
            self.widgets = []
        self.result = 0
        self.window = win
        self.edit_field = QLabel("0", win)
        self.answer_field = QLabel('', win)
        self.btn1 = QPushButton('1', win)
        self.btn2 = QPushButton('2', win)
        self.btn3 = QPushButton('3', win)
        self.btn4 = QPushButton('4', win)
        self.btn5 = QPushButton('5', win)
        self.btn6 = QPushButton('6', win)
        self.btn7 = QPushButton('7', win)
        self.btn8 = QPushButton('8', win)
        self.btn9 = QPushButton('9', win)
        self.btn0 = QPushButton('0', win)
        self.btn_plus = QPushButton('+', win)
        self.btn_minus = QPushButton('-', win)
        self.btn_mult = QPushButton('∙', win)
        self.btn_div = QPushButton('÷', win)
        self.btn_equal = QPushButton('=', win)
        self.btn_c = QPushButton('c', win)
        self.btn_ce = QPushButton('ce', win)
        self.btn_back = QPushButton('←', win)
        self.btn_dot = QPushButton('.', win)
        self.widgets += [self.edit_field, self.answer_field, self.btn1, self.btn2, self.btn3, self.btn4, self.btn5,
                         self.btn6, self.btn7, self.btn8, self.btn9, self.btn0, self.btn_plus, self.btn_minus,
                         self.btn_mult, self.btn_div, self.btn_equal, self.btn_c, self.btn_ce, self.btn_back,
                         self.btn_dot]

    def set_act_geom(self):
        """Method is for calling other methods that needed for adequate starting of application and cant be called from
        within the __init__ method"""
        self.set_actions()
        self.show_widgets()

    def set_actions(self):
        """Set action methods for all the virtual buttons"""
        self.btn0.clicked.connect(lambda: self.change_field('0'))
        self.btn1.clicked.connect(lambda: self.change_field('1'))
        self.btn2.clicked.connect(lambda: self.change_field('2'))
        self.btn3.clicked.connect(lambda: self.change_field('3'))
        self.btn4.clicked.connect(lambda: self.change_field('4'))
        self.btn5.clicked.connect(lambda: self.change_field('5'))
        self.btn6.clicked.connect(lambda: self.change_field('6'))
        self.btn7.clicked.connect(lambda: self.change_field('7'))
        self.btn8.clicked.connect(lambda: self.change_field('8'))
        self.btn9.clicked.connect(lambda: self.change_field('9'))
        self.btn_dot.clicked.connect(lambda: self.dot_action())
        self.btn_back.clicked.connect(lambda: self.backspace_action())
        self.btn_c.clicked.connect(lambda: self.c_action())
        self.btn_ce.clicked.connect(lambda: self.ce_action())
        self.btn_equal.clicked.connect(lambda: self.equal_action())
        self.btn_plus.clicked.connect(lambda: self.operand_action('+'))
        self.btn_minus.clicked.connect(lambda: self.operand_action('-'))
        self.btn_mult.clicked.connect(lambda: self.operand_action('*'))
        self.btn_div.clicked.connect(lambda: self.operand_action('/'))

    def backspace_action(self):
        """Delete the last symbol in the input field"""
        self.edit_field.setText(self.edit_field.text()[:-1])

    def c_action(self):
        """Clear input value method"""
        self.edit_field.setText('0')
        self.answer_status = True

    def dot_action(self):
        """Method checks out and adds (if can) period in input number"""
        text = self.edit_field.text()
        a = [index for index in range(len(text)) if text.startswith('.', index)]
        if len(a) == 0:
            self.change_field('.')

    def ce_action(self):
        """Clear All method. To delete both input field and answer field values"""
        self.edit_field.setText('0')
        self.answer_field.setText('')
        self.prev = ''
        self.result = 0
        self.answer_status = True
        self.err_status = True

    def operand_action(self, operand):
        """Method works when operand buttons are pressed. Used for basic math operations"""
        text = self.answer_field.text()
        text1 = self.edit_field.text()
        if text1 == '.':
            text1 = '0'
        if self.answer_status or self.err_status:
            self.answer_field.setText(text1+' '+operand)
            self.edit_field.setText('0')
            self.err_status = False
        elif text != '':
            if text[-1] in ['-', '+', '*', '/']:
                self.answer_field.setText(text[:-1]+operand)
            elif text1 != '':
                self.answer_field.setText(text+' '+operand)
                self.equal_action()
        elif text1 != '':
            self.answer_field.setText(self.edit_field.text()+' '+operand)
            self.edit_field.setText('0')
        else:
            self.answer_field.setText('0 '+operand)

    def equal_action(self):
        """the evaluate method. Works when the '=' button (enter key) is pressed"""
        text = self.answer_field.text()
        text1 = self.edit_field.text()
        if text1 == '.':
            text1 = '0'
        if text != '' and text1 != '':
            if text[-1] == '/' and text1 == '0':
                self.ce_action()
                self.answer_field.setText('Делить на ноль нельзя')
            elif text[-1] in ['-', '+', '*', '/']:
                self.prev = (text+' '+text1)
                self.result = eval(self.prev)
                self.edit_field.setText(str(self.result))
                self.answer_field.setText(str(self.prev))
        self.answer_status = True

    def change_field(self, inputs):
        """changing the input field value (add to or replace old value)"""
        if self.answer_status or self.edit_field.text() == '0':
            self.edit_field.setText(inputs)
            self.answer_status = False
        else:
            self.edit_field.setText(self.edit_field.text()+inputs)

    def set_geometry(self):
        """sizes and positions of window and widgets"""
        win = self.window
        win.setFixedSize(250, 280)
        btn_width = round((win.width()-50)/4)
        line1_x, line2_x, line3_x, line4_x, line5_x = 95, 130, 165, 200, 235
        self.answer_field.setGeometry(10, 23, win.width()-20, 30)
        self.edit_field.setGeometry(10, 57, win.width() - 20, 30)
        self.btn_ce.setGeometry(10, line1_x, btn_width, 30)
        self.btn_c.setGeometry(20+btn_width, line1_x, btn_width, 30)
        self.btn_back.setGeometry(30+btn_width*2, line1_x, btn_width, 30)
        self.btn_div.setGeometry(40+btn_width*3, line1_x, btn_width, 30)
        self.btn7.setGeometry(10, line2_x, btn_width, 30)
        self.btn8.setGeometry(20+btn_width, line2_x, btn_width, 30)
        self.btn9.setGeometry(30+btn_width*2, line2_x, btn_width, 30)
        self.btn_mult.setGeometry(40+btn_width*3, line2_x, btn_width, 30)
        self.btn4.setGeometry(10, line3_x, btn_width, 30)
        self.btn5.setGeometry(20+btn_width, line3_x, btn_width, 30)
        self.btn6.setGeometry(30+btn_width*2, line3_x, btn_width, 30)
        self.btn_minus.setGeometry(40+btn_width*3, line3_x, btn_width, 30)
        self.btn1.setGeometry(10, line4_x, btn_width, 30)
        self.btn2.setGeometry(20+btn_width, line4_x, btn_width, 30)
        self.btn3.setGeometry(30+btn_width*2, line4_x, btn_width, 30)
        self.btn_plus.setGeometry(40+btn_width*3, line4_x, btn_width, 30)
        self.btn_dot.setGeometry(10, line5_x, btn_width, 30)
        self.btn0.setGeometry(20+btn_width, line5_x, btn_width, 30)
        self.btn_equal.setGeometry(40+btn_width*3, line5_x, btn_width, 30)

    def show_widgets(self):
        """Set widgets visibility """
        self.set_geometry()
        self.widget_style()
        for i in self.widgets:
            i.parent = self.window
            i.show()

    def widget_style(self):
        """Styling widgets like CSS"""
        font_size = 14
        self.window.setWindowTitle('Калькулятор')
        for i in self.widgets:
            if type(i) is QPushButton:
                i.setStyleSheet(""" QPushButton {
                            border: 1px solid grey;
                            border-radius: 4px;
                            font-size: """+str(font_size)+"""px;
                            background-color: rgb(255, 255, 255);
                            } """)
        self.answer_field.setStyleSheet(""" QLabel {
                            border-radius: 4px;
                            font-size: """+str(font_size+2)+"""px;
                            background-color: #fff;
                            } """)
        self.edit_field.setStyleSheet(""" QLabel {
                                    font-size: """+str(font_size+10)+"""px;
                                    background-color: #fff;
                                    } """)
        self.edit_field.setAlignment(Qt.AlignRight)
        self.answer_field.setAlignment(Qt.AlignRight)

    def delete(self):
        """Delete (close) all widgets of class and delete class itself"""
        for i in self.widgets:
            i.parent = None
            i.close()
        self.widgets = []
        self = None


class EngineerCalc(StandardCalc):
    """Inherit class of Standard Calculator. Contains expanded variety of math methods"""
    def __init__(self, win):
        super().__init__(win)
        self.btn_sqr = QPushButton('квадрат', win)
        self.btn_sqrt = QPushButton('корень', win)
        self.btn_sqrt.setToolTip('типа корень, пока не добавлено')
        self.btn_sqr.setToolTip('типа степень, пока не добавлено')
        self.widgets += [self.btn_sqr, self.btn_sqrt]

    def set_geometry(self):
        win = self.window
        btn_width = round((win.width() - 50) / 4)
        self.btn_sqrt.setGeometry(30 + btn_width * 2, 250, btn_width, 30)
        self.btn_sqr.setGeometry(10, 290, btn_width, 30)
        super().set_geometry()


class MainWindow(QMainWindow):
    resized = pyqtSignal()

    def __init__(self):
        """Initiative method of window"""
        super(MainWindow, self).__init__()
        self.calc = None
        #self.create_menu()
        self.createUI()
        self.set_standard()

    def resizeEvent(self, event):
        """Resizing window causes changing of widgets' sizes"""
        self.resized.emit()
        self.calc.set_geometry()

    def keyPressEvent(self, e):  # doesnt work when app is in background
        """To use keyboard to input values"""
        if e.key() == Qt.Key_0:
            self.calc.change_field('0')
        elif e.key() == Qt.Key_1:
            self.calc.change_field('1')
        elif e.key() == Qt.Key_2:
            self.calc.change_field('2')
        elif e.key() == Qt.Key_3:
            self.calc.change_field('3')
        elif e.key() == Qt.Key_4:
            self.calc.change_field('4')
        elif e.key() == Qt.Key_5:
            self.calc.change_field('5')
        elif e.key() == Qt.Key_6:
            self.calc.change_field('6')
        elif e.key() == Qt.Key_7:
            self.calc.change_field('7')
        elif e.key() == Qt.Key_8:
            self.calc.change_field('8')
        elif e.key() == Qt.Key_9:
            self.calc.change_field('9')
        elif e.key() == Qt.Key_Backspace:
            self.calc.backspace_action()
        elif e.key() == Qt.Key_Plus:
            self.calc.operand_action('+')
        elif e.key() == Qt.Key_Minus:
            self.calc.operand_action('-')
        elif e.key() == Qt.Key_Enter:
            self.calc.equal_action()
        elif e.key() == Qt.Key_Asterisk:
            self.calc.operand_action('*')
        elif e.key() == Qt.Key_Backslash or e.key() == Qt.Key_Slash:
            self.calc.operand_action('/')
        elif e.key() == Qt.Key_Comma or e.key() == Qt.Key_Period:
            self.calc.dot_action()
        elif e.key() == Qt.Key_Escape:
            sys.exit()

    def createUI(self):
        """To set some window/app's options/settings/visual styles"""
        self.setStyleSheet(""" MainWindow {
                                    border-radius: 5px;
                                    background-color: #fff;
                                    } """)

    def create_menu(self):
        """Add main menu bar to the application"""
        menu = self.menuBar().addMenu('Калькулятор')
        standard_type = menu.addAction('Обычный')
        engineer_type = menu.addAction('Инженерный')
        standard_type.triggered.connect(self.set_standard)
        engineer_type.triggered.connect(self.set_engineer)

    def set_standard(self):
        """Creates class of standard calculator (base math methods)"""
        if self.calc:
            self.calc.delete()
        self.calc = StandardCalc(self)
        self.calc.set_act_geom()

    def set_engineer(self):
        """Creates class of engineer calculator (extended list of math methods)"""
        if self.calc:
            self.calc.delete()
        self.calc = EngineerCalc(self)
        self.calc.set_act_geom()

# Create application object and application window object
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
