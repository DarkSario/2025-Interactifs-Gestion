# SQL Access Map

This report maps all SQL database access in the codebase.

Generated: /home/runner/work/2025-Interactifs-Gestion/2025-Interactifs-Gestion

## Access by Table

### ADD

Total accesses: 1

**scripts/analyze_modules_columns_old.py**

- Line 193: `# ALTER TABLE ADD COLUMN`

### CREATE

Total accesses: 2

**scripts/analyze_modules_columns.py**

- Line 240: `# Use explicit type from CREATE TABLE if available`

**scripts/analyze_modules_columns_old.py**

- Line 227: `# Use explicit type from CREATE TABLE if available`

### IF

Total accesses: 65

**db/db.py**

- Line 65: `cur.execute(f"DROP TABLE IF EXISTS {table};")`
- Line 82: `CREATE TABLE IF NOT EXISTS comptes (`
- Line 151: `CREATE TABLE IF NOT EXISTS retrocessions_ecoles (`
- Line 160: `CREATE TABLE IF NOT EXISTS fournisseurs (`
- Line 166: `CREATE TABLE IF NOT EXISTS colonnes_modeles (`
- Line 173: `CREATE TABLE IF NOT EXISTS valeurs_modeles_colonnes (`
- Line 181: `CREATE TABLE IF NOT EXISTS depots_retraits_banque (`
- Line 193: `CREATE TABLE IF NOT EXISTS historique_clotures (`
- Line 199: `CREATE TABLE IF NOT EXISTS buvette_articles (`
- Line 211: `CREATE TABLE IF NOT EXISTS buvette_achats (`
- Line 224: `CREATE TABLE IF NOT EXISTS buvette_inventaires (`
- Line 234: `CREATE TABLE IF NOT EXISTS buvette_inventaire_lignes (`
- Line 244: `CREATE TABLE IF NOT EXISTS buvette_mouvements (`
- Line 257: `CREATE TABLE IF NOT EXISTS buvette_recettes (`
- Line 283: `CREATE TABLE IF NOT EXISTS config (`
- Line 295: `CREATE TABLE IF NOT EXISTS comptes (`
- Line 302: `CREATE TABLE IF NOT EXISTS retrocessions_ecoles (`
- Line 311: `CREATE TABLE IF NOT EXISTS categories (`
- Line 320: `CREATE TABLE IF NOT EXISTS membres (`
- Line 333: `CREATE TABLE IF NOT EXISTS events (`
- Line 342: `CREATE TABLE IF NOT EXISTS stock (`
- Line 355: `CREATE TABLE IF NOT EXISTS dons_subventions (`
- Line 365: `CREATE TABLE IF NOT EXISTS depenses_regulieres (`
- Line 383: `CREATE TABLE IF NOT EXISTS depenses_diverses (`
- Line 401: `CREATE TABLE IF NOT EXISTS inventaires (`
- Line 410: `CREATE TABLE IF NOT EXISTS inventaire_lignes (`
- Line 420: `CREATE TABLE IF NOT EXISTS mouvements_stock (`
- Line 434: `CREATE TABLE IF NOT EXISTS event_modules (`
- Line 443: `CREATE TABLE IF NOT EXISTS event_module_fields (`
- Line 454: `CREATE TABLE IF NOT EXISTS colonnes_modeles (`
- Line 461: `CREATE TABLE IF NOT EXISTS valeurs_modeles_colonnes (`
- Line 469: `CREATE TABLE IF NOT EXISTS event_module_data (`
- Line 480: `CREATE TABLE IF NOT EXISTS event_payments (`
- Line 494: `CREATE TABLE IF NOT EXISTS event_caisses (`
- Line 503: `CREATE TABLE IF NOT EXISTS event_caisse_details (`
- Line 514: `CREATE TABLE IF NOT EXISTS event_recettes (`
- Line 526: `CREATE TABLE IF NOT EXISTS event_depenses (`
- Line 548: `CREATE TABLE IF NOT EXISTS fournisseurs (`
- Line 554: `CREATE TABLE IF NOT EXISTS depots_retraits_banque (`
- Line 566: `CREATE TABLE IF NOT EXISTS historique_clotures (`
- Line 572: `CREATE TABLE IF NOT EXISTS buvette_articles (`
- Line 584: `CREATE TABLE IF NOT EXISTS buvette_achats (`
- Line 597: `CREATE TABLE IF NOT EXISTS buvette_inventaires (`
- Line 607: `CREATE TABLE IF NOT EXISTS buvette_inventaire_lignes (`
- Line 617: `CREATE TABLE IF NOT EXISTS buvette_mouvements (`
- Line 630: `CREATE TABLE IF NOT EXISTS buvette_recettes (`
- Line 639: `c.execute("DROP TABLE IF EXISTS members;")`

**init_db.py**

- Line 4: `CREATE TABLE IF NOT EXISTS events (`
- Line 12: `CREATE TABLE IF NOT EXISTS event_modules (`
- Line 19: `CREATE TABLE IF NOT EXISTS event_module_fields (`
- Line 27: `CREATE TABLE IF NOT EXISTS event_module_data (`
- Line 37: `CREATE TABLE IF NOT EXISTS members (`
- Line 47: `CREATE TABLE IF NOT EXISTS dons_subventions (`
- Line 55: `CREATE TABLE IF NOT EXISTS depenses_regulieres (`
- Line 64: `CREATE TABLE IF NOT EXISTS depenses_diverses (`
- Line 73: `CREATE TABLE IF NOT EXISTS journal (`
- Line 83: `CREATE TABLE IF NOT EXISTS categories (`
- Line 89: `CREATE TABLE IF NOT EXISTS stock (`

**modules/model_colonnes.py**

- Line 12: `CREATE TABLE IF NOT EXISTS colonnes_modeles (`
- Line 19: `CREATE TABLE IF NOT EXISTS valeurs_modeles_colonnes (`

**modules/stock_db.py**

- Line 40: `CREATE TABLE IF NOT EXISTS inventory_stock_journal (`
- Line 55: `CREATE TABLE IF NOT EXISTS article_purchase_batches (`

**scripts/apply_migrations.py**

- Line 62: `CREATE TABLE IF NOT EXISTS {MIGRATIONS_TABLE} (`

**src/db/connection.py**

- Line 9: `cur.execute("CREATE TABLE IF NOT EXISTS x (id INTEGER PRIMARY KEY, name TEXT)")`

**src/db/repository.py**

- Line 76: `CREATE TABLE IF NOT EXISTS members (`

### RENAME

Total accesses: 2

**scripts/update_db_structure.py**

- Line 548: `"""Vérifie si SQLite supporte ALTER TABLE RENAME COLUMN (version 3.25.0+)."""`

**scripts/update_db_structure_old.py**

- Line 508: `"""Vérifie si SQLite supporte ALTER TABLE RENAME COLUMN (version 3.25.0+)."""`

### SET

Total accesses: 2

**scripts/analyze_modules_columns.py**

- Line 11: `- N'extrait QUE depuis les patterns SQL: INSERT INTO, UPDATE SET, SELECT FROM`

**scripts/analyze_modules_columns_old.py**

- Line 183: `# UPDATE SET`

### Unknown

Total accesses: 377

**dashboard/dashboard.py**

- Line 103: `df_ops = pd.read_sql_query(`
- Line 107: `SELECT e.date as date, 'Recette évènement', er.source, er.montant`
- Line 115: `SELECT e.date as date, 'Dépense évènement', ed.categorie, -ed.montant`

**db/db.py**

- Line 42: `conn.execute("PRAGMA journal_mode=WAL;")`
- Line 43: `conn.execute("PRAGMA busy_timeout=5000;")`
- Line 81: `c.execute("""`
- Line 101: `c.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition};")`
- Line 282: `c.execute("""`
- Line 294: `c.execute("""`
- Line 301: `c.execute("""`
- Line 310: `c.execute("""`
- Line 319: `c.execute("""`
- Line 332: `c.execute("""`
- Line 341: `c.execute("""`
- Line 354: `c.execute("""`
- Line 364: `c.execute("""`
- Line 382: `c.execute("""`
- Line 400: `c.execute("""`
- Line 409: `c.execute("""`
- Line 419: `c.execute("""`
- Line 433: `c.execute("""`
- Line 442: `c.execute("""`
- Line 453: `c.execute("""`
- Line 460: `c.execute("""`
- Line 468: `c.execute("""`
- Line 479: `c.execute("""`
- Line 493: `c.execute("""`
- Line 502: `c.execute("""`
- Line 513: `c.execute("""`
- Line 525: `c.execute("""`
- Line 547: `c.execute("""`
- Line 553: `c.execute("""`
- Line 565: `c.execute("""`
- Line 571: `c.execute("""`
- Line 583: `c.execute("""`
- Line 596: `c.execute("""`
- Line 606: `c.execute("""`
- Line 616: `c.execute("""`
- Line 629: `c.execute("""`
- Line 691: `df = pd.read_sql_query(table_or_query, conn)`
- Line 697: `df = pd.read_sql_query(f"SELECT * FROM {table_or_query}", conn)`

**dialogs/cloture_confirm_dialog.py**

- Line 28: `conn.execute(f"DELETE FROM {tab}")`

**dialogs/depense_dialog.py**

- Line 155: `row = conn.execute(f"SELECT * FROM {self.table} WHERE id=?", (self.depense_id,)).fetchone()`
- Line 231: `req = f"UPDATE {self.table} SET {sets} WHERE id=?"`
- Line 236: `req = f"INSERT INTO {self.table} ({champs}) VALUES ({q})"`

**exports/export_bilan_argumente.py**

- Line 67: `events_df = pd.read_sql_query(`
- Line 73: `recettes_events = pd.read_sql_query("""`
- Line 74: `SELECT`
- Line 82: `recettes_subventions = pd.read_sql_query("""`
- Line 83: `SELECT`
- Line 92: `depenses_events = pd.read_sql_query("""`
- Line 93: `SELECT`
- Line 101: `depenses_regulieres = pd.read_sql_query("""`
- Line 102: `SELECT`
- Line 110: `depenses_diverses = pd.read_sql_query("""`
- Line 111: `SELECT`
- Line 133: `# Create PDF document`
- Line 377: `events_df = pd.read_sql_query(`
- Line 382: `recettes_events = pd.read_sql_query("""`
- Line 383: `SELECT source, SUM(montant) as total, COUNT(*) as count`
- Line 387: `recettes_subventions = pd.read_sql_query("""`
- Line 388: `SELECT type_entite as source, SUM(montant) as total, COUNT(*) as count`
- Line 392: `depenses_events = pd.read_sql_query("""`
- Line 393: `SELECT categorie, SUM(montant) as total, COUNT(*) as count`
- Line 397: `depenses_regulieres = pd.read_sql_query("""`
- Line 398: `SELECT categorie, SUM(montant) as total, COUNT(*) as count`
- Line 402: `depenses_diverses = pd.read_sql_query("""`
- Line 403: `SELECT categorie, SUM(montant) as total, COUNT(*) as count`
- Line 421: `# Create Word document`

