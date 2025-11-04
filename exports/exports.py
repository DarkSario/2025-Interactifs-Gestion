"""
Export utilities for dataframes and reports.

This module provides functions to export pandas DataFrames to various formats
(Excel, CSV, PDF) and to generate specialized report PDFs.
"""

import pandas as pd
from tkinter import filedialog, messagebox
from typing import Optional


def _ensure_df(df):
    """
    Ensure the input is a pandas DataFrame.
    
    Args:
        df: Input data (DataFrame, Series, or dict-like)
        
    Returns:
        pandas.DataFrame
    """
    if hasattr(df, "to_frame") and not hasattr(df, "to_excel"):
        # Series or similar -> convert to DataFrame
        return pd.DataFrame(df)
    if not hasattr(df, "to_excel") and not hasattr(df, "to_csv"):
        # dict or list-like -> convert to DataFrame
        return pd.DataFrame(df)
    return df


def export_dataframe_to_excel(df, file_path: Optional[str] = None, sheet_name: str = "Sheet1", 
                               index: bool = False, **kwargs):
    """
    Export a pandas DataFrame to Excel format.
    
    Args:
        df: pandas DataFrame or convertible data
        file_path: Optional output file path. If None, prompts user with file dialog.
        sheet_name: Name of the Excel sheet (default: "Sheet1")
        index: Whether to include DataFrame index in export (default: False)
        **kwargs: Additional arguments passed to pandas.DataFrame.to_excel()
        
    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        >>> export_dataframe_to_excel(df, 'output.xlsx')
    """
    df = _ensure_df(df)
    
    if file_path is None:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Export to Excel"
        )
    
    if not file_path:
        return  # User cancelled
    
    try:
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=index, **kwargs)
        
        if messagebox:
            messagebox.showinfo("Export Success", f"Data exported successfully to:\n{file_path}")
    except Exception as e:
        if messagebox:
            messagebox.showerror("Export Error", f"Failed to export to Excel:\n{str(e)}")
        raise


def export_dataframe_to_csv(df, file_path: Optional[str] = None, index: bool = False, 
                            encoding: str = 'utf-8', **kwargs):
    """
    Export a pandas DataFrame to CSV format.
    
    Args:
        df: pandas DataFrame or convertible data
        file_path: Optional output file path. If None, prompts user with file dialog.
        index: Whether to include DataFrame index in export (default: False)
        encoding: File encoding (default: 'utf-8')
        **kwargs: Additional arguments passed to pandas.DataFrame.to_csv()
        
    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        >>> export_dataframe_to_csv(df, 'output.csv')
    """
    df = _ensure_df(df)
    
    if file_path is None:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export to CSV"
        )
    
    if not file_path:
        return  # User cancelled
    
    try:
        df.to_csv(file_path, index=index, encoding=encoding, **kwargs)
        
        if messagebox:
            messagebox.showinfo("Export Success", f"Data exported successfully to:\n{file_path}")
    except Exception as e:
        if messagebox:
            messagebox.showerror("Export Error", f"Failed to export to CSV:\n{str(e)}")
        raise


def export_dataframe_to_pdf(df, file_path: Optional[str] = None, title: Optional[str] = None, **kwargs):
    """
    Export a pandas DataFrame to PDF format using reportlab.
    
    Args:
        df: pandas DataFrame or convertible data
        file_path: Optional output file path. If None, prompts user with file dialog.
        title: Optional title for the PDF document
        **kwargs: Additional styling options
        
    Raises:
        ImportError: If reportlab is not installed
        
    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        >>> export_dataframe_to_pdf(df, 'output.pdf', title='My Report')
    """
    df = _ensure_df(df)
    
    try:
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
    except ImportError as e:
        error_msg = "reportlab is required for PDF export. Install it with: pip install reportlab"
        if messagebox:
            messagebox.showerror("Missing Dependency", error_msg)
        raise ImportError(error_msg) from e
    
    if file_path is None:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Export to PDF"
        )
    
    if not file_path:
        return  # User cancelled
    
    try:
        # Determine page orientation based on DataFrame dimensions
        pagesize = landscape(A4) if len(df.columns) > 8 else A4
        
        doc = SimpleDocTemplate(
            file_path, 
            pagesize=pagesize,
            rightMargin=18, 
            leftMargin=18, 
            topMargin=24, 
            bottomMargin=24
        )
        
        styles = getSampleStyleSheet()
        elements = []
        
        # Add title if provided
        if title:
            elements.append(Paragraph(str(title), styles["Title"]))
            elements.append(Spacer(1, 12))
        
        # Prepare table data
        data = [list(df.columns)]
        for row in df.values:
            data.append([("" if pd.isna(v) else str(v)) for v in row])
        
        # Create table
        table = Table(data, hAlign="LEFT")
        table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e0e0e0")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        if messagebox:
            messagebox.showinfo("Export Success", f"PDF exported successfully to:\n{file_path}")
    except Exception as e:
        if messagebox:
            messagebox.showerror("Export Error", f"Failed to export to PDF:\n{str(e)}")
        raise


