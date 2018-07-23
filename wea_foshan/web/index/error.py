# -*- coding:utf-8 -*-
from flask import render_template
from . import index

@index.app_errorhandler(404)
def handle_404(e):
    return render_template('404.html'), 404
