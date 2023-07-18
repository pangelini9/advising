import xml.etree.ElementTree as ET
import json

def create_student_json(file_name):
    # XML file to read the transcripts from
    #xml_file = "students.xml"
    xml_file = file_name
    
    # JSON file to read the course id's from
    json_file_courses = "execution_files/courses.json"
    
    report_name = "execution_files/report.txt"
    myReportFile = open(report_name, "w")
    
    #1 if the student has the language waived, 0 if the student does not have the language courses waived
    language_waived = 1 # For now, fixed to 1 for everybody - we cannot know it
    #key corresponding to the major of the student under consideration
    major_code = 0 # For now, fixed to 0 for everybody - IT DOES NOT MATTER FOR PRE-REQ, IT WILL CHANGE FOR THE GENERAL PROGRAM
    
    with open(json_file_courses) as myFile:
        course_id_list = json.load(myFile)
    
    data_list = [] # to store the list of students
    
    # Parse the XML file
    tree = ET.parse(xml_file)
    
    # Set the namespace
    namespace = {"ns": "urn:crystal-reports:schemas"}
    
    # Get the root element
    root = tree.getroot()
    
    # up to the second FormattedAreaPair (level 2), each represents a single student
    students = root.findall("./ns:FormattedAreaPair/ns:FormattedAreaPair/ns:FormattedAreaPair", namespace)
    
    print("Students:", len(students))
    print()
    
    for s in students:
        
        # gets the sections in the header
        sections = s.findall("./ns:FormattedArea/ns:FormattedSections/ns:FormattedSection", namespace)
        
        # THIS CUOLD BE DONE WITH THE PARAMETER SectionNumber IN THE XPATH
            
        objects = s.findall("./ns:FormattedArea/ns:FormattedSections/ns:FormattedSection[@SectionNumber='2']/ns:FormattedReportObjects/ns:FormattedReportObject", namespace)
        
        for obj in objects:
            if obj.get("FieldName") == "{@SupressNameBreakForStudent}":
                student = obj.find("ns:Value", namespace).text
                #myReportFile.write(student + "\n")
                #print("Name: " + student)
            if obj.get("FieldName") == "{EA.StudentInfoString4}":
                major1 = obj.find("ns:Value", namespace).text
                #print("Major: " + str(major1))
            if obj.get("FieldName") == "{EA.StudentInfoString5}":
                minor = obj.find("ns:Value", namespace).text
                #print("Minor: " + str(minor))
            if obj.get("FieldName") == "{EA.StudentInfoString6}":
                major2 = obj.find("ns:Value", namespace).text
                #print("Second Major: " + str(major2))
            if obj.get("FieldName") == "{EA.StudentInfoString7}":
                minor2 = obj.find("ns:Value", namespace).text
                #print("Second Minor: " + str(minor2))
                #print()
    
        
        # To contain the list of courses for the current student
        stud_courses = []
            
        # gets the sections in the details
        sections = s.findall("./ns:FormattedAreaPair/ns:FormattedArea/ns:FormattedSections/ns:FormattedSection", namespace)
        
        # only section 0 is relevant, as it contains the courses info
        for sect in sections:
            if sect.get("SectionNumber") == "0":
                terms = sect.findall("./ns:FormattedReportObjects/ns:FormattedReportObject/ns:FormattedAreaPair/ns:FormattedAreaPair", namespace)
                
                #print(len(terms))
                
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
                            # print(current_course)
                            
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
                    
                    # print("END OF TERM\n")
                        
                    
                    
                #print("------\n")
                
        data = []
        #name, highschool_credits, major, minor1, minor2
        
    #    data.append(student[4:student.index(" ", 5)]) # add student's first name (ASSUMING SINGLE NAME - IT DOES NOT REALLY MATTER, I THINK)
    #    data.append(student[student.index(" ", 5)+1:]) # add student's last name
        data.append(student) # add student's name (first and last, we may clean from Ms. Mr. etc. but have to be careful with cases)
        data.append("") # add student's last name - TO BE REMOVED OR ADJUSTED FOR SPECIAL CASES
        data.append(language_waived) # for now, fixed to 1
        data.append(major_code) # for now, fixed to 0. WE SHOULD GET THE ID FROM JSON
        data.append("") # Minor 1 - NOT IMPLEMENTED YET
        data.append("") # Minor 2 - NOT IMPLEMENTED YET
        data.append(stud_courses)
        
        data_list.append(data)
        
    # print(data_list)
    
    # myReportFile.write(str(data_list))
    
    with open("execution_files\students_list.json", "w") as myFile:
        # DUMPING A LIST CONTAINING THE LIST DATA, AS IN THE ORIGINAL JSON
        # CHECK WHETHER THIS IS NEEDED. IF NOT, REMOVE []
        json.dump(data_list, myFile, indent=2)
        
    myReportFile.close()