def export_bilan_reporte_pdf(file_path: Optional[str] = None):
    """
    Export a formatted "bilan reporté" (carried forward balance sheet) to PDF.
    
    This function generates a specialized financial report PDF with data from
    the database, showing carried forward balances from the previous fiscal year.
    
    Args:
        file_path: Optional output file path. If None, prompts user with file dialog.
        
    Example:
        >>> export_bilan_reporte_pdf('bilan_reporte_2023.pdf')
    """
    try:
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
    except ImportError as e:
        error_msg = "reportlab is required for PDF export. Install it with: pip install reportlab"
        if messagebox:
            messagebox.showerror("Missing Dependency", error_msg)
        raise ImportError(error_msg) from e
    
    if file_path is None:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Export Bilan Reporté"
        )
    
    if not file_path:
        return  # User cancelled
    
    try:
        from db.db import get_connection
        
        conn = get_connection()
        
        # Fetch financial summary data
        # This is a placeholder - adjust SQL queries based on actual schema
        recettes_query = """
            SELECT COALESCE(SUM(montant), 0) as total
            FROM (
                SELECT montant FROM event_recettes
                UNION ALL
                SELECT montant FROM dons_subventions
            )
        """
        
        depenses_query = """
            SELECT COALESCE(SUM(montant), 0) as total
            FROM (
                SELECT montant FROM event_depenses
                UNION ALL
                SELECT montant FROM depenses_regulieres
                UNION ALL
                SELECT montant FROM depenses_diverses
            )
        """
        
        total_recettes = conn.execute(recettes_query).fetchone()[0] or 0.0
        total_depenses = conn.execute(depenses_query).fetchone()[0] or 0.0
        solde = total_recettes - total_depenses
        
        conn.close()
        
        # Create PDF document
        doc = SimpleDocTemplate(file_path, pagesize=A4, 
                              rightMargin=24, leftMargin=24, 
                              topMargin=24, bottomMargin=24)
        
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Center', alignment=1))
        
        elements = []
        
        # Title
        elements.append(Paragraph("<b>BILAN REPORTÉ</b>", styles["Title"]))
        elements.append(Spacer(1, 20))
        
        # Summary table
        summary_data = [
            ["<b>Poste</b>", "<b>Montant (€)</b>"],
            ["Total Recettes", f"{total_recettes:.2f}"],
            ["Total Dépenses", f"{total_depenses:.2f}"],
            ["<b>Solde Reporté</b>", f"<b>{solde:.2f}</b>"]
        ]
        
        summary_table = Table(summary_data, hAlign="CENTER", colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#cce6ff")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTSIZE", (0, 0), (-1, -1), 11),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#ffffcc")),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Footer note
        elements.append(Paragraph(
            "<i>Ce bilan reporté est généré automatiquement à partir des données de l'application.</i>",
            styles["Normal"]
        ))
        
        doc.build(elements)
        
        if messagebox:
            messagebox.showinfo("Export Success", f"Bilan reporté exported to:\n{file_path}")
            
    except Exception as e:
        if messagebox:
            messagebox.showerror("Export Error", f"Failed to generate bilan reporté:\n{str(e)}")
        raise
