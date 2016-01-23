import sqlite3
import sys
from PyQt4 import QtGui, QtCore
from datetime import date, datetime
import random

conn = sqlite3.connect('jeopardy.db')
c = conn.cursor()

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()


        screen_size = QtCore.QRect(QtGui.QDesktopWidget().availableGeometry())
        screen_size_w = screen_size.width()
        self.setGeometry(0.15*screen_size_w, 100, 0.7*screen_size_w, 700)
        self.setFixedWidth(0.7*screen_size_w)

        self.setWindowTitle("Jeopardy! Trainer")

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background,QtCore.Qt.darkBlue)
        self.setPalette(palette)

        #bring in non-standard fonts
        QtGui.QFontDatabase.addApplicationFont("Korinna Bold.ttf")
        QtGui.QFontDatabase.addApplicationFont("Swiss911.ttf")
        QtGui.QFontDatabase.addApplicationFont("Domestic_Manners.ttf")

        self.label_widget = QtGui.QDockWidget()

        self.home()

    def switchPage(self):
        print("Switched Page")
        self.button_widget.setCurrentIndex(1)

    def submitCorrect(self):
        print("Correct")
        c.execute("INSERT INTO responses(clue_ID, response_type, response_timestamp) VALUES (?, ?, ?)",
                  (self.transport_array[5],1,datetime.now()))
        conn.commit()
        self.button_widget.setCurrentIndex(0)
        self.home()

    def submitIncorrect(self):
        print("Incorrect")
        c.execute("INSERT INTO responses(clue_ID, response_type, response_timestamp) VALUES (?, ?, ?)",
                  (self.transport_array[5],0,datetime.now()))
        conn.commit()
        self.button_widget.setCurrentIndex(0)
        self.home()

    def home(self):
        self.response = ""
        self.transport_array = []
        self.transport_array = self.read_from_db()


        self.clue = ClueDisplay(self)
        self.label_widget.setWidget(self.clue)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, self.label_widget)
        self.label_widget.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        self.label_widget.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)

        self.read_from_db()
        self.label_widget.setTitleBarWidget(CategoryValueDisplay(self))
        self.button_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.button_widget)

        self.view_widget = ViewCorrectResponse(self)
        self.view_widget.button.setAutoDefault(True)
        self.view_widget.button.clicked.connect(self.switchPage)
        self.button_widget.addWidget(self.view_widget)

        self.submit_widget = SubmitResponse(self)

        self.submit_widget.correct_button.clicked.connect(self.submitCorrect)
        # self.submit_widget.correct_button.setAutoDefault(True)
        # self.submit_widget.incorrect_button.setDefault(True)

        self.submit_widget.incorrect_button.clicked.connect(self.submitIncorrect)

        self.button_widget.addWidget(self.submit_widget)
        # self.read_from_db()
        self.show()

    def read_from_db(self):
        db_values = []
        c.execute('SELECT max(ID) FROM jeopardy')
        max_clue_id = c.fetchone()[0]
        rand_number = random.randint(1, max_clue_id)
        c.execute('SELECT category, round, value, clue, correct_response, category_comment, ID FROM jeopardy WHERE ID = ?', (rand_number,))
        db_values = c.fetchone()
        category_text = db_values[0]
        #round_number = db_values[1]
        value_number = db_values[2]
        clue_text = db_values[3]
        correct_response_text = db_values[4]
        category_comment_text = db_values[5]
        clue_ID = db_values[6]
        return category_text, value_number, clue_text, correct_response_text, category_comment_text, clue_ID

class ViewCorrectResponse(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ViewCorrectResponse, self).__init__(parent)
        layout = QtGui.QHBoxLayout()
        self.button = QtGui.QPushButton('View Correct Res&ponse')
        layout.addStretch()
        layout.addWidget(self.button)
        layout.addStretch()
        layout.setMargin(20)
        self.setLayout(layout)

