# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError

from .. import db


class LocForm(FlaskForm):
    address_id = IntegerField('address id:', validators=[DataRequired(message='输入不能为空')])
    submit = SubmitField('Submit')

    def validate_address_id(self, field):
        address_name = db.get_address_name(field.data)

        if not address_name:
            print('error input:{}'.format(field.data))
            raise ValidationError('不存在[id: {}]记录'.format(field.data))
