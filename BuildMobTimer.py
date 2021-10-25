import os

import subprocess
from shutil import copy, copytree, make_archive, rmtree
import time

dist_path = './dist'
rmtree(dist_path)
py_installer_command = 'pyinstaller --clean --onefile --windowed MobTimer.spec'.split(" ")

subprocess.run(py_installer_command)

copy('./MobTimer.cfg', './dist/MobTimer.cfg')
copy('./time-bomb.ico', './dist/time-bomb.ico')
copytree('./Themes', './dist/Themes')
copytree('./Tips', './dist/Tips')
copytree('./Images', './dist/Images')

time_for_filename = time.strftime("%Y%m%d-%H%M%S")
output_filename = 'MobTimer' + time_for_filename

builds_path = './builds/'
if not os.path.exists(builds_path):
    os.makedirs(builds_path)

make_archive(builds_path + output_filename, 'zip', dist_path)
