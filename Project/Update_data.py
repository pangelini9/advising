import pandas as pd
import json
import numpy as np
import xml.etree.ElementTree as ET

#trim

def clean(myString):
    
    output = ""
    
    if type(myString) is str:
        
        output = myString.strip()
        
    elif type(myString) is float or myString is None:
        
        output = ""
        
    else:
        
        output = myString
        
    return output

#CREATES THE MAPPING FROM BLACKBAUD ABBREVATIONS TO FULL NAME OF MAJORS
def create_majors_names_mapping():
    #name of the excel file that contains the mapping of the names
    filename = 'excel_source\major_abbreviations.xlsx'
    
    df = pd.read_excel(filename)
    
    abbreviations = df["Major Name in Transcript"]
    complete = df["Corresponding Full Name"]
    
    mapping = {}
    
    for x in range(0,len(abbreviations)):
        
        #print(f"The actual name of {abbreviations[x]} is {complete[x]}")
        
        mapping[abbreviations[x].strip()] = complete[x].strip()
        
    with open("execution_files\json\majors_mapping.json", "w") as myFile:
        json.dump(mapping, myFile)
        

#CREATES THE LIST OF COURSES THAT THE UNIVERSITY OFFERS IN ADDDITION TO PREREQUISITES
def create_courses_list():
    #name of the excel file that contains the data of the courses done by the student
    filename = "excel_source\course_list.xlsx"
    
    df = pd.read_excel(filename, "courses")
    
    #print(df.keys())
    
    names_old = df["A"] # also PR or CR
    codes_old = df["B"] # also codes of pre/co req
    numbers_old = df["C"] # also lower for pre/co req
    creds_old = df["D"] # also upper for pre/co req
    ids_old = df["E"] # also required grade    
    period_old = df["F"]
    concentration_old = df["G"]
    on_site_old = df["H"]
      
    courses = []
    course = ""
    current = ""
    current_cr = ""
    req_grade = ""
        
    names = [] # also PR or CR
    codes = [] # also codes of pre/co req
    numbers = [] # also lower for pre/co req
    creds = [] # also upper for pre/co req
    ids = [] # also required grade    
    period = []
    concentration = []
    on_site = []
    
    
    for x in range(0,len(names_old)):
           
        names.append(clean(names_old[x]))
        codes.append(clean(codes_old[x]))
        numbers.append(clean(numbers_old[x]))
        creds.append(clean(creds_old[x]))
        ids.append(clean(ids_old[x]))
        period.append(clean(period_old[x]))
        concentration.append(clean(concentration_old[x]))
        on_site.append(clean(on_site_old[x]))
                    
    
    for x in range(0,len(names)):
        #print("Analyzing: ", names[x])    
        if names[x] != "":
            
            course_periods = []
            course_concentrations = []
            course_onsite = []
            
            split_string = names[x].split()
            
            if period[x]  != "":
                #split_string1 = period[x].split()
                split_string1 = np.array(period[x].split(', '))
                course_periods = split_string1.tolist()
                #print(f"\n{names[x]} has period: {course_periods}")
                
            if concentration[x] != "":    
                #split_string2 = concentration[x].split()
                split_string2 = np.array(concentration[x].split(', '))
                course_concentrations = split_string2.tolist()
                #print(f"\n{names[x]} has concentrations: {course_concentrations}")

            
            if on_site[x] != "":
                #split_string3 = on_site[x].split()
                split_string3 = np.array(on_site[x].split(','))
                course_onsite = split_string3.tolist()
                #print(f"\n{names[x]} has onsite: {course_onsite}")

            
            if split_string[0] != "PR" and split_string[0] != "CR":
    
                # this is a new course, so I have to:
                
                # store the previous one, if any
                if course != "":
                    courses.append(course)
                    # I also need to reset current, for the next pre-req
                    current = ""
                    current_cr = ""
                    req_grade = ""
                    
                #print("Work on ", x, names[x])
        
                # initialize a new one
                course = [names[x], codes[x], int(numbers[x]), int(creds[x]), {"prerequisite":[], "corequisite":[]}, int(ids[x]), course_periods, course_concentrations, course_onsite]
                
            elif split_string[0] == "PR":
                
                grade = "D-"
                if ids[x] != "NULL":
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
                if ids[x] != "":
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
    
    #print("")
    # add the last course
    if course:
        courses.append(course)            
                    
    with open("execution_files\json\courses.json", "w") as myFile:
        json.dump(courses, myFile, indent=2)        
        
        
