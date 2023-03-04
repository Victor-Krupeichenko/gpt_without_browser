import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from gpt_form import Ui_MainWindow
import openai
from config import API_KEY, MODEL_ENGINE


class Work(QThread):
    """Класс отдельного потока"""
    clear_signal = pyqtSignal()

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.is_runing = False
        self.messages = []

    def run(self):
        """Запускает в отдельном потоке"""

        openai.api_key = API_KEY
        while True:
            while self.is_runing:
                message = self.main_window.ui.textEdit.toPlainText()
                self.clear_signal.emit()
                self.main_window.ui.plainTextEdit.appendPlainText(f"\nVictor: {message}\n")
                self.main_window.ui.plainTextEdit.ensureCursorVisible()
                self.messages.append({"role": "user", "content": message})
                chat = openai.ChatCompletion.create(model=MODEL_ENGINE, messages=self.messages, temperature=0.5)
                reply = chat.choices[0]['message']['content']
                self.main_window.ui.plainTextEdit.appendPlainText(f"\nGPT-Bot:\n{reply}\n")
                self.main_window.ui.plainTextEdit.ensureCursorVisible()
                self.messages.append({"role": "assistant", "content": reply})
                self.is_runing = False


class MyGpt(QMainWindow):
    """Класс основного окна приложения"""

    def __init__(self):
        super(MyGpt, self).__init__(parent=None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.worker = Work(main_window=self)
        self.worker.start()
        self.ui.send_question.clicked.connect(self.send_question)
        self.worker.clear_signal.connect(self.clear_text_edit)

    def clear_text_edit(self):
        """Очищает поля ввода вопроса"""
        self.ui.textEdit.clear()

    def send_question(self):
        """Активирует отправку вопроса"""
        self.worker.is_runing = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_prog = MyGpt()
    main_prog.show()
    sys.exit(app.exec_())
