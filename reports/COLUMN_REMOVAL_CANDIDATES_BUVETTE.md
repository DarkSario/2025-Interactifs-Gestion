# Candidats pour Suppression de Colonnes - Module Buvette

**IMPORTANT:** Cette liste identifie des colonnes potentiellement inutiles ou redondantes
dans le module buvette. AUCUNE SUPPRESSION ne doit être effectuée automatiquement.
Chaque suppression nécessite une revue manuelle et une validation explicite.

## Date du rapport
Generated: $(date)

## Colonnes identifiées pour revue manuelle

### 1. buvette_articles.unite_type

**Contexte:**
- Colonne ajoutée lors de migration (voir scripts/migrate_articles_unite_to_quantite.py)
- L'utilisateur mentionne que "la colonne Type Unité semble inutile"
- Remplace l'ancienne colonne `unite`

**Utilisation actuelle:**
- Affichée dans l'UI (modules/buvette.py, ligne 69)
- Utilisée pour compatibilité pré/post-migration
- Accessible via `.get("unite_type", .get("unite", ""))` pattern

**Recommandation:**
- ⚠️  **REVUE MANUELLE REQUISE**
- Vérifier si la distinction entre `unite` et `quantite` est vraiment nécessaire
- Si toutes les données ont été migrées, considérer :
  - Renommer `unite_type` vers un nom plus clair si conservée
  - Supprimer si vraiment inutilisée dans la logique métier
- Vérifier l'utilisation dans les rapports et exports

**Actions nécessaires avant suppression:**
1. Audit complet de l'utilisation dans le code
2. Vérification des données existantes en DB
3. Migration des données si nécessaire
4. Tests de non-régression
5. Validation par l'utilisateur final

---

### 2. buvette_articles.commentaire

**Contexte:**
- Colonne optionnelle pour notes sur les articles
- Rarement utilisée dans l'UI actuelle

**Utilisation actuelle:**
- Affichée dans TreeView (modules/buvette.py)
- Éditable via ArticleDialog
- Pas de validation ou logique métier associée

**Recommandation:**
- ✅ **CONSERVER**
- Colonne utile pour traçabilité et notes
- Peu coûteuse en stockage
- Peut être utile pour debugging et historique

---

## Autres colonnes à surveiller

### buvette_inventaire_lignes.commentaire

**Statut:** ✅ Colonne utile, ajoutée récemment
**Raison:** Permet de documenter les lignes d'inventaire

### buvette_mouvements.motif

**Statut:** ✅ Colonne importante
**Raison:** Traçabilité des mouvements de stock

---

## Notes importantes

1. **Pas de suppression automatique:** Toutes les suppressions de colonnes DOIVENT
   être effectuées manuellement après validation.

2. **Migration requise:** Avant toute suppression, créer un script de migration
   qui sauvegarde les données existantes.

3. **Tests requis:** Chaque suppression nécessite :
   - Tests unitaires mis à jour
   - Tests d'intégration
   - Validation manuelle de l'UI

4. **Documentation:** Mettre à jour tous les schémas et documentations après
   modification de structure.

---

## Checklist pour suppression de colonne

Avant de supprimer une colonne, vérifier :
- [ ] Aucun code n'utilise cette colonne (grep complet)
- [ ] Aucun rapport/export n'utilise cette colonne
- [ ] Les données existantes ont été archivées/migrées
- [ ] Script de migration créé et testé
- [ ] Tests mis à jour
- [ ] Documentation mise à jour
- [ ] Validation utilisateur obtenue
- [ ] Backup DB créé avant modification
- [ ] Rollback plan disponible

---

**Fin du rapport**
