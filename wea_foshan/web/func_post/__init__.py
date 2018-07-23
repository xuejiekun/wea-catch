# -*- coding: utf-8 -*-
from flask import Blueprint

post_func = Blueprint('post_func', __name__)

from . import view
