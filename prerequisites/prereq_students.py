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

#major
import json

class Student:
    
    def __init__(self, name, surname, language_waived, major1, major2, double_major, double_degree, minor1, minor2):
        self.name = name
        self.surname = surname
        self.language_waived = language_waived #=1 if yes
        self.major1 = major1
        self.major2 = major2
        self.double_major = double_major #yes/no category - this is true if the two majors are written in the same cell
        self.double_degree = double_degree #yes/no category - this is true if the second major is written in the cell respective to "Second Degree"
        self.minor1 = minor1
        self.minor2 = minor2
        self.courses_done = []
        self.credits_total = 120
        self.credits_earned = 0
        self.credits_nxsem = 0
        self.credits_missing = 0
        self.transfer_credits = 0
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
        
    def get_name(self):
        return self.name
    
    def get_surname(self):
        return self.surname
    
    def get_highschool(self):
        return self.highschool_credits
    
    def get_major1(self):
        return self.major1
    
    def get_major2(self):
        return self.major2
    
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
    
    #adds to the list of courses the list for each course done by the student
    def add_course(self, course):
        self.courses_done.append(course)
    
    #change major key into major object
    def change_major1(self, majorobj):
        self.major1 = majorobj
        
    def change_major2(self, majorobj):
        self.major2 = majorobj
        
    #change list of courses into the list of objects of the class Courses_taken
    def change_courses(self, courses_taken_obj):
        self.courses_done = courses_taken_obj
        
    def change_credits_total(self):
        if self.double_degree == 1:
            self.credits_total = 150
    
    #for every course that has not been dropped, this function checks if the course has not been done in residency
    #if so, it adds its credits to the total
    def compute_transfer_credits(self):
        for i in self.reduced_courses_list: 
            if i.get_transfer() == 1:
                self.transfer_credits += i.course.get_credits()
    
    def add_transfer_credits(self):
        if self.transfer_credits > 60:
            self.credits_total += (self.transfer_credits - 60)
        
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
    
    #does not account for minors, nor for double majors
    def compute_credits_missing(self):
        self.credits_missing = self.credits_total - self.credits_nxsem 
            
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
        #if self.major == [lista di id per le varie versioni di political sciences and international affairs (che hanno 4 corsi di lingua)]:
            #self.m_flang["courses missing"] = 4

        counter = len(self.reduced_courses_list)
        while counter>0 and self.m_flang["courses missing"]!=0:
            if self.language_waived==1 and self.m_flang["courses missing"] == 4:
                number_list = ["First Required Course", "Second Required Course", "Third Required Course", "Fourth Required Course"]
                for i in range(0,4):
                    course = Course(number_list[i], "----", "----", "----", [], "")
                    cc = Course_taken(course, student, 1, "P", "waived", 0)
                    self.m_flang["courses missing"] -= 1
                    self.m_flang["courses done"].append([cc,1])
                    
            elif self.language_waived==1 and self.m_flang["courses missing"] != 4:
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
                                if i.get_grade() >= letter_to_number.get("current"): #check on grades
                                    self.m_flang["courses done"].append([i,2]) 
                                    self.reduced_courses_list.remove(i)
                                    self.check_flanguage_level(i)
                                elif i.get_grade() >= letter_to_number.get("C"): #check on grades (passing grade)
                                    self.m_flang["courses done"].append([i,1]) 
                                    self.reduced_courses_list.remove(i)
                                    self.check_flanguage_level(i)
                                else:
                                    self.m_flang["courses done"].append([i,0]) #check on grades (failing grade)
                                    self.reduced_courses_list.remove(i)                                
                    counter -=1
        return self.m_flang
    
    def check_flanguage_level(self, fl_course):
        cnumber = fl_course.course.get_number() 
        if cnumber == 301: 
            if self.m_flang["courses missing"] < 5:
                self.m_flang["courses missing"] = 0
            else:
                self.m_flang["courses missing"] -= 5
        elif cnumber == 202: 
            if self.m_flang["courses missing"] < 4:
                self.m_flang["courses missing"] = 0
            else:
                self.m_flang["courses missing"] -= 4
        elif cnumber == 201: 
            if self.m_flang["courses missing"] < 3:
                self.m_flang["courses missing"] = 0
            else:
                self.m_flang["courses missing"] -= 3
        elif cnumber == 102: 
            if self.m_flang["courses missing"] < 2:
                self.m_flang["courses missing"] = 0
            else:
                self.m_flang["courses missing"] -= 2
        elif cnumber == 101:
            self.m_flang["courses missing"] -= 1


    def return_missing(self):
        #"Math", "Math, Science, Computer Science", "Foreign Language", "Sosc", "Hum", "FA", "Additional Requirements", "Core Courses", "Major Electives", "Major 1", "Major 2"
        missing_numcourses = [self.m_ma["courses missing"], self.m_sci["courses missing"], self.m_flang["courses missing"], self.m_sosc["courses missing"], self.m_hum["courses missing"], self.m_fa["courses missing"], self.m_additional["courses missing"], self.m_core["courses missing"], self.m_majorelectives["courses missing"], "NA", "NA"]
        return missing_numcourses
      
        
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