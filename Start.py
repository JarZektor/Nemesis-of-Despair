import sys
import json
import game

from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QMainWindow, QCheckBox, QComboBox, QScrollBar
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.css = """
            QLabel{
            color: blue;
            font: 19px;
            }
            QComboBox{
            background-color: lightblue;
            }
            QCheckBox{
            font: 19px;
            color: blue;
            }
            QCheckBox::indicator {
            width: 25px;
            height: 25px;
            }
            QPushButton{
            background-color: lightblue;
            color: blue;
            font: 19px;
            }
        """

        self.items = ['800x450', '960x540', '1280x720', '1920x1080']
        self.fps = ["30 FPS", "60 FPS"]

        self.setWindowTitle('Экран загрузки pygame')
        self.setGeometry(500, 100, 1000, 1000)
        self.setFixedSize(500, 500)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setStyleSheet(self.css)

        # Изображение логотипа игры
        self.ask_accept = QLabel(self)
        self.ask_accept.setGeometry(0, -10, 500, 240)
        self.ask_accept.setStyleSheet("background-image: url(images/NoD_launcher.png)")

        # Выпадающий список разрешений
        self.size_win = QComboBox(self)
        self.size_win.setGeometry(25, 250, 200, 25)
        self.size_win.addItems(self.items)

        # Выпадающий список fps
        self.change_fps = QComboBox(self)
        self.change_fps.setGeometry(25, 315, 200, 25)
        self.change_fps.addItems(self.fps)

        # Скролл бар музыки
        self.scroll_music = QScrollBar(self)
        self.scroll_music.setGeometry(250, 250, 200, 25)
        self.scroll_music.setRange(0, 200)
        self.scroll_music.setValue(100)
        self.scroll_music.setStyleSheet("background: lightblue")
        self.scroll_music.setOrientation(QtCore.Qt.Horizontal)

        # Вывод для музыки
        self.label_music = QLabel("MUSIC VOLUME", self)
        self.label_music.setGeometry(250, 275, 200, 25)
        self.label_music.setWordWrap(True)
        self.label_music.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_music.valueChanged.connect(self.music)

        # Скролл бар звука
        self.scroll_sound = QScrollBar(self)
        self.scroll_sound.setGeometry(250, 315, 200, 25)
        self.scroll_sound.setRange(0, 200)
        self.scroll_sound.setValue(100)
        self.scroll_sound.setStyleSheet("background: lightblue")
        self.scroll_sound.setOrientation(QtCore.Qt.Horizontal)

        # Вывод для звука
        self.label_sound = QLabel("SOUND VOLUME", self)
        self.label_sound.setGeometry(250, 340, 200, 25)
        self.label_sound.setWordWrap(True)
        self.label_sound.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_sound.valueChanged.connect(self.sound)

        # Кнопка старта
        self.start_button = QPushButton('Старт', self)
        self.start_button.setGeometry(275, 450, 125, 25)
        self.start_button.clicked.connect(self.start)

        # Кнопка управления
        self.control_button = QPushButton('Управление', self)
        self.control_button.setGeometry(100, 450, 125, 25)
        self.control_button.clicked.connect(self.show_control)

        # Скролл бар master volume
        self.scroll_master_volume = QScrollBar(self)
        self.scroll_master_volume.setGeometry(250, 375, 200, 25)
        self.scroll_master_volume.setRange(0, 100)
        self.scroll_master_volume.setValue(100)
        self.scroll_master_volume.setStyleSheet("background: lightblue")
        self.scroll_master_volume.setOrientation(QtCore.Qt.Horizontal)

        # Вывод для master volume
        self.label_master_volume = QLabel("Master volume: 100%", self)
        self.label_master_volume.setGeometry(250, 400, 201, 25)
        self.label_master_volume.setWordWrap(True)
        self.label_master_volume.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_master_volume.valueChanged.connect(self.volume)

        # Чекбокс фуллскрин
        self.checkbox_full_screen = QCheckBox('Full screen', self)
        self.checkbox_full_screen.setGeometry(25, 360, 200, 50)
        self.checkbox_full_screen.setChecked(True)

        # Чекбокс debug
        self.checkbox_debug = QCheckBox('Debug mode', self)
        self.checkbox_debug.setGeometry(25, 385, 200, 50)
        self.checkbox_debug.setChecked(True)

        # Список чекбоксов и Список всех виджетов с настраиваемым значением (НЕ МЕНЯТЬ ПОД СТРАХОМ СМЕРТИ!)
        self.all_checkbox = [self.checkbox_full_screen, self.checkbox_debug]
        self.widget_with_value = [self.size_win, self.change_fps, self.scroll_sound,
                                  self.scroll_music, self.scroll_master_volume]

        # label для отображения управления
        self.controls = QLabel(self)
        self.controls.setGeometry(0, 0, 500, 500)
        self.controls.setStyleSheet("background-image: url(images/setting.png)")
        self.controls.hide()

        # Кнопка возврата в главное меню
        self.return_setting = QPushButton('->', self)
        self.return_setting.setGeometry(470, 0, 30, 30)
        self.return_setting.clicked.connect(self.hide_control)

        # Выставляем прошлые значения файлов
        self.set_value()

    def start(self):
        self.update_json()
        self.close()
        game.start()

    def hide_control(self):
        self.controls.hide()
        self.return_setting.hide()

    def show_control(self):
        self.controls.show()
        self.return_setting.show()

    def update_json(self):
        data = dict()
        data["object_value"] = [self.checkbox_full_screen.isChecked(), self.checkbox_debug.isChecked(),
                                self.size_win.currentText(), self.change_fps.currentText(),
                                self.scroll_music.value(), self.scroll_sound.value(), self.scroll_master_volume.value()]
        with open("values.json", "w") as file:
            json.dump(data, file, indent=4)

    def set_value(self):
        with open("values.json", "r") as file:
            data = json.load(file)['object_value']
        [self.all_checkbox[i].setChecked(data[i]) for i in range(2)]
        [self.widget_with_value[i - 2].setCurrentText(data[i]) for i in range(2, 4)]
        [self.widget_with_value[i - 2].setValue(data[i]) for i in range(4, 7)]

    def volume(self):
        self.label_master_volume.setText("Master volume: " + str(self.scroll_master_volume.value()) + "%")

    def music(self):
        self.label_music.setText("Music: " + str(self.scroll_music.value()) + "%")

    def sound(self):
        self.label_sound.setText("Sound: " + str(self.scroll_sound.value()) + "%")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Breeze')
    ex = Window()
    ex.show()
    sys.exit(app.exec())
