# -*- coding:utf-8 -*-
import os
from flask import Flask
from flask_bootstrap import Bootstrap

from ..base.dataorm import DataManager

bootstrap = Bootstrap()

base_url = os.path.abspath(r'data.db')
print(base_url)
db = DataManager('sqlite:///{}'.format(base_url))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hard to guess string'
    bootstrap.init_app(app)

    from .func_time import time_func
    app.register_blueprint(time_func)

    from .func_post import post_func
    app.register_blueprint(post_func)

    from .func_loc import loc_func
    app.register_blueprint(loc_func)

    from .api_1_0 import api_1_0
    app.register_blueprint(api_1_0, url_prefix='/api/1.0')

    from .func import func
    app.register_blueprint(func)

    from .index import index
    app.register_blueprint(index)

    return app
