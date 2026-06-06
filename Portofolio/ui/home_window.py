from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation, QRect

class HomeWindow(QWidget):
      def __init__(self, stack):
            super().__init__()
            layout = QVBoxLayout()

            title = QLabel("Wlecome to Salsabilla's Portofolio")
            title.setObjectName("titleLabel")

            projects_btn = QPushButton("View Projects")
            about_btn = QPushButton("About Me")
            contact_btn = QPushButton("Contact")

            # Animasi fade saat pindah window 
            def animate_transition(index):
                  effect = QGraphicsOpacityEffect
                  self.setGraphicsEffect(effect)
                  anim = QPropertyAnimation(stack, b"geometry")
                  anim.setDuration(400)
                  anim.setStartValue(QRect(0, 0, stack.width(), stack.height()))
                  anim.setEndValue(QRect(0, 0, stack.width(), stack.height()))
                  anim.finished.connect(lambda: stack.setCurrentIndex(index))
                  anim.start()
                  stack.setCurrentIndex(index)

            projects_btn.clicked.connect(lambda: animate_transition(1))
            about_btn.clicked.connect(lambda: animate_transition(2))
            contact_btn.clicked.connect(lambda: animate_transition(3))

            layout.addWidget(title)
            layout.addWidget(projects_btn)
            layout.addWidget(about_btn)
            layout.addWidget(contact_btn)
            self.setLayout(layout)