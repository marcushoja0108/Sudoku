from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QMovie

class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.backdrop = QWidget(self)
        self.backdrop.setStyleSheet("Background-color: rgba(255, 255, 255, 200);")
        self.backdrop.lower()
        # self.setStyleSheet("Background-color: rgba(255, 255, 255, 200);")
        
        self.movie_label = QLabel(self)
        self.movie = QMovie("Attempt 2/assets/loading_cube.gif")
        self.movie_label.setMovie(self.movie)
        self.movie_label.setAlignment(Qt.AlignCenter)
        self.movie.start()
        self.movie.setScaledSize(QSize(200, 200))
        
        
        label = QLabel("🧠 Generating board...")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 30px;"
                            "font-family: Arial;")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.movie_label)
        layout.addWidget(label)
        
        self.setLayout(layout)
        
        self.setGeometry(0, 0, parent.width(), parent.height())
        self.setGeometry(0, 0, self.width(), self.height())
        self.hide()
        
    def resizeEvent(self, event):
        if self.parent():
            self.setGeometry(0, 0, self.parent().width(), self.parent().height())
            self.backdrop.setGeometry(0, 0, self.parent().width(), self.parent().height())
        super().resizeEvent(event)
    
    def show_overlay(self):
        self.show()
        self.raise_()
        
    def hide_overlay(self):
        self.hide()