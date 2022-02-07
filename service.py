import subprocess
import psutil
import os
from ui_main import *

# создать из файла service.ui файл service.py для работы с ним
# venv\Scripts\pyuic5.exe service.ui -o service.py


class Service(QtWidgets.QMainWindow):
    # функция для доступа к переменным файла
    def __init__(self):
        super().__init__()
        self.service_count = int(29)
        # список с данными о службах
        self.service_list = []
        # выбранные службы
        self.service_list_check = []
        self.st_inf = subprocess.STARTUPINFO()
        self.st_inf.dwFlags = self.st_inf.dwFlags | subprocess.STARTF_USESHOWWINDOW

    def service_list_get(self):
        self.service_list.clear()
        with open(os.getcwd() + r'\data\service.txt', 'r') as service_file:
            for line in service_file:
                self.service_list.append(psutil.win_service_get(line.replace('\n', '')))
        service_file.close()

# создание кнопок и приввязка к функциям
    def service_table_create_button(self):
        for i in range(self.service_count):
            self.service_table.setItem(i, 0, QtWidgets.QTableWidgetItem(self.service_list[i].display_name()))
            self.service_table.setCellWidget(i, 2, QtWidgets.QCheckBox("Select"))
            self.service_table.cellWidget(i, 2).setStyleSheet(
                "QCheckBox::indicator"
                "{"
                    "background-color: rgb(33, 37, 42);"
                "}"
                "QCheckBox::indicator:checked"
                "{"
                    "border: 3px solid rgb(33, 37, 42);"
                    "background-color: rgba(255, 121, 198, 255);"
                "}"

            )

    # получить данные о службах
    def service_status_get(self):
        self.service_list_check.clear()
        for i in range(self.service_count):
            # вывод информации по сервисам
            self.service_table.setItem(i, 1, QtWidgets.QTableWidgetItem(self.service_list[i].start_type()))

    def service_on(self):
        for i in range(self.service_count):
            if self.service_table.cellWidget(i, 2).checkState() and (self.service_table.item(i, 1).text() == 'manual' or self.service_table.item(i, 1).text() == 'disabled'):
                self.service_list_check.append(self.service_list[i].name())
        if self.service_list_check:
            subprocess.run(['powershell.exe', 'Get-Service ' + ', '.join(self.service_list_check), " | where {$_.StartType -ne 'automatic'} | Set-Service -StartupType automatic"], startupinfo=self.st_inf)
        self.service_status_get()
    
    # отключение служб
    def service_off(self):
        for i in range(self.service_count):
            if self.service_table.cellWidget(i, 2).checkState() and (self.service_table.item(i, 1).text() == 'manual' or self.service_table.item(i, 1).text() == 'automatic'):
                self.service_list_check.append(self.service_list[i].name())
        if self.service_list_check:
            subprocess.run(['powershell.exe', 'Get-Service ' + ', '.join(self.service_list_check),
                            " | where {$_.Status -ne 'stopped'} | Stop-Service -force;",
                            'Get-Service ' + ', '.join(self.service_list_check),
                            " | where {$_.StartType -ne 'disabled'} | Set-Service -StartupType disabled"], startupinfo=self.st_inf)
        self.service_status_get()
