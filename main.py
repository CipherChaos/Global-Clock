from clock.ui.window import ClockWindow
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":

    try:
        app = QApplication([])
        window = ClockWindow()
        window.show()
        app.exec()
    except Exception as error:
        print(f"Application error: {error}")
