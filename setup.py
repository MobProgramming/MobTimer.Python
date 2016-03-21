def create_windows_exe():
    from distutils.core import setup
    import py2exe, sys, os
    from os import listdir
    from os.path import isfile, join
    sys.argv.append('py2exe')

    # Get theme files and store them in a list
    def get_file_paths(folder_name):
        file_paths = [f for f in listdir(folder_name) if isfile(join(folder_name, f))]
        return ['{}/{}'.format(folder_name, i) for i in file_paths]

    [os.remove(x) for x in get_file_paths('dist')]
    theme_file_paths = get_file_paths("Themes")
    tips_file_paths = get_file_paths("Tips")
    image_file_paths = get_file_paths("Images")
    setup(windows=[{
        "script": 'MobTimer.py',
        "icon_resources": [(1, "time-bomb.ico")]
    }]
            , data_files=[
                ('', ["MobTimer.cfg", "company-logo.png", "time-bomb.ico"]),
                ('Themes', theme_file_paths),
                ('Tips', tips_file_paths),
                ('Images', image_file_paths)]
            , requires=['screeninfo'])

def create_mac_app():
    from distutils.core import setup
    import py2app, sys, os
    from os import listdir
    from os.path import isfile, join
    sys.argv.append('py2app')

    # Get theme files and store them in a list
    def get_file_paths(folder_name):
        file_paths = [f for f in listdir(folder_name) if isfile(join(folder_name, f))]
        return ['{}/{}'.format(folder_name, i) for i in file_paths]

    theme_file_paths = get_file_paths("Themes")
    tips_file_paths = get_file_paths("Tips")
    image_file_paths = get_file_paths("Images")
    setup(app=[{
        "script": 'MobTimer.py',
        "icon_resources": [(1, "time-bomb.ico")]
    }]
            , data_files=[
                ('', ["MobTimer.cfg", "company-logo.png", "time-bomb.ico"]),
                ('Themes', theme_file_paths),
                ('Tips', tips_file_paths),
                ('Images', image_file_paths)]
            , requires=['py2app']
            )


import platform
import os
if platform.system() == 'Darwin':
    create_mac_app()
else:
    create_windows_exe()
