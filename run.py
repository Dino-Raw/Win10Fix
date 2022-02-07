from main_window import MainWindow
from PyQt5 import QtWidgets
import sys
# auto-py-to-exe


def main():
    # новый экземпляр QApplication
    app = QtWidgets.QApplication(sys.argv)
    # Создаём объект класса ExampleApp
    window = MainWindow()
    # Показываем окно
    window.show()
    # и запускаем приложение
    app.exec_()


# Если мы запускаем файл напрямую, а не импортируем
if __name__ == '__main__':
    # то запускаем функцию main()
    main()
