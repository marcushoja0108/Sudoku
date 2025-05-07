import os
import random
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QThread, pyqtSignal

from OCR import *

class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.backdrop = QWidget(self)
        self.backdrop.setStyleSheet("Background-color: rgba(255, 255, 255, 200);")
        self.backdrop.lower()
        
        self.movie_label = QLabel(self)
        self.movie = self.load_random_meme("App/assets/meme")
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
        
        
    def load_random_meme(self, folder_path):
        gif_files = [m for m in os.listdir(folder_path)]
        if not gif_files:
            raise FileNotFoundError("No gif file found")
        selected_gif = random.choice(gif_files)
        return QMovie(os.path.join(folder_path, selected_gif))
    
    def update_geometry(self):
        if self.parent():
            self.setGeometry(0, 0, self.parent().width(), self.parent().height())
            self.backdrop.setGeometry(0, 0, self.parent().width(), self.parent().height())
    
    def resizeEvent(self, event):
        self.update_geometry()
        super().resizeEvent(event)
    
    def show_overlay(self):
        if self.movie:
            self.movie.stop()
            self.movie_label.clear()
            
        self.movie = self.load_random_meme("App/assets/meme")
        self.movie.setScaledSize(QSize(300, 300))
        self.movie_label.setMovie(self.movie)
        self.movie.start()
        
        self.update_geometry()
        
        self.show()
        self.raise_()
        
    def hide_overlay(self):
        self.hide()

class OCRThread(QThread):
    ocr_done = pyqtSignal(object)
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
    def run(self):
        ocr_slots = run_ocr(self.file_path)
        self.ocr_done.emit(ocr_slots)