**exports/exports.py**

- Line 181: `# Create table`
- Line 248: `SELECT COALESCE(SUM(montant), 0) as total`
- Line 257: `SELECT COALESCE(SUM(montant), 0) as total`
- Line 273: `# Create PDF document`

**init_db.py**

- Line 16: `FOREIGN KEY(event_id) REFERENCES events(id) ON DELETE CASCADE`
- Line 24: `FOREIGN KEY(module_id) REFERENCES event_modules(id) ON DELETE CASCADE`
- Line 33: `FOREIGN KEY(module_id) REFERENCES event_modules(id) ON DELETE CASCADE,`
- Line 34: `FOREIGN KEY(field_id) REFERENCES event_module_fields(id) ON DELETE CASCADE`

**lib/db_articles.py**

- Line 15: `- create_article: Create a new article`
- Line 124: `cursor.execute("""`
- Line 125: `SELECT id, name, categorie, unite, contenance, commentaire, stock, purchase_price`
- Line 131: `cursor.execute("""`
- Line 132: `SELECT id, name, categorie, unite, contenance, commentaire, stock`
- Line 164: `cursor.execute("""`
- Line 165: `SELECT id, name, categorie, unite, contenance, commentaire, stock, purchase_price`
- Line 171: `cursor.execute("""`
- Line 172: `SELECT id, name, categorie, unite, contenance, commentaire, stock`
- Line 204: `cursor.execute("""`
- Line 205: `SELECT id, name, categorie, unite, contenance, commentaire, stock, purchase_price`
- Line 211: `cursor.execute("""`
- Line 212: `SELECT id, name, categorie, unite, contenance, commentaire, stock`
- Line 226: `Create a new article in the database.`
- Line 250: `cursor.execute("""`
- Line 256: `cursor.execute("""`
- Line 286: `cursor.execute("""`
- Line 325: `cursor.execute("""`

**modules/buvette.py**

- Line 380: `# Create treeview for stock display`

**modules/buvette_bilan_db.py**

- Line 44: `inv = conn.execute("""`
- Line 62: `rows = conn.execute("""`
- Line 63: `SELECT l.*, a.name as article_name, a.categorie, a.unite`
- Line 104: `row = conn.execute("""`
- Line 105: `SELECT SUM(montant) as recette`

**modules/buvette_bilan_dialogs.py**

- Line 18: `inv = conn.execute("""`
- Line 29: `rows = conn.execute("""`
- Line 30: `SELECT l.*, a.name as article_name, a.categorie, a.unite`
- Line 54: `row = conn.execute("""`
- Line 55: `SELECT SUM(montant) as recette`
- Line 70: `frm_select = tk.Frame(self)`

**modules/buvette_db.py**

- Line 8: `* Les SELECT ajoutent des alias (AS date, AS type, AS commentaire) pour`
- Line 119: `Insert new article.`
- Line 133: `conn.execute("""`
- Line 139: `conn.execute("""`
- Line 165: `conn.execute("""`
- Line 171: `conn.execute("""`
- Line 182: `"""Delete article by ID."""`
- Line 198: `rows = conn.execute("""`
- Line 199: `SELECT a.*, ar.name AS article_name, ar.contenance AS article_contenance`
- Line 214: `row = conn.execute("""`
- Line 215: `SELECT a.*, ar.name AS article_name, ar.contenance AS article_contenance`
- Line 238: `conn.execute("""`
- Line 246: `conn.execute("""`
- Line 280: `conn.execute("""`
- Line 289: `conn.execute("""`
- Line 304: `"""Delete achat by ID and revert stock adjustment."""`
- Line 319: `# Delete the achat`
- Line 326: `logger.info(f"Adjusted stock for article {article_id} by -{quantite} (delete purchase)")`
- Line 339: `rows = conn.execute("""`
- Line 340: `SELECT m.*,`
- Line 360: `row = conn.execute("""`
- Line 361: `SELECT m.*,`
- Line 377: `"""Insert new mouvement."""`
- Line 381: `conn.execute("""`
- Line 395: `conn.execute("""`
- Line 405: `"""Delete mouvement by ID."""`
- Line 421: `rows = conn.execute("""`
- Line 422: `SELECT l.*, ar.name AS article_name, ar.contenance AS article_contenance`
- Line 434: `"""Insert new inventory line."""`
- Line 438: `conn.execute("""`
- Line 452: `conn.execute("""`
- Line 462: `"""Delete inventory line by ID."""`
- Line 493: `cursor = conn.execute("PRAGMA table_info(buvette_articles)")`
- Line 544: `cursor = conn.execute("PRAGMA table_info(buvette_articles)")`

**modules/buvette_inventaire_db.py**

- Line 37: `rows = conn.execute("""`
- Line 38: `SELECT i.*, e.name as event_name, e.date as event_date`
- Line 53: `row = conn.execute("""`
- Line 54: `SELECT i.*, e.name as event_name, e.date as event_date`
- Line 65: `"""Insert new inventaire, returns ID of created record."""`
- Line 70: `cur.execute("""`
- Line 86: `conn.execute("""`
- Line 133: `Current: revert_inventory_effect() → delete records → recompute_stock()`
- Line 134: `Alternative could be: get affected articles → delete → recompute only`
- Line 145: `rows = conn.execute("""`
- Line 146: `SELECT DISTINCT article_id`
- Line 166: `conn.execute("PRAGMA foreign_keys = ON;")`
- Line 176: `cur.execute("BEGIN")`
- Line 181: `cur.execute(f"DELETE FROM {table} WHERE {fk_col} = ?", (inv_id,))`
- Line 182: `# Finally delete the parent`
- Line 215: `rows = conn.execute("""`
- Line 216: `SELECT l.*, a.name as article_name`
- Line 228: `"""Insert new inventory line."""`
- Line 232: `conn.execute("""`
- Line 246: `conn.execute("""`
- Line 257: `Delete inventory line by ID and recompute stock for the affected article.`
- Line 288: `# Delete the line`
- Line 312: `cur.execute("""`
- Line 317: `cur.execute("""`
- Line 322: `cur.execute("""`
- Line 355: `Example usage in inventory create flow:`
- Line 357: `# ... insert inventory lines ...`

**modules/buvette_inventaire_dialogs.py**

- Line 39: `# Create UI`
- Line 49: `"""Create the header section with date, type, event, and comment fields."""`
- Line 87: `"""Create the lines section with Treeview and add/remove buttons."""`
- Line 133: `"""Create the bottom button section."""`
- Line 304: `cursor.execute("PRAGMA table_info(buvette_articles)")`
- Line 354: `"""Create dialog widgets."""`
- Line 358: `# Checkbox to create new article`
- Line 366: `# Select existing article`
- Line 438: `# Create new article`
- Line 447: `# Insert new article using existing function`

**modules/buvette_mouvements_db.py**

- Line 10: `- Added SELECT aliases for UI compatibility (date_mouvement AS date, etc.)`
- Line 37: `rows = conn.execute("""`
- Line 38: `SELECT m.id, m.article_id, m.quantite, m.event_id,`
- Line 63: `row = conn.execute("""`
- Line 64: `SELECT m.id, m.article_id, m.quantite, m.event_id,`
- Line 82: `"""Insert new mouvement."""`
- Line 86: `conn.execute("""`
- Line 100: `conn.execute("""`
- Line 110: `"""Delete mouvement by ID."""`

**modules/categories.py**

- Line 43: `df = pd.read_sql_query("""`
- Line 44: `SELECT c.id, c.name, p.name as parent`

**modules/cloture_exercice.py**

- Line 66: `df = pd.read_sql_query(f"SELECT * FROM {tab}", conn)`

**modules/db_api.py**

- Line 63: `conn.execute("PRAGMA journal_mode=WAL;")`
- Line 64: `conn.execute("PRAGMA busy_timeout=5000;")`

**modules/depots_retraits_banque.py**

- Line 50: `df = pd.read_sql_query(query, get_connection(), params=(banque,))`

**modules/event_module_data.py**

- Line 40: `df = pd.read_sql_query(`

**modules/exports.py**

- Line 50: `recettes = pd.read_sql_query(`
- Line 55: `depenses = pd.read_sql_query(`
- Line 60: `caisses = pd.read_sql_query(`
- Line 246: `depenses = pd.read_sql_query("""`
- Line 247: `SELECT`
- Line 258: `SELECT`

**modules/historique_inventaire.py**

- Line 48: `df = pd.read_sql_query(`
- Line 50: `SELECT i.id, i.date_inventaire as date, e.name as evenement, i.commentaire,`
- Line 107: `SELECT l.stock_id, s.name, c.name as categorie, l.quantite_constatee`

**modules/inventaire.py**

- Line 63: `self.stock_df = pd.read_sql_query("""`
- Line 64: `SELECT s.id as stock_id, s.name, c.name as categorie, s.quantite`
- Line 102: `# Insert inventaire`
- Line 107: `inv_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]`
- Line 108: `# Insert lignes`

**modules/journal.py**

- Line 86: `df = pd.read_sql_query("""`
- Line 89: `SELECT e.date as date, 'Recette évènement', er.source, er.montant, er.commentaire`
- Line 97: `SELECT e.date as date, 'Dépense évènement', ed.categorie, -ed.montant, ed.commentaire`

**modules/model_colonnes.py**

- Line 11: `conn.execute("""`
- Line 18: `conn.execute("""`

**modules/mouvements_stock.py**

- Line 36: `df = pd.read_sql_query("""`
- Line 37: `SELECT m.id, m.date, s.name, m.type, m.quantite, m.prix_achat_total, m.prix_unitaire, m.date_perempt`

**modules/stock.py**

- Line 43: `df = pd.read_sql_query("""`
- Line 44: `SELECT s.id, s.name, c.name as categorie, s.quantite, s.seuil_alerte, s.date_peremption, s.lot, s.co`

**modules/stock_db.py**

