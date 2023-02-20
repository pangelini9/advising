# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 16:15:21 2022

@author: ilda1
"""

#from majors import Major
from courses import Course, Course_taken
from courses import letter_to_number
#NB: major = Major(...)
#    def __init__(self, name, surname, highschool_credits, major, minor1, minor2, courses_done):


import json

class Student:
    
    def __init__(self, name, surname, highschool_credits, major, minor1, minor2):
        self.name = name
        self.surname = surname
        self.highschool = highschool_credits #=1 if yes
        self.major = major
        self.minor1 = minor1
        self.minor2 = minor2
        self.courses_done = []
        self.credits_earned = 0
        self.credits_nxsem = 0
        self.credits_missing = 120
        self.gpa = 0
        self.curr_standing = ""
        self.nx_standing = ""
        self.reduced_courses_list = [] #created with the actual list gets reduced as requirements are checked
        self.m_en = []
        self.m_ma = {"courses missing"  : 1, "courses done" : []}
        self.m_sci = {"courses missing"  : 2, "courses done" : []}
        self.m_flang = {"courses missing"  : 2, "courses done" : []}
        self.m_sosc = {"courses missing"  : 2, "courses done" : []}
        self.m_hum = {"courses missing"  : 2, "courses done" : []}
        self.m_fa = {"courses missing"  : 1, "courses done" : []}
        self.m_additional = {"courses missing"  : 0, "courses done" : []}
        self.m_core = {"courses missing"  : 0, "courses done" : []}
        self.m_electives = {"courses missing"  : 0, "courses done" : []}
        
    def get_name(self):
        return self.name
    
    def get_surname(self):
        return self.surname
    
    def get_highschool(self):
        return self.highschool_credits
    
    def get_major(self):
        return self.major
    
    def get_minor1(self):
        return self.minor1
    
    def get_minor2(self):
        return self.minor2

    def get_coursesTaken(self):
        return self.courses_done
        #return self.reduced_courses_list
        
    def get_coursesReduced(self):
        return self.reduced_courses_list

    
    #adds to the lit of courses the list for each course done by the student
    def add_course(self, course):
        self.courses_done.append(course)
    
    #change major key into major object
    def change_major(self, majorobj):
        self.major = majorobj
        print(self.major)
        
    #change list of courses into the list of objects of the class Courses_taken
    def change_courses(self, courses_taken_obj):
        self.courses_done = courses_taken_obj
        
    def cumpute_gpa(self):
        #do they compure it on the semester and then they do the total or it's
        #the average of the courses' grades?
        #PA: It is the average of the courses grades, weighted on the credits
        creds = 0
        weighted_total=0
        for i in self.courses_done:
            grade = i.get_grade()
            # PA: I am excluding the grades that should not be counted:
            # P (5), W, NP, current, INC, TR (between 0.1 and 0.5 - using 0.6 just in case)
            # We should also consider the possible retake (if two grades, only consider the second)
            if grade != 5 and not (0.1 <= grade <= 0.6):
                course_credit = i.get_credits()
                creds += course_credit
                weighted_total += course_credit*grade
        self.gpa = round(weighted_total / creds, 2) # rounding to 2 decimal digits
    
    def compute_credits_earned(self):
        self.credits_earned = 0
        for i in self.courses_done:
            grade = i.get_grade()
            if grade != "": # PA: this should also be updated to use the dictionary values
                course_credit = i.get_credits()
                self.credits_earned += course_credit
            
    def compute_credits_nxsem(self):
        if self.highschool == 1:
            self.credits_nxsem = 30
        else:
             self.credits_nxsem = 0
        for i in self.courses_done:
            course_credit = i.get_credits()
            self.credits_nxsem += course_credit
    
    #does not account for minors
    def compute_credits_missing(self):
        self.credits_missing = 120 - self.credits_nxsem 
            
    def compute_cur_standing(self):
        if self.credits_earned >= 91:
            self.curr_standing = "Senior"
        elif self.credits_earned >= 61:
            self.curr_standing = "Junior"
        elif self.credits_earned >= 31:
            self.curr_standing = "Sophomore"
        else:
            self.curr_standing = "Freshman"

    def compute_nx_standing(self):
        if self.credits_nxsem >= 91:
            self.nx_standing = "Senior"
        elif self.credits_nxsem >= 61:
            self.nx_standing = "Junior"
        elif self.credits_nxsem >= 31:
            self.nx_standing = "Sophomore"
        else:
            self.nx_standing = "Freshman"
            
    #returns a list of informations to be printed in the additional information        
    def create_info_list(self):
        #["GPA", "Credits(earned)", "Current Standing", "Credits following semester", "Standing following semester", "Credits missing"]
        info_list = [self.gpa, self.credits_earned, self.curr_standing, self.credits_nxsem, self.nx_standing, self.credits_missing]
        return info_list
    
    def remove_retake(self):
        #poi da modificare per fare il confronto sul term
        special_courses = [0, 281, 299, 381, 399]
        for i in range(len(self.courses_done)-1, 0, -1):
            current_course = self.courses_done[i]
            to_insert = True #è da inserire in reduced
            for h in self.reduced_courses_list:
                if current_course.course.get_number() == h.course.get_number() and current_course.course.get_code() == h.course.get_code() and current_course.course.get_number() not in special_courses:
                    to_insert = False # non è d inserire
            if to_insert:
                self.reduced_courses_list.insert(0, current_course)
            print(len(self.reduced_courses_list))
        
    def check_ma_req(self):
        math_req = self.major.get_math_requirement()

        if math_req == 1:
            course_key = 54
            for i in self.reduced_courses_list:
                if course_key == i.course.get_course_key():
                    if i.get_grade() >= letter_to_number.get("C-"):
                        self.m_ma["courses missing"] -= 1
                        self.m_ma["courses done"].append([i, 1]) 
                        self.reduced_courses_list.remove(i)   
                    else:
                        self.m_ma["courses done"].append([i, 0]) 
                        self.reduced_courses_list.remove(i)       
        else:
            course_key = [53,54]
            for key in course_key:
                for i in self.reduced_courses_list:
                    if course_key == i.course.get_course_key():
                        if i.get_grade() >= letter_to_number.get("C-"):
                            self.m_ma["courses missing"] -= 1
                            self.m_ma["courses done"].append(i) 
                            self.reduced_courses_list.remove(i)
                        else:
                            self.m_ma["courses done"].append([i, 0]) 
                            self.reduced_courses_list.remove(i) 
                        break
        return self.m_ma
            
    #def check_additional(self):
        
    def check_core(self):
        core_courses = self.major.get_core_courses()
        for i in core_courses:
            found = False
            for j in self.reduced_courses_list:
                if i[0] == j.course.get_course_key():
                    self.m_core["courses done"].append(j)
                    self.reduced_courses_list.remove(j)
                    found = True
            if not found:
                self.m_core["courses missing"] += 1
        return self.m_core
                    
                    
    #def check_electives(self):
     
    def check_eng_requirement(self):
    
            #when passing the course to the list
            #0 = Failed (below D-)
            #1 = Grade requirement satifsfied (above C)
            #2 = Grade requirement not satifsfied (between D- and C-)
            #3 = current
            print(self.reduced_courses_list)
            lit_counter = 0
            for i in self.reduced_courses_list:
                print("ciao")
                print(i.course.get_code())
                if i.course.get_code()=="EN":
                    print("recognized en course")
                    if i.course.get_number() == 103:
                        if i.get_grade() >= letter_to_number.get("C"):
                            self.m_en.append([i,1]) 
                        elif i.get_grade() >= letter_to_number.get("D-"):
                            self.m_en.append([i,2])
                        elif i.get_grade() >= letter_to_number.get("current"):
                            self.m_en.append([i,3])
                        else:
                            self.m_en.append([i,0])
                        self.reduced_courses_list.remove(i)
    
                    elif i.course.get_number() == 105 or i.course.get_number() == 110:
                        if i.get_grade() >= letter_to_number.get("C"):
                            self.m_en.append([i,1]) 
                        elif i.get_grade() == letter_to_number.get("current"):
                            self.m_en.append([i,3])
                        else:
                            self.m_en.append([i,0])
                        self.reduced_courses_list.remove(i)
                        
                    elif i.course.get_number() >= 200 and lit_counter<2:
                        if i.get_grade() >= letter_to_number.get("D-"):
                            self.m_en.append([i,1])
                        elif i.get_grade() == letter_to_number.get("current"):
                            self.m_en.append([i,3])
                        else:
                            self.m_en.append([i,0])
                        self.reduced_courses_list.remove(i)
                        lit_counter += 1
                  
            return self.m_en
    

        
    def check_sosc(self, student):
        """
        course structure
        #Course(namecourse, code, number, credits_num, req_list, course_key)
        #Course_taken(course, student, course_section, grade, term, c_type)
        
        when passing the course to the list
        0 = Failed (below D-)
        1 = Grade requirement satifsfied (above C)
        2 = Grade requirement not satifsfied (between D- and C-)
        3 = current
        
        if self.highschool==1:
            course = Course("Social Science Elective", "SOSC", "----", 6, [], "")
            cc = Course_taken(course, student, 1, "P", "waived", 0)
            self.m_sosc["courses missing"] -= 2
            self.m_sosc["courses done"].append([cc,1])
        else:
        """
        counter = len(self.reduced_courses_list)
        while counter>0 and self.m_sosc["courses missing"]!=0:
            course_codes = ["COM", "CMS", "DMA", "DJRN", "EC", "GEOG", "PL", "PS", "SOSC"]
            for i in self.reduced_courses_list:
                if self.m_sosc["courses missing"] == 0:
                    break
                else:
                    for j in course_codes:
                        if j == i.course.get_code():
                            c_creds = i.course.get_credits()
                            if i.get_grade() >= letter_to_number.get("F"): #check on grades
                                self.m_sosc["courses done"].append([i,1]) 
                                self.reduced_courses_list.remove(i)
                                if c_creds == 3:                               #check on credits
                                    self.m_sosc["courses missing"] -= 1
                                elif c_creds == 6:
                                    self.m_sosc["courses missing"] -= 2
                            else:
                                self.m_sosc["courses done"].append([i,0]) 
                                self.reduced_courses_list.remove(i)        
                counter -= 1 
            return self.m_sosc
        
  
    def check_hum(self, student):
        """
        course structure
        #Course(namecourse, code, number, credits_num, req_list, course_key)
        #Course_taken(course, student, course_section, grade, term, c_type)
        
        when passing the course to the list
        0 = Failed (below D-)
        1 = Grade requirement satifsfied (above C)
        2 = Grade requirement not satifsfied (between D- and C-)
        3 = current
        
            if self.highschool==1:
                course = Course("Latin Elective", "LAT", "----", 6, [], "")
                cc = Course_taken(course, student, 1, "P", "waived", 0)
                self.m_hum["courses missing"] -= 2
                self.m_hum["courses done"].append([cc,1])
            else:
        """
        counter = len(self.reduced_courses_list)
        while counter>0 and self.m_hum["courses missing"]!=0:
            course_codes = ["CL", "EN", "GRK", "HM", "HS", "ITS", "LAT", "PH", "RL"]
            for i in self.reduced_courses_list:
                if self.m_hum["courses missing"] == 0:
                    break
                else:
                    for j in course_codes:
                        if j == i.course.get_code():
                            c_creds = i.course.get_credits()
                            if i.get_grade() >= letter_to_number.get("F"): #check on grades
                                self.m_hum["courses done"].append([i,1]) 
                                self.reduced_courses_list.remove(i)
                                if c_creds == 3:                               #check on credits
                                    self.m_hum["courses missing"] -= 1
                                elif c_creds == 6:
                                    self.m_hum["courses missing"] -= 2
                            else:
                                self.m_hum["courses done"].append([i,0]) 
                                self.reduced_courses_list.remove(i)    
                                
                counter -=1            
        return self.m_hum
        
    def check_arts(self, student):
        """
        course structure
        #Course(namecourse, code, number, credits_num, req_list, course_key)
        #Course_taken(course, student, course_section, grade, term, c_type)
        
        when passing the course to the list
        0 = Failed (below D-)
        1 = Grade requirement satifsfied (above C)
        2 = Grade requirement not satifsfied (between D- and C-)
        3 = current
        
            if self.highschool==1:
                course = Course("Fine Arts Elective", "FA", "----", 3, [], "")
                cc = Course_taken(course, student, 1, "P", "waived", 0)
                self.m_fa["courses missing"] -= 1
                self.m_fa["courses done"].append([cc,1])
            else:
        """

        counter = len(self.reduced_courses_list)
        while counter>0 and self.m_fa["courses missing"]!=0:
            course_codes = ["FA","AH", "ARCH", "AS", "CW", "DR", "MUS"]
            for i in self.reduced_courses_list:
                if self.m_fa["courses missing"] == 0:
                    break
                else:
                    for j in course_codes:
                        if j == i.course.get_code():
                            #c_creds = i.course.get_credits()
                            if i.get_grade() >= letter_to_number.get("F"): #check on grades
                                self.m_fa["courses done"].append([i,1]) 
                                self.reduced_courses_list.remove(i)
                                self.m_fa["courses missing"] -= 1
                            else:
                                self.m_fa["courses done"].append([i,0]) 
                                self.reduced_courses_list.remove(i)                                
                counter -= 1
        return self.m_fa
        
        
        
    def check_flanguage(self, student): 
        """
        course structure
        #Course(namecourse, code, number, credits_num, req_list, course_key)
        #Course_taken(course, student, course_section, grade, term, c_type)
        
        when passing the course to the list
        0 = Failed (below D-)
        1 = Grade requirement satifsfied (above C)
        2 = Grade requirement not satifsfied (between D- and C-)
        3 = current
        """
        counter = len(self.reduced_courses_list)
        while counter>0 and self.m_flang["courses missing"]!=0:
            if self.highschool==1:
                #should this only do a merge and print waived?
                number_list = ["First Required Course", "Second Required Course"]
                for i in range(0,2):
                    course = Course(number_list[i], "----", "----", "----", [], "")
                    cc = Course_taken(course, student, 1, "P", "waived", 0)
                    self.m_flang["courses missing"] -= 1
                    self.m_flang["courses done"].append([cc,1])

            else:
                course_codes = ["FR", "IT", "SPAN"]
                for i in self.reduced_courses_list:
                    for i in self.reduced_courses_list:
                        if self.m_flang["courses missing"] == 0:
                            break
                        for j in course_codes:
                            if j == i.course.get_code():
                                c_creds = i.course.get_credits()
                                if i.get_grade() >= letter_to_number.get("C"): #check on grades
                                    self.m_flang["courses done"].append([i,1]) 
                                    self.reduced_courses_list.remove(i)
                                    if c_creds == 3:                               #check on credits
                                        self.m_flang["courses missing"] -= 1
                                    elif c_creds == 6:
                                        self.m_flang["courses missing"] -= 2
                                else:
                                    self.m_flang["courses done"].append([i,0]) 
                                    self.reduced_courses_list.remove(i)                                
                    counter -=1
        return self.m_flang
    
    def return_missing(self):
        #"Math", "Math, Science, Computer Science", "Foreign Language", "Sosc", "Hum", "FA", "Additional Requirements", "Core Courses", "Major Electives", "Major 1", "Major 2"
        missing_numcourses = [self.m_ma["courses missing"], self.m_sci["courses missing"], self.m_flang["courses missing"], self.m_sosc["courses missing"], self.m_hum["courses missing"], self.m_fa["courses missing"], self.m_additional["courses missing"], self.m_core["courses missing"], self.m_electives["courses missing"], "NA", "NA"]
        return missing_numcourses
""" 
    #needs to be checked, ma not 100 nor 101
    def check_sciences(self, student):
        #MA, NS, CS
        #Course(self, namecourse, code, number, credits_num, req_list, course_key)
        #Course_taken(self, course, student, course_section, grade, term, c_type)
        while self.m_sci["courses missing"] > 0:
            if self.highschool==1:
                #first course
                course = Course("Mathematics Elective", "MA", "----", 3, [], "")
                cc = Course_taken(course, student, 1, "P", "waived", 0)
                self.m_sci["courses missing"] -= 1
                self.m_sci["courses done"].append([cc,1])
                #second course
                course = Course("Science Elective", "SCI", "----", 3, [], "")
                cc = Course_taken(course, student, 1, "P", "waived", 0)
                self.m_sci["courses missing"] -= 1
                self.m_sci["courses done"].append([cc,1])
            else:
                course_codes = ["CL", "EN", "GRK", "HM", "HS", "ITS", "LAT", "PH", "RL"]
                for i in self.reduced_courses_list:
                    for j in course_codes:
                        if j == i.course.get_code():
                            c_creds = i.course.get_credits()
                            if i.get_grade() >= letter_to_number.get("F"): #check on grades
                                self.m_sci["courses done"].append([i,1]) 
                                self.reduced_courses_list.remove(i)
                                if c_creds == 3:                               #check on credits
                                    self.m_sci["courses missing"] -= 1
                                elif c_creds == 6:
                                    self.m_sci["courses missing"] -= 2
                            else:
                                self.m_sci["courses done"].append([i,0]) 
                                self.reduced_courses_list.remove(i)                                
        return self.m_sci
"""        
        
        
    #def check_minor1(self):
    
    #def check_minor2
    #"English Composition and Literature", "Math Proficiency", "Math, Science, Computer Science", "Foreign Language", "Social Sciences", "Humanities", "Fine Arts", "Additional Requirements", "Core Courses", "Major Electives", "Major 1", "Major 2"    
    
    
    
        
def create_student_list():
    #with open('students_file.json', 'r') as myfile:
    with open('students_list.json', 'r') as myfile:
       students_list = json.load(myfile)
      
    student_obj = []
   
    for i in range(0, len(students_list)): 
        curr_student = students_list[i]
        student = Student(curr_student[0], curr_student[1], curr_student[2], curr_student[3], curr_student[4], curr_student[5])
        courses_t = curr_student[6]
        for course in courses_t:
            student.add_course(course)
        #print(student.courses_done)
        student_obj.append(student)
        i = i+1
        return student_obj