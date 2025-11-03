# SQL Access Map
Generated: 2025-11-03T17:45:52.845553
This report maps all database access patterns in the codebase.

## Summary
- sqlite3 imports: 41
- get_connection() calls: 193
- fetch patterns: 278
- row.get() usage: 56
- Positional indexing: 171
- execute() calls: 654
- sqlite3.connect() calls: 56

## SQLite3 Imports
- `db/db.py:12`
- `utils/db_operations.py:13`
- `scripts/migrate_articles_unite_to_quantite.py:8`
- `scripts/update_db_structure_old.py:21`
- `scripts/audit_db_usage.py:51`
- `scripts/migration.py:10`
- `scripts/enable_wal.py:14`
- `scripts/update_db_structure.py:21`
- `scripts/db_diagnostics.py:22`
- `scripts/migrate_add_purchase_price.py:14`
- `scripts/create_compat_views.py:11`
- `init_db.py:1`
- `lib/db_articles.py:20`
- `ui/startup_schema_check.py:17`
- `tests/test_inventory_lines_loader.py:8`
- `tests/test_articles_unite_migration.py:13`
- `tests/test_db_api_retry.py:7`
- `tests/test_row_to_dict_conversion.py:9`
- `tests/test_delete_inventaire.py:2`
- `tests/test_buvette_inventaire.py:2`
- `tests/test_buvette_stock.py:12`
- `tests/test_stock_buvette_tab.py:11`
- `tests/test_database_migration.py:7`
- `tests/test_buvette_purchase_price.py:12`
- `tests/test_src_row_utils.py:9`
- `tests/test_analyze_modules.py:125`
- `tests/test_smart_migration.py:7`
- `tests/test_db_row_utils.py:8`
- `tests/test_stock_journal.py:12`
- `tests/test_startup_schema_check.py:7`
- `src/db/repository.py:14`
- `src/db/compat.py:33`
- `src/db/row_utils.py:26`
- `src/db/connection.py:13`
- `dialogs/depense_dialog.py:2`
- `modules/buvette_db.py:27`
- `modules/db_api.py:15`
- `modules/buvette_mouvements_db.py:13`
- `modules/buvette_bilan_db.py:13`
- `modules/db_row_utils.py:18`
- `modules/buvette_bilan_dialogs.py:4`

## get_connection() Calls

### dashboard/dashboard.py
- Line 102: `conn = get_connection()`

### db/db.py
- Line 32: `def get_connection():`
- Line 75: `conn = get_connection()`
- Line 279: `conn = get_connection()`
- Line 652: `conn = get_connection()`
- Line 667: `conn = get_connection()`
- Line 688: `conn = get_connection()`

### dialogs/cloture_confirm_dialog.py
- Line 20: `conn = get_connection()`

### dialogs/depense_dialog.py
- Line 153: `conn = get_connection()`
- Line 227: `conn = get_connection()`

### dialogs/edit_don_dialog.py
- Line 54: `conn = get_connection()`
- Line 89: `conn = get_connection()`

### dialogs/edit_event_dialog.py
- Line 55: `conn = get_connection()`
- Line 85: `conn = get_connection()`

### dialogs/edit_field_dialog.py
- Line 35: `conn = get_connection()`
- Line 53: `conn = get_connection()`
- Line 70: `conn = get_connection()`
- Line 97: `conn = get_connection()`

### dialogs/edit_journal_dialog.py
- Line 59: `conn = get_connection()`
- Line 100: `conn = get_connection()`

### dialogs/edit_member_dialog.py
- Line 59: `conn = get_connection()`
- Line 95: `conn = get_connection()`

### dialogs/edit_module_data_dialog.py
- Line 15: `conn = get_connection()`
- Line 28: `conn = get_connection()`
- Line 91: `conn = get_connection()`
- Line 109: `conn = get_connection()`

### dialogs/edit_module_dialog.py
- Line 31: `conn = get_connection()`
- Line 47: `conn = get_connection()`

### dialogs/edit_stock_dialog.py
- Line 57: `conn = get_connection()`
- Line 67: `conn = get_connection()`
- Line 113: `conn = get_connection()`

### init_db.py
- Line 104: `conn = get_connection()`

### lib/db_articles.py
- Line 76: `Uses the unified db.get_connection() to ensure WAL mode and busy_timeout.`
- Line 77: `Row factory is already set to sqlite3.Row by get_connection().`
- Line 83: `conn = get_connection()`

### main.py
- Line 62: `conn = get_connection()`
- Line 76: `conn = get_connection()`
- Line 117: `conn = get_connection()`
- Line 199: `conn = get_connection()`

### modules/buvette_bilan_db.py
- Line 18: `conn = get_connection()`

### modules/buvette_bilan_dialogs.py
- Line 7: `conn = get_connection()`

### modules/buvette_db.py
- Line 36: `conn = get_connection()`

### modules/buvette_inventaire_db.py
- Line 24: `conn = get_connection()`

### modules/buvette_mouvements_db.py
- Line 18: `conn = get_connection()`

### modules/categories.py
- Line 42: `conn = get_connection()`
- Line 71: `conn = get_connection()`
- Line 91: `conn = get_connection()`
- Line 109: `conn = get_connection()`
- Line 129: `conn = get_connection()`

### modules/cloture_exercice.py
- Line 64: `conn = get_connection()`

### modules/db_api.py
- Line 43: `>>> conn = get_connection()`
- Line 100: `conn = get_connection()`
- Line 156: `conn = get_connection()`
- Line 204: `>>> conn = get_connection()`
- Line 210: `conn = get_connection()`
- Line 252: `conn = get_connection()`
- Line 328: `conn = get_connection()`

### modules/depenses_diverses.py
- Line 44: `conn = get_connection()`
- Line 50: `conn = get_connection()`
- Line 56: `conn = get_connection()`
- Line 123: `conn = get_connection()`
- Line 132: `conn = get_connection()`

### modules/depenses_regulieres.py
- Line 44: `conn = get_connection()`
- Line 50: `conn = get_connection()`
- Line 56: `conn = get_connection()`
- Line 123: `conn = get_connection()`
- Line 132: `conn = get_connection()`

### modules/depots_retraits_banque.py
- Line 50: `df = pd.read_sql_query(query, get_connection(), params=(banque,))`
- Line 111: `conn = get_connection()`
- Line 141: `conn = get_connection()`
- Line 153: `conn = get_connection()`

### modules/dons_subventions.py
- Line 44: `conn = get_connection()`
- Line 54: `conn = get_connection()`
- Line 110: `conn = get_connection()`

### modules/event_caisse_details.py
- Line 39: `conn = get_connection()`
- Line 76: `conn = get_connection()`
- Line 121: `conn = get_connection()`
- Line 151: `conn = get_connection()`

### modules/event_caisses.py
- Line 38: `conn = get_connection()`
- Line 80: `conn = get_connection()`
- Line 118: `conn = get_connection()`
- Line 144: `conn = get_connection()`

### modules/event_depenses.py
- Line 41: `conn = get_connection()`
- Line 86: `conn = get_connection()`
- Line 133: `conn = get_connection()`
- Line 165: `conn = get_connection()`

### modules/event_module_data.py
- Line 39: `conn = get_connection()`
- Line 68: `conn = get_connection()`
- Line 93: `conn = get_connection()`
- Line 103: `conn = get_connection()`
- Line 118: `conn = get_connection()`
- Line 137: `conn = get_connection()`

### modules/event_module_fields.py
- Line 48: `conn = get_connection()`
- Line 93: `conn = get_connection()`
- Line 106: `conn = get_connection()`
- Line 119: `conn = get_connection()`

