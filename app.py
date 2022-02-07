import subprocess
import codecs
import os
from ui_main import *

# создать из файла service.ui файл service.py для работы с ним
# venv\Scripts\pyuic5.exe service.ui -o service.py


class App(QtWidgets.QMainWindow):
    # функция для доступа к переменным файла
    def __init__(self):
        super().__init__()
        self.app_count = int(36)
        self.app_list_name = []
        self.app_list = []
        self.st_inf = subprocess.STARTUPINFO()
        self.st_inf.dwFlags = self.st_inf.dwFlags | subprocess.STARTF_USESHOWWINDOW

    def app_list_get(self):
        # считать названия приложений
        with open(os.getcwd() + r'\data\apps.txt', 'r') as app_file:
            for line in app_file:
                self.app_list.append(line.replace('\n', ''))
        app_file.close()

        # считать имена приложений
        with codecs.open(os.getcwd() + r'\data\apps_name.txt', 'r', "utf_8_sig") as app_file:
            for line in app_file:
                self.app_list_name.append(line.replace('\n', ''))
        app_file.close()

    def app_table_create_button(self):
        for i in range(self.app_count):
            self.app_table.setItem(i, 0, QtWidgets.QTableWidgetItem(self.app_list_name[i]))
            self.app_table.setCellWidget(i, 2, QtWidgets.QCheckBox("Select"))
            self.app_table.cellWidget(i, 2).setStyleSheet(
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

        # узнать статус приложений

    def app_status_get(self):
        subprocess.run(['powershell.exe',
                        "Get-AppxPackage | Select Name | Format-List | Out-File -Encoding \"UTF8\" data\\apps_user.txt"], startupinfo=self.st_inf)

        # узнать какие приложения установлены
        app_user = []
        with open(os.getcwd() + r'\data\apps_user.txt', 'r') as app_file:
            for line in app_file:
                if line != '\n' and 'Microsoft' in line:
                    line = line.replace('Name : ', '')
                    app_user.append(line.replace('\n', ''))
            app_file.close()

        # указать в программе какие приложения установлены из тех, что можно удалить
        for i in range(self.app_count):
            self.app_table.setItem(i, 1, QtWidgets.QTableWidgetItem("False"))
            for j in range(len(app_user)):
                if str(self.app_list[i]) in str(app_user[j]):
                    self.app_table.setItem(i, 1, QtWidgets.QTableWidgetItem("True"))
                    break

    def app_on(self):
        app_on_str = ''
        for i in range(self.app_count):
            if self.app_table.cellWidget(i, 2).checkState() and self.app_table.item(i, 1).text() == 'False':
                app_on_str += "Add-AppxPackage -Register \"C:\Program Files\\WindowsApps\\*" + str(self.app_list[i]) + \
                              "*\\AppxManifest.xml\" -DisableDevelopmentMode; "
                self.app_table.setItem(i, 1, QtWidgets.QTableWidgetItem("True"))
        if app_on_str:
            subprocess.Popen(['powershell.exe', app_on_str], startupinfo=self.st_inf)

    def app_off(self):
        app_off_str = ''
        for i in range(self.app_count):
            if self.app_table.cellWidget(i, 2).checkState() and self.app_table.item(i, 1).text() == 'True':
                app_off_str += "Get-AppXPackage *" + self.app_list[i] + "* | Remove-AppxPackage; "
                self.app_table.setItem(i, 1, QtWidgets.QTableWidgetItem("False"))

        if app_off_str:
            subprocess.Popen(['powershell.exe', app_off_str], startupinfo=self.st_inf)
