# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, request

from . import post_func
from .form import NameForm


@post_func.route('/form_flask', methods=['GET', 'POST'])
def form_flask():
    form = NameForm()
    print(form.name())

    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('.post_flask'))

    return render_template('form_flask.html', form=form)


@post_func.route('/post_flask')
def post_flask():
    return render_template('post_flask.html', name=session.get('name'))


###
# normal post
###
@post_func.route('/form_normal')
def form_normal():
    return render_template('form_normal.html')


@post_func.route('/post_normal', methods=['GET', 'POST'])
def post_normal():
    if request.form.get('name'):
        session['name'] = request.form.get('name')
        return redirect(url_for('.post_normal'))

    return render_template('post_normal.html', name=session.get('name'))