### modules/event_modules.py
- Line 66: `conn = get_connection()`
- Line 85: `conn = get_connection()`
- Line 105: `conn = get_connection()`
- Line 121: `conn = get_connection()`
- Line 204: `conn = get_connection()`
- Line 232: `conn = get_connection()`
- Line 250: `conn = get_connection()`
- Line 265: `conn = get_connection()`
- Line 287: `conn = get_connection()`
- Line 339: `conn = get_connection()`
- Line 356: `conn = get_connection()`
- Line 367: `conn = get_connection()`
- Line 393: `conn = get_connection()`
- Line 427: `conn = get_connection()`
- Line 483: `conn = get_connection()`
- Line 497: `conn = get_connection()`
- Line 538: `conn = get_connection()`
- Line 560: `conn = get_connection()`
- Line 598: `conn = get_connection()`

### modules/event_payments.py
- Line 38: `conn = get_connection()`
- Line 74: `conn = get_connection()`
- Line 123: `conn = get_connection()`
- Line 154: `conn = get_connection()`

### modules/event_recettes.py
- Line 12: `conn = get_connection()`
- Line 68: `conn = get_connection()`
- Line 103: `conn = get_connection()`
- Line 166: `conn = get_connection()`
- Line 178: `conn = get_connection()`
- Line 215: `conn = get_connection()`
- Line 232: `conn = get_connection()`
- Line 265: `conn = get_connection()`

### modules/events.py
- Line 81: `conn = get_connection()`
- Line 133: `conn = get_connection()`
- Line 208: `conn = get_connection()`
- Line 231: `conn = get_connection()`

### modules/exports.py
- Line 9: `conn = get_connection()`
- Line 212: `conn = get_connection()`
- Line 312: `conn = get_connection()`
- Line 375: `conn = get_connection()`
- Line 440: `conn = get_connection()`

### modules/fournisseurs.py
- Line 36: `conn = get_connection()`
- Line 53: `conn = get_connection()`
- Line 76: `conn = get_connection()`
- Line 98: `conn = get_connection()`
- Line 106: `conn = get_connection()`
- Line 125: `conn = get_connection()`

### modules/historique_clotures.py
- Line 34: `conn = get_connection()`
- Line 51: `conn = get_connection()`
- Line 61: `conn = get_connection()`
- Line 69: `conn = get_connection()`
- Line 81: `conn = get_connection()`

### modules/historique_inventaire.py
- Line 47: `conn = get_connection()`
- Line 104: `conn = get_connection()`

### modules/inventaire.py
- Line 56: `conn = get_connection()`
- Line 62: `conn = get_connection()`
- Line 96: `conn = get_connection()`

### modules/journal.py
- Line 77: `conn = get_connection()`

### modules/members.py
- Line 60: `conn = get_connection()`
- Line 108: `conn = get_connection()`
- Line 186: `conn = get_connection()`
- Line 224: `conn = get_connection()`

### modules/model_colonnes.py
- Line 10: `conn = get_connection()`
- Line 30: `conn = get_connection()`
- Line 36: `conn = get_connection()`
- Line 42: `conn = get_connection()`
- Line 92: `conn = get_connection()`
- Line 136: `conn = get_connection()`

### modules/mouvements_stock.py
- Line 35: `conn = get_connection()`

### modules/retrocessions_ecoles.py
- Line 38: `conn = get_connection()`
- Line 60: `conn = get_connection()`
- Line 102: `conn = get_connection()`
- Line 124: `conn = get_connection()`

### modules/solde_ouverture.py
- Line 25: `conn = get_connection()`
- Line 40: `conn = get_connection()`

### modules/stock.py
- Line 42: `conn = get_connection()`
- Line 87: `conn = get_connection()`
- Line 138: `conn = get_connection()`
- Line 164: `conn = get_connection()`

### modules/stock_db.py
- Line 35: `conn = get_connection()`

### modules/stock_inventaire.py
- Line 41: `conn = get_connection()`
- Line 78: `conn = get_connection()`

### modules/stock_stats.py
- Line 14: `conn = get_connection()`

### modules/stock_tab.py
- Line 78: `conn = get_connection()`

### scripts/audit_db_usage.py
- Line 58: `# Pattern: get_connection()`
- Line 168: `report.append(f"- get_connection() calls: {len(self.results['get_connection_calls'])}\n")`
- Line 183: `report.append("\n## get_connection() Calls\n")`
- Line 274: `report.append("\nAction: Use db.get_connection() or modules.db_api.get_connection() instead of direct sqlite3.connect()\n")`
- Line 274: `report.append("\nAction: Use db.get_connection() or modules.db_api.get_connection() instead of direct sqlite3.connect()\n")`

### scripts/db_diagnostics.py
- Line 152: `conn = get_connection()`
- Line 168: `conn = get_connection()`

### tests/test_delete_inventaire.py
- Line 49: `conn2 = get_connection()`

### ui/dialogs/base_list_dialog.py
- Line 92: `conn = get_connection()`

### ui/inventory_lines_dialog.py
- Line 373: `conn = get_connection()`

### ui/startup_schema_check.py
- Line 92: `conn = get_connection()`

### utils/cloture_exercice.py
- Line 28: `conn = get_connection()`
- Line 90: `conn = get_connection()`

### utils/db_operations.py
- Line 40: `conn = get_connection()`

## Fetch Patterns

### db/db.py
- Line 80 `.fetchone()`: `if not c.fetchone():`
- Line 89 `.fetchone()`: `if c.fetchone()["n"] == 0:`
- Line 91 `.fetchone()`: `row = c.fetchone()`
- Line 144 `.fetchone()`: `if not c.fetchone():`
- Line 655 `.fetchone()`: `res = c.fetchone()`
- Line 675 `.fetchone()`: `row = c.fetchone()`
- Line 99 `.fetchall()`: `cols = [r[1] for r in c.fetchall()]`

### dialogs/depense_dialog.py
- Line 155 `.fetchone()`: `row = conn.execute(f"SELECT * FROM {self.table} WHERE id=?", (self.depense_id,)).fetchone()`

### dialogs/edit_don_dialog.py
- Line 57 `.fetchone()`: `).fetchone()`

### dialogs/edit_event_dialog.py
- Line 58 `.fetchone()`: `).fetchone()`

### dialogs/edit_field_dialog.py
- Line 36 `.fetchone()`: `row_val = conn.execute("SELECT modele_colonne FROM event_module_fields WHERE id=?", (self.field_id,)).fetchone()`
- Line 75 `.fetchone()`: `).fetchone()`
- Line 80 `.fetchone()`: `).fetchone()`
- Line 54 `.fetchall()`: `rows = conn.execute("SELECT name FROM colonnes_modeles ORDER BY name").fetchall()`

### dialogs/edit_journal_dialog.py
- Line 62 `.fetchone()`: `).fetchone()`

### dialogs/edit_member_dialog.py
- Line 62 `.fetchone()`: `).fetchone()`

### dialogs/edit_module_data_dialog.py
- Line 18 `.fetchone()`: `).fetchone()`
- Line 114 `.fetchone()`: `).fetchone()[0]`
- Line 32 `.fetchall()`: `).fetchall()`
- Line 95 `.fetchall()`: `).fetchall()`

### dialogs/edit_module_dialog.py
- Line 34 `.fetchone()`: `).fetchone()`

### dialogs/edit_stock_dialog.py
- Line 71 `.fetchone()`: `).fetchone()`

### lib/db_articles.py
- Line 177 `.fetchone()`: `article = cursor.fetchone()`
- Line 217 `.fetchone()`: `article = cursor.fetchone()`
- Line 103 `.fetchall()`: `columns = [row[1] for row in cursor.fetchall()]`
- Line 137 `.fetchall()`: `articles = cursor.fetchall()`

