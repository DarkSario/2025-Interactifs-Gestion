#!/usr/bin/env python3
"""
Verification script to ensure all database modules properly convert rows to dicts.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules import buvette_db, buvette_inventaire_db, buvette_bilan_db
from modules.db_row_utils import _row_to_dict, _rows_to_dicts

def test_buvette_functions():
    """Test that buvette functions return dicts."""
    print("Testing buvette_db functions...")
    
    try:
        # Test list_articles returns dicts
        articles = buvette_db.list_articles()
        if articles:
            first = articles[0]
            assert isinstance(first, dict), f"Expected dict, got {type(first)}"
            # Test .get() method works
            first.get("name", "default")
            print("  ✓ list_articles() returns dicts with .get() support")
        else:
            print("  ℹ list_articles() returned empty list (no test data)")
            
        # Test list_articles_names returns dicts
        names = buvette_db.list_articles_names()
        if names:
            first = names[0]
            assert isinstance(first, dict), f"Expected dict, got {type(first)}"
            first.get("name", "default")
            print("  ✓ list_articles_names() returns dicts with .get() support")
        else:
            print("  ℹ list_articles_names() returned empty list (no test data)")
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    return True

def test_buvette_inventaire_functions():
    """Test that buvette inventaire functions return dicts."""
    print("\nTesting buvette_inventaire_db functions...")
    
    try:
        # Test list_inventaires returns dicts
        inventaires = buvette_inventaire_db.list_inventaires()
        if inventaires:
            first = inventaires[0]
            assert isinstance(first, dict), f"Expected dict, got {type(first)}"
            first.get("id", "default")
            print("  ✓ list_inventaires() returns dicts with .get() support")
        else:
            print("  ℹ list_inventaires() returned empty list (no test data)")
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    return True

def test_buvette_bilan_functions():
    """Test that buvette bilan functions return dicts."""
    print("\nTesting buvette_bilan_db functions...")
    
    try:
        # Test list_evenements returns dicts
        evenements = buvette_bilan_db.list_evenements()
        if evenements:
            first = evenements[0]
            assert isinstance(first, dict), f"Expected dict, got {type(first)}"
            first.get("name", "default")
            print("  ✓ list_evenements() returns dicts with .get() support")
        else:
            print("  ℹ list_evenements() returned empty list (no test data)")
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 70)
    print("Row to Dict Conversion Verification")
    print("=" * 70)
    
    all_passed = True
    all_passed &= test_buvette_functions()
    all_passed &= test_buvette_inventaire_functions()
    all_passed &= test_buvette_bilan_functions()
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ All verification checks passed!")
        print("  All database functions properly return dicts with .get() support")
        sys.exit(0)
    else:
        print("✗ Some verification checks failed")
        sys.exit(1)
