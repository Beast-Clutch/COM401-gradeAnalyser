from functions.fileIO import CSVImport, JSONImport
from functions.gui import startGUI
from functions.db import init_db
import functions.fileIO

def main():
    #Initialisation of GUI window
    init_db()
    startGUI()
    print("Main Application Starting")
    ##Testing
    #test = CSVImport(r"C:\Users\jackt\OneDrive - University of Chichester\COM401-ProceduralPrograming\gradeAnalyser\Notes\student_grades.csv")
    #print(test)
    #test = JSONImport(r"C:\Users\jackt\OneDrive - University of Chichester\COM401-ProceduralPrograming\gradeAnalyser\Notes\student_grades.json")
    #print(test)
# Main Function Starter
if __name__ == "__main__":
    main()
