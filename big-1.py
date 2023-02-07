from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QWidget

from api_utils import *
from map_utils import *


class myMap:
    def __init__(self):
        self.z = 15
        self.lat = 37.619585
        self.lon = 55.865172
        self.l = "map"
        self.show_pt = False


my_map = myMap()


# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(600, 600))  # Устанавливаем размеры
        self.setWindowTitle("Большая задача")  # Устанавливаем заголовок окна
        self.central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(self.central_widget)  # Устанавливаем центральный виджет
        self.grid_layout = QGridLayout()  # Создаём QGridLayout
        self.central_widget.setLayout(self.grid_layout)  # Устанавливаем данное размещение в центральный виджет
        # метка и кнопки
        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setText("Адрес:")
        self.grid_layout.addWidget(self.label, 0, 0, 1, 2)  # Добавляем метку в сетку
        # карта
        self.image = QLabel()
        self.grid_layout.addWidget(self.image, 1, 3, 10, 10)
        self.pixmap = QPixmap("data//empty.png")
        self.image.setPixmap(self.pixmap)

        self.plus = QPushButton("+", self)
        self.grid_layout.addWidget(self.plus, 1, 14, 1, 1)
        self.plus.clicked.connect(self.plus_z)
        self.minus = QPushButton("-", self)
        self.grid_layout.addWidget(self.minus, 1, 0, 1, 1)
        self.minus.clicked.connect(self.minus_z)

        self.map = QPushButton("map", self)
        self.grid_layout.addWidget(self.map, 1, 5, 1, 1)
        self.map.clicked.connect(lambda: self.set_map("map"))
        self.sat = QPushButton("sat", self)
        self.grid_layout.addWidget(self.sat, 1, 6, 1, 1)
        self.sat.clicked.connect(lambda: self.set_map("sat"))
        self.hybrid = QPushButton("hybrid", self)
        self.grid_layout.addWidget(self.hybrid, 1, 7, 1, 1)
        self.hybrid.clicked.connect(lambda: self.set_map("sat,skl"))

        # поле
        self.adress = QLineEdit()
        self.adress.setFont(font)
        self.grid_layout.addWidget(self.adress, 0, 3, 1, 9)  # Добавляем поле в сетку
        self.adress.setText('Пестеля, 5')
        # поле для вывода изображения карты
        # кнопка Найти
        self.btn2 = QPushButton("Найти", self)
        self.grid_layout.addWidget(self.btn2, 0, 12, 1, 2)  # Добавляем кнопку в сетку
        self.btn2.clicked.connect(self.new_search)
        self.skip_next = 0

        self.btn3 = QPushButton("Сбросить", self)
        self.grid_layout.addWidget(self.btn3, 0, 14, 1, 1)  # Добавляем кнопку в сетку
        self.btn3.clicked.connect(self.reset_search)
        self.show_index = True

        self.index_button = QPushButton("Отключить отображение индекса", self)
        self.grid_layout.addWidget(self.index_button, 1, 10, 1, 3)
        self.index_button.clicked.connect(self.set_index)

        self.installEventFilter(self)

    def set_index(self):
        if self.index_button.text() == "Отключить отображение индекса":
            self.show_index = False
            self.index_button.setText("Включить отображение индекса")
        else:
            self.show_index = True
            self.index_button.setText("Отключить отображение индекса")
        self.new_search()

    def reset_search(self):
        my_map.show_pt = False
        self.adress.setText("")
        self.change_z()

    def set_map(self, value):
        my_map.l = value
        self.change_z()

    def eventFilter(self, obj, event):
        if hasattr(event, "key"):
            if event.key() == self.skip_next:
                self.skip_next = 0
                return False
            self.skip_next = event.key()
            if event.key() == Qt.Key_Left:
                self.move("left")
            if event.key() == Qt.Key_Right:
                self.move("right")
            if event.key() == Qt.Key_Down:
                self.move("down")
            if event.key() == Qt.Key_Up:
                self.move("up")
            return True
        return False

    def new_search(self):
        toponym_to_find = self.adress.text()

        geo = geocode(toponym_to_find)["metaDataProperty"]["GeocoderMetaData"]
        self.adress.setText(geo["text"] + f', индекс {geo["Address"]["postal_code"]}' * self.show_index)
        # Получаем координаты центра карты
        my_map.lon, my_map.lat = get_coords(toponym_to_find)
        params = {
            "ll": ",".join([str(my_map.lon), str(my_map.lat)]),
            "z": str(my_map.z),
            "l": f"{my_map.l}",
            'pt': f"{my_map.lon},{my_map.lat}"
        }
        my_map.show_pt = True

        # обновить изображение
        self.pixmap = QPixmap(get_map(params))
        self.image.setPixmap(self.pixmap)

    def minus_z(self):
        if my_map.z > 0:
            my_map.z = my_map.z - 1
            self.change_z()

    def plus_z(self):
        if my_map.z < 17:
            my_map.z = my_map.z + 1
            self.change_z()

    def change_z(self):
        params = {
            "ll": ",".join([str(my_map.lon), str(my_map.lat)]),
            "z": str(my_map.z),
            "l": f"{my_map.l}",
            'pt': f"{my_map.lon},{my_map.lat}"
        }
        if not my_map.show_pt:
            del params["pt"]

        # обновить изображение
        self.pixmap = QPixmap(get_map(params))
        self.image.setPixmap(self.pixmap)
        self.btn2.setEnabled(True)  # включить кнопку "Найти"

    def move(self, destination):
        if destination == "left":
            my_map.lon -= 0.07  # мне лень искать значения, они нигде не написаны)
        if destination == "down":
            my_map.lat -= 0.07
        if destination == "right":
            my_map.lon += 0.07
        if destination == "up":
            my_map.lat += 0.07
        self.change_z()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
