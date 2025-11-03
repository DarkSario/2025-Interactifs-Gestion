# Database Access TODOs
Generated: 2025-11-03T17:45:52.846234

This report lists action items for fixing database access issues.

## 🔴 CRITICAL: Fix row.get() Usage
Priority: **HIGH** - These will cause AttributeError crashes

Action: Convert sqlite3.Row to dict before using .get()
Solution: Use `_row_to_dict(row)` or `_rows_to_dicts(rows)` from modules/db_row_utils.py

- [ ] dashboard/dashboard.py:131
  ```python
  name = row["name"] if "name" in row else row.get("evenement", "")
  ```

- [ ] utils/db_helpers.py:26
  ```python
  >>> value = row_dict.get('optional_column', 'default')
  ```

- [ ] scripts/analyze_modules_columns_old.py:112
  ```python
  # Recherche de références dictionary-style (row["column"], row.get("column"))
  ```

- [ ] scripts/analyze_modules_columns_old.py:135
  ```python
  """Extrait les références dictionary-style (row["column"], row.get("column"))."""
  ```

- [ ] scripts/analyze_modules_columns_old.py:147
  ```python
  # Pattern pour row.get("column") ou row.get('column')
  ```

- [ ] scripts/analyze_modules_columns_old.py:147
  ```python
  # Pattern pour row.get("column") ou row.get('column')
  ```

- [ ] scripts/audit_db_usage.py:78
  ```python
  # Pattern: row.get( or row.get('
  ```

- [ ] scripts/replace_row_get.py:14
  ```python
  - row.get('column')
  ```

- [ ] scripts/replace_row_get.py:15
  ```python
  - result.get('field', default)
  ```

- [ ] scripts/replace_row_get.py:16
  ```python
  - item.get('key')
  ```

- [ ] ui/dialogs/base_list_dialog.py:115
  ```python
  item_id = row.get('id', '')
  ```

- [ ] tests/test_db_api_retry.py:219
  ```python
  assert result.get('name') == 'test1'
  ```

- [ ] tests/test_db_api_retry.py:220
  ```python
  assert result.get('value') == 100
  ```

- [ ] tests/test_row_to_dict_conversion.py:74
  ```python
  self.assertEqual(row_dict.get('name'), 'test2')
  ```

- [ ] tests/test_row_to_dict_conversion.py:77
  ```python
  self.assertEqual(row_dict.get('nonexistent', 'default'), 'default')
  ```

- [ ] tests/test_row_to_dict_conversion.py:80
  ```python
  self.assertIsNone(row_dict.get('optional_field'))
  ```

- [ ] tests/test_row_to_dict_conversion.py:81
  ```python
  self.assertEqual(row_dict.get('optional_field', 'default'), None)
  ```

- [ ] tests/test_row_to_dict_conversion.py:113
  ```python
  self.assertEqual(row_dict.get('name'), 'test1')
  ```

- [ ] tests/test_row_to_dict_conversion.py:139
  ```python
  row.get('name')
  ```

- [ ] tests/test_src_row_utils.py:79
  ```python
  self.assertEqual(result.get("name"), "Test Item 2")
  ```

- [ ] tests/test_src_row_utils.py:80
  ```python
  self.assertIsNone(result.get("optional_field"))
  ```

- [ ] tests/test_src_row_utils.py:81
  ```python
  self.assertEqual(result.get("nonexistent_field", "default"), "default")
  ```

- [ ] tests/test_db_row_utils.py:82
  ```python
  self.assertEqual(result.get("name"), "Test Item 2")
  ```

- [ ] tests/test_db_row_utils.py:85
  ```python
  self.assertIsNone(result.get("optional_field"))
  ```

- [ ] tests/test_db_row_utils.py:86
  ```python
  self.assertIsNone(result.get("optional_field", "default"))  # Key exists, value is None
  ```

- [ ] tests/test_db_row_utils.py:88
  ```python
  self.assertEqual(result.get("nonexistent_field", "default"), "default")
  ```

- [ ] tests/test_db_row_utils.py:182
  ```python
  self.assertEqual(row_dict.get("name"), "Test Item 1")
  ```

- [ ] tests/test_db_row_utils.py:183
  ```python
  self.assertEqual(row_dict.get("nonexistent", "default"), "default")
  ```

