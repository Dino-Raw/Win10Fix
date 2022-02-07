import subprocess
import codecs
import psutil
import os
from winreg import *
from ui_main import *

# создать из файла service.ui файл service.py для работы с ним
# venv\Scripts\pyuic5.exe service.ui -o service.py


class System(QtWidgets.QMainWindow):
    # функция для доступа к переменным файла
    def __init__(self):
        super().__init__()
        self.st_inf = subprocess.STARTUPINFO()
        self.st_inf.dwFlags = self.st_inf.dwFlags | subprocess.STARTF_USESHOWWINDOW
        self.system_count = int(9)
        self.system_list = []
        self.reg_path = {
            "volumetric_objects": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FolderDescriptions\{31C0DD25-9439-4F12-BF41-7FF4EDA38722}\PropertyBag",
            "ttl": r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
            "win_def_1": r"SYSTEM\CurrentControlSet\Services\wscsvc",
            "win_def_2": r"SYSTEM\CurrentControlSet\Services\SecurityHealthService",
            "delay_start": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Serialize",
            "telemetry": r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
            "cortana": r"SOFTWARE\Policies\Microsoft\Windows\Windows Search",
            "UAC": r"Software\Microsoft\Windows\CurrentVersion\policies\system"
        }
        self.reg_key = {
            "volumetric_objects": "ThisPCPolicy",
            "ttl": "DefaultTTL",
            "win_def": "Start",
            "delay_start": "StartupDelayInMSec",
            "telemetry": "AllowTelemetry",
            "cortana": "AllowCortana",
            "UAC": "EnableLUA"
        }

    def system_list_get(self):
        with codecs.open(os.getcwd() + r'\data\system_name.txt', 'r', "utf_8_sig") as system_file:
            for line in system_file:
                self.system_list.append(line.replace('\n', ''))
        system_file.close()

    # создание кнопок и приввязка к функциям
    def system_table_create(self):
        # заполнение списков кнопок
        for i in range(self.system_count):
            self.system_table.setItem(i, 0, QtWidgets.QTableWidgetItem(self.system_list[i]))
            if i != 0:
                self.system_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str("True")))
            self.system_table.setCellWidget(i, 2, QtWidgets.QCheckBox("Select"))
            self.system_table.cellWidget(i, 2).setStyleSheet(
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

        try:
            if self.get_reg(self.reg_path["volumetric_objects"], self.reg_key["volumetric_objects"]) == "Hide":
                self.system_table.setItem(1, 1, QtWidgets.QTableWidgetItem(str("False")))
        except:
            #self.volumetric_objects("Show")
            self.system_table.setItem(1, 1, QtWidgets.QTableWidgetItem(str("True")))

        try:
            self.system_table.setItem(2, 1, QtWidgets.QTableWidgetItem(str(self.get_reg(self.reg_path["ttl"], self.reg_key["ttl"]))))
        except:
            self.set_reg(self.reg_path["ttl"], self.reg_key["ttl"], REG_DWORD, int(self.find_item("ping 127.0.0.1 -n 1", "TTL=")))
            self.system_table.setItem(2, 1, QtWidgets.QTableWidgetItem(str(self.get_reg(self.reg_path["ttl"], self.reg_key["ttl"]))))

        try:
            if self.get_reg(self.reg_path["win_def_1"], self.reg_key["win_def"]) == 4 and self.get_reg(self.reg_path["win_def_2"], self.reg_key["win_def"]) == 4:
                self.system_table.setItem(3, 1, QtWidgets.QTableWidgetItem("False"))
        except:
            #self.win_def(2)
            self.system_table.setItem(3, 1, QtWidgets.QTableWidgetItem("True"))

        try:
            if self.get_reg(self.reg_path["delay_start"], self.reg_key["delay_start"]) == 0:
                self.system_table.setItem(4, 1, QtWidgets.QTableWidgetItem(str("False")))
        except:
            #self.delay_start(1)
            self.system_table.setItem(4, 1, QtWidgets.QTableWidgetItem(str("True")))

        try:
            if self.get_reg(self.reg_path["telemetry"], self.reg_key["telemetry"]) == 0:
                self.system_table.setItem(5, 1, QtWidgets.QTableWidgetItem("False"))
        except:
            #self.telemetry(1)
            self.system_table.setItem(5, 1, QtWidgets.QTableWidgetItem("True"))

        try:
            if self.get_reg(self.reg_path["cortana"], self.reg_key["cortana"]) == 0:
                self.system_table.setItem(6, 1, QtWidgets.QTableWidgetItem("False"))
        except:
            #self.cortana(1)
            self.system_table.setItem(6, 1, QtWidgets.QTableWidgetItem("True"))

        if psutil.win_service_get("WSearch").start_type() == "disabled":
            self.system_table.setItem(7, 1, QtWidgets.QTableWidgetItem(str("False")))

        try:
            if self.get_reg(self.reg_path["UAC"], self.reg_key["UAC"]) == 0:
                self.system_table.setItem(8, 1, QtWidgets.QTableWidgetItem(str("False")))
        except:
            #self.uac(1)
            self.system_table.setItem(8, 1, QtWidgets.QTableWidgetItem(str("True")))

    def system_start(self, type):
        for i in range(self.system_count):
            if self.system_table.cellWidget(i, 2).checkState():
                if type:
                    self.system_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str("True")))
                else:
                    self.system_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str("False")))
                if i == 0:
                    self.one_drive(type)
                elif i == 1:
                    if type:
                        self.volumetric_objects("Show")
                    else:
                        self.volumetric_objects("Hide")
                elif i == 2:
                    if type:
                        self.ttl(1)
                    else:
                        self.ttl(-1)
                    self.system_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.get_reg(self.reg_path["ttl"], self.reg_key["ttl"]))))
                elif i == 3:
                    if type:
                        self.win_def(2)
                    else:
                        self.win_def(4)
                elif i == 4:
                    self.delay_start(type)
                elif i == 5:
                    self.telemetry(type)
                elif i == 6:
                    self.cortana(type)
                elif i == 7:
                    self.disk_index(type)
                elif i == 8:
                    self.uac(type)

    def one_drive(self, value):
        if value:
            subprocess.run(["powershell.exe", "cd $Env:SystemRoot\SysWOW64\;", ".\OneDriveSetup.exe"], startupinfo=self.st_inf)
        else:
            subprocess.run(['powershell.exe', "taskkill /f /im OneDrive.exe;",
                            "cd $Env:SystemRoot\SysWOW64\;", ".\OneDriveSetup.exe /uninstall"], startupinfo=self.st_inf)

    def volumetric_objects(self, value):
        self.set_reg(self.reg_path["volumetric_objects"], self.reg_key["volumetric_objects"], REG_SZ, value)

    def ttl(self, one):
        self.set_reg(self.reg_path["ttl"], self.reg_key["ttl"], REG_DWORD, self.get_reg(self.reg_path["ttl"], self.reg_key["ttl"]) + 1 * one)

    def win_def(self, value):
        self.set_reg(self.reg_path["win_def_1"], self.reg_key["win_def"], REG_DWORD, value)
        self.set_reg(self.reg_path["win_def_2"], self.reg_key["win_def"], REG_DWORD, value)

    def delay_start(self, value):
        self.set_reg(self.reg_path["delay_start"], self.reg_key["delay_start"], REG_DWORD, value)

    def telemetry(self, value):
        self.set_reg(self.reg_path["telemetry"], self.reg_key["telemetry"], REG_DWORD, value)
        if value:
            subprocess.run(['powershell.exe',
                            "Get-Service DiagTrack | where {$_.StartType -ne \'automatic\'} | Set-Service -StartupType automatic;",
                            "Get-Service dmwappushservice | where {$_.StartType -ne \'automatic\'} | Set-Service -StartupType automatic"], startupinfo=self.st_inf)
        else:
            subprocess.run(['powershell.exe',
                            "Get-Service DiagTrack | where {$_.Status -ne \'stopped\'} | Stop-Service -force;",
                            "Get-Service DiagTrack | where {$_.StartType -ne \'disabled\'} | Set-Service -StartupType disabled;",
                            "Get-Service dmwappushservice | where {$_.Status -ne \'stopped\'} | Stop-Service -force;",
                            "Get-Service dmwappushservice | where {$_.StartType -ne \'disabled\'} | Set-Service -StartupType disabled"], startupinfo=self.st_inf)

    def cortana(self, value):
        self.set_reg(self.reg_path["cortana"], self.reg_key["cortana"], REG_DWORD, value)

    def disk_index(self, value):
        if value:
            subprocess.run(['powershell.exe',
                            "Get-Service WSearch | where {$_.StartType -ne \'automatic\'} | Set-Service -StartupType automatic"], startupinfo=self.st_inf)
        else:
            subprocess.run(['powershell.exe',
                            "Get-Service WSearch | where {$_.Status -ne \'stopped\'} | Stop-Service -force;",
                            "Get-Service WSearch | where {$_.StartType -ne \'disabled\'} | Set-Service -StartupType disabled"], startupinfo=self.st_inf)

    def uac(self, value):
        self.set_reg(self.reg_path["UAC"], self.reg_key["UAC"], REG_DWORD, value)

    def set_reg(self, reg_path, name, type_reg, value):
        CreateKey(HKEY_LOCAL_MACHINE, reg_path)
        registry_key = OpenKey(HKEY_LOCAL_MACHINE, reg_path, 0, KEY_WRITE)
        SetValueEx(registry_key, name, 0, type_reg, value)
        CloseKey(registry_key)

    def get_reg(self, reg_path, name):
        registry_key = OpenKey(HKEY_LOCAL_MACHINE, reg_path, 0, KEY_READ)
        value, regtype = QueryValueEx(registry_key, name)
        CloseKey(registry_key)
        return value

    def find_item(self, chek_str, skip_str):
        data = subprocess.check_output(['powershell.exe', chek_str], universal_newlines=True, startupinfo=self.st_inf)
        key = ""
        find_key = data.find(skip_str) + len(skip_str)
        while True:
            if data[find_key] != '\n':
                key += str(data[find_key])
                find_key += 1
            else:
                break
        return key

    def check_item(self, chek_str, item):
        data = subprocess.check_output(['powershell.exe', chek_str], universal_newlines=True, startupinfo=self.st_inf)
        return data.find(item)