### main.py
- Line 65 `.fetchone()`: `row = cur.fetchone()`
- Line 202 `.fetchone()`: `row = cur.fetchone()`

### modules/buvette_bilan_db.py
- Line 45 `.fetchone()`: `""", (event_id, typ)).fetchone()`
- Line 83 `.fetchone()`: `row = conn.execute(q, params).fetchone()`
- Line 104 `.fetchone()`: `""", (event_id,)).fetchone()`
- Line 26 `.fetchall()`: `rows = conn.execute("SELECT id, name, date FROM events ORDER BY date DESC").fetchall()`
- Line 64 `.fetchall()`: `""", (inv_id,)).fetchall()`

### modules/buvette_bilan_dialogs.py
- Line 23 `.fetchone()`: `""", (event_id, typ)).fetchone()`
- Line 46 `.fetchone()`: `row = conn.execute(q, params).fetchone()`
- Line 58 `.fetchone()`: `""", (event_id,)).fetchone()`
- Line 12 `.fetchall()`: `rows = conn.execute("SELECT id, name, date FROM events ORDER BY date DESC").fetchall()`
- Line 35 `.fetchall()`: `""", (inv_id,)).fetchall()`

### modules/buvette_db.py
- Line 107 `.fetchone()`: `row = conn.execute("SELECT * FROM buvette_articles WHERE id=?", (article_id,)).fetchone()`
- Line 215 `.fetchone()`: `""", (achat_id,)).fetchone()`
- Line 267 `.fetchone()`: `).fetchone()`
- Line 324 `.fetchone()`: `""", (mvt_id,)).fetchone()`
- Line 502 `.fetchone()`: `row = conn.execute("SELECT stock FROM buvette_articles WHERE id=?", (article_id,)).fetchone()`
- Line 69 `.fetchall()`: `_schema_cache[cache_key] = [row[1] for row in cursor.fetchall()]`
- Line 96 `.fetchall()`: `rows = conn.execute("SELECT * FROM buvette_articles ORDER BY name").fetchall()`
- Line 199 `.fetchall()`: `""").fetchall()`
- Line 303 `.fetchall()`: `""").fetchall()`
- Line 381 `.fetchall()`: `""", (inventaire_id,)).fetchall()`
- Line 432 `.fetchall()`: `rows = conn.execute("SELECT id, name, contenance FROM buvette_articles ORDER BY name").fetchall()`
- Line 448 `.fetchall()`: `columns = [row["name"] for row in cursor.fetchall()]`
- Line 499 `.fetchall()`: `columns = [row["name"] for row in cursor.fetchall()]`

### modules/buvette_inventaire_db.py
- Line 54 `.fetchone()`: `""", (inv_id,)).fetchone()`
- Line 234 `.fetchone()`: `row = cur.fetchone()`
- Line 38 `.fetchall()`: `""").fetchall()`
- Line 99 `.fetchall()`: `tables = [r[0] for r in cur.fetchall()]`
- Line 104 `.fetchall()`: `fk_rows = conn.execute(f"PRAGMA foreign_key_list({t})").fetchall()`
- Line 180 `.fetchall()`: `""", (inventaire_id,)).fetchall()`
- Line 256 `.fetchall()`: `rows = conn.execute("SELECT id, name FROM events ORDER BY date DESC").fetchall()`

### modules/buvette_inventaire_dialogs.py
- Line 305 `.fetchall()`: `columns = [col[1] for col in cursor.fetchall()]`

### modules/buvette_mouvements_db.py
- Line 50 `.fetchone()`: `""", (mvt_id,)).fetchone()`
- Line 33 `.fetchall()`: `""").fetchall()`
- Line 101 `.fetchall()`: `rows = conn.execute("SELECT id, name FROM buvette_articles ORDER BY name").fetchall()`
- Line 112 `.fetchall()`: `rows = conn.execute("SELECT id, name FROM events ORDER BY date DESC").fetchall()`

### modules/categories.py
- Line 112 `.fetchone()`: `nb_children = cur.fetchone()[0]`
- Line 114 `.fetchone()`: `nb_stock = cur.fetchone()[0]`

### modules/db_api.py
- Line 46 `.fetchone()`: `>>> row = cursor.fetchone()`
- Line 108 `.fetchone()`: `row = cursor.fetchone()`
- Line 164 `.fetchall()`: `rows = cursor.fetchall()`

### modules/db_row_utils.py
- Line 37 `.fetchone()`: `>>> row = cursor.execute("SELECT * FROM table").fetchone()`
- Line 44 `.fetchone()`: `>>> row = cursor.fetchone()`
- Line 87 `.fetchall()`: `>>> rows = cursor.execute("SELECT * FROM table").fetchall()`
- Line 95 `.fetchall()`: `>>> rows = cursor.fetchall()`

### modules/depenses_diverses.py
- Line 140 `.fetchone()`: `mod = conn.execute("SELECT nom_module FROM event_modules WHERE id=?", (item["module_id"],)).fetchone()`
- Line 144 `.fetchone()`: `mem = conn.execute("SELECT name, prenom FROM membres WHERE id=?", (item["membre_id"],)).fetchone()`
- Line 45 `.fetchall()`: `modules = conn.execute("SELECT id, nom_module FROM event_modules ORDER BY nom_module").fetchall()`
- Line 51 `.fetchall()`: `fournisseurs = conn.execute("SELECT name FROM fournisseurs ORDER BY name").fetchall()`
- Line 57 `.fetchall()`: `membres = conn.execute("SELECT id, name, prenom FROM membres ORDER BY name, prenom").fetchall()`
- Line 135 `.fetchall()`: `).fetchall()`

### modules/depenses_regulieres.py
- Line 140 `.fetchone()`: `mod = conn.execute("SELECT nom_module FROM event_modules WHERE id=?", (item["module_id"],)).fetchone()`
- Line 144 `.fetchone()`: `mem = conn.execute("SELECT name, prenom FROM membres WHERE id=?", (item["membre_id"],)).fetchone()`
- Line 45 `.fetchall()`: `modules = conn.execute("SELECT id, nom_module FROM event_modules ORDER BY nom_module").fetchall()`
- Line 51 `.fetchall()`: `fournisseurs = conn.execute("SELECT name FROM fournisseurs ORDER BY name").fetchall()`
- Line 57 `.fetchall()`: `membres = conn.execute("SELECT id, name, prenom FROM membres ORDER BY name, prenom").fetchall()`
- Line 135 `.fetchall()`: `).fetchall()`

### modules/depots_retraits_banque.py
- Line 156 `.fetchone()`: `row = c.fetchone()`

### modules/dons_subventions.py
- Line 58 `.fetchall()`: `).fetchall()`

### modules/event_caisse_details.py
- Line 125 `.fetchone()`: `).fetchone()`
- Line 42 `.fetchall()`: `).fetchall()`

### modules/event_caisses.py
- Line 122 `.fetchone()`: `).fetchone()`
- Line 41 `.fetchall()`: `).fetchall()`

### modules/event_depenses.py
- Line 137 `.fetchone()`: `).fetchone()`
- Line 44 `.fetchall()`: `).fetchall()`

### modules/event_module_data.py
- Line 94 `.fetchone()`: `res = conn.execute("SELECT MAX(row_index) FROM event_module_data WHERE module_id=?", (self.module_id,)).fetchone()`
- Line 107 `.fetchall()`: `).fetchall()`

### modules/event_module_fields.py
- Line 107 `.fetchone()`: `champ = conn.execute("SELECT nom_champ, prix_unitaire FROM event_module_fields WHERE id=?", (fid,)).fetchone()`
- Line 51 `.fetchall()`: `).fetchall()`