- [ ] src/db/row_utils.py:9
  ```python
  This causes AttributeError when code tries to use row.get('column', default).
  ```

- [ ] src/db/row_utils.py:23
  ```python
  >>> value = row_dict.get('optional_column', 'default')
  ```

- [ ] src/db/row_utils.py:47
  ```python
  >>> value = row_dict.get('optional_column', 'default')
  ```

- [ ] modules/event_modules.py:262
  ```python
  modele_colonne = res.get("modele_colonne")
  ```

- [ ] modules/stock_db.py:216
  ```python
  article_id = item.get("article_id")
  ```

- [ ] modules/stock_db.py:217
  ```python
  new_quantity = item.get("quantite", 0)
  ```

- [ ] modules/stock_inventaire.py:51
  ```python
  self.tree.insert("", "end", values=(row["id"], row["name"], row.get("categorie", ""), row["quantite"], ""))
  ```

- [ ] modules/depots_retraits_banque.py:66
  ```python
  row.get("reference", ""),
  ```

- [ ] modules/depots_retraits_banque.py:67
  ```python
  row.get("banque", ""),
  ```

- [ ] modules/depots_retraits_banque.py:68
  ```python
  "Oui" if row.get("pointe", 0) else "Non",
  ```

- [ ] modules/depots_retraits_banque.py:69
  ```python
  row.get("commentaire", "")
  ```

- [ ] modules/members.py:67
  ```python
  row["id"], row["name"], row["prenom"], row["email"], row.get("cotisation", ""),
  ```

- [ ] modules/members.py:68
  ```python
  row.get("commentaire", ""), row.get("telephone", ""), row.get("statut", ""),
  ```

- [ ] modules/members.py:68
  ```python
  row.get("commentaire", ""), row.get("telephone", ""), row.get("statut", ""),
  ```

- [ ] modules/members.py:68
  ```python
  row.get("commentaire", ""), row.get("telephone", ""), row.get("statut", ""),
  ```

- [ ] modules/members.py:69
  ```python
  row.get("date_adhesion", "")
  ```

- [ ] modules/buvette_bilan_db.py:85
  ```python
  if row_dict and row_dict.get("qte"):
  ```

- [ ] modules/buvette_bilan_db.py:106
  ```python
  return row_dict.get("recette", 0.0) if row_dict else 0.0
  ```

- [ ] modules/buvette.py:426
  ```python
  unite_display = item.get("unite_type", item.get("unite", ""))
  ```

- [ ] modules/buvette.py:426
  ```python
  unite_display = item.get("unite_type", item.get("unite", ""))
  ```

- [ ] modules/buvette.py:427
  ```python
  quantite_display = item.get("quantite", "")
  ```

- [ ] modules/buvette.py:431
  ```python
  iid=item.get("id", 0),
  ```

- [ ] modules/buvette.py:433
  ```python
  item.get("name", ""),
  ```

- [ ] modules/buvette.py:434
  ```python
  item.get("categorie", ""),
  ```

- [ ] modules/buvette.py:435
  ```python
  item.get("stock", 0),
  ```

- [ ] modules/buvette.py:438
  ```python
  item.get("contenance", ""),
  ```

- [ ] modules/buvette.py:439
  ```python
  item.get("commentaire", "")
  ```

- [ ] modules/db_row_utils.py:39
  ```python
  >>> value = row_dict.get('optional_column', 'default')
  ```

## 🟡 RECOMMENDED: Standardize Connection Handling
Priority: **MEDIUM** - Should use centralized connection management

Action: Use db.get_connection() or modules.db_api.get_connection() instead of direct sqlite3.connect()
Benefit: Automatic WAL mode, busy timeout, and consistent error handling

- [ ] db/db.py:39
  ```python
  conn = sqlite3.connect(_db_file, timeout=5, detect_types=sqlite3.PARSE_DECLTYPES)
  ```

- [ ] scripts/migrate_articles_unite_to_quantite.py:29
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] scripts/update_db_structure_old.py:840
  ```python
  conn = sqlite3.connect(self.db_path, timeout=30)
  ```

- [ ] scripts/audit_db_usage.py:117
  ```python
  # Pattern: sqlite3.connect(
  ```

