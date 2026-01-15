import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from typing import Dict, Optional
import pandas as pd

from functions.fileIO import CSVImport, JSONImport, Expected_Columns
import functions.db as db

def df_to_treeview(tree: ttk.Treeview, df: pd.DataFrame | None):
    for iid in tree.get_children():
        tree.delete(iid)
    if df is None or df.empty:
        return
    cols = list(df.columns)
    tree["columns"] = cols
    tree["show"] = "headings"
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=100, anchor="center")
    for _, row in df.iterrows():
        values = [row[c] for c in cols]
        tree.insert("", "end", values=[row.get(c) for c in cols])


# Opening GUI Window with tkinter
def startGUI():
    root = tk.Tk()
    #Window Title
    root.title("Student Grade Analyser")
    root.geometry("1920x1080")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    #Notebook Tabs - Allows for different pages accessible through a menu at the top.
    notebook = ttk.Notebook(root)
    notebook.grid(row=0, column=0, sticky="nsew")
    f_input = ttk.Frame(notebook)
    f_db = ttk.Frame(notebook)
    f_analysis = ttk.Frame(notebook)
    notebook.add(f_input, text="Grade Input")
    notebook.add(f_db, text="Grade Statistics")
    notebook.add(f_analysis, text="Grade Graphs")

    ttk.Label(f_input, text="Tab 1: Grade Input").pack(anchor="w")
    ttk.Label(f_db, text="Tab 2: Grade Statistics").pack(anchor="w")
    ttk.Label(f_analysis, text="Tab 3: Grade Graphs").pack(anchor="w")

    top_frame = ttk.Frame(f_input, padding=6)
    top_frame.pack(fill="x", anchor="n")

    entries: Dict[str, ttk.Entry] = {}
    for i, col in enumerate(Expected_Columns):
        lbl = ttk.Label(top_frame, text=col.replace("_", " ").title())
        lbl.grid(row=0, column=i, padx=4, sticky="w")
        ent = ttk.Entry(top_frame, width=12)
        ent.grid(row=1, column=i, padx=4, sticky="w")
        entries[col] = ent

    def collect_manual() -> Dict[str, any]:
        row: Dict[str, any] = {}
        for c in Expected_Columns:
            v = entries[c].get().strip()
            row[c] = v if v != "" else None
        for numc in ("age", "attendance", "assignment_completed", "grade"):
            v = row.get(numc)
            if v is not None:
                try:
                    if numc in ("age", "assignment_completed"):
                        row[numc] = int(float(v))
                    else:
                        row[numc] = float(v)
                except Exception:
                    row[numc] = None
        return row

    def on_add_row():
        row = collect_manual()
        if not row.get("student_id") and not (row.get("first_name") and row.get("last_name")):
            messagebox.showerror("Invalid", "Provide Student ID or First and Last name.")
            return
        try:
            db.insert_grade(row)
            messagebox.showinfo("Saved", "Row inserted.")
            for e in entries.values():
                e.delete(0, "end")
            refresh_table()
        except Exception as e:
            messagebox.showerror("DB Error", f"Could not insert row: {e}")

    btn_add = ttk.Button(top_frame, text="Add Row", command=on_add_row)
    btn_add.grid(row=1, column=len(Expected_Columns), padx=8)

    mid_frame = ttk.Frame(f_input, padding=6)
    mid_frame.pack(fill="x", anchor="n", pady=(6, 0))

    btn_import_csv = ttk.Button(mid_frame, text="Import CSV")
    btn_import_json = ttk.Button(mid_frame, text="Import JSON")
    btn_preview = ttk.Button(mid_frame, text="Preview Last Import")
    btn_save_preview = ttk.Button(mid_frame, text="Save Preview to DB")
    btn_refresh = ttk.Button(mid_frame, text="Refresh Table")

    btn_import_csv.pack(side="left", padx=6)
    btn_import_json.pack(side="left", padx=6)
    btn_preview.pack(side="left", padx=16)
    btn_save_preview.pack(side="left", padx=6)
    btn_refresh.pack(side="right", padx=6)

    loaded_preview: Dict[str, Optional[pd.DataFrame]] = {"df": None}
    def _load_file(importer):
        path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
        if not path:
            return
        df = importer(path)
        if df is None:
            messagebox.showerror("Import error", f"Failed to import file:\n{path}")
            return
        loaded_preview["df"] = df
        df_to_treeview(preview_tree, df)

    def on_import_csv():
        _load_file(CSVImport)

    def on_import_json():
        _load_file(JSONImport)

    def on_preview():
        df = loaded_preview.get("df")
        if df is None or df.empty:
            messagebox.showinfo("No preview", "No imported preview available.")
            return
        df_to_treeview(preview_tree, df)
        notebook.select(f_input)  # ensure visible

    def on_save_preview():
        df = loaded_preview.get("df")
        if df is None or df.empty:
            messagebox.showinfo("No data", "No preview data to save.")
            return
        try:
            count = db.insert_dataframe(df)
            messagebox.showinfo("Saved", f"Inserted {count} rows into the database.")
            loaded_preview["df"] = None
            df_to_treeview(preview_tree, pd.DataFrame())
            refresh_table()
        except Exception as e:
            messagebox.showerror("DB Error", f"Could not save preview: {e}")

    btn_import_csv.config(command=on_import_csv)
    btn_import_json.config(command=on_import_json)
    btn_preview.config(command=on_preview)
    btn_save_preview.config(command=on_save_preview)
    btn_refresh.config(command=lambda: [refresh_table(), refresh_preview_table()])

    # Preview area (below mid buttons, above main table)
    preview_frame = ttk.LabelFrame(f_input, text="Import Preview", padding=6)
    preview_frame.pack(fill="x", padx=6, pady=(6, 0))

    preview_tree = ttk.Treeview(preview_frame, height=6)
    preview_tree.pack(fill="both", expand=True, side="left")
    preview_v = ttk.Scrollbar(preview_frame, orient="vertical", command=preview_tree.yview)
    preview_h = ttk.Scrollbar(preview_frame, orient="horizontal", command=preview_tree.xview)
    preview_tree.configure(yscrollcommand=preview_v.set, xscrollcommand=preview_h.set)
    preview_v.pack(side="right", fill="y")
    preview_h.pack(side="bottom", fill="x")

    # Bottom: main spreadsheet-style table (stored raw grades)
    table_frame = ttk.Frame(f_input, padding=6)
    table_frame.pack(fill="both", expand=True, padx=6, pady=(6, 8))

    tree = ttk.Treeview(table_frame)
    tree.pack(fill="both", expand=True, side="left")
    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")

    def refresh_table():
        try:
            df = db.fetch_all()
            # keep only expected order if present
            if df is not None and not df.empty:
                cols_in_df = [c for c in Expected_Columns if c in df.columns]
                if cols_in_df:
                    df = df.loc[:, cols_in_df]
            df_to_treeview(tree, df)
        except Exception as e:
            messagebox.showerror("DB Error", f"Could not read DB: {e}")

    def refresh_preview_table():
        # keep preview tree in sync if preview present
        df = loaded_preview.get("df")
        if df is not None:
            df_to_treeview(preview_tree, df)

    refresh_table()
    refresh_preview_table()


    root.mainloop()

