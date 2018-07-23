# -*- coding: utf-8 -*-
import os
from flask import render_template, request, make_response, redirect, url_for, session
from . import index

upload_path = os.path.abspath('uploads')
print(upload_path)

@index.route('/')
def main():
    user_agent = request.headers.get('user-agent')
    accept = request.headers.get('accept')

    repo = make_response('user-agent:{}\n'
                         'accept:{}'.format(user_agent, accept))
    repo.set_cookie('answer', '40')

    return render_template('index.html')


@index.route('/test', methods=['GET', 'POST'])
def test():

    if request.method == 'POST' and request.files.get('file'):
        file = request.files.get('file')
        file.save(os.path.join(upload_path, file.filename))
        session['upload'] = True
        return redirect(url_for('.test'))

    if session.get('upload'):
        session['upload'] = False
        return render_template('test.html', upload=True)
    return render_template('test.html', upload=False)
