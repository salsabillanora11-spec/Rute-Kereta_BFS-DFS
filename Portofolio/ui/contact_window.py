from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation, QRect

class ContactWindow(QWidget):
    def __init__(self, stack):
        super().__init__()
        layout = QVBoxLayout()

        title = QLabel("Contact Me")
        title.setObjectName("titleLabel")

        email_input = QLineEdit()
        email_input.setPlaceholderText("Your Email")

        message_input = QLineEdit()
        message_input.setPlaceholderText("Your Message")

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(lambda: print("Message sent!"))

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
        layout.addWidget(email_input)
        layout.addWidget(message_input)
        layout.addWidget(send_btn)
        self.setLayout(layout)
