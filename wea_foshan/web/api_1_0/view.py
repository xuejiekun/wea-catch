# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from flask import jsonify, request

from . import api_1_0
from .. import db
from ..jsoncode import JSONCode
from ...base.model import Address, Dat


# call this api get all address
# ex: http://www.example.com/address
@api_1_0.route('/address')
def address():
    addrs = db.session.query(Address).all()
    if not addrs:
        return jsonify(JSONCode.json_404), 404
    return jsonify({"address":[addr.to_json() for addr in addrs]})


# call this api get one address by id
# ex: http://www.example.com/address/1
@api_1_0.route('/address/<int:id>')
def get_address(id):
    addr = db.session.query(Address).filter(Address.id == id).first()
    if not addr:
        return jsonify(JSONCode.json_404), 404
    return jsonify(addr.to_json())


# call this api get the data by address id
# you can give the datetime arguments
# ex: http://www.example.com/address/1/data
#    http://www.example.com/address/1/data?start=2018061000&end=2018061023
@api_1_0.route('/address/<int:id>/data')
def get_address_data(id):
    addr = db.session.query(Address).filter(Address.id == id).first()
    if not addr:
        return jsonify(JSONCode.json_404), 404

    if request.args.get('start') and request.args.get('end'):
        try:
            start = datetime.strptime(request.args.get('start'), '%Y%m%d%H') - timedelta(hours=1)
            end = datetime.strptime(request.args.get('end'), '%Y%m%d%H')
        except:
            return jsonify(JSONCode.json_400), 400

        dats = addr.dats.filter(Dat.logtime >= start).filter(Dat.logtime <= end).all()
        return jsonify({"data": [dat.to_json() for dat in dats]})

    return jsonify({"data": [dat.to_json() for dat in addr.dats]})


# call this api get all data
# ex: http://www.example.com/data
@api_1_0.route('/data')
def data():
    dats = db.session.query(Dat).all()
    if not dats:
        return jsonify(JSONCode.json_404), 404
    return jsonify({"data":[dat.to_json() for dat in dats]})
