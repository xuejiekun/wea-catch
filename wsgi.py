import sys
import os
import inspect

current_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
sys.path.insert(0, current_dir)

from manage import app as application
