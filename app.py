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

@app.route('/')
def index():
    '''Show full inventory'''
    return render_template('index.html', inventory=inventory.find())

@app.route('/inventory/add')
def item_add():
    '''Add new item to inventory'''
    title = "Add Item"
    return render_template('item_add.html', title=title, inventory={})

@app.route('/inventory', methods=['POST'])
def inventory_submit():
    '''Submit new item to inventory'''
    item = {
        'name': request.form.get('name'),
        "price": request.form.get('price'),
        'category': request.form.get('category'),
        'ig_id': request.form.get('ig_id')
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
        'ig_id': request.form.get('ig_id')
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))