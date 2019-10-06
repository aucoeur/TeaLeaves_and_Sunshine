from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/3dgenerates')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
inventory = db.inventory

@app.route('/')
def index():
    '''Show full inventory'''
    return render_template('index.html', inventory=inventory.find())

@app.route('inventory/add')
def inventory_add():
    '''Add new item to inventory'''
    return render_template('item_add.html', inventory={})

@app.route('/inventory', methods=['POST'])
def inventory_submit():
    '''Submit new item to inventory'''
    item = {
        'item_name': request.form.get('item_name'),
        'description': request.form.get('description')
    }

    item_id = inventory.insert_one(item).inserted_id
    return redirect(url_for('inventory_show', item_id=item_id))

@app.route('/inventory/<item_id>')
def item_show(item_id):
    '''Show single item'''
    item = inventory.find_one({'_id': ObjectId(item_id)})
    return render_template('item.html', item=item)


@app.route('/inventory/<item_id>/edit')
def item_edit(item_id):
    '''Show edit form for an item'''
    item = inventory.find_one({'_id': ObjectId(item_id)})
    return render_template('item_edit.html', item=item)

@app.route('/inventory/<item_id>', methods=['POST'])
def item_update(item_id):
    '''Submit an edited item'''
    updated_item = {
        'item_name': request.form.get('item_name'),
        'description': request.form.get('description')
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