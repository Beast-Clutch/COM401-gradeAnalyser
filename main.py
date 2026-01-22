from functions.fileIO import CSVImport, JSONImport
from functions.gui import startGUI
from functions.db import init_db
import functions.fileIO

def main():
    #Initialisation of GUI window
    init_db()
    startGUI()
# Main Function Starter
if __name__ == "__main__":
    main()
