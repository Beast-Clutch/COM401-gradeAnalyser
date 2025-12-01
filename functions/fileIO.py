import pandas as pd

def CSVImport(filePath):
    try:
        grades = pd.read_csv(filePath)
    except:
        print("Error Importing File @ " + filePath)
    return grades

def JSONImport(filePath):
    try:
        grades = pd.read_json(filePath)
    except:
        print("Error Importing File @ " + filePath)
    return grades
