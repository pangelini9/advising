import pandas as pd
import json

def create_majors_names_mapping():
    #name of the excel file that contains the mapping of the names
    filename = 'major_abbreviations.xlsx'
    
    df = pd.read_excel(filename)
    
    abbreviations = df["Abbreviation"]
    complete = df["Complete"]
    
    mapping = {}
    
    for x in range(0,len(abbreviations)):
        
        print(f"The actual name of {abbreviations[x]} is {complete[x]}")
        
        mapping[abbreviations[x]] = complete[x]
        
    with open("majors_mapping.json", "w") as myFile:
        json.dump(mapping, myFile)

create_majors_names_mapping()
