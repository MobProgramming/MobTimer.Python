from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(windows=[{
    "script": 'MobTimer.py',
    "icon_resources": [(1, "time-bomb.ico")]
}]
    , data_files=[('', ["MobTimer.cfg"]), 'C:\\Python34\\tcl\\tcl8.6\\init.tcl']
    , requires=['screeninfo'])