- Line 38: `# Create inventory stock journal table`
- Line 39: `conn.execute("""`
- Line 54: `conn.execute("""`
- Line 197: `SELECT article_id, quantite`
- Line 229: `cursor.execute("""`
- Line 266: `rows = cursor.execute("""`
- Line 285: `# Delete journal entries for this inventory`
- Line 312: `rows = conn.execute("""`
- Line 313: `SELECT j.*, a.name as article_name`
- Line 342: `cursor.execute("""`
- Line 381: `rows = cursor.execute("""`
- Line 382: `SELECT id, remaining_quantity, unit_price`
- Line 406: `cursor.execute("""`
- Line 489: `rows = cursor.execute("""`
- Line 490: `SELECT type_mouvement, quantite`

**modules/stock_inventaire.py**

- Line 43: `SELECT s.id, s.name, c.name as categorie, s.quantite`
- Line 48: `df = pd.read_sql_query(query, conn)`

**modules/stock_stats.py**

- Line 15: `df = pd.read_sql_query("""`
- Line 16: `SELECT c.name as categorie, COUNT(s.id) as nb_articles, SUM(s.quantite) as total_qte`

**modules/stock_tab.py**

- Line 85: `# Build SELECT clause based on available columns`
- Line 116: `SELECT {select_clause}`

**scripts/analyze_modules_columns.py**

- Line 174: `"""Extrait les tables depuis SELECT statements (colonnes depuis liste explicite)."""`
- Line 183: `# Register the table (even with SELECT *)`
- Line 186: `# If not SELECT *, try to extract column names`
- Line 198: `# Pattern: CREATE TABLE [IF NOT EXISTS] table_name (columns...)`
- Line 342: `f.write("*Aucune colonne specifique detectee (possiblement SELECT \\*)*\n")`

**scripts/analyze_modules_columns_old.py**

- Line 46: `# SELECT queries`
- Line 48: `# INSERT INTO`
- Line 52: `# ALTER TABLE`
- Line 54: `# CREATE TABLE`
- Line 159: `# SELECT FROM`
- Line 173: `# INSERT INTO`
- Line 200: `# CREATE TABLE`
- Line 338: `f.write("*Aucune colonne spécifique détectée (possiblement SELECT \\*)*\n")`

**scripts/apply_migrations.py**

- Line 48: `Create a backup of the database.`
- Line 75: `cursor.execute(f"SELECT filename FROM {MIGRATIONS_TABLE}")`
- Line 111: `conn.execute("BEGIN")`
- Line 118: `f"INSERT INTO {MIGRATIONS_TABLE} (filename, applied_at) VALUES (?, ?)",`
- Line 155: `cursor.execute(f"SELECT filename, applied_at FROM {MIGRATIONS_TABLE} ORDER BY id")`
- Line 219: `conn.execute(f"DELETE FROM {MIGRATIONS_TABLE} WHERE filename = ?", (args.force,))`
- Line 222: `# Create backup`
- Line 249: `# Create backup before applying`

**scripts/audit_db_usage.py**

- Line 309: `# Create auditor and scan`
- Line 313: `# Create reports directory if it doesn't exist`

**scripts/auto_fix_buvette_rows.py**

- Line 75: `# Insert after the last import`
- Line 80: `# No imports found, insert at top after docstring`
- Line 134: `"""Create a unified diff string."""`
- Line 151: `Process a single file: create backup, inject conversions, create diff.`
- Line 185: `# Create backup`
- Line 193: `# Create diff file`

**scripts/check_buvette.py**

- Line 137: `# Pattern 1: INSERT avec 'date' au lieu de 'date_mouvement'`
- Line 141: `issues.append(f"Ligne {i}: INSERT utilise 'date' au lieu de 'date_mouvement'")`
- Line 158: `# Pattern 4: SELECT sans alias AS date, AS type`

**scripts/create_compat_views.py**

- Line 2: `Create compatibility views for backward compatibility after articles migration.`
- Line 17: `"""Create compatibility view for buvette_articles."""`
- Line 22: `cur = conn.execute("PRAGMA table_info(buvette_articles)")`
- Line 28: `# Drop existing view if it exists`
- Line 29: `conn.execute("DROP VIEW IF EXISTS buvette_articles_compat")`
- Line 31: `# Create compatibility view that exposes 'unite' as alias for 'unite_type'`
- Line 32: `conn.execute("""`
- Line 33: `CREATE VIEW buvette_articles_compat AS`
- Line 34: `SELECT`
- Line 63: `description="Create compatibility views for backward compatibility"`

**scripts/db_diagnostics.py**

- Line 89: `cursor.execute("PRAGMA journal_mode;")`
- Line 112: `cursor.execute("PRAGMA busy_timeout;")`
- Line 134: `cursor.execute("PRAGMA integrity_check;")`
- Line 154: `cursor.execute("SELECT 1;")`
- Line 190: `cursor.execute("""`
- Line 220: `cursor.execute(f"SELECT COUNT(*) FROM {quoted_table};")`

**scripts/enable_wal.py**

- Line 50: `cursor.execute("PRAGMA journal_mode;")`
- Line 61: `cursor.execute("PRAGMA journal_mode=WAL;")`
- Line 71: `cursor.execute("PRAGMA synchronous=NORMAL;")`
- Line 75: `cursor.execute("PRAGMA synchronous;")`

**scripts/find_missing_columns.py**

- Line 92: `# Find SELECT statements`
- Line 104: `# Find INSERT statements`
- Line 238: `report_lines.append("2. Create migration scripts for confirmed missing columns")`
- Line 272: `# Create empty database`

**scripts/generate_audit_reports.py**

- Line 38: `re.compile(r'read_sql', re.IGNORECASE),`

**scripts/migrate_add_purchase_price.py**

- Line 33: `Create a backup of the database file.`
- Line 61: `cursor.execute("PRAGMA journal_mode=WAL;")`
- Line 65: `cursor.execute("PRAGMA synchronous=NORMAL;")`
- Line 85: `# Create backup`
- Line 89: `print(f"✗ Failed to create backup. Migration aborted for safety.")`
- Line 99: `cursor.execute("BEGIN TRANSACTION;")`
- Line 102: `cursor.execute("""`
- Line 118: `cursor.execute("PRAGMA table_info(buvette_articles)")`

**scripts/migrate_articles_unite_to_quantite.py**

- Line 34: `conn.execute("PRAGMA foreign_keys = ON;")`
- Line 44: `cur.execute("BEGIN")`
- Line 46: `# Create new table: adapt columns to match your real schema if needed`
- Line 47: `cur.execute("""`
- Line 62: `old_cols = [r[1] for r in conn.execute("PRAGMA table_info(buvette_articles)").fetchall()]`
- Line 65: `# Build both INSERT columns and SELECT expressions dynamically`

**scripts/project_audit.py**

- Line 587: `report.append("   - Create issues for important TODOs")`
- Line 611: `report.append("# Create and activate virtual environment (optional but recommended)")`

**scripts/safe_add_columns.py**

- Line 44: `Create a backup of the database.`
- Line 136: `sql = f"ALTER TABLE {table} ADD COLUMN {column} {column_type} DEFAULT {default}"`
- Line 254: `# Create backup`

**scripts/update_db_structure.py**

- Line 509: `self.log(f"Failed to create backup: {e}", "ERROR")`
- Line 551: `cursor.execute("SELECT sqlite_version()")`
- Line 651: `# SQLite ne supporte pas toujours les transactions pour ALTER TABLE,`
- Line 653: `cursor.execute("BEGIN TRANSACTION")`
- Line 665: `rename_sql = f"ALTER TABLE {table} RENAME COLUMN {fuzzy_match} TO {col_name}"`
- Line 680: `alter_sql = f"ALTER TABLE {table} ADD COLUMN {quoted_col} {col_type}"`
- Line 682: `alter_sql = f"ALTER TABLE {table} ADD COLUMN {quoted_col} {col_type} DEFAULT {default_value}"`
- Line 692: `copy_sql = f"UPDATE {table} SET {quoted_new} = {quoted_old}"`
- Line 712: `alter_sql = f"ALTER TABLE {table} ADD COLUMN {quoted_col} {col_type}"`
- Line 714: `alter_sql = f"ALTER TABLE {table} ADD COLUMN {quoted_col} {col_type} DEFAULT {default_value}"`
- Line 752: `cursor.execute("PRAGMA journal_mode=WAL")`
- Line 761: `cursor.execute("PRAGMA synchronous=NORMAL")`
- Line 769: `cursor.execute("ANALYZE")`
- Line 883: `self.log("Database Structure Update - Smart Migration with Fuzzy Matching")`
- Line 897: `self.log("Migration aborted: could not create backup", "ERROR")`

**scripts/update_db_structure_old.py**

- Line 469: `self.log(f"Failed to create backup: {e}", "ERROR")`
- Line 511: `cursor.execute("SELECT sqlite_version()")`
- Line 605: `# SQLite ne supporte pas toujours les transactions pour ALTER TABLE,`
- Line 607: `cursor.execute("BEGIN TRANSACTION")`
- Line 619: `rename_sql = f"ALTER TABLE {table} RENAME COLUMN {fuzzy_match} TO {col_name}"`
- Line 634: `alter_sql = f"ALTER TABLE {table} ADD COLUMN {quoted_col} {col_type}"`
- Line 636: `alter_sql = f"ALTER TABLE {table} ADD COLUMN {quoted_col} {col_type} DEFAULT {default_value}"`
- Line 646: `copy_sql = f"UPDATE {table} SET {quoted_new} = {quoted_old}"`
- Line 666: `alter_sql = f"ALTER TABLE {table} ADD COLUMN {quoted_col} {col_type}"`
- Line 668: `alter_sql = f"ALTER TABLE {table} ADD COLUMN {quoted_col} {col_type} DEFAULT {default_value}"`
- Line 706: `cursor.execute("PRAGMA journal_mode=WAL")`
- Line 715: `cursor.execute("PRAGMA synchronous=NORMAL")`
- Line 723: `cursor.execute("ANALYZE")`
- Line 817: `self.log("Database Structure Update - Smart Migration with Fuzzy Matching")`
- Line 831: `self.log("Migration aborted: could not create backup", "ERROR")`

**src/db/compat.py**

- Line 39: `_conn.execute("PRAGMA journal_mode=WAL;")`
- Line 40: `_conn.execute("PRAGMA busy_timeout=5000;")`
- Line 55: `cur.execute("BEGIN")`

**src/db/connection.py**

- Line 54: `conn.execute("PRAGMA foreign_keys = ON;")`
- Line 56: `conn.execute("PRAGMA journal_mode = WAL;")`
- Line 59: `conn.execute("PRAGMA synchronous = NORMAL;")`
- Line 86: `cur.execute("BEGIN")`

**src/services/inventory_service.py**

