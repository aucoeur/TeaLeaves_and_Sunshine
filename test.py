from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_item_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_item = {
    'name': 'Grape',
    'price': '5.21',
    'category': 'fresh',
}

sample_form_data = {
    'name': sample_item['name'],
    'price': sample_item['price'],
    'category': sample_item['category']
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

if __name__ == '__main__':
    unittest_main()