class SubmitResponse(QtGui.QWidget):
    def __init__(self, mainWindow):
        super(SubmitResponse, self).__init__(mainWindow)

        self.correct_response_label = QtGui.QLabel()
        self.correct_response_label.setText(mainWindow.transport_array[3])
        self.correct_response_label.setStyleSheet("""
            .QLabel {
                color:#ffffff;
                font-size: 45px;
                font-family: 'Domestic Manners';
                }
            """)

        super_layout = QtGui.QVBoxLayout()
        layout1 = QtGui.QHBoxLayout()
        layout2 = QtGui.QHBoxLayout()

        layout1.addStretch()
        layout1.addWidget(self.correct_response_label)
        layout1.addStretch()

        self.correct_button = QtGui.QPushButton('Subm&it as Correct')
        self.incorrect_button = QtGui.QPushButton('Submit as Inc&orrect')

        layout2.addStretch()
        layout2.addWidget(self.correct_button)
        layout2.addWidget(self.incorrect_button)
        layout2.addStretch()
        layout2.addStrut(100)

        super_layout.addLayout(layout1)
        super_layout.addLayout(layout2)
        self.setLayout(super_layout)

class CategoryValueDisplay(QtGui.QWidget):
    def __init__(self, mainWindow):
        super(CategoryValueDisplay, self).__init__(mainWindow)
        layout = QtGui.QHBoxLayout()
        self.label1 = QtGui.QLabel()
        self.label1.setText(mainWindow.transport_array[0])
        self.label1.setMargin(20)
        self.label1.setStyleSheet("""
            .QLabel {
                color:#ffffff;
                font-size: 70px;
                font-family: Swiss911 XCm BT;
                }
            """)
        effect1 = QtGui.QGraphicsDropShadowEffect()
        effect1.setBlurRadius(0)
        effect1.setColor(QtGui.QColor('#000000'))
        effect1.setOffset(3,3)
        self.label1.setGraphicsEffect(effect1)

        self.label2 = QtGui.QLabel()

        #show 'FINAL JEOPARDY" in place of value if Final Jeopardy Clue
        if mainWindow.transport_array[1] == None:
            self.label2.setText('FINAL JEOPARDY')
        else:
            self.label2.setText('$' + str(mainWindow.transport_array[1]))

        self.label2.setMargin(20)

        #self.label2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label2.setStyleSheet("""
            .QLabel {
                color:rgb(209, 161, 76);
                font-size: 70px;
                font-family: Swiss911 XCm BT;
                text-align: right;
                }
            """)
        effect2 = QtGui.QGraphicsDropShadowEffect()
        effect2.setBlurRadius(0)
        effect2.setColor(QtGui.QColor('#000000'))
        effect2.setOffset(3,3)
        self.label2.setGraphicsEffect(effect2)

        layout.addStretch()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addStretch()

        if mainWindow.transport_array[4] != None:
            super_layout = QtGui.QVBoxLayout()
            self.cat_comment = QtGui.QLabel(mainWindow.transport_array[4])
            self.cat_comment.setStyleSheet("""
                .QLabel {
                    color:#ffffff;
                    font-size: 30px;
                    font-family: Swiss911 XCm BT;
                    }
                """)
            effect3 = QtGui.QGraphicsDropShadowEffect()
            effect3.setBlurRadius(0)
            effect3.setColor(QtGui.QColor('#000000'))
            effect3.setOffset(2,2)
            self.cat_comment.setGraphicsEffect(effect3)

            comment_row = QtGui.QHBoxLayout()
            comment_row.addStretch()
            comment_row.addWidget(self.cat_comment)
            comment_row.addStretch()
            super_layout.addLayout(layout)
            super_layout.addLayout(comment_row)
            self.setLayout(super_layout)
        else:
            self.setLayout(layout)


class ClueDisplay(QtGui.QWidget):
    def __init__(self, mainWindow):
        super(ClueDisplay, self).__init__(mainWindow)
        layout = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel()
        self.label.setText(mainWindow.transport_array[2])
        self.label.setStyleSheet("""
            .QLabel {
                color:#ffffff;
                font-size: 30px;
                font-weight: bold;
                font-family:Korinna
                }
            """)
        effect = QtGui.QGraphicsDropShadowEffect()
        effect.setBlurRadius(0)
        effect.setColor(QtGui.QColor('#000000'))
        effect.setOffset(2,2)
        self.label.setGraphicsEffect(effect)
        self.label.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.label.setWordWrap(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(self.label)
        layout.addStretch()
        layout.setMargin(110)
        layout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.setLayout(layout)

def run():
    app = QtGui.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

run()