- Line 57: `f"SELECT id, {product_col} AS product_id, {qty_col} AS qty, {inv_fk} as inventaire_id "`
- Line 91: `# Build INSERT based on available columns`
- Line 95: `f"INSERT INTO {table_name} (name, created_at) VALUES (?, CURRENT_TIMESTAMP)",`
- Line 101: `f"INSERT INTO {table_name} (date_inventaire, event_id, commentaire) VALUES (CURRENT_TIMESTAMP, ?, ?)`
- Line 106: `cur.execute(f"INSERT INTO {table_name} DEFAULT VALUES")`

**ui/article_dialog.py**

- Line 59: `"""Create the form fields."""`
- Line 153: `# Create new article`

**ui/inventory_lines_dialog.py**

- Line 86: `"""Create the header section with date, type, event, and comment fields."""`
- Line 133: `"""Create the lines section with Treeview and buttons."""`
- Line 194: `"""Create the bottom button section."""`
- Line 306: `# Try to find and select the event in combobox`
- Line 383: `# Delete existing lines`
- Line 388: `# Insert mode: Create new inventory`
- Line 396: `# Insert line (with commentaire column for consistency)`
- Line 397: `cursor.execute("""`
- Line 469: `"""Create the UI elements."""`
- Line 584: `# Try to select the article`
- Line 646: `# Create new article`

**utils/cloture_exercice.py**

- Line 33: `df = pd.read_sql_query(f"SELECT * FROM {table}", conn)`

**utils/db_operations.py**

- Line 52: `Execute a SELECT query and return results as list of dicts.`
- Line 55: `query: SQL SELECT query`
- Line 100: `Execute an INSERT statement and return the new row ID.`
- Line 122: `query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"`
- Line 156: `query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"`
- Line 167: `Execute a DELETE statement and return the number of affected rows.`
- Line 184: `query = f"DELETE FROM {table} WHERE {where_clause}"`

### article

Total accesses: 6

**modules/buvette_db.py**

- Line 243: `# Update article's purchase_price if prix_unitaire is provided`
- Line 286: `# Update article's purchase_price if prix_unitaire is provided`

**modules/buvette_inventaire_dialogs.py**

- Line 284: `# Update article stock if quantite field exists (legacy support)`
- Line 299: `"""Update article stock based on inventory quantities (if quantite field exists)."""`
- Line 328: `logger.warning(f"Could not update article stock: {e}")`

**ui/inventory_lines_dialog.py**

- Line 402: `# Update article stock (stock = quantity counted)`

### article_purchase_batches

Total accesses: 2

**modules/stock_db.py**

- Line 343: `INSERT INTO article_purchase_batches`
- Line 407: `UPDATE article_purchase_batches`

### articles

Total accesses: 7

**modules/db_api.py**

- Line 45: `>>> cursor.execute("SELECT * FROM articles")`
- Line 92: `>>> article = query_one("SELECT * FROM articles WHERE id = ?", (1,))`
- Line 147: `>>> articles = query_all("SELECT * FROM articles WHERE categorie = ?", ('Boisson',))`
- Line 199: `>>>     cursor.execute("INSERT INTO articles (...) VALUES (...)")`
- Line 245: `...     "UPDATE articles SET stock = ? WHERE id = ?",`
- Line 310: `...     "UPDATE articles SET stock = ? WHERE id = ?",`

**ui/dialogs/base_list_dialog.py**

- Line 81: `...     "SELECT id, name, categorie FROM articles",`

### automatique

Total accesses: 1

**modules/event_recettes.py**

- Line 46: `logger.error(f"Erreur lors de l'update automatique 'Vente sur place': {e}")`

### avec

Total accesses: 2

**scripts/check_buvette.py**

- Line 144: `# Pattern 2: UPDATE avec 'date=' au lieu de 'date_mouvement='`
- Line 151: `# Pattern 3: UPDATE avec 'type=' au lieu de 'type_mouvement='`

### batch

Total accesses: 1

**modules/stock_db.py**

- Line 404: `# Update batch remaining quantity`

### buvette_achats

Total accesses: 6

**modules/buvette_bilan_db.py**

- Line 82: `q = "SELECT SUM(quantite*prix_unitaire) as total, SUM(quantite) as qte FROM buvette_achats WHERE art`

**modules/buvette_bilan_dialogs.py**

- Line 41: `q = "SELECT SUM(quantite*prix_unitaire) as total, SUM(quantite) as qte FROM buvette_achats WHERE art`

**modules/buvette_db.py**

- Line 239: `INSERT INTO buvette_achats (article_id, date_achat, quantite, prix_unitaire, fournisseur, facture, e`
- Line 281: `UPDATE buvette_achats SET article_id=?, date_achat=?, quantite=?, prix_unitaire=?,`
- Line 311: `"SELECT article_id, quantite FROM buvette_achats WHERE id=?",`
- Line 320: `conn.execute("DELETE FROM buvette_achats WHERE id=?", (achat_id,))`

### buvette_articles

Total accesses: 24

**lib/db_articles.py**

- Line 251: `INSERT INTO buvette_articles (name, categorie, unite, contenance, commentaire, stock, purchase_price`
- Line 257: `INSERT INTO buvette_articles (name, categorie, unite, contenance, commentaire, stock)`
- Line 287: `UPDATE buvette_articles`
- Line 326: `UPDATE buvette_articles`

**modules/buvette_db.py**

- Line 100: `rows = conn.execute("SELECT * FROM buvette_articles ORDER BY name").fetchall()`
- Line 111: `row = conn.execute("SELECT * FROM buvette_articles WHERE id=?", (article_id,)).fetchone()`
- Line 134: `INSERT INTO buvette_articles (name, categorie, unite_type, commentaire, contenance, purchase_price)`
- Line 140: `INSERT INTO buvette_articles (name, categorie, unite, commentaire, contenance, purchase_price)`
- Line 166: `UPDATE buvette_articles SET name=?, categorie=?, unite_type=?, commentaire=?, contenance=?, purchase`
- Line 172: `UPDATE buvette_articles SET name=?, categorie=?, unite=?, commentaire=?, contenance=?, purchase_pric`
- Line 186: `conn.execute("DELETE FROM buvette_articles WHERE id=?", (article_id,))`
- Line 247: `UPDATE buvette_articles`
- Line 290: `UPDATE buvette_articles`
- Line 478: `rows = conn.execute("SELECT id, name, contenance FROM buvette_articles ORDER BY name").fetchall()`
- Line 497: `conn.execute("ALTER TABLE buvette_articles ADD COLUMN stock INTEGER DEFAULT 0")`
- Line 524: `conn.execute("UPDATE buvette_articles SET stock=? WHERE id=?", (stock, article_id))`
- Line 548: `row = conn.execute("SELECT stock FROM buvette_articles WHERE id=?", (article_id,)).fetchone()`

**modules/buvette_inventaire_dialogs.py**

- Line 319: `"UPDATE buvette_articles SET quantite=? WHERE id=?",`

**modules/buvette_mouvements_db.py**

- Line 126: `rows = conn.execute("SELECT id, name FROM buvette_articles ORDER BY name").fetchall()`

**modules/stock_db.py**

- Line 94: `"SELECT stock FROM buvette_articles WHERE id=?",`
- Line 116: `"UPDATE buvette_articles SET stock=? WHERE id=?",`

**scripts/migrate_add_purchase_price.py**

- Line 130: `cursor.execute("ALTER TABLE buvette_articles ADD COLUMN purchase_price REAL")`

**scripts/migrate_articles_unite_to_quantite.py**

- Line 125: `cur.execute("DROP TABLE buvette_articles;")`

**scripts/migration.py**

- Line 30: `"ALTER TABLE buvette_articles ADD COLUMN purchase_price REAL"`

### buvette_articles_new

Total accesses: 3

**scripts/migrate_articles_unite_to_quantite.py**

- Line 48: `CREATE TABLE buvette_articles_new (`
- Line 117: `copy_sql = f"INSERT INTO buvette_articles_new ({insert_sql}) SELECT {select_sql} FROM buvette_articl`
- Line 126: `cur.execute("ALTER TABLE buvette_articles_new RENAME TO buvette_articles;")`

### buvette_inventaire_lignes

Total accesses: 12

**modules/buvette_db.py**

- Line 439: `INSERT INTO buvette_inventaire_lignes (inventaire_id, article_id, quantite, commentaire)`
- Line 453: `UPDATE buvette_inventaire_lignes SET article_id=?, quantite=?, commentaire=?`
- Line 466: `conn.execute("DELETE FROM buvette_inventaire_lignes WHERE id=?", (ligne_id,))`

**modules/buvette_inventaire_db.py**

- Line 233: `INSERT INTO buvette_inventaire_lignes (inventaire_id, article_id, quantite, commentaire)`
- Line 247: `UPDATE buvette_inventaire_lignes SET article_id=?, quantite=?, commentaire=?`
- Line 278: `"SELECT article_id FROM buvette_inventaire_lignes WHERE id=?",`
- Line 289: `conn.execute("DELETE FROM buvette_inventaire_lignes WHERE id=?", (ligne_id,))`
- Line 313: `SELECT id FROM buvette_inventaire_lignes WHERE inventaire_id=? AND article_id=?`
- Line 318: `UPDATE buvette_inventaire_lignes SET quantite=?, commentaire=?`
- Line 323: `INSERT INTO buvette_inventaire_lignes (inventaire_id, article_id, quantite, commentaire)`

**ui/inventory_lines_dialog.py**

- Line 384: `cursor.execute("DELETE FROM buvette_inventaire_lignes WHERE inventaire_id=?", (self.inventory_id,))`
- Line 398: `INSERT INTO buvette_inventaire_lignes (inventaire_id, article_id, quantite, commentaire)`

### buvette_inventaires

Total accesses: 5

**modules/buvette_bilan_db.py**

- Line 45: `SELECT * FROM buvette_inventaires`

**modules/buvette_bilan_dialogs.py**

- Line 19: `SELECT * FROM buvette_inventaires`

**modules/buvette_inventaire_db.py**

- Line 71: `INSERT INTO buvette_inventaires (date_inventaire, event_id, type_inventaire, commentaire)`
- Line 87: `UPDATE buvette_inventaires SET date_inventaire=?, event_id=?, type_inventaire=?, commentaire=?`
- Line 183: `cur.execute("DELETE FROM buvette_inventaires WHERE id = ?", (inv_id,))`

### buvette_mouvements

Total accesses: 6

**modules/buvette_db.py**

- Line 382: `INSERT INTO buvette_mouvements (date_mouvement, article_id, type_mouvement, quantite, motif)`
- Line 396: `UPDATE buvette_mouvements SET date_mouvement=?, article_id=?, type_mouvement=?, quantite=?, motif=?`
- Line 409: `conn.execute("DELETE FROM buvette_mouvements WHERE id=?", (mvt_id,))`

