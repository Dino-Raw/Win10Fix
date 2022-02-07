from cx_Freeze import setup, Executable
import sys
import os

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [Executable('run.py', base=base, icon="ico/raw.png")]

excludes = ['']


zip_include_packages = ['subprocess', 'PyQt5', 'sys', 'encodings', 'codecs', 'psutil', 'winreg', 'codecs', 'functools', 'os']
include_files = [(os.getcwd() + r'\data')]
packages = ['ui_main', 'service', 'app', 'system', 'main_window']

options = {
    'build_exe': {
        'include_msvcr': True,
        'excludes': excludes,
        'packages': packages,
        'zip_include_packages': zip_include_packages,
        'build_exe': './/build_windows',
        'include_files': include_files,
    }
}

setup(name='W10Fix',
      version='0.0.10',
      description='',
      executables=executables,
      options=options)