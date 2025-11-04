-- Migration: Add commentaire column to buvette_inventaire_lignes table
-- This column is referenced in code but missing from the schema
-- Date: 2025-11-04
-- Author: Audit automation

-- Add commentaire column (TEXT type, nullable, default empty string)
ALTER TABLE buvette_inventaire_lignes ADD COLUMN commentaire TEXT DEFAULT '';