- [ ] scripts/audit_db_usage.py:173
  ```python
  report.append(f"- sqlite3.connect() calls: {len(self.results['connection_patterns'])}\n")
  ```

- [ ] scripts/audit_db_usage.py:274
  ```python
  report.append("\nAction: Use db.get_connection() or modules.db_api.get_connection() instead of direct sqlite3.connect()\n")
  ```

- [ ] scripts/audit_db_usage.py:337
  ```python
  print(f"  - Direct sqlite3.connect() calls: {len(auditor.results['connection_patterns'])}")
  ```

- [ ] scripts/migration.py:62
  ```python
  conn = sqlite3.connect(DB_PATH)
  ```

- [ ] scripts/enable_wal.py:46
  ```python
  conn = sqlite3.connect(db_path, timeout=DEFAULT_TIMEOUT)
  ```

- [ ] scripts/update_db_structure.py:906
  ```python
  conn = sqlite3.connect(self.db_path, timeout=30)
  ```

- [ ] scripts/db_diagnostics.py:87
  ```python
  conn = sqlite3.connect(self.db_path, timeout=5)
  ```

- [ ] scripts/db_diagnostics.py:110
  ```python
  conn = sqlite3.connect(self.db_path, timeout=5)
  ```

- [ ] scripts/db_diagnostics.py:132
  ```python
  conn = sqlite3.connect(self.db_path, timeout=5)
  ```

- [ ] scripts/db_diagnostics.py:188
  ```python
  conn = sqlite3.connect(self.db_path, timeout=5)
  ```

- [ ] scripts/db_diagnostics.py:212
  ```python
  conn = sqlite3.connect(self.db_path, timeout=5)
  ```

- [ ] scripts/migrate_add_purchase_price.py:95
  ```python
  conn = sqlite3.connect(db_path, timeout=DEFAULT_TIMEOUT)
  ```

- [ ] scripts/replace_sqlite_connect.py:1
  ```python
  """AST-based replacer: replace sqlite3.connect(...) with get_connection(...)
  ```

- [ ] scripts/replace_sqlite_connect.py:28
  ```python
  # match sqlite3.connect(...)
  ```

- [ ] scripts/create_compat_views.py:18
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_inventory_lines_loader.py:21
  ```python
  self.conn = sqlite3.connect(self.db_path)
  ```

- [ ] tests/test_inventory_lines_loader.py:113
  ```python
  conn = sqlite3.connect(self.db_path)
  ```

- [ ] tests/test_inventory_lines_loader.py:146
  ```python
  conn = sqlite3.connect(self.db_path)
  ```

- [ ] tests/test_articles_unite_migration.py:30
  ```python
  conn = sqlite3.connect(db_file)
  ```

- [ ] tests/test_db_api_retry.py:30
  ```python
  conn = sqlite3.connect(path)
  ```

- [ ] tests/test_row_to_dict_conversion.py:21
  ```python
  self.conn = sqlite3.connect(self.db_path)
  ```

- [ ] tests/test_delete_inventaire.py:17
  ```python
  conn = sqlite3.connect(str(dbfile))
  ```

- [ ] tests/test_delete_inventaire.py:62
  ```python
  conn3 = sqlite3.connect(str(dbfile))
  ```

- [ ] tests/test_buvette_inventaire.py:16
  ```python
  conn = sqlite3.connect(db_file)
  ```

- [ ] tests/test_buvette_stock.py:22
  ```python
  conn = sqlite3.connect(db_file)
  ```

- [ ] tests/test_stock_buvette_tab.py:26
  ```python
  conn = sqlite3.connect(db_file)
  ```

- [ ] tests/test_database_migration.py:19
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_database_migration.py:123
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_database_migration.py:146
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_database_migration.py:181
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_database_migration.py:221
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_database_migration.py:233
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_database_migration.py:273
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_database_migration.py:298
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_buvette_purchase_price.py:18
  ```python
  conn = sqlite3.connect(db_file)
  ```

- [ ] tests/test_src_row_utils.py:21
  ```python
  self.conn = sqlite3.connect(self.db_path)
  ```

- [ ] tests/test_analyze_modules.py:128
  ```python
  conn = sqlite3.connect("test.db")
  ```

- [ ] tests/test_analyze_modules.py:133
  ```python
  conn = sqlite3.connect("test.db")
  ```