**modules/buvette_mouvements_db.py**

- Line 87: `INSERT INTO buvette_mouvements (article_id, date_mouvement, type_mouvement, quantite, motif, event_i`
- Line 101: `UPDATE buvette_mouvements SET article_id=?, date_mouvement=?, type_mouvement=?, quantite=?, motif=?,`
- Line 114: `conn.execute("DELETE FROM buvette_mouvements WHERE id=?", (mvt_id,))`

### categories

Total accesses: 8

**dialogs/edit_stock_dialog.py**

- Line 58: `df = pd.read_sql_query("SELECT id, name FROM categories ORDER BY name", conn)`

**modules/categories.py**

- Line 73: `cur.execute("INSERT INTO categories (name, parent_id) VALUES (?, ?)", (data['name'], data['parent_id`
- Line 94: `"UPDATE categories SET name=?, parent_id=? WHERE id=?",`
- Line 111: `cur.execute("SELECT COUNT(*) FROM categories WHERE parent_id=?", (cat_id,))`
- Line 122: `cur.execute("DELETE FROM categories WHERE id=?", (cat_id,))`
- Line 130: `df_cat = pd.read_sql_query("SELECT id, name FROM categories WHERE parent_id IS NULL", conn)`

**modules/stock.py**

- Line 139: `cats = conn.execute("SELECT name FROM categories ORDER BY name").fetchall()`
- Line 167: `row = conn.execute("SELECT id FROM categories WHERE name=?", (cat,)).fetchone()`

### child

Total accesses: 1

**modules/buvette_inventaire_db.py**

- Line 177: `# Delete from child tables first`

### code

Total accesses: 1

**scripts/find_missing_columns.py**

- Line 240: `report_lines.append("4. Update code to handle missing columns gracefully if not migrating")`

### colonnes_modeles

Total accesses: 7

**dialogs/edit_field_dialog.py**

- Line 54: `rows = conn.execute("SELECT name FROM colonnes_modeles ORDER BY name").fetchall()`

**modules/event_modules.py**

- Line 357: `row = conn.execute("SELECT id FROM colonnes_modeles WHERE name=?", (modele_colonne_nom,)).fetchone()`

**modules/model_colonnes.py**

- Line 31: `res = conn.execute("SELECT * FROM colonnes_modeles ORDER BY name").fetchall()`
- Line 44: `cur.execute("INSERT OR IGNORE INTO colonnes_modeles (name, type_modele) VALUES (?, ?)", (name, typ))`
- Line 45: `modele_id = cur.execute("SELECT id FROM colonnes_modeles WHERE name=?", (name,)).fetchone()["id"]`
- Line 93: `conn.execute("DELETE FROM colonnes_modeles WHERE id=?", (modele_id,))`
- Line 137: `c = conn.execute("SELECT * FROM colonnes_modeles WHERE id=?", (modele_id,)).fetchone()`

### comptes

Total accesses: 3

**db/db.py**

- Line 88: `c.execute("SELECT COUNT(*) as n FROM comptes")`
- Line 93: `c.execute("INSERT INTO comptes (name, solde) VALUES (?, ?)", ("Banque Principale", row["solde_report`
- Line 677: `c.execute("INSERT OR IGNORE INTO comptes (name, solde) VALUES (?, ?)", ("Banque Principale", row["so`

### config

Total accesses: 10

**db/db.py**

- Line 90: `c.execute("SELECT solde_report FROM config ORDER BY id DESC LIMIT 1")`
- Line 654: `c.execute("SELECT COUNT(*) FROM config")`
- Line 670: `"INSERT INTO config (exercice, date, date_fin, disponible_banque) VALUES (?, ?, ?, ?)",`
- Line 674: `c.execute("SELECT solde_report FROM config ORDER BY id DESC LIMIT 1")`

**main.py**

- Line 64: `cur.execute("SELECT exercice, date FROM config ORDER BY id DESC LIMIT 1")`
- Line 79: `"UPDATE config SET exercice=?, date=?, disponible_banque=? WHERE id=(SELECT id FROM config ORDER BY `
- Line 201: `cur.execute("SELECT * FROM config ORDER BY id DESC LIMIT 1")`

**modules/journal.py**

- Line 81: `row = conn.execute("SELECT solde_report FROM config ORDER BY id DESC LIMIT 1").fetchone()`

**modules/solde_ouverture.py**

- Line 26: `row = conn.execute("SELECT solde_report FROM config ORDER BY id DESC LIMIT 1").fetchone()`
- Line 41: `conn.execute("UPDATE config SET solde_report=? WHERE id=(SELECT MAX(id) FROM config)", (float_val,))`

### depenses_diverses

Total accesses: 5

**dashboard/dashboard.py**

- Line 113: `SELECT date_depense as date, 'Dépense diverse', commentaire, -montant FROM depenses_diverses`

**exports/exports.py**

- Line 263: `SELECT montant FROM depenses_diverses`

**modules/depenses_diverses.py**

- Line 124: `conn.execute("DELETE FROM depenses_diverses WHERE id = ?", (id_,))`
- Line 134: `"SELECT id, categorie, module_id, montant, fournisseur, date_depense, paye_par, membre_id, statut_re`

**modules/journal.py**

- Line 95: `SELECT date_depense as date, 'Dépense diverse', commentaire, -montant, commentaire AS justificatif F`

### depenses_regulieres

Total accesses: 5

**dashboard/dashboard.py**

- Line 111: `SELECT date_depense as date, 'Dépense régulière', categorie, -montant FROM depenses_regulieres`

**exports/exports.py**

- Line 261: `SELECT montant FROM depenses_regulieres`

**modules/depenses_regulieres.py**

- Line 124: `conn.execute("DELETE FROM depenses_regulieres WHERE id = ?", (id_,))`
- Line 134: `"SELECT id, categorie, module_id, montant, fournisseur, date_depense, paye_par, membre_id, statut_re`

**modules/journal.py**

- Line 93: `SELECT date_depense as date, 'Dépense régulière', categorie, -montant, commentaire AS justificatif F`

### depots_retraits_banque

Total accesses: 6

**modules/depots_retraits_banque.py**

- Line 47: `query = "SELECT * FROM depots_retraits_banque"`
- Line 54: `banques = sorted(get_df_or_sql("SELECT DISTINCT banque FROM depots_retraits_banque WHERE banque IS N`
- Line 114: `"""INSERT INTO depots_retraits_banque (date, type, montant, reference, banque, commentaire)`
- Line 143: `c.execute("DELETE FROM depots_retraits_banque WHERE id=?", (id_,))`
- Line 155: `c.execute("SELECT pointe FROM depots_retraits_banque WHERE id=?", (id_,))`
- Line 159: `c.execute("UPDATE depots_retraits_banque SET pointe=? WHERE id=?", (new_val, id_))`

### dons_subventions

Total accesses: 10

**dashboard/dashboard.py**

- Line 105: `SELECT date, 'Recette' as type, source as libelle, montant FROM dons_subventions`

**dialogs/edit_don_dialog.py**

- Line 56: `"SELECT donateur, montant, date, commentaire FROM dons_subventions WHERE id=?", (self.don_id,)`
- Line 93: `"INSERT INTO dons_subventions (donateur, montant, date, commentaire) VALUES (?, ?, ?, ?)",`
- Line 98: `"UPDATE dons_subventions SET donateur=?, montant=?, date=?, commentaire=? WHERE id=?",`

**exports/exports.py**

- Line 252: `SELECT montant FROM dons_subventions`

**modules/dons_subventions.py**

- Line 46: `conn.execute("DELETE FROM dons_subventions WHERE id = ?", (id_,))`
- Line 57: `"SELECT id, type, source, montant, date, justificatif FROM dons_subventions ORDER BY date DESC, id D`
- Line 113: `"INSERT INTO dons_subventions (type, source, montant, date, justificatif) VALUES (?, ?, ?, ?, ?)",`

**modules/exports.py**

- Line 346: `subventions = pd.read_sql_query("SELECT * FROM dons_subventions", conn)`

**modules/journal.py**

- Line 87: `SELECT date, 'Recette' as type, source as libelle, montant, justificatif FROM dons_subventions`

### event_caisse_details

Total accesses: 9

**modules/event_caisse_details.py**

- Line 41: `"SELECT * FROM event_caisse_details WHERE caisse_id = ? ORDER BY date, id", (self.caisse_id,)`
- Line 77: `conn.execute("DELETE FROM event_caisse_details WHERE id=? AND caisse_id=?", (oid, self.caisse_id))`
- Line 123: `"SELECT * FROM event_caisse_details WHERE id=? AND caisse_id=?",`
- Line 154: `"UPDATE event_caisse_details SET date=?, type_op=?, montant=?, description=?, justificatif=? WHERE i`
- Line 159: `"INSERT INTO event_caisse_details (caisse_id, date, type_op, montant, description, justificatif) VAL`

**modules/event_recettes.py**

- Line 18: `"SELECT SUM(CASE WHEN type='cheque' THEN valeur ELSE valeur*quantite END) AS tot FROM event_caisse_d`
- Line 22: `"SELECT SUM(CASE WHEN type='cheque' THEN valeur ELSE valeur*quantite END) AS tot FROM event_caisse_d`

**modules/exports.py**

- Line 69: `"SELECT SUM(CASE WHEN type='cheque' THEN valeur ELSE valeur*quantite END) as total FROM event_caisse`
- Line 72: `"SELECT SUM(CASE WHEN type='cheque' THEN valeur ELSE valeur*quantite END) as total FROM event_caisse`

### event_caisses

Total accesses: 7

**modules/event_caisses.py**

- Line 40: `"SELECT * FROM event_caisses WHERE event_id = ? ORDER BY id", (self.event_id,)`
- Line 81: `conn.execute("DELETE FROM event_caisses WHERE id=? AND event_id=?", (cid, self.event_id))`
- Line 120: `"SELECT nom, solde_initial, responsable FROM event_caisses WHERE id=? AND event_id=?",`
- Line 147: `"UPDATE event_caisses SET nom=?, solde_initial=?, responsable=? WHERE id=? AND event_id=?",`
- Line 152: `"INSERT INTO event_caisses (event_id, nom, solde_initial, responsable) VALUES (?, ?, ?, ?)",`

**modules/event_recettes.py**

- Line 14: `caisses = conn.execute("SELECT id FROM event_caisses WHERE event_id=?", (event_id,)).fetchall()`

**modules/exports.py**

- Line 61: `"SELECT id, nom_caisse, commentaire FROM event_caisses WHERE event_id=?",`

### event_depenses

Total accesses: 9

