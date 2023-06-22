# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 16:15:21 2022

@author: ilda1
"""

#from majors import Major
from courses import Course, Course_taken
#from courses import letter_to_number
#NB: major = Major(...)
#    def __init__(self, name, surname, highschool_credits, major, minor1, minor2, courses_done):
import math

letter_to_number = {
    "A" : 4,
    "A-" : 3.67,
    "B+" : 3.33,
    "B" : 3,
    "B-" : 2.67,
    "C+" : 2.33,
    "C" : 2,
    "C-" : 1.67,
    "D+" : 1.33,
    "D" : 1,
    "D-" : 0.67, 
    "F" : 0,
    "INC" : 0.1,
    "P" : 5,
    "NP" : 0.2,
    "W" : 0.3,
    "current" : 0.4,
    "TR" : 0.5 # PA: added this entry, for Transfer credits,
    }

number_to_letter = {
    4 : "A",
    3.67 :"A-",
    3.33 :"B+",
    3 : "B",
    2.67 : "B-",
    2.33 : "C+",
    2 : "C",
    1.67 : "C-",
    1.33 : "D+",
    1 : "D",
    0.67: "D-", 
    0 : "F",
    0.1 : "INC", #incomplete
    5 : "P",
    0.2 : "NP",
    0.3 : "W",
    0.4 : "current",
    0.5 : "TR", # PA: added this entry, for Transfer credits
    }

import json

class Student:
    
    def __init__(self, name, surname, language_waived, major, minor1, minor2):
        self.name = name
        self.surname = surname
        self.language_waived = language_waived #=1 if yes
        self.major = major
        self.minor1 = minor1
        self.minor2 = minor2
        self.courses_done = []
        self.credits_earned = 0
        self.credits_nxsem = 0
        #must be changed to account for double major
        self.credits_missing = 120
        self.gpa = 0
        self.curr_standing = ""
        self.nx_standing = ""
        self.reduced_courses_list = [] #created with the actual list gets reduced as requirements are checked
        self.m_en = {"courses remaining": [["EN", 103],["EN", 105],["EN", 110]], "courses prov" : [], "output courses":[]}
        self.m_ma = {"courses missing"  : 1, "courses done" : []}
        self.m_sci = {"courses missing"  : 2, "courses done" : []}
        self.m_flang = {"courses missing"  : 2, "courses done" : []}
        self.m_sosc = {"courses missing"  : 2, "courses done" : []}
        self.m_hum = {"courses missing"  : 2, "courses done" : []}
        self.m_fa = {"courses missing"  : 1, "courses done" : []}
        self.m_additional = {"courses missing"  : 0, "courses done" : [], "courses remaining": []}
        self.m_core = {"courses missing"  : 0, "courses done" : [], "courses remaining": []}
        self.m_majorelectives = {"courses missing"  : 0, "courses done" : []}
        self.m_genelectives = []
        
        
        #attributes for the prerequisites check
        self.current_courses = []
        self.noncurrent_courses = []
        self.req_satisfied = []
        self.req_not_satisfied = []
        self.iteration = 0
        #self.prerequisite_reason = ""
        self.single_reason = ""
        self.prerequisite_reason = []
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Return Functions
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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
    
    def get_additional_remaining(self):
        return self.m_additional["courses remaining"]
    
    def get_core_remaining(self):
        return self.m_core["courses remaining"]
    
    
    #adds to the lit of courses the list for each course done by the student
    def add_course(self, course):
        self.courses_done.append(course)
    
    #change major key into major object
    def change_major(self, majorobj):
        self.major = majorobj
        #print(self.major)
        
    #change list of courses into the list of objects of the class Courses_taken
    def change_courses(self, courses_taken_obj):
        self.courses_done = courses_taken_obj
        
    def cumpute_gpa(self):
        #do they compure it on the semester and then they do the total or it's
        #the average of the courses' grades?
        #PA: It is the average of the courses grades, weighted on the credits
        creds = 0
        weighted_total=0
        for i in self.reduced_courses_list:
            grade = i.get_grade()
            # PA: I am excluding the grades that should not be counted:
            # P (5), W, NP, current, INC, TR (between 0.1 and 0.5 - using 0.6 just in case)
            # We should also consider the possible retake (if two grades, only consider the second)
            if grade != 5 and not (0.1 <= grade <= 0.6):
                course_credit = i.get_credits()
                creds += course_credit
                weighted_total += course_credit*grade
        if creds != 0:
            self.gpa = round(weighted_total / creds, 2) # rounding to 2 decimal digits
        else:
            self.gpa = 0
    
    def compute_credits_earned(self):
        self.credits_earned = 0
        for i in self.reduced_courses_list:
            if i.get_grade()>= letter_to_number.get("D-"):
            #if grade != "": # PA: this should also be updated to use the dictionary values
                course_credit = i.get_credits()
                self.credits_earned += course_credit
            
    def compute_credits_nxsem(self):
        for i in self.reduced_courses_list:
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
        for i in range(len(self.courses_done)-1, -1, -1):
            current_course = self.courses_done[i]
            to_insert = True #è da inserire in reduced
            #print(current_course.course.get_code())
            for h in self.reduced_courses_list:
                if current_course.course.get_number() == h.course.get_number() and current_course.course.get_code() == h.course.get_code() and (current_course.course.get_number() not in special_courses or (current_course.course.get_number()==299 and current_course.course.get_code()=="MA")):
                        to_insert = False # non è da inserire
            if to_insert:
                self.reduced_courses_list.insert(0, current_course)
                
            #print(len(self.reduced_courses_list))
        
    def check_ma_req(self):
        math_req = self.major.get_math_requirement()

        if math_req == 1:
            course_key = 54
            for i in self.reduced_courses_list[:]:
                if course_key == i.course.get_course_key():
                    if i.get_grade() == letter_to_number.get("current"):
                        self.m_ma["courses missing"] -= 1
                        self.m_ma["courses done"].append([i, 2]) 
                        self.reduced_courses_list.remove(i)  
                    elif i.get_grade() >= letter_to_number.get("C-"):
                        self.m_ma["courses missing"] -= 1
                        self.m_ma["courses done"].append([i, 1]) 
                        self.reduced_courses_list.remove(i)   
                    else:
                        self.m_ma["courses done"].append([i, 0]) 
                        self.reduced_courses_list.remove(i)       
        else:
            course_key = [53,54]
            for key in course_key:
                for i in self.reduced_courses_list[:]:
                    if course_key == i.course.get_course_key():
                        if i.get_grade() == letter_to_number.get("current"):
                            self.m_ma["courses missing"] -= 1
                            self.m_ma["courses done"].append([i, 2]) 
                            self.reduced_courses_list.remove(i) 
                        elif i.get_grade() >= letter_to_number.get("C-"):
                            self.m_ma["courses missing"] -= 1
                            self.m_ma["courses done"].append([i,1]) 
                            self.reduced_courses_list.remove(i)
                        else:
                            self.m_ma["courses done"].append([i, 0]) 
                            self.reduced_courses_list.remove(i) 
                        break
        return self.m_ma

 
    def check_additional(self):
        additional_courses = self.major.get_additional_requirements()
        for i in additional_courses[:]:
            counter = i[0] 
            self.m_additional["courses missing"] += i[0]
            for j in self.reduced_courses_list[:]:
                for m in i[1]:
                    if counter!=0 and j.course.get_number() >= m[1] and j.course.get_number() <= m[2] and (j.course.get_code().startswith(m[0]) or j.course.get_code().endswith(m[0])):
                        if j.get_grade() == letter_to_number.get("current"):
                            self.m_additional["courses done"].append([j,2])
                            self.reduced_courses_list.remove(j)
                            additional_courses.remove(i)
                            counter -= 1
                            self.m_additional["courses missing"] -= 1
                        elif j.get_grade() >= letter_to_number.get("D"):
                            self.m_additional["courses done"].append([j,1])
                            self.reduced_courses_list.remove(j)
                            additional_courses.remove(i)
                            counter -= 1
                            self.m_additional["courses missing"] -= 1
                        else:
                            self.m_additional["courses done"].append([j,0])
                            self.reduced_courses_list.remove(j)
                            additional_courses.remove(i)
                            counter -= 1
                            self.m_additional["courses missing"] -= 1
        self.m_additional["courses remaining"] = additional_courses
        return self.m_additional 
    

    def check_core(self):
        core_courses = self.major.get_core_courses()
        #print(core_courses)
        for i in core_courses[:]:
            counter = i[0] 
            self.m_core["courses missing"] += i[0]
            for j in self.reduced_courses_list[:]:
                for m in i[1]:
                    if counter!=0 and j.course.get_number() >= m[1] and j.course.get_number() <= m[2] and (j.course.get_code().startswith(m[0]) or j.course.get_code().endswith(m[0])):
                        if j.get_grade() == letter_to_number.get("current"):
                            #print(j.course.get_code())
                            #print(j.course.get_number())
                            self.m_core["courses done"].append([j,2])
                            self.reduced_courses_list.remove(j)
                            core_courses.remove(i)
                            counter -= 1
                            self.m_core["courses missing"] -= 1
                        elif j.get_grade() > letter_to_number.get("D"):
                            #print(j.course.get_code())
                            #print(j.course.get_number())
                            self.m_core["courses done"].append([j,1])
                            self.reduced_courses_list.remove(j)
                            core_courses.remove(i)
                            counter -= 1
                            self.m_core["courses missing"] -= 1
                        elif j.get_grade() == letter_to_number.get("D"):
                            #print(j.course.get_code())
                            #print(j.course.get_number())
                            self.m_core["courses done"].append([j,3])
                            self.reduced_courses_list.remove(j)
                            core_courses.remove(i)
                            counter -= 1
                            self.m_core["courses missing"] -= 1
                        else:
                            #print(j.course.get_code())
                            #print(j.course.get_number())                            
                            self.m_core["courses done"].append([j,0])
                            self.reduced_courses_list.remove(j)
                            core_courses.remove(i)
                            counter -= 1
                            self.m_core["courses missing"] -= 1
        self.m_core["courses remaining"] = core_courses
        return self.m_core

    
    def check_major_electives(self):
        """
        STRUCTURE:
            "major electives": [[3, [["EC", 300, 1000], ["FIN", 300, 1000]]], [3, [["EC", 200, 1000], ["FIN", 200, 1000], ["BUS", 200, 1000], ["LAW", 200, 1000], ["MA", 200, 1000], ["MGT", 200, 1000], ["MKT", 200, 1000], ["PL", 200, 1000], ["PS", 200, 1000]]]]
            [cap courses, [list of possible electives indicated with code and interval of valid numbers]]
        """
        melective_list = self.major.get_major_electives()
        #if self.major.get_name != "Business Administration" : 
        for i in melective_list:
            counter = i[0] 
            self.m_majorelectives["courses missing"] += i[0]
            for j in self.reduced_courses_list[:]:
                for m in i[1]:
                    if counter!=0 and j.course.get_number() >= m[1] and j.course.get_number() <= m[2] and (j.course.get_code().startswith(m[0]) or j.course.get_code().endswith(m[0])):
                        if j.get_grade() == letter_to_number.get("current"):
                            self.m_majorelectives["courses done"].append([j,2])
                            self.reduced_courses_list.remove(j)
                            counter -= 1
                            self.m_majorelectives["courses missing"] -= 1
                        elif j.get_grade() >= letter_to_number.get("D"):
                            self.m_majorelectives["courses done"].append([j,1])
                            self.reduced_courses_list.remove(j)
                            counter -= 1
                            self.m_majorelectives["courses missing"] -= 1
                        else:
                            self.m_majorelectives["courses done"].append([j,0])
                            self.reduced_courses_list.remove(j)
                            counter -= 1
                            self.m_majorelectives["courses missing"] -= 1
    
        return self.m_majorelectives
      
        
    def check_genelectives(self):
        for i in self.reduced_courses_list[:]:
            if i.get_grade() == letter_to_number.get("current"):
                self.m_genelectives.append([i,2])
            elif i.get_grade() >= letter_to_number.get("D"):
                self.m_genelectives.append([i,1])
            else:
                self.m_genelectives.append([i,0])
        return self.m_genelectives

#new ver with en as dictionary

    def generate_en_courses(self, courses_list):
        for i in range(0, len(self.m_en["courses remaining"])):
            curr_info = self.m_en["courses remaining"][i]
            for m in courses_list: #m is an object course
                if curr_info[0]==m.get_code() and curr_info[1]==m.get_number():
                    self.m_en["courses prov"].append(m)
    
    def substitute_courses_done(self):
        for i in range(0, len(self.m_en["courses prov"])):
            curr_course = self.m_en["courses prov"][i]
            #course, student, course_section, grade, term, c_type
            en_taken_prov = Course_taken(curr_course, self, "", "", "", "")
            self.m_en["output courses"].append([en_taken_prov,1])
        

    def check_eng_composition(self):
            #when passing the course to the list
            #0 = Failed (below D-)
            #1 = Grade requirement satifsfied (above C)
            #2 = Grade requirement not satifsfied (between D- and C-)
            #3 = current
            #self.m_en = {"courses remaining": [["EN", 103],["EN", 105],["EN", 110]],"courses prov" : [],  "output courses":[]}
            
            for i in self.reduced_courses_list[:]:
                if i.course.get_code().startswith("EN") or i.course.get_code().endswith("EN"):
                #if i.course.get_code()=="EN":
                    if i.course.get_number() == 103:
                        if i.get_grade() >= letter_to_number.get("C"):
                            self.m_en["output courses"][0] = [i,1]
                        elif i.get_grade() >= letter_to_number.get("D-"):
                            self.m_en["output courses"][0] = [i,2]
                        elif i.get_grade() >= letter_to_number.get("current"):
                            self.m_en["output courses"][0] = [i,3]
                        else:
                            self.m_en["output courses"][0] = [i,0]
                        self.reduced_courses_list.remove(i)
    
                    elif i.course.get_number() == 105 :
                        if i.get_grade() >= letter_to_number.get("C"):
                            self.m_en["output courses"][1] = [i,1] 
                        elif i.get_grade() == letter_to_number.get("current"):
                            self.m_en["output courses"][1] = [i,3]
                        else:
                            self.m_en["output courses"][1] = [i,0]
                        self.reduced_courses_list.remove(i)
                        
                    elif i.course.get_number() == 110:
                        if i.get_grade() >= letter_to_number.get("C"):
                            self.m_en["output courses"][2] = [i,1] 
                        elif i.get_grade() == letter_to_number.get("current"):
                            self.m_en["output courses"][2] = [i,3]
                        else:
                            self.m_en["output courses"][2] = [i,0]
                        self.reduced_courses_list.remove(i)
                        
                        
    def check_eng_literature(self):  
            lit_counter = 0       
            approved_substitute = False #for the approved substitute for en
            for i in self.reduced_courses_list[:]:
                if i.course.get_code().startswith("EN") or i.course.get_code().endswith("EN"):
                    if i.course.get_number() >= 200 and lit_counter<2:
                        if i.get_grade() >= letter_to_number.get("D-"):
                            self.m_en["output courses"].append([i,1])
                        elif i.get_grade() == letter_to_number.get("current"):
                            self.m_en["output courses"].append([i,3])
                        else:
                            self.m_en["output courses"].append([i,0])
                        self.reduced_courses_list.remove(i)
                        lit_counter += 1
                    
                elif  i.course.get_code()== "CL" and approved_substitute==False and lit_counter<2:
                    if i.course.get_number()== 268 or i.course.get_number()== 278:
                        if i.get_grade() >= letter_to_number.get("D-"):
                            self.m_en["output courses"].append([i,1])
                        elif i.get_grade() == letter_to_number.get("current"):
                            self.m_en["output courses"].append([i,3])
                        else:
                            self.m_en["output courses"].append([i,0])
                        self.reduced_courses_list.remove(i)
                        approved_substitute = True
                        lit_counter += 1
                        
                elif i.course.get_code()== "ITS" and i.course.get_number()==292 and approved_substitute==False and lit_counter<2:
                    if i.get_grade() >= letter_to_number.get("D-"):
                        self.m_en["output courses"].append([i,1])
                    elif i.get_grade() == letter_to_number.get("current"):
                        self.m_en["output courses"].append([i,3])
                    else:
                        self.m_en["output courses"].append([i,0])
                    self.reduced_courses_list.remove(i)
                    approved_substitute = True
                    lit_counter += 1
                    
            return self.m_en    
        
    def check_sci(self, student):
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
        while counter>0 and self.m_sci["courses missing"]!=0:
            course_codes = ["MA", "NS", "SCI", "CS"]
            for i in self.reduced_courses_list[:]:
                if self.m_sci["courses missing"] == 0:
                    break
                else:
                    for j in course_codes:
                        if i.course.get_code().startswith(j) or i.course.get_code().endswith(j):
                        #if j == i.course.get_code():
                            c_creds = i.course.get_credits()
                            if i.get_grade() == letter_to_number.get("current"):
                                self.m_sci["courses done"].append([i,2]) 
                                self.reduced_courses_list.remove(i)
                                if c_creds == 3:                               #check on credits
                                    self.m_sci["courses missing"] -= 1
                                elif c_creds == 6:
                                    self.m_sci["courses missing"] -= 2
                            elif i.get_grade() >= letter_to_number.get("F"): #check on grades
                                self.m_sci["courses done"].append([i,1]) 
                                self.reduced_courses_list.remove(i)
                                if c_creds == 3:                               #check on credits
                                    self.m_sci["courses missing"] -= 1
                                elif c_creds == 6:
                                    self.m_sci["courses missing"] -= 2
                            else:
                                self.m_sci["courses done"].append([i,0]) 
                                self.reduced_courses_list.remove(i)        
                counter -= 1 
        return self.m_sci

        
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
        
        if self.language_waived==1:
            course = Course("Social Science Elective", "SOSC", "----", 6, [], "")
            cc = Course_taken(course, student, 1, "P", "waived", 0)
            self.m_sosc["courses missing"] -= 2
            self.m_sosc["courses done"].append([cc,1])
        else:
        """
        counter = len(self.reduced_courses_list)
        while counter>0 and self.m_sosc["courses missing"]!=0:
            course_codes = ["COM", "CMS", "DMA", "DJRN", "EC", "GEOG", "PL", "PS", "SOSC"]
            for i in self.reduced_courses_list[:]:
                if self.m_sosc["courses missing"] == 0:
                    break
                else:
                    for j in course_codes:
                        if i.course.get_code().startswith(j) or i.course.get_code().endswith(j):
                        #if j == i.course.get_code():
                            c_creds = i.course.get_credits()
                            if i.get_grade() == letter_to_number.get("current"):
                                self.m_sosc["courses done"].append([i,2]) 
                                self.reduced_courses_list.remove(i)
                                if c_creds == 3:                               #check on credits
                                    self.m_sosc["courses missing"] -= 1
                                elif c_creds == 6:
                                    self.m_sosc["courses missing"] -= 2
                            elif i.get_grade() >= letter_to_number.get("F"): #check on grades
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
        
            if self.language_waived==1:
                course = Course("Latin Elective", "LAT", "----", 6, [], "")
                cc = Course_taken(course, student, 1, "P", "waived", 0)
                self.m_hum["courses missing"] -= 2
                self.m_hum["courses done"].append([cc,1])
            else:
        """
        counter = len(self.reduced_courses_list)
        while counter>0 and self.m_hum["courses missing"]!=0:
            course_codes = ["CL", "EN", "GRK", "HM", "HS", "ITS", "LAT", "PH", "RL"]
            for i in self.reduced_courses_list[:]:
                if self.m_hum["courses missing"] == 0:
                    break
                else:
                    for j in course_codes:
                        if i.course.get_code().startswith(j) or i.course.get_code().endswith(j):
                        #if j == i.course.get_code():
                            c_creds = i.course.get_credits()
                            if i.get_grade() == letter_to_number.get("current"):
                                self.m_hum["courses done"].append([i,2]) 
                                self.reduced_courses_list.remove(i)
                                if c_creds == 3:                               #check on credits
                                    self.m_hum["courses missing"] -= 1
                                elif c_creds == 6:
                                    self.m_hum["courses missing"] -= 2
                            elif i.get_grade() >= letter_to_number.get("F"): #check on grades
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
        
            if self.language_waived==1:
                course = Course("Fine Arts Elective", "FA", "----", 3, [], "")
                cc = Course_taken(course, student, 1, "P", "waived", 0)
                self.m_fa["courses missing"] -= 1
                self.m_fa["courses done"].append([cc,1])
            else:
        """

        counter = len(self.reduced_courses_list)
        while counter>0 and self.m_fa["courses missing"]!=0:
            course_codes = ["FA","AH", "ARCH", "AS", "CW", "DR", "MUS"]
            for i in self.reduced_courses_list[:]:
                if self.m_fa["courses missing"] == 0:
                    break
                else:
                    #print("entered check")
                    for j in course_codes:
                        if (i.course.get_code().startswith(j) or i.course.get_code().endswith(j)) and i.course.get_code()!="RAS":
                        #if j == i.course.get_code():
                            #c_creds = i.course.get_credits()
                            if i.get_grade() >= letter_to_number.get("F"): #check on grades
                                #print("added course")
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
            if self.language_waived==1:
                #should this only do a merge and print waived?
                number_list = ["First Required Course", "Second Required Course"]
                for i in range(0,2):
                    course = Course(number_list[i], "----", "----", "----", [], "")
                    cc = Course_taken(course, student, 1, "P", "waived", 0)
                    self.m_flang["courses missing"] -= 1
                    self.m_flang["courses done"].append([cc,1])

            else:
                course_codes = ["FR", "IT", "SPAN"]
                for i in self.reduced_courses_list[:]:
                    for i in self.reduced_courses_list[:]:
                        if self.m_flang["courses missing"] == 0:
                            break
                        for j in course_codes:
                            #if j == i.course.get_code():
                            if i.course.get_code().startswith(j) or i.course.get_code().endswith(j):
                                c_creds = i.course.get_credits()
                                if i.get_grade() >= letter_to_number.get("current"): #check on grades
                                    self.m_flang["courses done"].append([i,2]) 
                                    self.reduced_courses_list.remove(i)
                                    if c_creds == 3:                               #check on credits
                                        self.m_flang["courses missing"] -= 1
                                    elif c_creds == 6:
                                        self.m_flang["courses missing"] -= 2
                                elif i.get_grade() >= letter_to_number.get("C"): #check on grades
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
        missing_numcourses = [self.m_ma["courses missing"], self.m_sci["courses missing"], self.m_flang["courses missing"], self.m_sosc["courses missing"], self.m_hum["courses missing"], self.m_fa["courses missing"], self.m_additional["courses missing"], self.m_core["courses missing"], self.m_majorelectives["courses missing"], "NA", "NA"]
        return missing_numcourses
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Prerequisites Check
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
    def create_curr_list(self):
        """
        this function creates a list that contains only the courses that the student is taking currently 
        and one that contains all the courses that the student has done in the past semesters
        """
        copy_list = self.reduced_courses_list[:]
        self.noncurrent_courses = copy_list
        for i in self.reduced_courses_list[:]:
            if i.get_grade() == 0.4:
                #print(f"adding {i.course.get_name()}")
                self.current_courses.append(i)
                self.noncurrent_courses.remove(i)
                
    
    def return_current(self):
        print(self.current_courses)
        return self.current_courses
    

    def attributes_check(self, courses_taken, prerequisite, req_type, counter_alts):
        """
        this function gets one course out of all the courses that satisfy the same prerequisite
        and the list of all the courses that should be looked into to find the requirement
        so, the attrribute that should be passed for prerequisites is the list of courses excluding the current ones
        while the one that should be passed for corequisites is the list of all courses including current
        """
        #self.prerequisite_reason = ""
        
        found = False
        #self.single_reason = ""
        
        courses_taken = courses_taken #list of courses that the student has taken
        prerequisite = prerequisite #single alternative for the specific prerequisite
        req_type = req_type #either prerequisites or corequisites
        counter_alts = counter_alts #number of courses that satisfy the same requirement
        
        single_reason = ""
        requirement_pair = []
        
        #self.single_reason = "" #Appoggio per dare una reason a ciascuna delle alternative
        
        #missing_list = []
        #goes through all courses done
        for c_taken in courses_taken[:]:
            #specific for each course to mantain the structure
            #appoggio = {"course": [], "reason": []}
            
            taken_code = c_taken.course.get_code()
            taken_num = c_taken.course.get_number()
            taken_grade = c_taken.get_grade()    
            
            prereq_code = prerequisite["code"]
            prereq_grade = prerequisite["grade"]
            
            #if prereq_grade is float:
                #prereq_grade = "D-"
                    
            lower_bound = prerequisite["lower bound"]
            upper_bound = prerequisite["upper bound"]
            
            if found == True:
                break
            
            #se il prerequisito è lo standing
            elif prereq_code == "S":
                if self.credits_earned>=lower_bound:
                    found = True
                    
            #se il prerequisito è un qualunque corso o range di corsi
            else:
                #if remove.course.get_code() == "CS" and remove.course.get_number() == 320:
                    #print(f"analyzing for {remove.course.get_code()}{remove.course.get_number()}: {taken_code} {taken_num}")

                if taken_code == prereq_code and ((int(taken_num)>int(lower_bound) and int(taken_num)<int(upper_bound)) or (int(taken_num)==int(lower_bound) and int(taken_num)==int(upper_bound))):
                     #print(counter_alts)
                     #prerequisiti 
                     if req_type == "prerequisite":
                         if taken_grade>=letter_to_number.get(prereq_grade):
                             #print(f"found: {prerequisite}")
                             found = True
                             #print("found")
                             break
                         else: 
                             if taken_grade==letter_to_number.get("NP") or taken_grade==letter_to_number.get("W"):
                                 if counter_alts == 1:
                                     single_reason = "Failed"
                                     #self.prerequisite_reason.append(single_reason)
                                     #print("append 1")
                                 else:
                                     single_reason = f"{taken_code}{taken_num} Failed"
                                     #self.prerequisite_reason.append(single_reason)
                                     #print("append 2")
                                    
                             elif taken_grade==letter_to_number.get("INC"):
                                 if counter_alts == 1:
                                     single_reason = "Incomplete"
                                     #self.prerequisite_reason.append(single_reason)
                                 else:
                                     single_reason = f"{taken_code}{taken_num} Incomplete"
                                     #self.prerequisite_reason.append(single_reason)
                            
                             elif taken_grade==letter_to_number.get("F"):
                                 if counter_alts == 1:
                                     single_reason = "Failed"
                                     #self.prerequisite_reason.append(single_reason)
                                     #print("append 1")
                                 else:
                                     single_reason = f"{taken_code}{taken_num} Failed"
                                     #self.prerequisite_reason.append(single_reason)
                                     #print("append 2")
                             else:
                                #print("Grade requirement entered")
                                if counter_alts == 1:
                                    grade = number_to_letter.get(taken_grade)

                                    single_reason = f"Grade req ({grade})"
                                    #self.prerequisite_reason.append(single_reason)
                                else:
                                    grade = number_to_letter.get(taken_grade)
                                    single_reason = f"Grade req ({grade} in {taken_code}{taken_num})"
                                    #self.prerequisite_reason.append(single_reason)
                                 
                                 
                    
                     #corequisiti dovrebbero avere anche current ammissibile come voto
                     elif req_type == "corequisite":
                        
                        if (taken_grade>=letter_to_number.get(prereq_grade)) or (taken_grade == letter_to_number.get("current")):
                            #print(f"found: {prerequisite}")
                            found = True
                            #print("found")
                            break
                        
                        else:
                             if counter_alts == 1:
                                grade = number_to_letter.get(taken_grade)
                                single_reason = f"Grade req ({grade})"
                                #self.prerequisite_reason.append(single_reason)
                             else:
                                grade = number_to_letter.get(taken_grade)
                                single_reason = f"Grade req ({grade} in {taken_code}{taken_num})"                                 
                                #self.prerequisite_reason.append(single_reason)
                            

            """        
            if self.single_reason == "":
                self.single_reason = "Missing"
                self.prerequisite_reason.append(self.single_reason) 
            """
        requirement_pair.append(found)
        requirement_pair.append(single_reason)

        return requirement_pair
                    
    def check_requirements(self):
        myReportFile = open("report.txt", "w")

        #for loop sui current course:
        info_list = [] #will contain the current courses that do not satisfy the requirements in addition to the missing requirements
        
        for m in self.current_courses[:]:
            #print('\n')
            #print(m.course.get_name())  
            info = []
            missing_req = {"prerequisite" : [], "corequisite" : []} #will contain the missing requirement, will be different for each of the courses
            
            #di ogni corso prende prerequisites e corequisites e li mette in req_list:
            current_requirements = m.course.get_requirements_dictionary() # current_prerequisites1 = {"prerequisite" : [[{}, {}]], "corequisite": [[{}], [{}]]}
            req_list = ["prerequisite", "corequisite"]
            
               
            #for loop su req_list:
            for i in req_list[:]: #first checks prereq then coreq
                requirements = current_requirements[i] #either prerequisites or corequisites [[{}, {}], [{}], [{}]]
                found = False
                self.iteration = len(requirements)
                #missing
                #self.prerequisite_reason.clear()
                for requirement in requirements[:]: #[{}, {}, {}] # a single requirement, which is a list of the possible alternatives that satisfy it
                    #found = False    
                #print(requirement)
                    #print(requirements)
                    #print("\n")
                    #self.single_reason = ""
                    reasons = []
                    counter_alts = len(requirement)
                    #self.prerequisite_reason.clear()
                    #prerequisite_reason = []
                    
                    for alternative in requirement[:]: #one of the list of courses that satisfy the same requirement
                        req_reason = ""    
                    #self.single_reason = ""
                        #counter_alts = len(requirement)
                        if found == True:
                            break
                        
                        elif found == False:
                            #print("not")
                            #if m.course.get_code() == "CL" and m.course.get_number() == 381:
                                #print(alternative)
                            if i == "prerequisite":
                                requirement_pair = self.attributes_check(self.noncurrent_courses, alternative, i, counter_alts)
                            elif i == "corequisite":
                                requirement_pair = self.attributes_check(self.reduced_courses_list, alternative, i, counter_alts)
                        #else:
                            #break
                            found = requirement_pair[0]
                            req_reason = requirement_pair[1]
                            if req_reason == "":
                                req_reason = "Missing"
                                                
                        reasons.append(req_reason) 
                        #print(req_reason)
                        #print(reasons)

                    if found == False: #il requirement non è stato soddisfatto 
                        if req_reason == "":
                            req_reason = "Missing"
                        #if self.single_reason == "":
                            #self.single_reason = "Missing"
                        #self.prerequisite_reason.append(self.single_reason)
                        #stuff = self.prerequisite_reason
                        missing_req[i].append([requirement, reasons])
                        #print("not found")
                        #break
                        
                    found = False
            
            #se al corso non mancano requirements da soddisfare lo ignora 
            #if len(missing_req["prerequisite"]) == 0 and len(missing_req["corequisite"]) == 0:
                #print("no missing prerequisites or corequisites")
                
            if len(missing_req["prerequisite"])!=0 or len(missing_req["corequisite"])!=0:
                info.append(m)
                info.append(missing_req)
                info_list.append(info)
                #print(info_list)
                myReportFile.write(f"\nCurrent course:  {m.course.get_name()}. Missing requirements: {missing_req}.")
                #myReportFile.write("Current course: " + m.course.get_name() + "missing requirements " + missing_req + ". \nFinal structure: info_list" + "\n")
        #myReportFile.close()
        print("\n")
        #print(info_list)
        myReportFile.write(f"\n\n\n{info_list}")

        return info_list
               
            
    def create_prereq_message(self):
        return "nope"
      
        
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
            print(course)
            student.add_course(course)
        #print(student.courses_done)
        student_obj.append(student)
        return student_obj