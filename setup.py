from distutils.core import setup
import py2exe, sys, os
from os import listdir
from os.path import isfile, join

sys.argv.append('py2exe')
#Get theme files and store them in a list



def get_file_paths(folder_name):
    file_paths = [f for f in listdir(folder_name) if isfile(join(folder_name, f))]
    return ['{}/{}'.format(folder_name,i) for i in file_paths]


theme_file_paths = get_file_paths("Themes")
tips_file_paths = get_file_paths("Tips")

tcl__path = '{}\\tcl\\tcl8.6\\init.tcl'.format(os.path.dirname(sys.executable))

setup(windows=[{
    "script": 'MobTimer.py',
    "icon_resources": [(1, "time-bomb.ico")]
}]
    , data_files=[
        ('', ["MobTimer.cfg"]),
        ('', ["time-bomb.ico"]),
        ('Themes', theme_file_paths),
        ('Tips', tips_file_paths),
        tcl__path]
    , requires=['screeninfo'])
