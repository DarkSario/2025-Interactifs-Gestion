Scanning from: /home/runner/work/2025-Interactifs-Gestion/2025-Interactifs-Gestion

================================================================================
Row.get() Usage Detection Report
================================================================================

Found 67 potential issues in 16 files

These locations use .get() on variables that might be sqlite3.Row objects.
sqlite3.Row does not have a .get() method and will raise AttributeError.

Recommended fix: Convert to dict using row_to_dict() from src.db.row_utils


📄 dashboard/dashboard.py
--------------------------------------------------------------------------------
  Line 131: row.get(...)
    name = row["name"] if "name" in row else row.get("evenement", "")

📄 modules/buvette.py
--------------------------------------------------------------------------------
  Line 426: item.get(...)
    unite_display = item.get("unite_type", item.get("unite", ""))
  Line 426: item.get(...)
    unite_display = item.get("unite_type", item.get("unite", ""))
  Line 427: item.get(...)
    quantite_display = item.get("quantite", "")
  Line 431: item.get(...)
    iid=item.get("id", 0),
  Line 433: item.get(...)
    item.get("name", ""),
  Line 434: item.get(...)
    item.get("categorie", ""),
  Line 435: item.get(...)
    item.get("stock", 0),
  Line 438: item.get(...)
    item.get("contenance", ""),
  Line 439: item.get(...)
    item.get("commentaire", "")
  Line 493: article.get(...)
    unite_value = article.get("unite_type", article.get("unite", ""))
  Line 493: article.get(...)
    unite_value = article.get("unite_type", article.get("unite", ""))

📄 modules/buvette_bilan_db.py
--------------------------------------------------------------------------------
  Line 85: row_dict.get(...)
    if row_dict and row_dict.get("qte"):
  Line 106: row_dict.get(...)
    return row_dict.get("recette", 0.0) if row_dict else 0.0

📄 modules/buvette_inventaire_dialogs.py
--------------------------------------------------------------------------------
  Line 208: article.get(...)
    article.get("name", ""),
  Line 209: article.get(...)
    article.get("categorie", ""),
  Line 210: article.get(...)
    article.get("contenance", ""),
  Line 483: article.get(...)
    categorie = article.get("categorie", "")
  Line 484: article.get(...)
    contenance = article.get("contenance", "")

📄 modules/depots_retraits_banque.py
--------------------------------------------------------------------------------
  Line 66: row.get(...)
    row.get("reference", ""),
  Line 67: row.get(...)
    row.get("banque", ""),
  Line 68: row.get(...)
    "Oui" if row.get("pointe", 0) else "Non",
  Line 69: row.get(...)
    row.get("commentaire", "")

📄 modules/event_modules.py
--------------------------------------------------------------------------------
  Line 262: res.get(...)
    modele_colonne = res.get("modele_colonne")

📄 modules/members.py
--------------------------------------------------------------------------------
  Line 67: row.get(...)
    row["id"], row["name"], row["prenom"], row["email"], row.get("cotisation", ""),
  Line 68: row.get(...)
    row.get("commentaire", ""), row.get("telephone", ""), row.get("statut", ""),
  Line 68: row.get(...)
    row.get("commentaire", ""), row.get("telephone", ""), row.get("statut", ""),
  Line 68: row.get(...)
    row.get("commentaire", ""), row.get("telephone", ""), row.get("statut", ""),
  Line 69: row.get(...)
    row.get("date_adhesion", "")

📄 modules/stock_db.py
--------------------------------------------------------------------------------
  Line 216: item.get(...)
    article_id = item.get("article_id")
  Line 217: item.get(...)
    new_quantity = item.get("quantite", 0)

📄 modules/stock_inventaire.py
--------------------------------------------------------------------------------
  Line 51: row.get(...)
    self.tree.insert("", "end", values=(row["id"], row["name"], row.get("categorie", ""), row["quantite"], ""))