#CREATES THE JSON FILE WITH MAJORS INFORMATION       
def create_majors_dict():
    #name of the excel file that contains the data of the courses done by the student
    filename = 'excel_source\majors_list.xlsx'
    
    df = pd.read_excel(filename, "Majors")
    
    majors_dict = {} # the general dictionary with all majors
    major = {} # the dict for each single major
    name = "" # the name of the major, which will be used as key for the general dictionary

    # the three lists that will be used in the dictionary of each major    
    add_reqs = []
    core_courses = []
    electives = []

    # the three current variables to handle the OR
    curr_add = ""
    curr_core = ""
    curr_el = ""

    names_old = df["Major Name"] # Major name or type of entry (ADD, COR, ELC)
    reqs_nums_old = df["Math requirement"] # Math requirement 0/1 or number of courses
    elect_codes_old = df["Electives Description"] # Elective descriptions or code
    type_lower_old = df["Planner Type"] # Type of the planner or lower bound
    keys_upper_old = df["Major Key"] # Key of the major or upper bound
    descriptions_old = df["next id"] # None or text description

    names = []
    reqs_nums = []
    elect_codes = []
    type_lower = []
    keys_upper = []    
    descriptions = []
    
    for x in range(0,len(names_old)):
               
        names.append(clean(names_old[x]))
        reqs_nums.append(clean(reqs_nums_old[x]))
        elect_codes.append(clean(elect_codes_old[x]))
        type_lower.append(clean(type_lower_old[x]))
        keys_upper.append(clean(keys_upper_old[x]))
        descriptions.append(clean(descriptions_old[x]))
        
    for x in range(0,len(names)):
    
        # to skip empty lines
        if names[x] != "":
            
            split_name = names[x].split()

            if split_name[0] != "ADD" and split_name[0] != "COR" and split_name[0] != "ELC":
    
                # in this case, we are starting a new major
                
                # I first store the previous one, if any, into the main dictonary
                if name != "":
                    # add the three lists to the major
                    major["additional requirements"] = add_reqs
                    major["core courses"] = core_courses
                    major["major electives"] = electives
                    
                    # add the major to the dict of majors
                    majors_dict[name] = major

                    # I also need to reset the currents and the lists                    
                    add_reqs = []
                    core_courses = []
                    electives = []
                    curr_add = ""
                    curr_core = ""
                    curr_el = ""
                    
                # store the values into appropriate variables
                name = names[x]
                math = int(reqs_nums[x])
                description = elect_codes[x]
                pl_type = int(type_lower[x])
                key = int(keys_upper[x])
                
                major = {
                    "math requirement" : math,
                    "electives description" : description,
                    "planner_type" : pl_type,
                    "major key" : key
                    }
                                
            else:
                # this is one of the requirements, so we store the values into variables
                
                code = ""
                if elect_codes[x] != "":
                    code = str(elect_codes[x])

                if type(type_lower[x]) is int:
                    lower_bound = int(type_lower[x])
                else:
                    lower_bound = -1

                if type(keys_upper[x]) is int:
                    upper_bound = int(keys_upper[x])
                else:
                    upper_bound = -1
                    
                desc = descriptions[x]                      
                
                if split_name[0] == "ADD":
                    
                    #if a new requirement is starting, we create a new list and remember the current
                    #if len(split_name)<1:
                    if curr_add != split_name[1]:
                        number = int(reqs_nums[x])
                        add_reqs.append([number, []])
                        curr_add = split_name[1]
                        
                    # we now add the current requirement to the list of additional requirements
                    add_reqs[-1][1].append([code, lower_bound, upper_bound, desc])
                        
                elif split_name[0] == "COR":
                
                    # if a new requirement is starting, we create a new list and remember the current
                    if curr_core != split_name[1]:                        
                        
                        number = int(reqs_nums[x])
                        core_courses.append([number, []])
                        curr_core = split_name[1]
                        
                    # we now add the current requirement to the list of core requirements                
                    core_courses[-1][1].append([code, lower_bound, upper_bound, desc])

                elif split_name[0] == "ELC":
                    
                    # if a new requirement is starting, we create a new list and remember the current
                    if curr_el != split_name[1]:
                        number = int(reqs_nums[x])
                        electives.append([number, []])
                        curr_el = split_name[1]
                        
                    # we now add the current requirement to the list of elective requirements
                    electives[-1][1].append([code, lower_bound, upper_bound, desc])
        
    # add the last major
    if name != "":
        major["additional requirements"] = add_reqs
        major["core courses"] = core_courses
        major["major electives"] = electives
        
        # add the major to the dict of majors
        majors_dict[name] = major
    
    #print(majors_dict)
    
    with open("execution_files\json\majors_list.json", "w") as myFile:
        json.dump(majors_dict, myFile, indent=2)        
        

