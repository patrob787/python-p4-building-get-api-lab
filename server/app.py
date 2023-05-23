#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []

    for bakery in Bakery.query.all():
        bakery_dict = {
            "id": bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at,
            "updated_at": bakery.updated_at
        }
        bakeries.append(bakery_dict)
    
    resp = make_response(bakeries, 200)
    resp.headers['Content-Type'] = 'application/json' 

    return resp

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    bakery_dict = bakery.to_dict()
    resp = make_response(bakery_dict, 200)
    resp.headers['Content-Type'] = 'application/json'
    
    return resp

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    sorted_goods = BakedGood.query.order_by(BakedGood.price).all()

    sorted_dict = [good.to_dict() for good in sorted_goods] 
    resp = make_response(sorted_dict, 200)
    resp.headers['Content-Type'] = 'application/json'

    return resp

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()

    expensive_dict = expensive_good.to_dict()
    resp = make_response(expensive_dict, 200)
    resp.headers["Content-Type"] = 'application/json'
    
    return resp

if __name__ == '__main__':
    app.run(port=555, debug=True)
