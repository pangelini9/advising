import pandas as pd
import json

#name of the excel file that contains the data of the courses done by the student
filename = "course list.xlsx"

df = pd.read_excel(filename, "lista corsi")

print(df.keys())

names = df["A"] # also PR or CR
codes = df["B"] # also codes of pre/co req
numbers = df["C"] # also lower for pre/co req
creds = df["D"] # also upper for pre/co req
ids = df["E"] # also required grade

courses = []
course = ""
current = ""

for x in range(0,len(names)):
    #print("Analyzing: ", names[x])    
    if type(names[x]) is not float:
        
        if not (names[x].startswith("PR") and names[x][3].isdigit()) and not (names[x].startswith("CR") and names[x][3].isdigit()):
            
            # this is a new course, so I have to:
            
            # store the previous one, if any
            if course != "":
                courses.append(course)
                # I also need to reset current, for the next pre-req
                current = ""
    
            # initialize a new one
            course = [names[x], codes[x], numbers[x], creds[x], {"prerequisite":[], "corequisite":[]}, ids[x]]
            
        elif names[x].startswith("PR"):
            
            # this is a pre-req
            # create the pre-req
            c = {"code": codes[x],
                 "lower bound" : numbers[x],
                 "upper bound" : creds[x],
                 "grade" : ids[x]}
            
            # add it to the list in the prereq entry of the dictionary at course[4]
            # this is a list of lists, we have to decide whether it gets appended to the last list
            curr = names[x][3:5]
            print(curr)
            if current == curr:
                course[4]["prerequisite"][-1].append(c)
            # or we have to create a new list
            else:
                course[4]["prerequisite"].append([c])
                current = curr
    
        elif names[x].startswith("CR"):
            
            # this is a pre-req
            # create the pre-req
            c = {"code": codes[x],
                 "lower bound" : numbers[x],
                 "upper bound" : creds[x],
                 "grade" : ids[x]}
            
            # add it to the list in the prereq entry of the dictionary at course[4]
            # this is a list of lists, we have to decide whether it gets appended to the last list
            curr = names[x][3]
            if curr == "1" or current != curr:
                course[4]["corequisite"].append([c])
                current = curr
            else:
                course[4]["corequisite"][-1].append(c)
                
with open("courses.json", "w") as myFile:
    json.dump(courses, myFile, indent=2)