- [ ] tests/test_smart_migration.py:20
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_smart_migration.py:97
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_smart_migration.py:168
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_smart_migration.py:196
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_smart_migration.py:260
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_smart_migration.py:280
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_smart_migration.py:311
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_db_row_utils.py:20
  ```python
  self.conn = sqlite3.connect(self.db_path)
  ```

- [ ] tests/test_stock_journal.py:27
  ```python
  conn = sqlite3.connect(db_file)
  ```

- [ ] tests/test_startup_schema_check.py:47
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] tests/test_startup_schema_check.py:158
  ```python
  conn = sqlite3.connect(db_path)
  ```

- [ ] src/db/compat.py:36
  ```python
  _conn = sqlite3.connect(p, timeout=5, detect_types=sqlite3.PARSE_DECLTYPES)
  ```

- [ ] src/db/connection.py:46
  ```python
  conn = sqlite3.connect(
  ```

- [ ] modules/db_api.py:51
  ```python
  conn = sqlite3.connect(
  ```

## 🟢 LOW PRIORITY: Review Fetch Patterns
These files use fetch patterns but don't show .get() usage in this scan.
Review to ensure they don't need dict conversion.
- [ ] db/db.py
- [ ] dialogs/depense_dialog.py
- [ ] dialogs/edit_don_dialog.py
- [ ] dialogs/edit_event_dialog.py
- [ ] dialogs/edit_field_dialog.py
- [ ] dialogs/edit_journal_dialog.py
- [ ] dialogs/edit_member_dialog.py
- [ ] dialogs/edit_module_data_dialog.py
- [ ] dialogs/edit_module_dialog.py
- [ ] dialogs/edit_stock_dialog.py
- [ ] lib/db_articles.py
- [ ] main.py
- [ ] modules/buvette_bilan_dialogs.py
- [ ] modules/buvette_db.py
- [ ] modules/buvette_inventaire_db.py
- [ ] modules/buvette_inventaire_dialogs.py
- [ ] modules/buvette_mouvements_db.py
- [ ] modules/categories.py
- [ ] modules/db_api.py
- [ ] modules/depenses_diverses.py
- [ ] modules/depenses_regulieres.py
- [ ] modules/dons_subventions.py
- [ ] modules/event_caisse_details.py
- [ ] modules/event_caisses.py
- [ ] modules/event_depenses.py
- [ ] modules/event_module_data.py
- [ ] modules/event_module_fields.py
- [ ] modules/event_payments.py
- [ ] modules/event_recettes.py
- [ ] modules/events.py
- [ ] modules/exports.py
- [ ] modules/fournisseurs.py
- [ ] modules/historique_clotures.py
- [ ] modules/historique_inventaire.py
- [ ] modules/inventaire.py
- [ ] modules/journal.py
- [ ] modules/model_colonnes.py
- [ ] modules/retrocessions_ecoles.py
- [ ] modules/solde_ouverture.py
- [ ] modules/stock.py
- [ ] modules/stock_tab.py
- [ ] scripts/auto_fix_buvette_rows.py
- [ ] scripts/create_compat_views.py
- [ ] scripts/db_diagnostics.py
- [ ] scripts/enable_wal.py
- [ ] scripts/migrate_add_purchase_price.py
- [ ] scripts/migrate_articles_unite_to_quantite.py
- [ ] scripts/migration.py
- [ ] scripts/update_db_structure.py
- [ ] scripts/update_db_structure_old.py
- [ ] src/db/repository.py
- [ ] src/services/inventory_service.py
- [ ] tests/test_analyze_modules.py
- [ ] tests/test_articles_unite_migration.py
- [ ] tests/test_buvette_inventaire.py
- [ ] tests/test_buvette_purchase_price.py
- [ ] tests/test_buvette_stock.py
- [ ] tests/test_connection.py
- [ ] tests/test_database_migration.py
- [ ] tests/test_db_locking.py
- [ ] tests/test_delete_inventaire.py
- [ ] tests/test_inventory_integration.py
- [ ] tests/test_smart_migration.py
- [ ] tests/test_stock_journal.py
- [ ] ui/startup_schema_check.py
- [ ] utils/cloture_exercice.py
- [ ] utils/db_operations.py