### modules/event_modules.py
- Line 242 `.fetchone()`: `).fetchone()`
- Line 251 `.fetchone()`: `id_col = conn.execute("SELECT id_col_total FROM event_modules WHERE id=?", (self.module_id,)).fetchone()`
- Line 357 `.fetchone()`: `row = conn.execute("SELECT id FROM colonnes_modeles WHERE name=?", (modele_colonne_nom,)).fetchone()`
- Line 370 `.fetchone()`: `).fetchone()`
- Line 431 `.fetchone()`: `).fetchone()`
- Line 509 `.fetchone()`: `).fetchone()`
- Line 518 `.fetchone()`: `).fetchone()`
- Line 575 `.fetchone()`: `).fetchone()`
- Line 613 `.fetchone()`: `).fetchone()`
- Line 67 `.fetchall()`: `mods = conn.execute("SELECT * FROM event_modules WHERE event_id = ?", (self.event_id,)).fetchall()`
- Line 207 `.fetchall()`: `).fetchall()`
- Line 235 `.fetchall()`: `).fetchall()`
- Line 361 `.fetchall()`: `choix = [v["valeur"] for v in conn.execute("SELECT valeur FROM valeurs_modeles_colonnes WHERE modele_id=?", (modele_id,)).fetchall()]`
- Line 541 `.fetchall()`: `).fetchall()`
- Line 563 `.fetchall()`: `).fetchall()`
- Line 566 `.fetchall()`: `).fetchall()`
- Line 601 `.fetchall()`: `).fetchall()`
- Line 604 `.fetchall()`: `).fetchall()`

### modules/event_payments.py
- Line 124 `.fetchone()`: `p = conn.execute("SELECT * FROM event_payments WHERE id=?", (self.payment_id,)).fetchone()`
- Line 41 `.fetchall()`: `).fetchall()`

### modules/event_recettes.py
- Line 19 `.fetchone()`: `).fetchone()`
- Line 23 `.fetchone()`: `).fetchone()`
- Line 26 `.fetchone()`: `exist = conn.execute("SELECT id FROM event_recettes WHERE event_id=? AND source='Vente sur place'", (event_id,)).fetchone()`
- Line 73 `.fetchone()`: `mod = conn.execute("SELECT nom_module FROM event_modules WHERE id=?", (r["module_id"],)).fetchone()`
- Line 104 `.fetchone()`: `r = conn.execute("SELECT source FROM event_recettes WHERE id=?", (rid,)).fetchone()`
- Line 233 `.fetchone()`: `r = conn.execute("SELECT * FROM event_recettes WHERE id=?", (self.recette_id,)).fetchone()`
- Line 14 `.fetchall()`: `caisses = conn.execute("SELECT id FROM event_caisses WHERE event_id=?", (event_id,)).fetchall()`
- Line 69 `.fetchall()`: `recettes = conn.execute("SELECT * FROM event_recettes WHERE event_id=? ORDER BY source", (self.event_id,)).fetchall()`
- Line 167 `.fetchall()`: `mods = conn.execute("SELECT id, nom_module FROM event_modules WHERE event_id=?", (self.event_id,)).fetchall()`
- Line 179 `.fetchall()`: `fields = conn.execute("SELECT id, nom_champ FROM event_module_fields WHERE module_id=?", (module_id,)).fetchall()`
- Line 218 `.fetchall()`: `).fetchall()`

### modules/events.py
- Line 87 `.fetchone()`: `).fetchone()[0]`
- Line 90 `.fetchone()`: `).fetchone()[0]`
- Line 209 `.fetchone()`: `ev = conn.execute("SELECT * FROM events WHERE id = ?", (self.event_id,)).fetchone()`
- Line 82 `.fetchall()`: `events = conn.execute("SELECT * FROM events ORDER BY date DESC").fetchall()`

### modules/exports.py
- Line 11 `.fetchone()`: `event = conn.execute("SELECT * FROM events WHERE id=?", (event_id,)).fetchone()`
- Line 37 `.fetchone()`: `).fetchone()["total"] or 0.0`
- Line 40 `.fetchone()`: `).fetchone()["total"] or 0.0`
- Line 376 `.fetchall()`: `events = conn.execute("SELECT id, name FROM events ORDER BY date DESC").fetchall()`
- Line 441 `.fetchall()`: `events = conn.execute("SELECT id, name, date FROM events ORDER BY date DESC").fetchall()`

### modules/fournisseurs.py
- Line 99 `.fetchone()`: `old = conn.execute("SELECT name FROM fournisseurs WHERE id=?", (fid,)).fetchone()`
- Line 37 `.fetchall()`: `fournisseurs = conn.execute("SELECT * FROM fournisseurs ORDER BY name").fetchall()`

### modules/historique_clotures.py
- Line 62 `.fetchone()`: `old = conn.execute("SELECT date_cloture FROM historique_clotures WHERE id=?", (cid,)).fetchone()`
- Line 35 `.fetchall()`: `clotures = conn.execute("SELECT id, date_cloture FROM historique_clotures ORDER BY date_cloture DESC").fetchall()`

### modules/historique_inventaire.py
- Line 114 `.fetchall()`: `).fetchall()`

### modules/inventaire.py
- Line 99 `.fetchone()`: `row = conn.execute("SELECT id FROM events WHERE name=?", (evt_name,)).fetchone()`
- Line 107 `.fetchone()`: `inv_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]`
- Line 57 `.fetchall()`: `evts = conn.execute("SELECT name FROM events ORDER BY date DESC").fetchall()`

### modules/journal.py
- Line 81 `.fetchone()`: `row = conn.execute("SELECT solde_report FROM config ORDER BY id DESC LIMIT 1").fetchone()`

### modules/members.py
- Line 190 `.fetchone()`: `).fetchone()`

### modules/model_colonnes.py
- Line 45 `.fetchone()`: `modele_id = cur.execute("SELECT id FROM colonnes_modeles WHERE name=?", (name,)).fetchone()["id"]`
- Line 137 `.fetchone()`: `c = conn.execute("SELECT * FROM colonnes_modeles WHERE id=?", (modele_id,)).fetchone()`
- Line 31 `.fetchall()`: `res = conn.execute("SELECT * FROM colonnes_modeles ORDER BY name").fetchall()`
- Line 37 `.fetchall()`: `res = conn.execute("SELECT valeur FROM valeurs_modeles_colonnes WHERE modele_id=? ORDER BY valeur", (modele_id,)).fetchall()`

### modules/retrocessions_ecoles.py
- Line 61 `.fetchone()`: `old = conn.execute("SELECT * FROM retrocessions_ecoles WHERE id=?", (cid,)).fetchone()`
- Line 41 `.fetchall()`: `).fetchall()`

### modules/solde_ouverture.py
- Line 26 `.fetchone()`: `row = conn.execute("SELECT solde_report FROM config ORDER BY id DESC LIMIT 1").fetchone()`

### modules/stock.py
- Line 167 `.fetchone()`: `row = conn.execute("SELECT id FROM categories WHERE name=?", (cat,)).fetchone()`
- Line 139 `.fetchall()`: `cats = conn.execute("SELECT name FROM categories ORDER BY name").fetchall()`

### modules/stock_db.py
- Line 96 `.fetchone()`: `).fetchone()`
- Line 191 `.fetchone()`: `).fetchone()`
- Line 200 `.fetchall()`: `""", (inventaire_id,)).fetchall()`
- Line 269 `.fetchall()`: `""", (inventaire_id,)).fetchall()`
- Line 318 `.fetchall()`: `""", (inv_id,)).fetchall()`
- Line 386 `.fetchall()`: `""", (article_id, scope)).fetchall()`

