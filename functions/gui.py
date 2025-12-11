import tkinter as tk
import tkinter.ttk as ttk


# Opening GUI Window with tkinter
def startGUI():
    root = tk.Tk()
    #Window Title
    root.title("Student Grade Analyser")
    root.geometry("1280x720")
    mainframe = ttk.Frame(root, padding=4)
    mainframe.grid(column=0, row=0, sticky="nsew")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    mainframe.columnconfigure(0, weight=1)

    notebook = ttk.Notebook(mainframe)
    notebook.grid(row=0, column=0, sticky="nsew")
    f1 = ttk.Frame(notebook)
    f2 = ttk.Frame(notebook)
    f3 = ttk.Frame(notebook)
    notebook.add(f1, text="Grade Input")
    notebook.add(f2, text="Grade Database")
    notebook.add(f3, text="Grade Analysis")


    ttk.Label(f1, text="Tab 1: Grade Input").pack(anchor="w")
    ttk.Label(f2, text="Tab 2: Grade Database").pack(anchor="w")
    ttk.Label(f3, text="Tab 3: Grade Analysis").pack(anchor="w")




    root.mainloop()

