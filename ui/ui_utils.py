import tkinter as tk
from tkinter import ttk

def clear_treeview(tree):
    """
    Safely clear all items from a treeview widget.
    
    Includes guards to prevent TclError when widget has been destroyed.
    """
    try:
        # Check if widget still exists
        if not tree.winfo_exists():
            return
        for row in tree.get_children():
            tree.delete(row)
    except tk.TclError:
        # Widget was destroyed during operation
        pass


def safe_treeview_operation(tree, operation):
    """
    Safely execute an operation on a treeview widget.
    
    Args:
        tree: The treeview widget
        operation: A callable that performs operations on the tree
        
    Returns:
        True if operation succeeded, False if widget was destroyed
        
    Example:
        >>> def populate():
        ...     tree.insert("", "end", values=("data",))
        >>> safe_treeview_operation(tree, populate)
    """
    try:
        if not tree.winfo_exists():
            return False
        operation()
        return True
    except tk.TclError:
        # Widget was destroyed during operation
        return False

def ask_confirm(title, message):
    from tkinter import messagebox
    return messagebox.askyesno(title, message)

def show_info(title, message):
    from tkinter import messagebox
    messagebox.showinfo(title, message)

def show_error(title, message):
    from tkinter import messagebox
    messagebox.showerror(title, message)

def create_popup(title, message):
    popup = tk.Toplevel()
    popup.title(title)
    tk.Label(popup, text=message, padx=20, pady=20).pack()
    tk.Button(popup, text="Fermer", command=popup.destroy).pack(pady=12)
    popup.grab_set()
    popup.wait_window()