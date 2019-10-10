from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_item_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_item = {
    'name': 'Grape',
    'price': '5.21',
    'category': 'fresh',
    'quantity': None
}

sample_form_data = {
    'name': sample_item['name'],
    'price': sample_item['price'],
    'category': sample_item['category'],
    'quantity': sample_item['quantity'],
}

class InventoryTests(TestCase):
    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
    
    def test_index(self):
        """Test the inventory homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
    
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_item(self, mock_find):
        """Test showing a single item."""
        mock_find.return_value = sample_item

        result = self.client.get(f'/inventory/{sample_item_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Grape', result.data)
    
    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_item(self, mock_insert):
        """Test submitting a new item."""
        result = self.client.post('/inventory', data=sample_form_data)

        # After submitting, should redirect to that playlist's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_item)

if __name__ == '__main__':
    unittest_main()