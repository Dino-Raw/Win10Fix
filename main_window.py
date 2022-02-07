from functools import partial
from ui_main import *
from service import Service
from app import App
from system import System

# создать из файла service.ui файл service.py для работы с ним
# venv\Scripts\pyuic5.exe service.ui -o service.py


class MainWindow(Ui_MainWindow, Service, App, System):
    # функция для доступа к переменным файла
    def __init__(self):
        super().__init__()
        # инициализация дизайна
        self.setupUi(self)
        # убираем заголовок окна
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.button_exit.clicked.connect(self.close)
        self.button_service.clicked.connect(partial(self.pages.setCurrentWidget, self.page_service))
        self.button_app.clicked.connect(partial(self.pages.setCurrentWidget, self.page_app))
        self.button_system.clicked.connect(partial(self.pages.setCurrentWidget, self.page_system))
        self.button_info.clicked.connect(partial(self.pages.setCurrentWidget, self.page_info))

        # # # # # Управление службами # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        self.service_table.setColumnCount(3)
        # и с service_count количеством строк
        self.service_table.setRowCount(self.service_count)

        # Устанавливаем заголовки таблицы
        self.service_table.setHorizontalHeaderLabels(["Название", "Тип работы", " "])

        # считать список служб с файла
        self.service_list_get()
        # получить информацию о службах
        self.service_status_get()

        # создание кнопок и приввязка к функциям
        self.service_table_create_button()

        # делаем ресайз колонок по содержимому
        self.service_table.resizeColumnsToContents()

        self.service_button_off.clicked.connect(partial(self.service_off))
        self.service_button_on.clicked.connect(partial(self.service_on))

        # # # # # Управление приложениями # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # таблица с 4 колонками
        self.app_table.setColumnCount(3)
        # и с n-ым количеством строк
        self.app_table.setRowCount(self.app_count)

        # Устанавливаем заголовки таблицы
        self.app_table.setHorizontalHeaderLabels(["Название", "Статус", ""])

        # получить информацию о приложениях
        self.app_list_get()
        # получить статус приложений
        self.app_status_get()
        # создать таблицу приложений
        self.app_table_create_button()

        # делаем ресайз колонок по содержимому
        self.app_table.resizeColumnsToContents()

        self.app_button_off.clicked.connect(partial(self.app_off))
        self.app_button_on.clicked.connect(partial(self.app_on))

    # # # # # Управление остальным # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        self.system_table.setColumnCount(3)
        # и с service_count количеством строк
        self.system_table.setRowCount(self.system_count)
        # Устанавливаем заголовки таблицы
        self.system_table.setHorizontalHeaderLabels(["Название", "Статус", "выбор функции"])
        self.system_list_get()
        self.system_table_create()
        self.system_table.resizeColumnsToContents()
        self.system_button_on.clicked.connect(partial(self.system_start, 1))
        self.system_button_off.clicked.connect(partial(self.system_start, 0))

    # # # # # Функции переноса окна # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # вызывается при нажатии кнопки мыши по левой форме
    def mousePressEvent(self, event):
        # Если нажата левая кнопка мыши
        if event.button() == QtCore.Qt.LeftButton:
            # получаем координаты окна относительно экрана
            x = self.geometry().x()
            y = self.geometry().y()
            # получаем координаты курсора относительно окна нашей программы
            cursor_x = QtGui.QCursor.pos().x()
            cursor_y = QtGui.QCursor.pos().y()
            # проверяем условием позицию курсора на нужной области программы
            # если всё ок - перемещаем
            # иначе игнорируем
            if x <= cursor_x <= x + self.geometry().width():
                if y <= cursor_y <= y + self.frame_left_menu.geometry().height():
                    self.old_pos = event.pos()
                else:
                    self.old_pos = None
        elif event.button() == QtCore.Qt.RightButton:
            self.old_pos = None

    # вызывается при отпускании кнопки мыши
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = None

    # вызывается всякий раз, когда мышь перемещается
    def mouseMoveEvent(self, event):
        if not self.old_pos:
            return

        self.move(self.pos() + event.pos() - self.old_pos)
