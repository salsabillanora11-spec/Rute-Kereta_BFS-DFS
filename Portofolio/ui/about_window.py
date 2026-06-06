from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation, QRect

class AboutWindow(QWidget):
    def __init__(self, stack):
        super().__init__()
        layout = QVBoxLayout()

        title = QLabel("About Me")
        title.setObjectName("titleLabel")

        bio = QLabel("I am Salsabilla, passionate about Python, UI/UX design, and building hospital apps.")
        skills = QLabel("Skills: Python, PySide6, Docker, Nginx, Statistics")

        # Animasi fade saat kembali ke Home
        def back_home():
            effect = QGraphicsOpacityEffect(self)
            self.setGraphicsEffect(effect)
            anim = QPropertyAnimation(stack, b"geometry")
            anim.setDuration(400)
            anim.setStartValue(QRect(0, 0, stack.width(), stack.height()))
            anim.setEndValue(QRect(0, 0, stack.width(), stack.height()))
            anim.finished.connect(lambda: stack.setCurrentIndex(0))
            anim.start()
            stack.setCurrentIndex(0)

        layout.addWidget(title)
        layout.addWidget(bio)
        layout.addWidget(skills)
        self.setLayout(layout)
