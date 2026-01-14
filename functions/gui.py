import tkinter as tk
import tkinter.ttk as ttk
from functions.fileIO  import CSVImport, JSONImport


# Opening GUI Window with tkinter
def startGUI():
    root = tk.Tk()
    #Window Title
    root.title("Student Grade Analyser")
    root.geometry("1280x720")
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





    root.mainloop()