### modules/stock_tab.py
- Line 50 `.fetchall()`: `_schema_cache[cache_key] = [row[1] for row in cursor.fetchall()]`
- Line 119 `.fetchall()`: `""").fetchall()`

### scripts/auto_fix_buvette_rows.py
- Line 7 `.fetchone()`: `- rows = cursor.fetchall() or row = cursor.fetchone() are used`
- Line 102 `.fetchone()`: `- row = cursor.fetchone() -> add: row = _row_to_dict(row)`
- Line 120 `.fetchone()`: `# Match patterns like: variable = something.fetchone()`
- Line 7 `.fetchall()`: `- rows = cursor.fetchall() or row = cursor.fetchone() are used`
- Line 101 `.fetchall()`: `- rows = cursor.fetchall() -> add: rows = _rows_to_dicts(rows)`
- Line 112 `.fetchall()`: `# Match patterns like: variable = something.fetchall()`

### scripts/create_compat_views.py
- Line 23 `.fetchall()`: `cols = [r[1] for r in cur.fetchall()]`

### scripts/db_diagnostics.py
- Line 90 `.fetchone()`: `mode = cursor.fetchone()[0]`
- Line 113 `.fetchone()`: `timeout = cursor.fetchone()[0]`
- Line 135 `.fetchone()`: `result = cursor.fetchone()[0]`
- Line 155 `.fetchone()`: `cursor.fetchone()`
- Line 221 `.fetchone()`: `count = cursor.fetchone()[0]`
- Line 195 `.fetchall()`: `tables = [row[0] for row in cursor.fetchall()]`

### scripts/enable_wal.py
- Line 51 `.fetchone()`: `current_mode = cursor.fetchone()[0]`
- Line 62 `.fetchone()`: `result = cursor.fetchone()[0]`
- Line 76 `.fetchone()`: `sync_mode = cursor.fetchone()[0]`

### scripts/migrate_add_purchase_price.py
- Line 62 `.fetchone()`: `result = cursor.fetchone()`
- Line 106 `.fetchone()`: `table_exists = cursor.fetchone()`
- Line 119 `.fetchall()`: `columns = [row[1] for row in cursor.fetchall()]`

### scripts/migrate_articles_unite_to_quantite.py
- Line 16 `.fetchone()`: `if not cur.fetchone():`
- Line 20 `.fetchall()`: `cols = [r[1] for r in cur.fetchall()]`
- Line 62 `.fetchall()`: `old_cols = [r[1] for r in conn.execute("PRAGMA table_info(buvette_articles)").fetchall()]`

### scripts/migration.py
- Line 40 `.fetchall()`: `return conn.execute(f"PRAGMA table_info({table});").fetchall()`

### scripts/update_db_structure.py
- Line 552 `.fetchone()`: `version = cursor.fetchone()[0]`
- Line 753 `.fetchone()`: `result = cursor.fetchone()`
- Line 537 `.fetchall()`: `tables = [row[0] for row in cursor.fetchall()]`
- Line 542 `.fetchall()`: `columns = set(row[1] for row in cursor.fetchall())`

### scripts/update_db_structure_old.py
- Line 512 `.fetchone()`: `version = cursor.fetchone()[0]`
- Line 707 `.fetchone()`: `result = cursor.fetchone()`
- Line 497 `.fetchall()`: `tables = [row[0] for row in cursor.fetchall()]`
- Line 502 `.fetchall()`: `columns = set(row[1] for row in cursor.fetchall())`

### src/db/repository.py
- Line 50 `.fetchone()`: `row = cur.fetchone()`
- Line 35 `.fetchall()`: `rows = cur.fetchall()`
- Line 65 `.fetchall()`: `rows = cur.fetchall()`

### src/db/row_utils.py
- Line 21 `.fetchone()`: `>>> row = cursor.execute("SELECT * FROM table").fetchone()`
- Line 45 `.fetchone()`: `>>> row = cursor.execute("SELECT * FROM table").fetchone()`
- Line 84 `.fetchall()`: `>>> rows = cursor.execute("SELECT * FROM table").fetchall()`

### src/services/inventory_service.py
- Line 30 `.fetchall()`: `found = [r[0] for r in cur.fetchall()]`
- Line 61 `.fetchall()`: `rows = cur.fetchall()`
- Line 78 `.fetchall()`: `found = [r[0] for r in cur.fetchall()]`
- Line 89 `.fetchall()`: `columns = [row[1] for row in cur.fetchall()]`

### tests/test_analyze_modules.py
- Line 130 `.fetchall()`: `return cursor.fetchall()`

### tests/test_articles_unite_migration.py
- Line 235 `.fetchall()`: `columns = [row[1] for row in cursor.fetchall()]`

### tests/test_buvette_inventaire.py
- Line 100 `.fetchone()`: `inv = cur.fetchone()`
- Line 121 `.fetchone()`: `inv = cur.fetchone()`
- Line 138 `.fetchone()`: `inv = cur.fetchone()`
- Line 178 `.fetchone()`: `inv = cur.fetchone()`
- Line 228 `.fetchall()`: `inventaires = cur.fetchall()`

### tests/test_buvette_purchase_price.py
- Line 73 `.fetchone()`: `article = cursor.fetchone()`
- Line 91 `.fetchone()`: `article = cursor.fetchone()`
- Line 111 `.fetchone()`: `article_id = cursor.fetchone()['id']`
- Line 123 `.fetchone()`: `updated_price = cursor.fetchone()['purchase_price']`
- Line 169 `.fetchone()`: `article = cursor.fetchone()`
- Line 56 `.fetchall()`: `columns = [row[1] for row in cursor.fetchall()]`
- Line 155 `.fetchall()`: `columns_before = [row[1] for row in cursor.fetchall()]`
- Line 164 `.fetchall()`: `columns_after = [row[1] for row in cursor.fetchall()]`

### tests/test_buvette_stock.py
- Line 74 `.fetchone()`: `row = cursor.fetchone()`
- Line 90 `.fetchone()`: `row = cursor.fetchone()`
- Line 108 `.fetchone()`: `article_id = cursor.fetchone()['id']`
- Line 116 `.fetchone()`: `row = cursor.fetchone()`
- Line 155 `.fetchone()`: `row = cursor.fetchone()`
- Line 59 `.fetchall()`: `columns = [row[1] for row in cursor.fetchall()]`
- Line 147 `.fetchall()`: `columns = [row[1] for row in cursor.fetchall()]`

### tests/test_connection.py
- Line 23 `.fetchone()`: `row = cur.fetchone()`

### tests/test_database_migration.py
- Line 241 `.fetchone()`: `row = cursor.fetchone()`
- Line 192 `.fetchall()`: `config_cols = {row[1] for row in cursor.fetchall()}`
- Line 200 `.fetchall()`: `membres_cols = {row[1] for row in cursor.fetchall()}`
- Line 248 `.fetchall()`: `rows = cursor.fetchall()`

### tests/test_db_locking.py
- Line 60 `.fetchone()`: `assert cr.fetchone()[0] == 2`

