import subprocess
from shutil import copy, copytree, rmtree

rmtree('./dist')
py_installer_command = 'pyinstaller --clean --onefile --windowed MobTimer.spec'.split(" ")

# Run py installer
subprocess.run(py_installer_command)

# Copy files MobTimer.spec and TimeBomb icon into dist/ directory


copy('./MobTimer.cfg', './dist/MobTimer.cfg')
copy('./time-bomb.ico', './dist/time-bomb.ico')
copytree('./Themes', './dist/Themes')
copytree('./Tips', './dist/Tips')
copytree('./Images', './dist/Images')
