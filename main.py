from functions.fileIO import CSVImport, JSONImport
from functions.gui import startGUI
import functions.fileIO

def main():
    #\Initialisation of GUI window
    #startGUI()

    ##Testing
    test = CSVImport(r"C:\Users\jackt\OneDrive - University of Chichester\COM401-ProceduralPrograming\gradeAnalyser\Notes\student_grades.csv")
    test = JSONImport(r"C:\Users\jackt\OneDrive - University of Chichester\COM401-ProceduralPrograming\gradeAnalyser\Notes\student_grades.json")
# Main Function Starter
if __name__ == "__main__":
    main()
