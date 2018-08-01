# -*- coding:utf-8 -*-
from wea_foshan.gui.ui import run_gui
from config import Config


if __name__ == '__main__':
    cf = Config()
    cf.set_reload(False)
    cf.set_overwrite(True)
    run_gui(cf)
