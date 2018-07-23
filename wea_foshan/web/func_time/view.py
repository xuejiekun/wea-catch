# -*- coding: utf-8 -*-
import time
from flask import render_template
from . import time_func


@time_func.route('/time')
def get_time():
    return render_template('time.html', time=int(time.time()*1000))
