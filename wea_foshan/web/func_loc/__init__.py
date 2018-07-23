# -*- coding: utf-8 -*-
from flask import Blueprint

loc_func = Blueprint('loc_func', __name__)

from . import view