### tests/test_db_row_utils.py
- Line 59 `.fetchone()`: `row = cursor.execute("SELECT * FROM test_table WHERE id=1").fetchone()`
- Line 76 `.fetchone()`: `row = cursor.execute("SELECT * FROM test_table WHERE id=2").fetchone()`
- Line 138 `.fetchone()`: `row1 = cursor.execute("SELECT * FROM test_table WHERE id=1").fetchone()`
- Line 139 `.fetchone()`: `row2 = cursor.execute("SELECT * FROM test_table WHERE id=2").fetchone()`
- Line 155 `.fetchone()`: `row = cursor.execute("SELECT * FROM test_table WHERE id=1").fetchone()`
- Line 164 `.fetchone()`: `row = cursor.execute("SELECT * FROM test_table WHERE id=1").fetchone()`
- Line 172 `.fetchone()`: `row = cursor.execute("SELECT * FROM test_table WHERE id=1").fetchone()`
- Line 106 `.fetchall()`: `rows = cursor.execute("SELECT * FROM test_table ORDER BY id").fetchall()`

### tests/test_delete_inventaire.py
- Line 66 `.fetchone()`: `assert cur.fetchone()[0] == 0`
- Line 68 `.fetchone()`: `assert cur.fetchone()[0] == 0`

### tests/test_inventory_integration.py
- Line 40 `.fetchone()`: `inv_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]`
- Line 101 `.fetchone()`: `inv_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]`
- Line 149 `.fetchone()`: `inv_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]`
- Line 207 `.fetchone()`: `inv_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]`
- Line 245 `.fetchone()`: `inv_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]`

### tests/test_row_to_dict_conversion.py
- Line 53 `.fetchone()`: `row = self.conn.execute("SELECT * FROM test_table WHERE id=1").fetchone()`
- Line 70 `.fetchone()`: `row = self.conn.execute("SELECT * FROM test_table WHERE id=2").fetchone()`
- Line 106 `.fetchone()`: `row = self.conn.execute("SELECT * FROM test_table WHERE id=1").fetchone()`
- Line 121 `.fetchone()`: `row = self.conn.execute("SELECT * FROM test_table WHERE id=1").fetchone()`
- Line 135 `.fetchone()`: `row = self.conn.execute("SELECT * FROM test_table WHERE id=1").fetchone()`
- Line 90 `.fetchall()`: `rows = self.conn.execute("SELECT * FROM test_table").fetchall()`

### tests/test_smart_migration.py
- Line 238 `.fetchone()`: `row = cursor.fetchone()`
- Line 225 `.fetchall()`: `columns = {row[1] for row in cursor.fetchall()}`
- Line 283 `.fetchall()`: `columns = {row[1] for row in cursor.fetchall()}`

### tests/test_src_row_utils.py
- Line 56 `.fetchone()`: `row = cursor.execute("SELECT * FROM test_table WHERE id=1").fetchone()`
- Line 73 `.fetchone()`: `row = cursor.execute("SELECT * FROM test_table WHERE id=2").fetchone()`
- Line 127 `.fetchone()`: `row1 = cursor.execute("SELECT * FROM test_table WHERE id=1").fetchone()`
- Line 128 `.fetchone()`: `row2 = cursor.execute("SELECT * FROM test_table WHERE id=2").fetchone()`
- Line 99 `.fetchall()`: `rows = cursor.execute("SELECT * FROM test_table ORDER BY id").fetchall()`

### tests/test_stock_journal.py
- Line 123 `.fetchone()`: `result = cursor.fetchone()`
- Line 298 `.fetchone()`: `""", (inv_id,)).fetchone()`
- Line 381 `.fetchone()`: `""", (batch_id,)).fetchone()`
- Line 438 `.fetchone()`: `""", (batch1_id,)).fetchone()`
- Line 444 `.fetchone()`: `""", (batch2_id,)).fetchone()`
- Line 450 `.fetchone()`: `""", (batch3_id,)).fetchone()`
- Line 214 `.fetchall()`: `""", (inv_id,)).fetchall()`

### ui/dialogs/base_list_dialog.py
- Line 100 `.fetchall()`: `rows = cursor.fetchall()`

### ui/startup_schema_check.py
- Line 97 `.fetchall()`: `tables = [row[0] for row in cursor.fetchall()]`
- Line 108 `.fetchall()`: `columns = set(row[1] for row in cursor.fetchall())`

### utils/cloture_exercice.py
- Line 31 `.fetchall()`: `tables = [row[0] for row in cursor.fetchall()]`

### utils/db_helpers.py
- Line 24 `.fetchone()`: `>>> row = cursor.execute("SELECT * FROM table").fetchone()`
- Line 74 `.fetchone()`: `>>> row = cursor.execute("SELECT * FROM table").fetchone()`
- Line 46 `.fetchall()`: `>>> rows = cursor.execute("SELECT * FROM table").fetchall()`

### utils/db_operations.py
- Line 74 `.fetchone()`: `row = cursor.fetchone()`
- Line 35 `.fetchall()`: `rows = cursor.fetchall()`
- Line 77 `.fetchall()`: `rows = cursor.fetchall()`

## ⚠️ CRITICAL: row.get() Usage (Will Crash!)
These locations use .get() on sqlite3.Row objects, which will cause AttributeError.
These MUST be fixed by converting rows to dicts first.

### dashboard/dashboard.py
- Line 131 (var: `row`): `name = row["name"] if "name" in row else row.get("evenement", "")`

### modules/buvette.py
- Line 426 (var: `item`): `unite_display = item.get("unite_type", item.get("unite", ""))`
- Line 426 (var: `item`): `unite_display = item.get("unite_type", item.get("unite", ""))`
- Line 427 (var: `item`): `quantite_display = item.get("quantite", "")`
- Line 431 (var: `item`): `iid=item.get("id", 0),`
- Line 433 (var: `item`): `item.get("name", ""),`
- Line 434 (var: `item`): `item.get("categorie", ""),`
- Line 435 (var: `item`): `item.get("stock", 0),`
- Line 438 (var: `item`): `item.get("contenance", ""),`
- Line 439 (var: `item`): `item.get("commentaire", "")`

### modules/buvette_bilan_db.py
- Line 85 (var: `row_dict`): `if row_dict and row_dict.get("qte"):`
- Line 106 (var: `row_dict`): `return row_dict.get("recette", 0.0) if row_dict else 0.0`

### modules/db_row_utils.py
- Line 39 (var: `row_dict`): `>>> value = row_dict.get('optional_column', 'default')`

### modules/depots_retraits_banque.py
- Line 66 (var: `row`): `row.get("reference", ""),`
- Line 67 (var: `row`): `row.get("banque", ""),`
- Line 68 (var: `row`): `"Oui" if row.get("pointe", 0) else "Non",`
- Line 69 (var: `row`): `row.get("commentaire", "")`

### modules/event_modules.py
- Line 262 (var: `res`): `modele_colonne = res.get("modele_colonne")`

### modules/members.py
- Line 67 (var: `row`): `row["id"], row["name"], row["prenom"], row["email"], row.get("cotisation", ""),`
- Line 68 (var: `row`): `row.get("commentaire", ""), row.get("telephone", ""), row.get("statut", ""),`
- Line 68 (var: `row`): `row.get("commentaire", ""), row.get("telephone", ""), row.get("statut", ""),`
- Line 68 (var: `row`): `row.get("commentaire", ""), row.get("telephone", ""), row.get("statut", ""),`
- Line 69 (var: `row`): `row.get("date_adhesion", "")`

### modules/stock_db.py
- Line 216 (var: `item`): `article_id = item.get("article_id")`
- Line 217 (var: `item`): `new_quantity = item.get("quantite", 0)`

### modules/stock_inventaire.py
- Line 51 (var: `row`): `self.tree.insert("", "end", values=(row["id"], row["name"], row.get("categorie", ""), row["quantite"], ""))`

### scripts/analyze_modules_columns_old.py
- Line 112 (var: `row`): `# Recherche de références dictionary-style (row["column"], row.get("column"))`
- Line 135 (var: `row`): `"""Extrait les références dictionary-style (row["column"], row.get("column"))."""`
- Line 147 (var: `row`): `# Pattern pour row.get("column") ou row.get('column')`
- Line 147 (var: `row`): `# Pattern pour row.get("column") ou row.get('column')`

