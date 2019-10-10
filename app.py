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

inventory.drop()
cart.drop()

inventory.insert_many([
    {"name": "Persimmon", "category": "fresh", "price": 3.24, "image": "static/img/fresh/persimmon.jpg", "quantity": 100},
    {"name": "Artichoke", "category": "fresh", "price": 4.24, "image": "static/img/fresh/artichoke.jpg", "quantity": 100},
    {"name": "Dragonfruit", "category": "fresh", "price": 7.26, "image": "static/img/fresh/dragonfruit.jpg", "quantity": 100},
    {"name": "Orange", "category": "fresh", "price": 1.54, "image": "static/img/fresh/orange.jpg", "quantity": 100},
    {"name": "Avocado", "category": "fresh", "price": 2.24, "image": "static/img/fresh/avocado.jpg", "quantity": 100},
    {"name": "Watermelon", "category": "fresh", "price": 5.36, "image": "static/img/fresh/watermelon.jpg", "quantity": 100},
    {"name": "Lobster", "category": "prepped", "price": 25.48, "image": "static/img/prepped/lobster.jpg", "quantity": 100},
    {"name": "Paella", "category": "prepped", "price": 14.56, "image": "static/img/prepped/paella.jpg", "quantity": 100},
    {"name": "Farfalle Alfredo", "category": "prepped", "price": 12.74, "image": "static/img/prepped/pasta.jpg", "quantity": 100},
    {"name": "Pizza", "category": "fresh", "price": 9.96, "image": "static/img/prepped/pizza.jpg", "quantity": 100},
    {"name": "Taco", "category": "fresh", "price": 2.15, "image": "static/img/prepped/taco.jpg", "quantity": 100}
    ])

@app.route('/')
def show_inventory():
    """Show all inventory."""
    # This will display all inventory by looping through the database
    return render_template('index.html', inventory=inventory.find())

@app.route('/admin')
def show_admin():
    """Show inventory on admin."""
    # This will display all inventory by looping through the database
    return render_template('admin.html', inventory=inventory.find())

@app.route('/cart')
def show_cart():
    """Show cart."""
    carts = cart.find()
    # This will display all inventory by looping through the database
    # total_price = list(cart.find({}))
    # total = 0
    # for i in range(len(total_price)):
    #     total += total_price[i]["price"]*total_price[i]["quantity"]

    return render_template('cart.html', cart=carts)

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
        'category': request.form.get('category'),
        'image': request.form.get('image')
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
        'category': request.form.get('category'),
        'image': request.form.get('image')
    }

    inventory.update_one(
        {'_id': ObjectId(item_id)},
        {'$set': updated_item})

    return redirect(url_for('item_show', item_id=item_id))

@app.route('/inventory/<item_id>/delete', methods=['POST'])
def item_delete(item_id):
    '''Delete item'''
    inventory.delete_one({'_id': ObjectId(item_id)})

    return redirect(url_for('show_admin'))

@app.route('/cart', methods=['POST'])
def add_to_cart():
    '''Submit new item to cart'''
    item = {
        'name': request.form.get('name'),
        "price": request.form.get('price'),
        'category': request.form.get('category')
        # 'quantity': request.form.get('quantity')
    }

    add_item = cart.insert_one(item).inserted_id
    return redirect(url_for('show_cart', add_item=add_item))

@app.route('/cart/<item_id>/delete', methods=['POST'])
def remove_from_cart(item_id):
    '''Remove item from cart'''
    cart.delete_one({'_id': ObjectId(item_id)})

    return redirect(url_for('show_cart'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))