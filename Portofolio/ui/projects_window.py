from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation, QRect
import json 

class ProjectsWindow(QWidget):
      def __init__(self, stack):
            super().__init__()
            layout = QVBoxLayout()

            title = QLabel("My Projects")
            title.setObjectName("titleLabel")

            projects_list = QListWidget()
            with open("data/projects.json") as f:
                  projects = json.load(f)
                  for p in projects:
                        projects_list.addItem(f"{p['title']} - {p['description']}")

            # Animasi fade saat kembali ke home
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
            layout.addWidget(projects_list)
            self.setLayout(layout)