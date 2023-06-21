import pandas as pd
import json

#name of the excel file that contains the data of the courses done by the student
filename = "scianetti_export.xls"
#name of the excel sheet that contains the data for the student
worksheets = ["E"]
#1 if the student has the language waived, 0 if the student does not have the language courses waived
language_waived = 1
#key corresponding to the major of the student under consideration
major_code = 0


#with open("../course_id_list.json") as myFile:

with open("courses.json") as myFile:
    course_id_list = json.load(myFile)
    #print(course_id_list)

data_list = []

#for name in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]: 
    #df = pd.read_excel('fall23.xlsx', sheet_name=name)
for name in worksheets:
    df = pd.read_excel(filename, sheet_name=name)
    student = df['Unnamed: 0'][10]
    print(f"Name: {student}")
    
    # store relevant Excel columns (lists) into appropriate variables
    terms = df['Unnamed: 0']
    courses = df['Unnamed: 1']
    course_names = df['Unnamed: 3']
    grades = df['Unnamed: 7']
    creds = df['Unnamed: 8']
    
    stud_courses = []
    
    current_term = ""
    
    # the first 25 rows contain data about the student. If needed (maybe the major), 
    # we should access them directly, as we did with the name
    # now we start reading the main part, containing the courses
    for x in range(25, len(terms)):
        if type(terms[x]) is str:
    #        print(terms[x])
            current_term = terms[x]
            # DON'T REMEMBER HOW WE ENCODE TRANSFER CREDS: WE MAY NEED TO CHANGE THE CODE HERE
            if not (current_term.startswith("Fall") or current_term.startswith("Spring") or current_term.startswith("Sum")):
                current_term = "TR"
    
        if type(courses[x]) is str and courses[x] != "Course ID" and not courses[x].startswith("ADMIN"):
            print(f"{current_term} - {courses[x]} - {course_names[x]}. Grade: {grades[x]}. Credits: {creds[x]}")
            
            # search for the ID in the json file
            # SOME COURSES (ONLY EN?) HAVE i OR ii AT THE END OF THE CODE. ASK REGISTRAR
            # IF WE CAN IGNORE, FOR NOW WE SIMPLY REMOVE THE i FROM THE STRING BEFORE THE TEST
            # we also remove the H for the honors
            if courses[x].endswith("H"):
                cou = courses[x][0:-2]
            elif courses[x].endswith("ii"):
                cou = courses[x][0:-2]
            elif courses[x].endswith("i"):
                cou = courses[x][0:-1]
            else:
                cou = courses[x]
    
            course_id = "error"
            for c in course_id_list:
                if c[2] != 0:
                    if cou == f"{c[1]} {c[2]}":
                        course_id = c[5]
                else:
                    if cou == f"{c[1]}":
                        course_id = c[5]
            
            honors = 0 
            # change to 1 if taken with honors
            # there should be an H at the end of the code
            if courses[x].endswith("H"):
                honors = 1
                
            something = 1 # CHECK WHAT THIS MEANS AND CHANGE THIS TO 2 IF NEEDED
            if type(grades[x]) is str:
                term = current_term
                grade = grades[x]
            else:
                term = "current"
                grade = "current"
            new_course = [course_id, something, grade, term, honors]
            stud_courses.append(new_course)
            
    data = []
    #name, surname, highschool_credits, major, minor1, minor2
    
    data.append(student[4:student.index(" ", 5)]) # add student's first name (ASSUMING SINGLE NAME - IT DOES NOT REALLY MATTER, I THINK)
    data.append(student[student.index(" ", 5)+1:]) # add student's last name
    data.append(language_waived) # CHECK WHAT 1 MEANS HERE - LANGUAGE - Deafult 0?
    data.append(major_code) # CHECK WHAT 0 MEANS HERE - MAJOR - GET THE ID FROM JSON
    data.append("") # CHECK WHAT "" MEANS HERE - Minor 1 - NOT IMPLEMENTED
    data.append("") # CHECK WHAT "" MEANS HERE - Minor 2 - NOT IMPLEMENTED
    data.append(stud_courses)
    
    data_list.append(data)
        
with open("students_list.json", "w") as myFile:
    # DUMPING A LIST CONTAINING THE LIST DATA, AS IN THE ORIGINAL JSON
    # CHECK WHETHER THIS IS NEEDED. IF NOT, REMOVE []
    json.dump(data_list, myFile, indent=2)
        
        