**dashboard/dashboard.py**

- Line 135: `depenses = get_df_or_sql(f"SELECT SUM(montant) FROM event_depenses WHERE event_id={id_evt}")["SUM(mo`

**exports/exports.py**

- Line 259: `SELECT montant FROM event_depenses`

**modules/event_depenses.py**

- Line 43: `"SELECT * FROM event_depenses WHERE event_id = ? ORDER BY date, id", (self.event_id,)`
- Line 87: `conn.execute("DELETE FROM event_depenses WHERE id=? AND event_id=?", (did, self.event_id))`
- Line 135: `"SELECT * FROM event_depenses WHERE id=? AND event_id=?",`
- Line 168: `"UPDATE event_depenses SET date=?, fournisseur=?, categorie=?, montant=?, description=?, justificati`
- Line 173: `"INSERT INTO event_depenses (event_id, date, fournisseur, categorie, montant, description, justifica`

**modules/events.py**

- Line 89: `"SELECT COALESCE(SUM(montant), 0) FROM event_depenses WHERE event_id = ?", (event_id,)`

**modules/exports.py**

- Line 56: `"SELECT categorie, montant, fournisseur, date_depense, paye_par, membre_id, commentaire FROM event_d`

### event_module_data

Total accesses: 28

**dialogs/edit_module_data_dialog.py**

- Line 93: `"SELECT field_id, valeur FROM event_module_data WHERE module_id=? AND row_index=?",`
- Line 113: `"SELECT MAX(row_index) FROM event_module_data WHERE module_id=?", (self.module_id,)`
- Line 118: `conn.execute("DELETE FROM event_module_data WHERE module_id=? AND row_index=?", (self.module_id, row`
- Line 121: `"INSERT INTO event_module_data (module_id, row_index, field_id, valeur) VALUES (?, ?, ?, ?)",`

**modules/event_module_data.py**

- Line 69: `df = pd.read_sql_query("SELECT * FROM event_module_data WHERE module_id=? ORDER BY row_index", conn,`
- Line 94: `res = conn.execute("SELECT MAX(row_index) FROM event_module_data WHERE module_id=?", (self.module_id`
- Line 121: `"INSERT INTO event_module_data (module_id, row_index, field_id, valeur) VALUES (?, ?, ?, ?)",`
- Line 138: `conn.execute("DELETE FROM event_module_data WHERE module_id=? AND row_index=?", (self.module_id, row`

**modules/event_modules.py**

- Line 124: `conn.execute("DELETE FROM event_module_data WHERE module_id=?", (mid,))`
- Line 234: `"SELECT row_index FROM event_module_data WHERE module_id = ? GROUP BY row_index ORDER BY row_index",`
- Line 240: `"SELECT valeur FROM event_module_data WHERE module_id = ? AND row_index = ? AND field_id = ?",`
- Line 288: `conn.execute("DELETE FROM event_module_data WHERE module_id=? AND field_id=?", (self.module_id, fiel`
- Line 369: `"SELECT MAX(row_index) as mx FROM event_module_data WHERE module_id = ?", (self.module_id,)`
- Line 375: `"INSERT INTO event_module_data (module_id, row_index, field_id, valeur) VALUES (?, ?, ?, ?)",`
- Line 394: `conn.execute("DELETE FROM event_module_data WHERE module_id=? AND row_index=?", (self.module_id, row`
- Line 429: `"SELECT id FROM event_module_data WHERE module_id=? AND row_index=? AND field_id=?",`
- Line 434: `"UPDATE event_module_data SET valeur=? WHERE id=?",`
- Line 439: `"INSERT INTO event_module_data (module_id, row_index, field_id, valeur) VALUES (?, ?, ?, ?)",`
- Line 507: `"SELECT valeur FROM event_module_data WHERE module_id=? AND row_index=? AND field_id=?",`
- Line 516: `"SELECT id FROM event_module_data WHERE module_id=? AND row_index=? AND field_id=?",`
- Line 521: `"UPDATE event_module_data SET valeur=? WHERE id=?",`
- Line 526: `"INSERT INTO event_module_data (module_id, row_index, field_id, valeur) VALUES (?, ?, ?, ?)",`
- Line 540: `"SELECT row_index FROM event_module_data WHERE module_id = ? GROUP BY row_index ORDER BY row_index",`
- Line 561: `"SELECT row_index FROM event_module_data WHERE module_id = ? GROUP BY row_index ORDER BY row_index",`
- Line 569: `"SELECT valeur FROM event_module_data WHERE module_id=? AND row_index=? AND field_id=?",`
- Line 595: `"SELECT row_index FROM event_module_data WHERE module_id = ? GROUP BY row_index ORDER BY row_index",`
- Line 603: `"SELECT valeur FROM event_module_data WHERE module_id=? AND row_index=? AND field_id=?",`

**modules/event_recettes.py**

- Line 217: `"SELECT valeur FROM event_module_data WHERE module_id=? AND field_id=?", (module_id, field_id)`

### event_module_fields

Total accesses: 21

**dialogs/edit_field_dialog.py**

- Line 36: `row_val = conn.execute("SELECT modele_colonne FROM event_module_fields WHERE id=?", (self.field_id,)`
- Line 73: `"SELECT nom_champ, type_champ, modele_colonne FROM event_module_fields WHERE id=?",`
- Line 78: `"SELECT nom_champ, type_champ FROM event_module_fields WHERE id=?",`
- Line 102: `"INSERT INTO event_module_fields (module_id, nom_champ, type_champ, modele_colonne) VALUES (?, ?, ?,`
- Line 107: `"INSERT INTO event_module_fields (module_id, nom_champ, type_champ) VALUES (?, ?, ?)",`
- Line 113: `"UPDATE event_module_fields SET nom_champ=?, type_champ=?, modele_colonne=? WHERE id=?",`
- Line 118: `"UPDATE event_module_fields SET nom_champ=?, type_champ=? WHERE id=?",`

**dialogs/edit_module_data_dialog.py**

- Line 17: `"SELECT modele_colonne FROM event_module_fields WHERE id=?", (fid,)`

**modules/event_module_data.py**

- Line 41: `"SELECT id, nom_champ, modele_colonne FROM event_module_fields WHERE module_id=?",`

**modules/event_module_fields.py**

- Line 50: `"SELECT id, nom_champ, type_champ, prix_unitaire, modele_colonne FROM event_module_fields WHERE modu`
- Line 94: `conn.execute("DELETE FROM event_module_fields WHERE id=?", (fid,))`
- Line 107: `champ = conn.execute("SELECT nom_champ, prix_unitaire FROM event_module_fields WHERE id=?", (fid,)).`
- Line 120: `conn.execute("UPDATE event_module_fields SET prix_unitaire=? WHERE id=?", (new_price if new_price el`

**modules/event_modules.py**

- Line 123: `conn.execute("DELETE FROM event_module_fields WHERE module_id=?", (mid,))`
- Line 206: `"SELECT * FROM event_module_fields WHERE module_id = ? ORDER BY id", (self.module_id,)`
- Line 267: `"INSERT INTO event_module_fields (module_id, nom_champ, type_champ, prix_unitaire, modele_colonne) V`
- Line 289: `conn.execute("DELETE FROM event_module_fields WHERE id=?", (field_id,))`
- Line 484: `conn.execute("UPDATE event_module_fields SET prix_unitaire=? WHERE id=?", (new_price if new_price el`
- Line 558: `"SELECT * FROM event_module_fields WHERE module_id = ? ORDER BY id", (self.module_id,)`
- Line 592: `"SELECT * FROM event_module_fields WHERE module_id = ? ORDER BY id", (self.module_id,)`

**modules/event_recettes.py**

- Line 179: `fields = conn.execute("SELECT id, nom_champ FROM event_module_fields WHERE module_id=?", (module_id,`

### event_modules

Total accesses: 16

**dialogs/edit_module_dialog.py**

- Line 33: `"SELECT nom_module FROM event_modules WHERE id=?", (self.module_id,)`
- Line 51: `"INSERT INTO event_modules (event_id, nom_module) VALUES (?, ?)",`
- Line 56: `"UPDATE event_modules SET nom_module=? WHERE id=?",`

**modules/depenses_diverses.py**

- Line 45: `modules = conn.execute("SELECT id, nom_module FROM event_modules ORDER BY nom_module").fetchall()`
- Line 140: `mod = conn.execute("SELECT nom_module FROM event_modules WHERE id=?", (item["module_id"],)).fetchone`

**modules/depenses_regulieres.py**

- Line 45: `modules = conn.execute("SELECT id, nom_module FROM event_modules ORDER BY nom_module").fetchall()`
- Line 140: `mod = conn.execute("SELECT nom_module FROM event_modules WHERE id=?", (item["module_id"],)).fetchone`

**modules/event_modules.py**

- Line 67: `mods = conn.execute("SELECT * FROM event_modules WHERE event_id = ?", (self.event_id,)).fetchall()`
- Line 87: `"INSERT INTO event_modules (event_id, nom_module) VALUES (?, ?)",`
- Line 106: `conn.execute("UPDATE event_modules SET nom_module=? WHERE id=?", (name, mid))`
- Line 122: `conn.execute("DELETE FROM event_modules WHERE id=?", (mid,))`
- Line 251: `id_col = conn.execute("SELECT id_col_total FROM event_modules WHERE id=?", (self.module_id,)).fetcho`
- Line 291: `conn.execute("UPDATE event_modules SET id_col_total=NULL WHERE id=?", (self.module_id,))`
- Line 340: `conn.execute("UPDATE event_modules SET id_col_total=? WHERE id=?", (field_id, self.module_id))`

**modules/event_recettes.py**

- Line 73: `mod = conn.execute("SELECT nom_module FROM event_modules WHERE id=?", (r["module_id"],)).fetchone()`
- Line 167: `mods = conn.execute("SELECT id, nom_module FROM event_modules WHERE event_id=?", (self.event_id,)).f`

### event_payments

Total accesses: 5

**modules/event_payments.py**

- Line 40: `"SELECT * FROM event_payments WHERE event_id = ? ORDER BY id DESC", (self.event_id,)`
- Line 75: `conn.execute("DELETE FROM event_payments WHERE id=?", (pid,))`
- Line 124: `p = conn.execute("SELECT * FROM event_payments WHERE id=?", (self.payment_id,)).fetchone()`
- Line 157: `"UPDATE event_payments SET nom_payeuse=?, classe=?, mode_paiement=?, banque=?, numero_cheque=?, mont`
- Line 162: `"INSERT INTO event_payments (event_id, nom_payeuse, classe, mode_paiement, banque, numero_cheque, mo`

### event_recettes

