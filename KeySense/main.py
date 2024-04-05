# Authors: Liam Arguedas <iliamftw2013@gmail.com>
# License: BSD 3 clause

import os
import sys
from KeySense import KeyboardSense

if __name__ == "__main__":

    config_name = 'Script.yml'

    if getattr(sys, 'frozen', False):

        application_path = os.path.dirname(sys.executable)
    
    elif __file__:
    
        application_path = os.path.dirname(__file__)

    config_path = os.path.join(application_path, config_name)

    keyboard = KeyboardSense(scripts_path=config_path)
    keyboard.listener()
