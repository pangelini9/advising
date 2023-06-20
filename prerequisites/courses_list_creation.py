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
current_cr = ""
req_grade = ""

for x in range(0,len(names)):
    print("Analyzing: ", names[x])    
    if type(names[x]) is not float:
        
        split_string = names[x].split()
        
        if split_string[0] != "PR" and split_string[0] != "CR":

            # this is a new course, so I have to:
            
            # store the previous one, if any
            if course != "":
                courses.append(course)
                # I also need to reset current, for the next pre-req
                current = ""
                current_cr = ""
                req_grade = ""
                
            print("Work on ", x, names[x])
    
            # initialize a new one
            course = [names[x], codes[x], int(numbers[x]), int(creds[x]), {"prerequisite":[], "corequisite":[]}, int(ids[x])]
            
        elif split_string[0] == "PR":
            
            grade = "D-"
            if type(ids[x]) is not float:
                grade = ids[x]
            
            # this is a pre-req
            # create the pre-req
            c = {"code": codes[x],
                 "lower bound" : numbers[x],
                 "upper bound" : creds[x],
                 "grade" : grade}
            
            # add it to the list in the prereq entry of the dictionary at course[4]
            # this is a list of lists, we have to decide whether it gets appended to the last list

            #print(curr)
            if current == split_string[1]:
                course[4]["prerequisite"][-1].append(c)
            # or we have to create a new list
            else:
                course[4]["prerequisite"].append([c])
                current = split_string[1]
    
        elif split_string[0] == "CR":
            
            grade = "D-"
            if type(ids[x]) is not float:
                grade = ids[x]

            # this is a pre-req
            # create the pre-req
            c = {"code": codes[x],
                 "lower bound" : numbers[x],
                 "upper bound" : creds[x],
                 "grade" : grade}
            
            # add it to the list in the prereq entry of the dictionary at course[4]
            # this is a list of lists, we have to decide whether it gets appended to the last list
            if current_cr == split_string[1]:
                course[4]["corequisite"][-1].append(c)
            # or we have to create a new list
            else:
                course[4]["corequisite"].append([c])
                current_cr = split_string[1]
                
with open("courses.json", "w") as myFile:
    json.dump(courses, myFile, indent=2)