### scripts/audit_db_usage.py
- Line 78 (var: `row`): `# Pattern: row.get( or row.get('`

### scripts/replace_row_get.py
- Line 14 (var: `row`): `- row.get('column')`
- Line 15 (var: `result`): `- result.get('field', default)`
- Line 16 (var: `item`): `- item.get('key')`

### src/db/row_utils.py
- Line 9 (var: `row`): `This causes AttributeError when code tries to use row.get('column', default).`
- Line 23 (var: `row_dict`): `>>> value = row_dict.get('optional_column', 'default')`
- Line 47 (var: `row_dict`): `>>> value = row_dict.get('optional_column', 'default')`

### tests/test_db_api_retry.py
- Line 219 (var: `result`): `assert result.get('name') == 'test1'`
- Line 220 (var: `result`): `assert result.get('value') == 100`

### tests/test_db_row_utils.py
- Line 82 (var: `result`): `self.assertEqual(result.get("name"), "Test Item 2")`
- Line 85 (var: `result`): `self.assertIsNone(result.get("optional_field"))`
- Line 86 (var: `result`): `self.assertIsNone(result.get("optional_field", "default"))  # Key exists, value is None`
- Line 88 (var: `result`): `self.assertEqual(result.get("nonexistent_field", "default"), "default")`
- Line 182 (var: `row_dict`): `self.assertEqual(row_dict.get("name"), "Test Item 1")`
- Line 183 (var: `row_dict`): `self.assertEqual(row_dict.get("nonexistent", "default"), "default")`

### tests/test_row_to_dict_conversion.py
- Line 74 (var: `row_dict`): `self.assertEqual(row_dict.get('name'), 'test2')`
- Line 77 (var: `row_dict`): `self.assertEqual(row_dict.get('nonexistent', 'default'), 'default')`
- Line 80 (var: `row_dict`): `self.assertIsNone(row_dict.get('optional_field'))`
- Line 81 (var: `row_dict`): `self.assertEqual(row_dict.get('optional_field', 'default'), None)`
- Line 113 (var: `row_dict`): `self.assertEqual(row_dict.get('name'), 'test1')`
- Line 139 (var: `row`): `row.get('name')`

### tests/test_src_row_utils.py
- Line 79 (var: `result`): `self.assertEqual(result.get("name"), "Test Item 2")`
- Line 80 (var: `result`): `self.assertIsNone(result.get("optional_field"))`
- Line 81 (var: `result`): `self.assertEqual(result.get("nonexistent_field", "default"), "default")`

### ui/dialogs/base_list_dialog.py
- Line 115 (var: `row`): `item_id = row.get('id', '')`

### utils/db_helpers.py
- Line 26 (var: `row_dict`): `>>> value = row_dict.get('optional_column', 'default')`

## Positional Indexing (row[0], row[1], ...)
These use positional access and should continue to work.

### db/db.py
- Line 99: `cols = [r[1] for r in c.fetchall()]`
- Line 649: `Uses positional access res[0] which works with both sqlite3.Row and tuples.`
- Line 659: `return res[0] == 0`
- Line 694: `tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table';")]`

### dialogs/edit_don_dialog.py
- Line 61: `self.donateur_var.set(row[0])`
- Line 62: `self.montant_var.set(str(row[1]))`
- Line 63: `self.date_var.set(row[2])`
- Line 65: `self.commentaire_widget.insert("1.0", row[3] if row[3] else "")`

### dialogs/edit_event_dialog.py
- Line 62: `self.name_var.set(row[0])`
- Line 63: `self.date_var.set(row[1])`
- Line 64: `self.lieu_var.set(row[2] if row[2] else "")`
- Line 66: `self.commentaire_widget.insert("1.0", row[3] if row[3] else "")`

### dialogs/edit_field_dialog.py
- Line 83: `self.nom_var.set(row[0])`
- Line 84: `self.type_var.set(row[1])`

### dialogs/edit_journal_dialog.py
- Line 66: `self.date_var.set(row[0])`
- Line 67: `self.libelle_var.set(row[1])`
- Line 68: `self.montant_var.set(str(row[2]))`
- Line 69: `self.type_var.set(row[3])`
- Line 70: `self.categorie_var.set(row[4] if row[4] else "")`
- Line 72: `self.commentaire_widget.insert("1.0", row[5] if row[5] else "")`

### dialogs/edit_member_dialog.py
- Line 66: `self.nom_var.set(row[0])`
- Line 67: `self.prenom_var.set(row[1])`
- Line 68: `self.email_var.set(row[2] if row[2] else "")`
- Line 69: `self.classe_var.set(row[3] if row[3] else "")`
- Line 70: `self.cotisation_var.set(str(row[4]) if row[4] else "")`
- Line 72: `self.commentaire_widget.insert("1.0", row[5] if row[5] else "")`

### dialogs/edit_module_data_dialog.py
- Line 21: `return row[0]`

### dialogs/edit_module_dialog.py
- Line 37: `self.nom_var.set(row[0])`

### dialogs/edit_stock_dialog.py
- Line 75: `self.nom_var.set(row[0])`
- Line 76: `self.qte_var.set(row[1])`
- Line 77: `self.seuil_var.set(row[2])`
- Line 78: `self.lot_var.set(row[3] if row[3] else "")`
- Line 79: `self.date_var.set(row[4] if row[4] else "")`
- Line 81: `self.commentaire_widget.insert("1.0", row[5] if row[5] else "")`
- Line 82: `cat_id = row[6]`

### lib/db_articles.py
- Line 103: `columns = [row[1] for row in cursor.fetchall()]`

### modules/buvette_db.py
- Line 69: `_schema_cache[cache_key] = [row[1] for row in cursor.fetchall()]`
- Line 270: `article_id = row[0]`
- Line 271: `quantite = row[1]`

### modules/buvette_inventaire_db.py
- Line 99: `tables = [r[0] for r in cur.fetchall()]`

### modules/depots_retraits_banque.py
- Line 158: `new_val = 0 if row[0] else 1`

### modules/event_module_data.py
- Line 95: `next_idx = (res[0] or 0) + 1`

### modules/event_module_fields.py
- Line 54: `prix = item["prix_unitaire"] if isinstance(item, dict) else item[3]`
- Line 56: `modele = item["modele_colonne"] if isinstance(item, dict) else item[4]`
- Line 58: `item["id"] if isinstance(item, dict) else item[0],`
- Line 59: `item["nom_champ"] if isinstance(item, dict) else item[1],`
- Line 60: `item["type_champ"] if isinstance(item, dict) else item[2],`

