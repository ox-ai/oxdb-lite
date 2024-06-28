import unittest
import shutil
import os
from ox_db.oxd.d import OxDoc  


class TestOxDoc(unittest.TestCase):
    def setUp(self):
        """Set up a temporary directory for testing."""
        self.test_dir = "test_oxdoc"
        self.doc = OxDoc(self.test_dir)
        self.doc.load_index()

    def tearDown(self):
        """Clean up the temporary directory after tests."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_set_and_get(self):
        """Test setting and getting a value."""
        self.doc.set("test_key", {"field": "value"})
        result = self.doc.get("test_key")
        self.assertEqual(result, {"field": "value"})

    def test_update_value(self):
        """Test updating an existing value."""
        self.doc.set("test_key", {"field": "value"})
        self.doc.set("test_key", {"field": "new_value"})
        result = self.doc.get("test_key")
        self.assertEqual(result, {"field": "new_value"})

    def test_delete_value(self):
        """Test deleting a value."""
        self.doc.set("test_key", {"field": "value"})
        self.doc.delete("test_key")
        result = self.doc.get("test_key")
        self.assertIsNone(result)

    def test_add_multiple_values(self):
        """Test adding multiple values at once."""
        data = {
            "key1": {"field": "value1"},
            "key2": {"field": "value2"},
        }
        self.doc.add(data)
        result1 = self.doc.get("key1")
        result2 = self.doc.get("key2")
        self.assertEqual(result1, {"field": "value1"})
        self.assertEqual(result2, {"field": "value2"})

    def test_compact(self):
        """Test compacting the file."""
        self.doc.set("key1", {"field": "value1"})
        self.doc.set("key2", {"field": "value2"})
        self.doc.delete("key1")
        self.doc.compact()
        result = self.doc.get("key2")
        self.assertEqual(result, {"field": "value2"})
        self.assertIsNone(self.doc.get("key1"))

    def test_free_list_reuse(self):
        """Test that free list space is reused."""
        self.doc.set("key1", {"field": "value1"})
        self.doc.delete("key1")
        self.doc.set("key2", {"field": "value2"})
        result = self.doc.get("key2")
        self.assertEqual(result, {"field": "value2"})

    def test_load_data(self):
        """Test loading all data."""
        data = {
            "key1": {"field": "value1"},
            "key2": {"field": "value2"},
        }
        self.doc.add(data)
        loaded_data = self.doc.load_data()
        self.assertEqual(loaded_data["key1"], {"field": "value1"})
        self.assertEqual(loaded_data["key2"], {"field": "value2"})

if __name__ == '__main__':
    unittest.main()
