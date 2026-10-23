import sys
import os
import signal
import menu
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie

print('gif')

# Ignorowanie sygnału SIGINT (np. Ctrl+C)
signal.signal(signal.SIGINT, signal.SIG_IGN)


def get_resurce_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


class desktop_gif_widget(QWidget):
    def __init__(self, gif_name):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint | Qt.SubWindow)


        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        self.label = QLabel(self)
        gif_path = get_resurce_path(gif_name)
        
       
        self.movie = QMovie(gif_path)

        if not self.movie.isValid():
            print(f"Error: Could not load GIF file at: {gif_path}")
            sys.exit(1)

        self.label.setMovie(self.movie)
        self.movie.start()
        self.movie.frameChanged.connect(self.resize_to_gif)
        self.drag_position = None

    def resize_to_gif(self):
        
        size = self.movie.currentImage().size()
        self.resize(size)
        self.label.resize(size)

        def gif_on(self):
            self.movie.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            menu.show(self)
            event.accept()
        elif event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_position = None

    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            event.ignore()

    
    def closeEvent(self, event):
        event.ignore()
def create_viewer():
    gif_viewer = desktop_gif_widget("yaris.gif")
    gif_viewer.show()
    return gif_viewer
def bounce(gif_viewer):
    if not hasattr(gif_viewer, "dx"):
        gif_viewer.dx = 4
        gif_viewer.dy = 3
    x = gif_viewer.x() + gif_viewer.dx
    y = gif_viewer.y() + gif_viewer.dy

    screen = gif_viewer.screen().availableGeometry()
    if x <= screen.left() or x + gif_viewer.width() >= screen.right():
        gif_viewer.dx *= -1
        x = gif_viewer.x() + gif_viewer.dx

    if y <= screen.top() or y + gif_viewer.height() >= screen.bottom():
        gif_viewer.dy *= -1
        y = gif_viewer.y() + gif_viewer.dy

    gif_viewer.move(x, y)
def start():
    app = QApplication.instance() or QApplication(sys.argv)
    gif_viewer = create_viewer()
    sys.exit(app.exec_())