### modules/exports.py
- Line 121: `Paragraph(str(row[0]), styles["Normal"]),`
- Line 122: `Paragraph(str(row[1]), styles["Normal"]),`
- Line 123: `Paragraph(str(row[2]), styles["Normal"]),`
- Line 124: `Paragraph(str(row[3]), styles["Normal"])`
- Line 150: `Paragraph(str(row[0]), styles["Normal"]),  # categorie`
- Line 151: `Paragraph(str(row[1]), styles["Normal"]),  # montant`
- Line 152: `Paragraph(str(row[2]), styles["Normal"]),  # fournisseur`
- Line 153: `Paragraph(str(row[3]), styles["Normal"]),  # date_depense`
- Line 154: `Paragraph(str(row[4]), styles["Normal"]),  # paye_par`
- Line 155: `Paragraph(str(row[5]), styles["Normal"]),  # membre_id`
- Line 156: `Paragraph(str(row[6]), styles["Normal"])   # commentaire`
- Line 181: `Paragraph(str(row[0]), styles["Normal"]),`
- Line 182: `Paragraph(str(row[1]), styles["Normal"]),`
- Line 183: `Paragraph(str(row[2]), styles["Normal"]),`
- Line 184: `Paragraph(str(row[3]), styles["Normal"]),`
- Line 185: `Paragraph(str(row[4]), styles["Normal"])`
- Line 271: `Paragraph(str(row[0]), styles["Normal"]), # date`
- Line 272: `Paragraph(str(row[1]), styles["Normal"]), # categorie`
- Line 273: `Paragraph(str(row[2]), styles["Normal"]), # montant`
- Line 274: `Paragraph(str(row[3]), styles["Normal"]), # fournisseur`
- Line 275: `Paragraph(str(row[4]), styles["Normal"]), # paye_par`
- Line 276: `Paragraph(str(row[5]), styles["Normal"]), # membre_id`
- Line 277: `Paragraph(str(row[6]), styles["Normal"]), # commentaire`
- Line 278: `Paragraph(str(row[7]), styles["Normal"])  # type_depense`

### modules/inventory_lines_dialog.py
- Line 128: `f"Row type: {type(raw_rows[0]).__name__ if raw_rows else 'N/A'}",`
- Line 136: `first_row = raw_rows[0]`

### modules/journal.py
- Line 82: `if row and row[0] is not None:`
- Line 83: `solde_ouverture = float(row[0])`

### modules/members.py
- Line 193: `self.nom_var.set(row[0])`
- Line 194: `self.prenom_var.set(row[1])`
- Line 195: `self.email_var.set(row[2] if row[2] else "")`
- Line 196: `self.cotisation_var.set(row[3] if row[3] else COTISATION_ETATS[1])  # défaut: "Non réglé"`
- Line 197: `self.commentaire_var.set(row[4] if row[4] else "")`
- Line 198: `self.tel_var.set(row[5] if row[5] else "")`
- Line 199: `self.statut_var.set(row[6] if row[6] else STATUTS[0])`
- Line 200: `self.date_var.set(row[7] if row[7] else "")`

### modules/solde_ouverture.py
- Line 28: `if row and row[0] is not None:`
- Line 29: `self.solde_var.set(f"{row[0]:.2f}")`

### modules/stock_db.py
- Line 98: `return row[0] if row[0] is not None else 0`
- Line 203: `snapshot.append({"article_id": row[0], "quantite": row[1]})`
- Line 272: `article_id = row[0]`
- Line 273: `delta = row[1]`
- Line 396: `batch_id = row[0]`
- Line 397: `batch_remaining = row[1]`
- Line 398: `batch_unit_price = row[2]`

### modules/stock_tab.py
- Line 50: `_schema_cache[cache_key] = [row[1] for row in cursor.fetchall()]`

### scripts/audit_db_usage.py
- Line 9: `- positional indexing (row[0], row[1], etc.)`
- Line 91: `# Pattern: row[0], row[1], etc. (positional indexing)`
- Line 230: `report.append("\n## Positional Indexing (row[0], row[1], ...)\n")`

### scripts/create_compat_views.py
- Line 23: `cols = [r[1] for r in cur.fetchall()]`

### scripts/db_diagnostics.py
- Line 195: `tables = [row[0] for row in cursor.fetchall()]`

### scripts/migrate_add_purchase_price.py
- Line 63: `print(f"✓ WAL mode enabled: {result[0]}")`
- Line 119: `columns = [row[1] for row in cursor.fetchall()]`

### scripts/migrate_articles_unite_to_quantite.py
- Line 20: `cols = [r[1] for r in cur.fetchall()]`
- Line 62: `old_cols = [r[1] for r in conn.execute("PRAGMA table_info(buvette_articles)").fetchall()]`

### scripts/update_db_structure.py
- Line 537: `tables = [row[0] for row in cursor.fetchall()]`
- Line 542: `columns = set(row[1] for row in cursor.fetchall())`
- Line 754: `self.log(f"Journal mode set to: {result[0]}")`

### scripts/update_db_structure_old.py
- Line 497: `tables = [row[0] for row in cursor.fetchall()]`
- Line 502: `columns = set(row[1] for row in cursor.fetchall())`
- Line 708: `self.log(f"Journal mode set to: {result[0]}")`

### src/services/inventory_service.py
- Line 30: `found = [r[0] for r in cur.fetchall()]`
- Line 44: `'lines_table': result[0],`
- Line 45: `'product_col': result[1],`
- Line 46: `'qty_col': result[2],`
- Line 47: `'inv_fk': result[3]`
- Line 78: `found = [r[0] for r in cur.fetchall()]`
- Line 89: `columns = [row[1] for row in cur.fetchall()]`

### tests/test_articles_unite_migration.py
- Line 235: `columns = [row[1] for row in cursor.fetchall()]`

### tests/test_buvette_purchase_price.py
- Line 56: `columns = [row[1] for row in cursor.fetchall()]`
- Line 155: `columns_before = [row[1] for row in cursor.fetchall()]`
- Line 164: `columns_after = [row[1] for row in cursor.fetchall()]`

### tests/test_buvette_stock.py
- Line 59: `columns = [row[1] for row in cursor.fetchall()]`
- Line 147: `columns = [row[1] for row in cursor.fetchall()]`

### tests/test_database_migration.py
- Line 192: `config_cols = {row[1] for row in cursor.fetchall()}`
- Line 200: `membres_cols = {row[1] for row in cursor.fetchall()}`
- Line 242: `assert row[0] == "2024-2025"`
- Line 243: `assert row[1] == "2024-09-01"`
- Line 245: `assert row[2] == ""`
- Line 250: `assert rows[0][0] == "Dupont"`
- Line 251: `assert rows[0][1] == "Jean"`
- Line 252: `assert rows[0][2] == ""  # Default value for new column`

### tests/test_inventory_service.py
- Line 36: `assert rows2[0]["product_id"] == 42`

### tests/test_smart_migration.py
- Line 225: `columns = {row[1] for row in cursor.fetchall()}`
- Line 239: `assert row[0] == "Dupont", "Data should be preserved"`
- Line 283: `columns = {row[1] for row in cursor.fetchall()}`

### tests/test_stock_journal.py
- Line 217: `self.assertEqual(rows[0]["article_id"], article1_id)`
- Line 219: `rows[0]["delta"], 3, "Article 1 delta should be +3 (8-5)"`
- Line 221: `self.assertEqual(rows[1]["article_id"], article2_id)`
- Line 223: `rows[1]["delta"], -3, "Article 2 delta should be -3 (7-10)"`
- Line 384: `self.assertEqual(row[0], article_id)`
- Line 385: `self.assertEqual(row[1], 10, "Quantity should be 10")`
- Line 386: `self.assertEqual(row[2], 10, "Remaining quantity should be 10")`
- Line 387: `self.assertEqual(row[3], 2.5, "Unit price should be 2.5")`
- Line 439: `self.assertEqual(row1[0], 0, "Batch1 should be fully consumed")`
- Line 445: `self.assertEqual(row2[0], 3, "Batch2 should have 3 remaining")`
- Line 451: `self.assertEqual(row3[0], 8, "Batch3 should be untouched")`

### ui/dialogs/base_list_dialog.py
- Line 125: `item_id = row[0] if len(row) > 0 else ''`

### ui/startup_schema_check.py
- Line 97: `tables = [row[0] for row in cursor.fetchall()]`
- Line 108: `columns = set(row[1] for row in cursor.fetchall())`

### utils/cloture_exercice.py
- Line 31: `tables = [row[0] for row in cursor.fetchall()]`
