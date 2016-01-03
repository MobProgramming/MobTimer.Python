from distutils.core import setup
import py2exe, sys, os
from os import listdir
from os.path import isfile, join

sys.argv.append('py2exe')
#Get theme files and store them in a list
theme_file_paths = [f for f in listdir("Themes") if isfile(join("Themes", f))]
theme_file_paths = ['Themes/{0}'.format(i) for i in theme_file_paths]
tcl__path = '{}\\tcl\\tcl8.6\\init.tcl'.format(os.path.dirname(sys.executable))

setup(windows=[{
    "script": 'MobTimer.py',
    "icon_resources": [(1, "time-bomb.ico")]
}]
    , data_files=[
        ('', ["MobTimer.cfg"]),
        ('', ["time-bomb.ico"]),
        ('Themes', theme_file_paths),
        tcl__path]
    , requires=['screeninfo'])
