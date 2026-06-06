from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from PySide6.QtCore import QPropertyAnimation
from PySide6.QtWidgets import QGraphicsOpacityEffect

class PortfolioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Salsabilla Portfolio")
        self.resize(800, 600)

        # Apply stylesheet
        with open("assets/style.qss") as f:
            self.setStyleSheet(f.read())

        # Stacked widget untuk navigasi antar window
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Tambahkan setiap window
        self.home = HomeWindow(self.stack)
        self.projects = ProjectsWindow(self.stack)
        self.about = AboutWindow(self.stack)
        self.contact = ContactWindow(self.stack)

        self.stack.addWidget(self.home)     # index 0
        self.stack.addWidget(self.projects) # index 1
        self.stack.addWidget(self.about)    # index 2
        self.stack.addWidget(self.contact)  # index 3

        # Fade in otomatis saat aplikasi dibuka
        self.fade_in(self.home)

    def fade_in(self, widget):
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(800)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.start()

if __name__ == "__main__":
    app = QApplication([])
    window = PortfolioApp()
    window.show()
    app.exec()
