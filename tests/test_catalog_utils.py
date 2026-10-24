"""
Unit tests for the Knowledge Catalog utilities.
"""

import unittest
import os
import json
import tempfile
from src.catalog_utils import load_catalog, save_catalog, add_entry, search_entries, get_statistics


class TestCatalogUtils(unittest.TestCase):
    """Test cases for catalog_utils module."""

    def setUp(self):
        """Create a temporary file for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_catalog.json")

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_catalog_new(self):
        """Test loading a catalog when file doesn't exist."""
        catalog = load_catalog(self.test_file)
        self.assertIn("entries", catalog)
        self.assertIn("metadata", catalog)
        self.assertEqual(len(catalog["entries"]), 0)

    def test_add_entry(self):
        """Test adding an entry to the catalog."""
        catalog = load_catalog(self.test_file)
        entry = add_entry(catalog, "Test Title", "Test Description", ["test"])
        self.assertEqual(entry["title"], "Test Title")
        self.assertEqual(entry["id"], 1)
        self.assertEqual(len(catalog["entries"]), 1)

    def test_search_entries(self):
        """Test searching entries by title."""
        catalog = load_catalog(self.test_file)
        add_entry(catalog, "Python Guide", "Learn Python", ["python"])
        add_entry(catalog, "Java Guide", "Learn Java", ["java"])
        results = search_entries(catalog, "Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Python Guide")

    def test_search_entries_by_description(self):
        """Test searching entries by description."""
        catalog = load_catalog(self.test_file)
        add_entry(catalog, "Topic A", "Deep learning fundamentals", ["ml"])
        add_entry(catalog, "Topic B", "Web development basics", ["web"])
        results = search_entries(catalog, "deep learning")
        self.assertEqual(len(results), 1)

    def test_save_and_load(self):
        """Test saving and reloading a catalog."""
        catalog = load_catalog(self.test_file)
        add_entry(catalog, "Saved Entry", "Persisted data", ["save"])
        save_catalog(catalog, self.test_file)
        reloaded = load_catalog(self.test_file)
        self.assertEqual(len(reloaded["entries"]), 1)
        self.assertEqual(reloaded["entries"][0]["title"], "Saved Entry")

    def test_get_statistics(self):
        """Test catalog statistics."""
        catalog = load_catalog(self.test_file)
        add_entry(catalog, "Entry 1", "Desc 1", ["python", "beginner"])
        add_entry(catalog, "Entry 2", "Desc 2", ["python", "advanced"])
        add_entry(catalog, "Entry 3", "Desc 3", ["java"])
        stats = get_statistics(catalog)
        self.assertEqual(stats["total_entries"], 3)
        self.assertEqual(stats["unique_tags"], 4)

    def test_empty_search(self):
        """Test search with no results."""
        catalog = load_catalog(self.test_file)
        add_entry(catalog, "Only Entry", "Some description", ["tag"])
        results = search_entries(catalog, "nonexistent")
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()
