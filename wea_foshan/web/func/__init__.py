# -*- coding: utf-8 -*-
from flask import Blueprint

func = Blueprint('func', __name__)

from . import view
