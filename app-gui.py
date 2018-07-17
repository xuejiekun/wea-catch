# -*- coding:utf-8 -*-
from sky.ui.ui import run_gui
from config import Config

if __name__ == '__main__':
    cf = Config(current=True)
    cf.set_reload(True)
    run_gui(cf)
