from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
   QAction,
   QApplication,
   QDialog,
   QHBoxLayout,
   QLabel,
   QMenu,
   QPushButton,
   QSlider,
   QVBoxLayout,
)

import website.Yaris.music as music


_menu = None
_big_menu = None


def _quit():
   QApplication.quit()


def _show_big_menu():
   global _big_menu

   if _big_menu is not None:
      _big_menu.close()

   _big_menu = QDialog()
   _big_menu.setWindowTitle("YARIS options")
   _big_menu.setMinimumWidth(320)
   _big_menu.setStyleSheet("""
      QDialog {
         background-color: #171a21;
         color: #f4f7fb;
      }
      QLabel {
         color: #f4f7fb;
         font-size: 15px;
      }
      QPushButton {
         background-color: #26313d;
         border: 1px solid #3a4150;
         border-radius: 6px;
         color: #f4f7fb;
         padding: 9px 12px;
      }
      QPushButton:hover {
         background-color: #2e8b8b;
      }
      QSlider::groove:horizontal {
         background: #3a4150;
         height: 6px;
         border-radius: 3px;
      }
      QSlider::handle:horizontal {
         background: #2e8b8b;
         width: 14px;
         margin: -4px 0;
         border-radius: 7px;
      }
   """)

   layout = QVBoxLayout(_big_menu)
   layout.addWidget(QLabel("YARIS options"))

   volume_label = QLabel("Volume: 100%")
   layout.addWidget(volume_label)

   volume_slider = QSlider(Qt.Horizontal)
   volume_slider.setRange(0, 100)
   volume_slider.setValue(100)

   def update_volume(value):
      volume_label.setText(f"Volume: {value}%")
      music.set_volume(value / 100)

   volume_slider.valueChanged.connect(update_volume)
   layout.addWidget(volume_slider)

   volume_buttons = QHBoxLayout()
   volume_down_button = QPushButton("Volume down")
   volume_down_button.clicked.connect(music.volume_down)
   volume_buttons.addWidget(volume_down_button)

   volume_up_button = QPushButton("Volume up")
   volume_up_button.clicked.connect(music.volume_up)
   volume_buttons.addWidget(volume_up_button)
   layout.addLayout(volume_buttons)

   mute_button = QPushButton("Mute")
   mute_button.clicked.connect(music.mute)
   layout.addWidget(mute_button)

   close_button = QPushButton("Close")
   close_button.clicked.connect(_big_menu.close)
   layout.addWidget(close_button)

   exit_button = QPushButton("Exit YARIS")
   exit_button.clicked.connect(_quit)
   layout.addWidget(exit_button)

   _big_menu.show()


def show():
   """Show the application menu at the current cursor position."""
   global _menu

   if QApplication.instance() is None:
      return

   if _menu is not None:
      _menu.close()

   _menu = QMenu()
   _menu.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
   _menu.setAttribute(Qt.WA_TranslucentBackground)
   _menu.setStyleSheet("""
      QMenu {
         background-color: #171a21;
         border: 1px solid #3a4150;
         border-radius: 10px;
         padding: 8px;
         color: #f4f7fb;
         font-size: 14px;
      }
      QMenu::item {
         padding: 10px 28px 10px 12px;
         border-radius: 6px;
      }
      QMenu::item:selected {
         background-color: #2e8b8b;
      }
      QMenu::separator {
         height: 1px;
         background: #343b49;
         margin: 6px 4px;
      }
   """)

   title = QAction("YARIS", _menu)
   title.setEnabled(False)
   _menu.addAction(title)
   _menu.addSeparator()

   volume_up_action = QAction("Volume up", _menu)
   volume_up_action.triggered.connect(music.volume_up)
   _menu.addAction(volume_up_action)

   mute_action = QAction("Mute", _menu)
   mute_action.triggered.connect(music.mute)
   _menu.addAction(mute_action)

   more_options_action = QAction("More options...", _menu)
   more_options_action.triggered.connect(_show_big_menu)
   _menu.addAction(more_options_action)

   _menu.addSeparator()
   quit_action = QAction("Exit", _menu)
   quit_action.triggered.connect(_quit)
   _menu.addAction(quit_action)

   _menu.popup(QApplication.desktop().cursor().pos())

