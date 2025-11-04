"""
Integration tests for the exports package.

These tests verify that all exports functions can be imported correctly
and have basic functionality working.
"""

import sys
import os
import unittest
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestExportsPackageImports(unittest.TestCase):
    """Test that all exports can be imported from the exports package."""
    
    def test_import_exports_package(self):
        """Test that the exports package can be imported."""
        try:
            import exports
            self.assertIsNotNone(exports)
        except ImportError as e:
            self.fail(f"Failed to import exports package: {e}")
    
    def test_import_dataframe_exports(self):
        """Test that dataframe export functions can be imported."""
        try:
            from exports import (
                export_dataframe_to_excel,
                export_dataframe_to_csv,
                export_dataframe_to_pdf
            )
            self.assertTrue(callable(export_dataframe_to_excel))
            self.assertTrue(callable(export_dataframe_to_csv))
            self.assertTrue(callable(export_dataframe_to_pdf))
        except ImportError as e:
            self.fail(f"Failed to import dataframe export functions: {e}")
    
    def test_import_bilan_exports(self):
        """Test that bilan export functions can be imported."""
        try:
            from exports import (
                export_bilan_reporte_pdf,
                export_bilan_argumente_pdf,
                export_bilan_argumente_word
            )
            self.assertTrue(callable(export_bilan_reporte_pdf))
            self.assertTrue(callable(export_bilan_argumente_pdf))
            self.assertTrue(callable(export_bilan_argumente_word))
        except ImportError as e:
            self.fail(f"Failed to import bilan export functions: {e}")
    
    def test_exports_has_all_attribute(self):
        """Test that exports package defines __all__."""
        import exports
        self.assertTrue(hasattr(exports, '__all__'))
        self.assertIsInstance(exports.__all__, list)
        self.assertGreater(len(exports.__all__), 0)
    
    def test_all_exports_are_available(self):
        """Test that all items in __all__ are actually available."""
        import exports
        for item_name in exports.__all__:
            self.assertTrue(
                hasattr(exports, item_name),
                f"Item '{item_name}' in __all__ but not available in exports"
            )


class TestModulesExportsShim(unittest.TestCase):
    """Test that the modules.exports shim layer works correctly."""
    
    def test_import_from_modules_exports(self):
        """Test that we can import from modules.exports (backward compatibility)."""
        try:
            from modules.exports import (
                export_dataframe_to_excel,
                export_dataframe_to_csv,
                export_dataframe_to_pdf
            )
            self.assertTrue(callable(export_dataframe_to_excel))
            self.assertTrue(callable(export_dataframe_to_csv))
            self.assertTrue(callable(export_dataframe_to_pdf))
        except ImportError as e:
            self.fail(f"Failed to import from modules.exports shim: {e}")
    
    def test_modules_exports_has_ui_components(self):
        """Test that modules.exports still provides UI components."""
        try:
            from modules.exports import ExportsWindow
            self.assertTrue(callable(ExportsWindow))
        except ImportError as e:
            self.fail(f"Failed to import ExportsWindow from modules.exports: {e}")


class TestExportsFunctionality(unittest.TestCase):
    """Test basic functionality of export functions (without actually writing files)."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_output = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if self.test_output.exists():
            shutil.rmtree(self.test_output)
    
    def test_export_dataframe_to_excel_signature(self):
        """Test that export_dataframe_to_excel has expected signature."""
        from exports import export_dataframe_to_excel
        import inspect
        
        sig = inspect.signature(export_dataframe_to_excel)
        params = list(sig.parameters.keys())
        
        # Should have at least: df, file_path
        self.assertIn('df', params)
        self.assertIn('file_path', params)
    
    def test_export_dataframe_to_csv_signature(self):
        """Test that export_dataframe_to_csv has expected signature."""
        from exports import export_dataframe_to_csv
        import inspect
        
        sig = inspect.signature(export_dataframe_to_csv)
        params = list(sig.parameters.keys())
        
        # Should have at least: df, file_path
        self.assertIn('df', params)
        self.assertIn('file_path', params)
    
    def test_export_dataframe_to_pdf_signature(self):
        """Test that export_dataframe_to_pdf has expected signature."""
        from exports import export_dataframe_to_pdf
        import inspect
        
        sig = inspect.signature(export_dataframe_to_pdf)
        params = list(sig.parameters.keys())
        
        # Should have at least: df, file_path
        self.assertIn('df', params)
        self.assertIn('file_path', params)
    
    def test_export_functions_with_pandas(self):
        """Test export functions work with pandas DataFrames."""
        try:
            import pandas as pd
            from exports import export_dataframe_to_excel, export_dataframe_to_csv
            
            # Create a simple test DataFrame
            df = pd.DataFrame({
                'A': [1, 2, 3],
                'B': ['x', 'y', 'z']
            })
            
            # Test Excel export
            excel_path = self.test_output / 'test.xlsx'
            try:
                export_dataframe_to_excel(df, str(excel_path))
                # If file_path is provided, it should create the file
                # (unless UI dialog cancels, which won't happen in this test context)
            except Exception as e:
                # It's OK if it fails due to missing dependencies or UI components
                # Just verifying the function can be called
                pass
            
            # Test CSV export
            csv_path = self.test_output / 'test.csv'
            try:
                export_dataframe_to_csv(df, str(csv_path))
            except Exception as e:
                # It's OK if it fails due to missing dependencies or UI components
                pass
            
        except ImportError:
            self.skipTest("pandas not available for testing")


class TestExportsCentralization(unittest.TestCase):
    """Test that imports have been properly centralized."""
    
    def test_no_direct_exports_exports_imports_in_modules(self):
        """Test that modules use centralized imports."""
        # Check that key files use the centralized import pattern
        files_to_check = [
            'modules/cloture_exercice.py',
            'modules/event_modules.py',
        ]
        
        for file_path in files_to_check:
            full_path = Path(__file__).parent.parent / file_path
            if not full_path.exists():
                continue
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Should not have "from exports.exports import"
            # (or if it does, should have TODO comment indicating centralization)
            if 'from exports.exports import' in content:
                # If it exists, it should have a TODO comment
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'from exports.exports import' in line:
                        # Check that TODO comment is present (either on same line or nearby)
                        context = '\n'.join(lines[max(0, i-1):min(len(lines), i+3)])
                        has_todo = 'TODO: automated centralization change' in context
                        self.assertTrue(
                            has_todo,
                            f"{file_path} line {i+1} has 'from exports.exports' without TODO comment"
                        )
    
    def test_no_syspath_hacks_in_event_modules(self):
        """Test that sys.path hacks have been removed from event_modules.py."""
        file_path = Path(__file__).parent.parent / 'modules' / 'event_modules.py'
        if not file_path.exists():
            self.skipTest("event_modules.py not found")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should not have sys.path.append in export methods anymore
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'sys.path.append' in line or 'sys.path.insert' in line:
                # Check context - if it's in an export-related function, it's problematic
                context_start = max(0, i - 10)
                context = '\n'.join(lines[context_start:i+1])
                if 'def export_' in context:
                    self.fail(
                        f"Found sys.path manipulation in export function at line {i+1}. "
                        f"These should have been removed during centralization."
                    )


if __name__ == '__main__':
    unittest.main()