📄 tests/test_buvette_audit.py
--------------------------------------------------------------------------------
  Line 78: row.get(...)
    row.get('name')
  Line 85: row_dict.get(...)
    self.assertEqual(row_dict.get('name'), 'Test Article 1')
  Line 86: row_dict.get(...)
    self.assertEqual(row_dict.get('categorie'), 'Boissons')
  Line 87: row_dict.get(...)
    self.assertEqual(row_dict.get('stock'), 10)
  Line 88: row_dict.get(...)
    self.assertEqual(row_dict.get('nonexistent', 'default'), 'default')

📄 tests/test_buvette_repository.py
--------------------------------------------------------------------------------
  Line 73: result.get(...)
    self.assertEqual(result.get('name'), 'Test Article 1')
  Line 74: result.get(...)
    self.assertEqual(result.get('categorie'), 'Boissons')
  Line 75: result.get(...)
    self.assertEqual(result.get('stock'), 10)
  Line 78: result.get(...)
    self.assertEqual(result.get('nonexistent_field', 'default'), 'default')
  Line 93: result.get(...)
    self.assertIsNone(result.get('commentaire'))
  Line 94: result.get(...)
    self.assertEqual(result.get('commentaire', 'default'), None)  # NULL is present but None
  Line 97: result.get(...)
    self.assertEqual(result.get('nonexistent', 'default'), 'default')
  Line 137: article.get(...)
    name = article.get('name')
  Line 141: article.get(...)
    self.assertEqual(article.get('nonexistent_field', 'default'), 'default')
  Line 156: article.get(...)
    self.assertEqual(article['name'], article.get('name'))

📄 tests/test_db_api_retry.py
--------------------------------------------------------------------------------
  Line 219: result.get(...)
    assert result.get('name') == 'test1'
  Line 220: result.get(...)
    assert result.get('value') == 100

📄 tests/test_db_row_utils.py
--------------------------------------------------------------------------------
  Line 82: result.get(...)
    self.assertEqual(result.get("name"), "Test Item 2")
  Line 85: result.get(...)
    self.assertIsNone(result.get("optional_field"))
  Line 86: result.get(...)
    self.assertIsNone(result.get("optional_field", "default"))  # Key exists, value is None
  Line 88: result.get(...)
    self.assertEqual(result.get("nonexistent_field", "default"), "default")
  Line 182: row_dict.get(...)
    self.assertEqual(row_dict.get("name"), "Test Item 1")
  Line 183: row_dict.get(...)
    self.assertEqual(row_dict.get("nonexistent", "default"), "default")

📄 tests/test_row_to_dict_conversion.py
--------------------------------------------------------------------------------
  Line 74: row_dict.get(...)
    self.assertEqual(row_dict.get('name'), 'test2')
  Line 77: row_dict.get(...)
    self.assertEqual(row_dict.get('nonexistent', 'default'), 'default')
  Line 80: row_dict.get(...)
    self.assertIsNone(row_dict.get('optional_field'))
  Line 81: row_dict.get(...)
    self.assertEqual(row_dict.get('optional_field', 'default'), None)
  Line 113: row_dict.get(...)
    self.assertEqual(row_dict.get('name'), 'test1')
  Line 139: row.get(...)
    row.get('name')

📄 tests/test_src_row_utils.py
--------------------------------------------------------------------------------
  Line 79: result.get(...)
    self.assertEqual(result.get("name"), "Test Item 2")
  Line 80: result.get(...)
    self.assertIsNone(result.get("optional_field"))
  Line 81: result.get(...)
    self.assertEqual(result.get("nonexistent_field", "default"), "default")

📄 ui/dialogs/base_list_dialog.py
--------------------------------------------------------------------------------
  Line 115: row.get(...)
    item_id = row.get('id', '')
  Line 118: row.get(...)
    value = row.get(col, '')
  Line 257: row.get(...)
    value = row.get(key, default)

================================================================================
Next steps:
  1. Review each location to determine if the variable is a sqlite3.Row
  2. If it is, wrap with row_to_dict(): var = row_to_dict(var)
  3. Or update the source to return dicts from repository methods
  4. Add: from src.db.row_utils import row_to_dict
================================================================================
