from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(windows=['MobTimer.py'], data_files=['C:\\Python34\\tcl\\tcl8.6\\init.tcl'])