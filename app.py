from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/papernoms')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
inventory = db.inventory
carts = db.carts

inventory.drop()
inventory.insert_many([
    {"name": "Persimmon", "category": "fresh", "price": 3.24, "image": "static/img/fresh/persimmon.jpg"},
    {"name": "Artichoke", "category": "fresh", "price": 4.24, "image": "static/img/fresh/artichoke.jpg"},
    {"name": "Dragonfruit", "category": "fresh", "price": 7.26, "image": "static/img/fresh/dragonfruit.jpg"},
    {"name": "Orange", "category": "fresh", "price": 1.54, "image": "static/img/fresh/orange.jpg"},
    {"name": "Avocado", "category": "fresh", "price": 2.24, "image": "static/img/fresh/avocado.jpg"},
    {"name": "Watermelon", "category": "fresh", "price": 5.36, "image": "static/img/fresh/watermelon.jpg"},
    {"name": "Lobster", "category": "prepped", "price": 25.48, "image": "static/img/fresh/lobster.jpg"},
    {"name": "Paella", "category": "prepped", "price": 14.56, "image": "static/img/fresh/paella.jpg"},
    {"name": "Farfalle Alfredo", "category": "prepped", "price": 12.74, "image": "static/img/fresh/pasta.jpg"},
    {"name": "Pizza", "category": "fresh", "price": 9.96, "image": "static/img/fresh/pizza.jpg"},
    {"name": "Taco", "category": "fresh", "price": 2.15, "image": "static/img/fresh/avocado.jpg"}
    ])

@app.route('/')
def index():
    '''Show full inventory'''
    return render_template('index.html', inventory=inventory.find())

@app.route('/inventory/add')
def item_add():
    '''Add new item to cart'''
    title = "Add Item"
    return render_template('item_add.html', title=title, inventory={})

@app.route('/inventory', methods=['POST'])
def inventory_submit():
    '''Submit new item to inventory'''
    item = {
        'name': request.form.get('name'),
        "price": request.form.get('price'),
        'category': request.form.get('category')
    }

    item_id = inventory.insert_one(item).inserted_id
    return redirect(url_for('item_show', item_id=item_id))

@app.route('/inventory/<item_id>')
def item_show(item_id):
    '''Show single item'''
    item = inventory.find_one({'_id': ObjectId(item_id)})
    return render_template('item.html', item=item)

@app.route('/inventory/<item_id>/edit')
def item_edit(item_id):
    '''Show edit form for an item'''
    title = "Edit Item"
    item = inventory.find_one({'_id': ObjectId(item_id)})
    return render_template('item_edit.html', title=title, item=item)

@app.route('/inventory/<item_id>', methods=['POST'])
def item_update(item_id):
    '''Submit an edited item'''
    updated_item = {
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'category': request.form.get('category')
    }

    inventory.update_one(
        {'_id': ObjectId(item_id)},
        {'$set': updated_item})

    return redirect(url_for('item_show', item_id=item_id))

@app.route('/inventory/<item_id>/delete', methods=['POST'])
def item_delete(item_id):
    '''Delete item'''
    inventory.delete_one({'_id': ObjectId(item_id)})

    return redirect(url_for('index'))

@app.route('/cart')
def cart_show():
    '''Show cart'''  
    cart = carts.find()

    cart_items = list(cart.find({}))
    total_price = 0
    for i in range(len(cart_items)):
        total_price += cart_items[i]["price"]*cart_items[i]["quantity"]

    return render_template('cart.html', cart=cart, total_price=total_price)

# @app.route('/cart/add', methods=['POST'])
# def cart_submit():
#     '''Submit new item to cart'''
#     item = {
#         '_id': request.form.get('item_id'),
#         'name': request.form.get('name'),
#         "price": request.form.get('price'),
#         'quantity': request.form.get('quantity'),
#     }
#     cart_item = cart.find_one({'_id': ObjectId(item.id)})

#     quant = int(item.quantity)

#     if item._id == cart_item:
#         cart.update_one(
#             { '_id': ObjectId(item.id) },
#             { '$inc': { 'quantity': quant } }
#             )
#     else:
#         cart_id = cart.insert_one(item).inserted_id

#     return redirect(url_for('cart_show', cart_id=cart_item))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))