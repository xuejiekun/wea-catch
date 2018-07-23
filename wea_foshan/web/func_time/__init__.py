# -*- coding: utf-8 -*-
from flask import Blueprint

time_func = Blueprint('time_func', __name__)

from . import view