#CREATES IN JSON THE LIST OF STUDENTS ENROLLED (FROM THE XML EXPORT)        
def create_student_json(file_name):
        
    # XML file to read the transcripts from
    #xml_file = "students.xml"
    xml_file = file_name
        
    report_name = "information_not_found.txt"
    myReportFile = open(report_name, "w")

    # JSON file to read the course id's from
    json_file_courses = "execution_files\json\courses.json"
    
    with open(json_file_courses) as myFile:
        course_id_list = json.load(myFile)

    # JSON file to read the major id's from
    json_file_majors = "execution_files\json\majors_list.json"

    with open(json_file_majors) as myFile:
        major_id_list = json.load(myFile)

    # JSON file to read the major names mapping from
    json_file_mapping = "execution_files\json\majors_mapping.json"
    
    with open(json_file_mapping) as myFile:
        majors_mapping = json.load(myFile)

    data_list = [] # to store the list of students
    
    # Parse the XML file
    tree = ET.parse(xml_file)
    
    # Set the namespace
    namespace = {"ns": "urn:crystal-reports:schemas"}
    
    # Get the root element
    root = tree.getroot()
    
    # up to the second FormattedAreaPair (level 2), each represents a single student
    students = root.findall("./ns:FormattedAreaPair/ns:FormattedAreaPair/ns:FormattedAreaPair", namespace)
    
    myReportFile.write("Students:" + str(len(students)) + "\n")
    #print()
    
    for s in students:
        
        # majors of the student - can be one or two
        majors = []
        
        # gets the sections in the header
        sections = s.findall("./ns:FormattedArea/ns:FormattedSections/ns:FormattedSection", namespace)
        
        # THIS CUOLD BE DONE WITH THE PARAMETER SectionNumber IN THE XPATH
            
        objects = s.findall("./ns:FormattedArea/ns:FormattedSections/ns:FormattedSection[@SectionNumber='2']/ns:FormattedReportObjects/ns:FormattedReportObject", namespace)
        
        for obj in objects:
            if obj.get("FieldName") == "{@SupressNameBreakForStudent}":
                student = obj.find("ns:Value", namespace).text
                myReportFile.write("\n" + student + "\n")
                #print("Name: " + student)
            if obj.get("FieldName") == "{EA.StudentInfoString4}":
                major1 = obj.find("ns:Value", namespace).text
                myReportFile.write("Major 1:" + str(major1) + "\n")
                #print("Major: " + str(major1))
            if obj.get("FieldName") == "{EA.StudentInfoString5}":
                minor1 = obj.find("ns:Value", namespace).text
                myReportFile.write("Minor:" + str(minor1) + "\n")
                #print("Minor: " + str(minor))
            if obj.get("FieldName") == "{EA.StudentInfoString6}":
                major2 = obj.find("ns:Value", namespace).text
                myReportFile.write("Major 2:" + str(major2) + "\n")
                #print("Second Major: " + str(major2))
            if obj.get("FieldName") == "{EA.StudentInfoString7}":
                minor2 = obj.find("ns:Value", namespace).text
                myReportFile.write("Minor 2:" + str(minor2) + "\n")
                #print("Second Minor: " + str(minor2))
                #print()
        
        # Remove Mr. and Ms.
        if student.startswith("Mr.") or student.startswith("Ms."):
            student = student[4:]

        if student.startswith("Mrs."):
            student = student[5:]

        # 2 (double-degree), 1 (double-major), or 0 (normal).
        if "/" in major1:
            majors = major1.split("/")
            double_degree = 1
        else:
            majors.append(major1)
            if major2 is not None:
                majors.append(major2)
                double_degree = 2
            else:
                double_degree = 0
                
        #print(double_degree, majors)
        
        #1 if the student has the language waived, 0 if the student does not have the language courses waived
        language_waived = 0 # For now, fixed to 0 for everybody - we cannot know it
        
        # To contain the list of courses for the current student
        stud_courses = []
                 
        # gets the sections in the details
        sect = s.find("./ns:FormattedAreaPair/ns:FormattedArea/ns:FormattedSections/ns:FormattedSection[@SectionNumber = '0']", namespace)
 
        terms = sect.findall("./ns:FormattedReportObjects/ns:FormattedReportObject/ns:FormattedAreaPair/ns:FormattedAreaPair", namespace)
        
        for t in terms:
            
            current_term = t.find("./ns:FormattedArea/ns:FormattedSections/ns:FormattedSection/ns:FormattedReportObjects/ns:FormattedReportObject/ns:Value", namespace).text
            #print(current_term)
            
            in_residence = 1 # Whether the course has been taken at JCU. Initially, always 1

            if not (current_term.startswith("Fall") or current_term.startswith("Spring") or current_term.startswith("Sum")):
                current_term = "TR"
                in_residence = 0
            
            school = t.find("./ns:FormattedAreaPair/ns:FormattedAreaPair/ns:FormattedAreaPair/ns:FormattedArea/ns:FormattedSections/ns:FormattedSection/ns:FormattedReportObjects/ns:FormattedReportObject[@FieldName = '{@OutsideSchoolName}']/ns:Value", namespace)
            
            if school.text != None:
                #print("School", school.text)
                in_residence = 0
            
            courses = t.findall(".//ns:FormattedAreaPair[@Level='9']", namespace)
            #print("Courses", len(courses))
            
            for x in courses:
                
                curr_course = x.find("./ns:FormattedArea/ns:FormattedSections/ns:FormattedSection/ns:FormattedReportObjects/ns:FormattedReportObject[@FieldName = '{EA.StringColumn2}']/ns:Value", namespace)
                
                if curr_course != None:
                    current_course = curr_course.text
                    #print(current_course)
                    
                    if not current_course.startswith("ENLUS") and not current_course.startswith("ADMIN") and not current_course.startswith("Semester")  and not current_course.startswith("Cumulative"):
                        
                        # remove the H for the honors, and remember if we do it
                        honors = 0
                        
                        # remove possible final characters, like i, ii, -A, and variations
                        end = len(current_course)-1
                        while end > 0:
                            if current_course[end].isdigit() and current_course[end-1].isdigit():
                                current_course = current_course[:end+1]
                                end = 0
                            else:
                                if current_course[end] == "H":
                                    honors = 1
                                end = end - 1
                                
                        end = len(current_course)-1
                        general = False
                        while end > 0:
                            if current_course[end].isdigit():
                                end = end - 1
                                general = True
                            else:
                                if current_course[end] != " " and general == True:
                                    current_course = current_course[:end+1] + " " + current_course[end+1:]
                                    #print("Adjusted", current_course)
                                end = 0
                        
                        
                                
                        # reads the credits
                        # now it is not used, but we will probably need to add it in the course
                        cr = x.find("./ns:FormattedArea/ns:FormattedSections/ns:FormattedSection/ns:FormattedReportObjects/ns:FormattedReportObject[@FieldName = '{EA.StringColumn5}']/ns:Value", namespace).text

                        # Read the course_id from the JSON file
                        course_id = "error"
                        for c in course_id_list:
                            if c[2] != 0:
#                                    if cou == f"{c[1]} {c[2]}" and float(cr) - honors == float(c[3]):
                                if current_course == f"{c[1]} {c[2]}":
                                    course_id = c[5]
                            else:
                                if current_course == f"{c[1]}":
                                    course_id = c[5]

                        if course_id == "error":
                            myReportFile.write(student + " ID not found for: " + current_course + ", creds: " + cr + ", in " + current_term + "\n")
                            
                        # reads the grade
                        g = x.find("./ns:FormattedArea/ns:FormattedSections/ns:FormattedSection/ns:FormattedReportObjects/ns:FormattedReportObject[@FieldName = '{EA.StringColumn4}']/ns:Value", namespace)

                        grade = "current"
                        if g.text != None:
                            #grade = g.text
                            grade = g.text
                        
                        #in_residence = 1 # Whether the course has been taken at JCU. For now, always 1
                        course_creds = float(cr)
                        
                        #new_course = [course_id, in_residence, grade, current_term, honors]
                        #had to substitute in residence with credits because in the GPA computation and in the standing it needs the actual amount of credits that the student has
                        new_course = [course_id, course_creds, grade, current_term, honors, in_residence]

                        stud_courses.append(new_course)
                                
        
        iteration = 0
        
        minors = [clean(minor1), clean(minor2)]
        
        for maj in majors:

            #key corresponding to the major of the student under consideration
            #major_code = 0 # For now, fixed to 0 for everybody - get the code from the json using the "maj" variable
            # Using the mapping to first transform the stored name of the major into its complete version
            if majors_mapping.get(maj, -1) == -1:
                myReportFile.write(student + " Major name not found " + maj + " so assigned Undeclared " + "\n")
                m = major_id_list.get("Undeclared") 
            else:
                m = major_id_list.get(majors_mapping[maj], -1)
            
            if m != -1:
                major_code = m.get("major key")
            else:
                #major_code = 0 # giving 0 whenever the major is not found!
                major_code = 28
                myReportFile.write(student + " Major not found for " + majors_mapping[maj] + " so assigned Undeclared" + "\n")
            
            #print(f"Major: {maj}, code {major_code}")
            
            min1 = ""
            min2 = ""
            
            #print(minors[iteration])
            
            if "/" in minors[iteration]:
                print("Found a double minor")
                mins = minors[iteration].split("/")
                min1 = clean(mins[0])
                min2 = clean(mins[1])
            else:
                min1 = clean(minors[iteration])
                    
            print(f"Minors: {min1} - {min2}")

            data = []
            #name, highschool_credits, major, minor1, minor2
                            
            # name, surname, language, major, minor 1, minor 2, courses_list, double_flag            
            data.append(student) # add student's name
            data.append("") # add student's last name - TO BE REMOVED OR ADJUSTED FOR SPECIAL CASES
            data.append(language_waived) # for now, fixed to 1
            data.append(major_code) # major-code, taken from json
            data.append(min1) # Minor 1 - For now, only the name
            data.append(min2) # Minor 2 - For now, only the name
            data.append(stud_courses)
            
            data.append(double_degree) # whether double degree (2), double major (1), or normal (0)
            
            data_list.append(data)
            
            iteration += 1
            
        
    # print(data_list)
    
    # myReportFile.write(str(data_list))
    
    with open("execution_files\json\students_list.json", "w") as myFile:
        json.dump(data_list, myFile, indent=2)
        
    myReportFile.close()
     
        
        
"""""""""""""""""""""""""""
CALLING FUNCTIONS
"""""""""""""""""""""""""""            
create_majors_names_mapping()        
create_courses_list()    
create_majors_dict()
#create_student_json("students.xml")
