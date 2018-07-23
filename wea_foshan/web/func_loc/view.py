# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for

from . import loc_func
from .form import LocForm
from .. import db
from ...base.model import Address, Dat


@loc_func.route('/query_loc', methods=['GET', 'POST'])
def query_loc():
    form = LocForm()

    if form.validate_on_submit():
        session['address_id'] = form.address_id.data
        form.address_id.data = ''
        return redirect(url_for('.show_loc'))
    return render_template('query_loc.html', form=form)


@loc_func.route('/show_loc')
def show_loc():
    addr = db.session.query(Address).filter(Address.id == session.get('address_id')).first()
    return render_template('show_loc.html', addr=addr)