Total accesses: 13

**dashboard/dashboard.py**

- Line 134: `recettes = get_df_or_sql(f"SELECT SUM(montant) FROM event_recettes WHERE event_id={id_evt}")["SUM(mo`

**exports/exports.py**

- Line 250: `SELECT montant FROM event_recettes`

**modules/event_recettes.py**

- Line 26: `exist = conn.execute("SELECT id FROM event_recettes WHERE event_id=? AND source='Vente sur place'", `
- Line 28: `conn.execute("UPDATE event_recettes SET montant=? WHERE id=?", (gain_total, exist["id"]))`
- Line 30: `conn.execute("INSERT INTO event_recettes (event_id, source, montant) VALUES (?, 'Vente sur place', ?`
- Line 69: `recettes = conn.execute("SELECT * FROM event_recettes WHERE event_id=? ORDER BY source", (self.event`
- Line 104: `r = conn.execute("SELECT source FROM event_recettes WHERE id=?", (rid,)).fetchone()`
- Line 109: `conn.execute("DELETE FROM event_recettes WHERE id=?", (rid,))`
- Line 233: `r = conn.execute("SELECT * FROM event_recettes WHERE id=?", (self.recette_id,)).fetchone()`
- Line 268: `"UPDATE event_recettes SET source=?, montant=?, commentaire=?, module_id=? WHERE id=?",`
- Line 273: `"INSERT INTO event_recettes (event_id, source, montant, commentaire, module_id) VALUES (?, ?, ?, ?, `

**modules/events.py**

- Line 86: `"SELECT COALESCE(SUM(montant), 0) FROM event_recettes WHERE event_id = ?", (event_id,)`

**modules/exports.py**

- Line 51: `"SELECT source, montant, commentaire, module_id FROM event_recettes WHERE event_id=?",`

### events

Total accesses: 20

**dialogs/edit_event_dialog.py**

- Line 57: `"SELECT name, date, lieu, commentaire FROM events WHERE id=?", (self.event_id,)`
- Line 89: `"INSERT INTO events (name, date, lieu, commentaire) VALUES (?, ?, ?, ?)",`
- Line 94: `"UPDATE events SET name=?, date=?, lieu=?, commentaire=? WHERE id=?",`

**exports/export_bilan_argumente.py**

- Line 68: `"SELECT name, date, lieu FROM events ORDER BY date DESC",`
- Line 378: `"SELECT name, date, lieu FROM events ORDER BY date DESC",`

**modules/buvette_bilan_db.py**

- Line 30: `rows = conn.execute("SELECT id, name, date FROM events ORDER BY date DESC").fetchall()`

**modules/buvette_bilan_dialogs.py**

- Line 12: `rows = conn.execute("SELECT id, name, date FROM events ORDER BY date DESC").fetchall()`

**modules/buvette_inventaire_db.py**

- Line 337: `rows = conn.execute("SELECT id, name FROM events ORDER BY date DESC").fetchall()`

**modules/buvette_mouvements_db.py**

- Line 137: `rows = conn.execute("SELECT id, name FROM events ORDER BY date DESC").fetchall()`

**modules/events.py**

- Line 82: `events = conn.execute("SELECT * FROM events ORDER BY date DESC").fetchall()`
- Line 134: `conn.execute("DELETE FROM events WHERE id = ?", (eid,))`
- Line 209: `ev = conn.execute("SELECT * FROM events WHERE id = ?", (self.event_id,)).fetchone()`
- Line 234: `"UPDATE events SET name=?, date=?, lieu=?, description=? WHERE id=?",`
- Line 239: `"INSERT INTO events (name, date, lieu, description) VALUES (?, ?, ?, ?)",`

**modules/exports.py**

- Line 44: `event = conn.execute("SELECT * FROM events WHERE id=?", (event_id,)).fetchone()`
- Line 409: `events = conn.execute("SELECT id, name FROM events ORDER BY date DESC").fetchall()`
- Line 474: `events = conn.execute("SELECT id, name, date FROM events ORDER BY date DESC").fetchall()`

**modules/inventaire.py**

- Line 57: `evts = conn.execute("SELECT name FROM events ORDER BY date DESC").fetchall()`
- Line 99: `row = conn.execute("SELECT id FROM events WHERE name=?", (evt_name,)).fetchone()`

**scripts/migration.py**

- Line 21: `"ALTER TABLE events ADD COLUMN description TEXT"`

### existing

Total accesses: 11

**modules/buvette_db.py**

- Line 151: `Update existing article.`
- Line 269: `Update existing achat and update purchase_price if changed.`
- Line 391: `"""Update existing mouvement."""`
- Line 448: `"""Update existing inventory line."""`

**modules/buvette_inventaire_db.py**

- Line 82: `"""Update existing inventaire."""`
- Line 242: `"""Update existing inventory line."""`

**modules/buvette_inventaire_dialogs.py**

- Line 149: `# Update existing line`

**modules/buvette_mouvements_db.py**

- Line 96: `"""Update existing mouvement."""`

**ui/article_dialog.py**

- Line 142: `# Update existing article`

**ui/inventory_lines_dialog.py**

- Line 227: `# Update existing line`
- Line 377: `# Edit mode: Update existing inventory`

### flows

Total accesses: 1

**modules/buvette_inventaire_db.py**

- Line 11: `- Added apply_inventory_snapshot_wrapper helper for inventory create/update flows`

### for

Total accesses: 1

**modules/stock_db.py**

- Line 53: `# Create article purchase batches table for FIFO costing`

### fournisseurs

Total accesses: 8

**modules/depenses_diverses.py**

- Line 51: `fournisseurs = conn.execute("SELECT name FROM fournisseurs ORDER BY name").fetchall()`

**modules/depenses_regulieres.py**

- Line 51: `fournisseurs = conn.execute("SELECT name FROM fournisseurs ORDER BY name").fetchall()`

**modules/fournisseurs.py**

- Line 37: `fournisseurs = conn.execute("SELECT * FROM fournisseurs ORDER BY name").fetchall()`
- Line 55: `conn.execute("INSERT INTO fournisseurs (name) VALUES (?)", (name.strip(),))`
- Line 81: `c.execute("INSERT OR IGNORE INTO fournisseurs (name) VALUES (?)", (name,))`
- Line 99: `old = conn.execute("SELECT name FROM fournisseurs WHERE id=?", (fid,)).fetchone()`
- Line 108: `conn.execute("UPDATE fournisseurs SET name=? WHERE id=?", (new_nom.strip(), fid))`
- Line 127: `conn.execute("DELETE FROM fournisseurs WHERE id=?", (fid,))`

### historique_clotures

Total accesses: 5

**modules/historique_clotures.py**

- Line 35: `clotures = conn.execute("SELECT id, date_cloture FROM historique_clotures ORDER BY date_cloture DESC`
- Line 52: `conn.execute("INSERT INTO historique_clotures (date_cloture) VALUES (?)", (date,))`
- Line 62: `old = conn.execute("SELECT date_cloture FROM historique_clotures WHERE id=?", (cid,)).fetchone()`
- Line 70: `conn.execute("UPDATE historique_clotures SET date_cloture=? WHERE id=?", (new_date, cid))`
- Line 82: `conn.execute("DELETE FROM historique_clotures WHERE id=?", (cid,))`

### if

Total accesses: 2

**modules/buvette_db.py**

- Line 274: `Consider: Only update if this achat date_achat is the most recent`

**scripts/apply_migrations.py**

- Line 60: `"""Create migrations tracking table if it doesn't exist."""`

### inventaire_lignes

Total accesses: 2

**modules/historique_inventaire.py**

- Line 51: `(SELECT COUNT(*) FROM inventaire_lignes WHERE inventaire_id = i.id) as nb_lignes`

**modules/inventaire.py**

- Line 114: `"INSERT INTO inventaire_lignes (inventaire_id, stock_id, quantite_constatee) VALUES (?, ?, ?)",`

### inventaires

Total accesses: 1

**modules/inventaire.py**

- Line 104: `"INSERT INTO inventaires (date_inventaire, event_id, commentaire) VALUES (?, ?, ?)",`

### inventory

Total accesses: 5

**modules/buvette.py**

- Line 292: `self.refresh_inventaires()  # Update inventory list`

**modules/buvette_inventaire_db.py**

- Line 307: `"""Insert or update inventory line for article in inventory."""`

**modules/buvette_inventaire_dialogs.py**

- Line 261: `# Insert or update inventory`

**ui/inventory_lines_dialog.py**

- Line 380: `# Update inventory header`
- Line 391: `# Insert/update inventory lines and update stock`

### inventory_stock_journal

Total accesses: 3

**modules/stock_db.py**

- Line 230: `INSERT INTO inventory_stock_journal`
- Line 267: `SELECT article_id, delta FROM inventory_stock_journal`
- Line 287: `"DELETE FROM inventory_stock_journal WHERE inventaire_id=?",`

### journal

Total accesses: 3

**dialogs/edit_journal_dialog.py**

- Line 61: `"SELECT date, libelle, montant, type, categorie, commentaire FROM journal WHERE id=?", (self.journal`
- Line 104: `"INSERT INTO journal (date, libelle, montant, type, categorie, commentaire) VALUES (?, ?, ?, ?, ?, ?`
- Line 109: `"UPDATE journal SET date=?, libelle=?, montant=?, type=?, categorie=?, commentaire=? WHERE id=?",`

### members

Total accesses: 6

**src/db/repository.py**

- Line 87: `"INSERT INTO members (name, email) VALUES (?, ?)",`
- Line 94: `return self.fetchone("SELECT * FROM members WHERE id = ?", (member_id,))`
- Line 98: `return self.fetchall("SELECT * FROM members ORDER BY id")`

**utils/db_operations.py**

- Line 63: `rows = execute_query("SELECT * FROM members WHERE id=?", (1,), fetch="one")`
- Line 64: `all_members = execute_query("SELECT * FROM members ORDER BY name")`
- Line 206: `return execute_query("SELECT * FROM members")`

### membres

Total accesses: 12

**dialogs/edit_member_dialog.py**

- Line 61: `"SELECT name, prenom, email, classe, cotisation, commentaire FROM membres WHERE id=?", (self.member_`
- Line 99: `"INSERT INTO membres (name, prenom, email, classe, cotisation, commentaire) VALUES (?, ?, ?, ?, ?, ?`
- Line 104: `"UPDATE membres SET name=?, prenom=?, email=?, classe=?, cotisation=?, commentaire=? WHERE id=?",`

**modules/depenses_diverses.py**

