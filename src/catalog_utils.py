"""
OKF Google Repo - Knowledge Catalog Utilities
A collection of helper functions for managing knowledge catalog entries.
"""

import json
import os
from datetime import datetime


def load_catalog(filepath: str) -> dict:
    """Load a knowledge catalog from a JSON file."""
    if not os.path.exists(filepath):
        return {"entries": [], "metadata": {"created": datetime.now().isoformat()}}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_catalog(catalog: dict, filepath: str) -> None:
    """Save the knowledge catalog to a JSON file."""
    catalog["metadata"]["updated"] = datetime.now().isoformat()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)


def add_entry(catalog: dict, title: str, description: str, tags: list = None) -> dict:
    """Add a new entry to the knowledge catalog."""
    entry = {
        "id": len(catalog["entries"]) + 1,
        "title": title,
        "description": description,
        "tags": tags or [],
        "created_at": datetime.now().isoformat(),
    }
    catalog["entries"].append(entry)
    return entry


def search_entries(catalog: dict, query: str) -> list:
    """Search catalog entries by title or description."""
    query_lower = query.lower()
    return [
        entry
        for entry in catalog["entries"]
        if query_lower in entry["title"].lower()
        or query_lower in entry["description"].lower()
    ]


def get_statistics(catalog: dict) -> dict:
    """Get statistics about the knowledge catalog."""
    entries = catalog.get("entries", [])
    all_tags = [tag for entry in entries for tag in entry.get("tags", [])]
    return {
        "total_entries": len(entries),
        "unique_tags": len(set(all_tags)),
        "most_common_tags": _get_top_tags(all_tags, n=5),
    }


def _get_top_tags(tags: list, n: int = 5) -> list:
    """Get the top N most common tags."""
    tag_counts = {}
    for tag in tags:
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    return [{"tag": tag, "count": count} for tag, count in sorted_tags[:n]]


if __name__ == "__main__":
    # Demo usage
    catalog = load_catalog("catalog.json")
    add_entry(catalog, "Python Basics", "Introduction to Python programming", ["python", "beginner"])
    add_entry(catalog, "Machine Learning", "Overview of ML concepts", ["ml", "ai", "data-science"])
    add_entry(catalog, "Web Development", "Modern web dev practices", ["web", "javascript", "html"])
    save_catalog(catalog, "catalog.json")
    print(f"Catalog stats: {get_statistics(catalog)}")
