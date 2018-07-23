# -*- coding: utf-8 -*-
from flask import render_template, abort

from ...base.model import Address, Dat

from . import func
from .. import db


@func.route('/address')
def address():
    addrs = db.session.query(Address).all()
    return render_template('address.html', addrs=addrs)


@func.route('/address/<int:id>')
def get_address(id):
    addr = db.session.query(Address).filter(Address.id == id).first()
    if not addr:
        abort(404)
    # if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
    #     return jsonify(addr.to_json())

    return '<h1>{}</h1>' \
           '<h2>{}</h2>'.format(addr.name, addr.eng_name)
