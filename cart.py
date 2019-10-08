from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/papernoms')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
inventory = db.inventory
cart = db.cart

@app.route('/cart')
def show_cart():
    '''Show cart'''
    
    return render_template('cart.html')

@app.route('/cart/add', methods=['POST'])
def item_to_cart():
    '''Add new item to cart'''
    item = {
        'item_id': request.form.get('item_id'),
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'quantity': request.form.get('quantity')
    }

    cart_id = cart.insert_one(item).inserted_id
    
    cart.update_one(
        {'_id': ObjectId(cart_id)},
        {'$set': item})

    return redirect(url_for('show_cart'))

@app.route('/cart/<cart_id>')
def cart_unique():
    pass