- Line 57: `membres = conn.execute("SELECT id, name, prenom FROM membres ORDER BY name, prenom").fetchall()`
- Line 144: `mem = conn.execute("SELECT name, prenom FROM membres WHERE id=?", (item["membre_id"],)).fetchone()`

**modules/depenses_regulieres.py**

- Line 57: `membres = conn.execute("SELECT id, name, prenom FROM membres ORDER BY name, prenom").fetchall()`
- Line 144: `mem = conn.execute("SELECT name, prenom FROM membres WHERE id=?", (item["membre_id"],)).fetchone()`

**modules/members.py**

- Line 61: `df = pd.read_sql_query("SELECT * FROM membres ORDER BY name, prenom", conn)`
- Line 109: `conn.execute("DELETE FROM membres WHERE id=?", (mid,))`
- Line 188: `"SELECT name, prenom, email, cotisation, commentaire, telephone, statut, date_adhesion FROM membres `
- Line 227: `"UPDATE membres SET name=?, prenom=?, email=?, cotisation=?, commentaire=?, telephone=?, statut=?, d`
- Line 232: `"INSERT INTO membres (name, prenom, email, cotisation, commentaire, telephone, statut, date_adhesion`

### on

Total accesses: 2

**modules/buvette_db.py**

- Line 271: `TODO (audit/fixes-buvette): Review if price should update on achat modification.`

**ui/inventory_lines_dialog.py**

- Line 8: `- Automatic stock update on save`

### orders

Total accesses: 1

**modules/db_api.py**

- Line 316: `...     "INSERT INTO orders (...) VALUES (...)",`

### purchase

Total accesses: 1

**ui/inventory_lines_dialog.py**

- Line 405: `# Update purchase price if provided`

### purchase_price

Total accesses: 3

**modules/buvette_db.py**

- Line 227: `Insert new achat, adjust stock, and update purchase_price.`
- Line 253: `logger.warning(f"Could not update purchase_price for article {article_id}: {e}")`
- Line 296: `logger.warning(f"Could not update purchase_price for article {article_id}: {e}")`

### queries

Total accesses: 1

**scripts/analyze_modules_columns_old.py**

- Line 50: `# UPDATE queries`

### retrocessions_ecoles

Total accesses: 5

**modules/retrocessions_ecoles.py**

- Line 40: `"SELECT id, date, ecole, montant, commentaire FROM retrocessions_ecoles ORDER BY date DESC"`
- Line 61: `old = conn.execute("SELECT * FROM retrocessions_ecoles WHERE id=?", (cid,)).fetchone()`
- Line 104: `conn.execute("UPDATE retrocessions_ecoles SET date=?, ecole=?, montant=?, commentaire=? WHERE id=?",`
- Line 107: `conn.execute("INSERT INTO retrocessions_ecoles (date, ecole, montant, commentaire) VALUES (?, ?, ?, `
- Line 125: `conn.execute("DELETE FROM retrocessions_ecoles WHERE id=?", (cid,))`

### sqlite_master

Total accesses: 15

**db/db.py**

- Line 79: `c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='comptes'")`
- Line 143: `c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}'")`
- Line 694: `tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table';")]`

**modules/buvette_inventaire_db.py**

- Line 102: `cur.execute("SELECT name FROM sqlite_master WHERE type='table'")`

**modules/stock_db.py**

- Line 189: `"SELECT name FROM sqlite_master WHERE type='table' AND name=?",`

**scripts/db_diagnostics.py**

- Line 191: `SELECT name FROM sqlite_master`

**scripts/find_missing_columns.py**

- Line 53: `cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")`

**scripts/migrate_add_purchase_price.py**

- Line 103: `SELECT name FROM sqlite_master`

**scripts/migrate_articles_unite_to_quantite.py**

- Line 15: `cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))`

**scripts/update_db_structure.py**

- Line 536: `cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")`

**scripts/update_db_structure_old.py**

- Line 496: `cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")`

**src/services/inventory_service.py**

- Line 27: `"SELECT name FROM sqlite_master WHERE type='table' "`
- Line 75: `"SELECT name FROM sqlite_master WHERE type='table' "`

**ui/startup_schema_check.py**

- Line 96: `cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")`

**utils/cloture_exercice.py**

- Line 30: `cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")`

### statement

Total accesses: 2

**scripts/safe_add_columns.py**

- Line 135: `# Build ALTER TABLE statement`

**utils/db_operations.py**

- Line 133: `Execute an UPDATE statement and return the number of affected rows.`

### statements

Total accesses: 4

**scripts/analyze_modules_columns.py**

- Line 141: `"""Extrait les colonnes depuis INSERT INTO statements."""`
- Line 159: `"""Extrait les colonnes depuis UPDATE statements."""`
- Line 197: `"""Extrait les colonnes depuis CREATE TABLE statements."""`

**scripts/find_missing_columns.py**

- Line 112: `# Find UPDATE statements`

### stock

Total accesses: 12

**dialogs/edit_stock_dialog.py**

- Line 69: `"SELECT name, quantite, seuil_alerte, lot, date_peremption, commentaire, categorie_id FROM stock WHE`
- Line 116: `"""INSERT INTO stock (name, categorie_id, quantite, seuil_alerte, lot, date_peremption, commentaire)`
- Line 123: `"""UPDATE stock SET name=?, categorie_id=?, quantite=?, seuil_alerte=?, lot=?, date_peremption=?, co`

**modules/buvette_inventaire_dialogs.py**

- Line 277: `# Apply inventory snapshot to update stock and record in journal`
- Line 312: `# Update stock for each line`

**modules/categories.py**

- Line 113: `cur.execute("SELECT COUNT(*) FROM stock WHERE categorie_id=?", (cat_id,))`

**modules/db_api.py**

- Line 200: `>>>     cursor.execute("UPDATE stock SET ...")`

**modules/stock.py**

- Line 88: `conn.execute("DELETE FROM stock WHERE id=?", (sid,))`
- Line 172: `"UPDATE stock SET name=?, categorie_id=?, quantite=?, seuil_alerte=?, date_peremption=?, lot=?, comm`
- Line 177: `"INSERT INTO stock (name, categorie_id, quantite, seuil_alerte, date_peremption, lot, commentaire) V`

**modules/stock_db.py**

- Line 225: `# Update stock`

**modules/stock_inventaire.py**

- Line 79: `conn.execute("UPDATE stock SET quantite=? WHERE id=?", (nouvelle_qte, stock_id))`

### strategy

Total accesses: 1

**modules/buvette_db.py**

- Line 229: `TODO (audit/fixes-buvette): Review price update strategy.`

### table

Total accesses: 11

**modules/db_row_utils.py**

- Line 37: `>>> row = cursor.execute("SELECT * FROM table").fetchone()`
- Line 43: `>>> cursor.execute("SELECT * FROM table")`
- Line 87: `>>> rows = cursor.execute("SELECT * FROM table").fetchall()`
- Line 94: `>>> cursor.execute("SELECT * FROM table")`

**src/db/row_utils.py**

- Line 21: `>>> row = cursor.execute("SELECT * FROM table").fetchone()`
- Line 45: `>>> row = cursor.execute("SELECT * FROM table").fetchone()`
- Line 84: `>>> rows = cursor.execute("SELECT * FROM table").fetchall()`

**utils/db_helpers.py**

- Line 24: `>>> row = cursor.execute("SELECT * FROM table").fetchone()`
- Line 46: `>>> rows = cursor.execute("SELECT * FROM table").fetchall()`
- Line 74: `>>> row = cursor.execute("SELECT * FROM table").fetchone()`

**utils/db_operations.py**

- Line 34: `cursor.execute("SELECT * FROM table")`

### table_name

Total accesses: 4

**scripts/analyze_modules_columns.py**

- Line 142: `# Pattern: INSERT INTO table_name (col1, col2, col3)`
- Line 160: `# Pattern: UPDATE table_name SET col1=?, col2=?`
- Line 175: `# Pattern: SELECT col1, col2 FROM table_name`
- Line 176: `# or SELECT * FROM table_name`

### the

Total accesses: 6

**lib/db_articles.py**

- Line 16: `- update_article_stock: Update the stock quantity of an article`
- Line 17: `- update_article_purchase_price: Update the purchase price of an article`
- Line 272: `Update the stock quantity of an article.`
- Line 301: `Update the purchase price of an article.`

**modules/stock_db.py**

- Line 519: `# Update the article's stock`

**scripts/replace_row_get.py**

- Line 206: `print("  3. Or update the source to return dicts from repository methods")`

### tree

Total accesses: 2

**modules/event_modules.py**

- Line 209: `# Update tree columns`

**ui/dialogs/base_list_dialog.py**

- Line 111: `# Insert items into tree`

### unite_type

Total accesses: 1

**scripts/create_compat_views.py**

- Line 5: `(mapped from unite_type) so existing SELECT statements referencing 'unite' continue to work`

### utilise

Total accesses: 2

**scripts/check_buvette.py**

- Line 148: `issues.append(f"Ligne {i}: UPDATE utilise 'date=' au lieu de 'date_mouvement='")`
- Line 155: `issues.append(f"Ligne {i}: UPDATE utilise 'type=' au lieu de 'type_mouvement='")`

### utilisent

Total accesses: 1

**modules/buvette_db.py**

- Line 6: `* INSERT et UPDATE utilisent maintenant date_mouvement, type_mouvement, motif`

### valeurs_modeles_colonnes

Total accesses: 7

**dialogs/edit_module_data_dialog.py**

- Line 30: `"SELECT valeur FROM valeurs_modeles_colonnes WHERE modele_id=(SELECT id FROM colonnes_modeles WHERE `

**modules/event_module_data.py**

- Line 105: `"SELECT valeur FROM valeurs_modeles_colonnes WHERE modele_id=(SELECT id FROM colonnes_modeles WHERE `

**modules/event_modules.py**

- Line 361: `choix = [v["valeur"] for v in conn.execute("SELECT valeur FROM valeurs_modeles_colonnes WHERE modele`

**modules/model_colonnes.py**

- Line 37: `res = conn.execute("SELECT valeur FROM valeurs_modeles_colonnes WHERE modele_id=? ORDER BY valeur", `
- Line 47: `cur.execute("DELETE FROM valeurs_modeles_colonnes WHERE modele_id=?", (modele_id,))`
- Line 49: `cur.execute("INSERT INTO valeurs_modeles_colonnes (modele_id, valeur) VALUES (?, ?)", (modele_id, v)`
- Line 94: `conn.execute("DELETE FROM valeurs_modeles_colonnes WHERE modele_id=?", (modele_id,))`

### x

Total accesses: 1

**src/db/connection.py**

- Line 10: `cur.execute("INSERT INTO x (name) VALUES (?)", ("Alice",))`
