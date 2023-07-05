# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 16:15:21 2022

@author: ilda1
"""
#KEYWORDS
#get_credits


#from majors import Major
from courses import Course, Course_taken
from compareTerms import compare
#from courses import letter_to_number
#NB: major = Major(...)
#    def __init__(self, name, surname, highschool_credits, major, minor1, minor2, courses_done):

#myReportFile = open("reasoning.txt", "w")
#Report2 = open("removeretake.txt", "w")
#removeretake
 
import json
import math
import numpy as np
import pandas as pd

#print
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
    "TR" : 0.5, # PA: added this entry, for Transfer credits,
    "AU" : 0.01} 

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
    0.01 : "AU"}

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
        self.retaken_classes =  []
    
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
    
    def return_gpa(self):
        return self.gpa
    
    def return_creds_done(self):
        return self.credits_earned
    
    def return_courses_information(self):
        message = f"\nthe student has taken {len(self.courses_done)} in total, not retaken {len(self.reduced_courses_list)}, and is taking {len(self.current_courses)} currently."
        return message
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Action Functions
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    #adds to the lit of courses the list for each course done by the student
    def add_course(self, course):
        self.courses_done.append(course)
    
    #change major key into major object
    def change_major(self, majorobj):
        self.major = majorobj
        
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
            grade = i.get_grade()
            if pd.isnull(grade) != True:
                if i.get_grade()>= letter_to_number.get("D-") and letter_to_number.get("TR"):
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
    
    #removes from the list of courses that the student has done, and that the program uses
    #for the check, the courses that the student has taken again 
    
    def remove_retake(self):
        found_retake = False
        #poi da modificare perchè rimuova non rimuova l'old course se il nuovo voto è W, NP, INC
        #non deve togliere i duplicates dei corsi fatti non in residence
        special_courses = [0, 281, 299, 381, 399]
        #Report2.write(f"\n\n{self.get_name()}")
        #print(f"\n{self.get_name()}")
        for i in range(len(self.courses_done)-1, -1, -1):
            
            #for current_course in self.courses_done:
            current_course = self.courses_done[i] #first time around
            to_insert = True #è da inserire in reduced
            for h in self.reduced_courses_list[:]: #second time around
                if current_course.get_grade() == letter_to_number.get("AU"):
                    to_insert = False # non è da inserire
                    #Report2.write(f"\ndropping {current_course.course.get_name()} because AU")
                    #print(f"\ndropping {current_course.course.get_name()} because AU")
                    #found_retake = True
                elif pd.isnull(current_course.get_grade()) == True:
                    to_insert = False
                    #Report2.write(f"\ndropping {current_course.course.get_name()} because null")
                    #print(f"\ndropping {current_course.course.get_name()} because null")
                    found_retake = True
                    break
                elif current_course.course.get_number() == h.course.get_number() and current_course.course.get_code() == h.course.get_code() and (current_course.course.get_number()!=388 and current_course.course.get_code()!="RAS") and (current_course.course.get_number() not in special_courses or (current_course.course.get_number()==299 and current_course.course.get_code()=="MA")):
                    #to_insert = False # non è da inserire
                    #print(f"dropping {current_course.course.get_name()} because done in {current_course.get_term()} and again in {h.get_term()}")
                    if h.get_grade()==letter_to_number.get("INC") or h.get_grade()==letter_to_number.get("NP") or h.get_grade()==letter_to_number.get("W") or h.get_grade()==letter_to_number.get("current"):
                        'You are either retaking the class in a future semester, not got the grade yet, or this second time you got INC, NP, or W'
                        'then does not have to be dropped nor added to the retake'
                        #Report2.write(f"\nbreak: {current_course.course.get_name()} done in {current_course.get_term()} ({number_to_letter.get(current_course.get_grade())}), kept because {number_to_letter.get(h.get_grade())} in {h.get_term()}")
                        #print(f"\nbreak: {current_course.course.get_name()} done in {current_course.get_term()} kept because {number_to_letter.get(h.get_grade())} in {h.get_term()}")
                        found_retake = True
                        break
                        
                    elif h.get_grade()!=letter_to_number.get("INC") and h.get_grade()!=letter_to_number.get("NP") and h.get_grade()!=letter_to_number.get("W") and h.get_grade()!=letter_to_number.get("current"):
                        'you took a class twice, but the second time the grade was acceptable'
                        to_insert = False # non è da inserire
                        #Report2.write(f"\ndropping {current_course.course.get_name()} because done in {current_course.get_term()} ({number_to_letter.get(current_course.get_grade())}) and again in {h.get_term()} ({number_to_letter.get(h.get_grade())})")
                        found_retake = True
                        #print(f"\ndropping {current_course.course.get_name()} because done in {current_course.get_term()} and again in {h.get_term()}")
                #elif h.get_grade()!="INC" and h.get_grade()!="NP" and h.get_grade()!="W" and current_course.get_grade()!="INC" and current_course.get_grade()!="NP" and current_course.get_grade()!="W":
                    #if current_course.course.get_number() == h.course.get_number() and current_course.course.get_code() == h.course.get_code() and (current_course.course.get_number() not in special_courses or (current_course.course.get_number()==299 and current_course.course.get_code()=="MA")):
                        #to_insert = False # non è da inserire
                        #print(f"dropping {current_course.course.get_name()} because done in {current_course.get_term()} and again in {h.get_term()}")
                    """
                    (if h.get_grade()=="INC" or h.get_grade()=="NP" or h.get_grade()=="W") or current_course.get_grade()=="INC" or current_course.get_grade()=="NP" or current_course.get_grade()=="W":
                        to_insert = True
                        print("Warning! repeated and not finished")
                    else:
                        to_insert = False # non è da inserire
                        print(f"dropping {current_course.course.get_name()} because done in {current_course.get_term()} and again in {h.get_term()}")
                        """
                        
            if to_insert:
                #self.reduced_courses_list.insert(0, current_course)
                self.reduced_courses_list.insert(0, current_course)
                #self.retaken_classes.append(current_course)
            
            #elif found_retake==True:
                #self.retaken_classes.append(current_course)
        #if len(self.retaken_classes)!=0:
            #print(f"{self.get_name()}, total:{len(self.courses_done)}, left:{len(self.reduced_courses_list)}, retaken:{len(self.retaken_classes)}")
        
        #if found_retake == True:
            #Report2.write("\n")
            #self.print_courses()
        #to double check the student
        #if self.get_name()== "Ms. Taleha Whyte":
           #self.print_courses()
            #print(len(self.reduced_courses_list))
    '''
    def print_courses(self):
        for thing in self.reduced_courses_list:
            Report2.write(f"\n{thing.course.get_name()} in {thing.get_term()}")
        '''
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Degree Planner Checks Functions
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""    
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
                            #c_creds = i.course.get_credits()
                            c_creds = i.get_credits()
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
                            c_creds = i.get_credits()
                            #c_creds = i.course.get_credits()
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
                            #c_creds = i.course.get_credits()
                            c_creds = i.get_credits()
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
                                #c_creds = i.course.get_credits()
                                c_creds = i.get_credits()
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
        NB the current courses done in semesters other than the last one are still dropped from the current list
        rather they are put in the noncurrent_courses list
        This is because otherwise it would raise problems on prerequisites that the student might fullfill in the active semester
        """
        copy_list = self.reduced_courses_list[:]
        self.noncurrent_courses = copy_list
        for i in self.reduced_courses_list[:]:
            if i.get_grade() == 0.4:
                #print(f"adding {i.course.get_name()}")
                self.current_courses.append(i)
                
                #self.noncurrent_courses.remove(i)
        
    '''
    def remove_not_finished(self):
        """This function removes from the current list the courses that the student is following in the ongoing semester 
        so the prerequisite check does not double check those prereuisites"""
        for ccourse in self.current_courses[:]:
            term1 = ccourse.get_term()
            for comparison in self.current_courses[:]:
                term2 = comparison.get_term()
                result = compare(term1, term2)
                if result == 1:
                    if comparison in self.current_courses:
                        self.current_courses.remove(comparison)
                        self.noncurrent_courses.append(comparison)
                        #print(f"dropping {comparison.course.get_name()}")
                if result == 2:
                    if ccourse in self.current_courses:
                        self.current_courses.remove(ccourse)
                        self.noncurrent_courses.append(ccourse)
                        #print(f"dropping {ccourse.course.get_name()}")

    
    def leave_chosen_curr(self, semester):
        """This function removes from the current list all the courses that are not  
        done in the semester of interest (aka the one provided by user input)"""
        curr_semester = semester
        for ccourse in self.current_courses[:]:
            term1 = ccourse.get_term()
            result = compare(curr_semester, term1)
            if result == 1: #current after term 1
                if ccourse in self.current_courses:
                    self.current_courses.remove(ccourse)
                    self.noncurrent_courses.append(ccourse)
                    print(f"cause 1: dropping {ccourse.course.get_name()}")
            if result == 2: #term 1 after current
                if ccourse in self.current_courses:
                    self.current_courses.remove(ccourse)
                    print(f"cause 2: dropping {ccourse.course.get_name()}")
    
    def create_curr_ver2(self, semester):
        curr_semester = semester
        copy_list = self.reduced_courses_list[:]
        self.noncurrent_courses = copy_list
        for ccourse in self.reduced_courses_list[:]:
            print(f"analyzing: {ccourse.course.get_name()}")
            term1 = ccourse.get_term()
            if term1 == "TR":
                self.current_courses.append(ccourse)
                self.noncurrent_courses.remove(ccourse)
                print(f"cause TR: dropping {ccourse.course.get_name()}")
            else:
                result = compare(curr_semester, term1)
                if ccourse.get_grade()==0.4 and result==0:
                    self.current_courses.append(ccourse)
                    self.noncurrent_courses.remove(ccourse)
                    print(f"cause 1: dropping {ccourse.course.get_name()}")
        print(self.current_courses)
    '''                
                
    def return_current(self):
        print(self.current_courses)
        return self.current_courses
    
    def print_current(self):
        message  = ""
        for i in self.current_courses:
            message += f"{i.course.get_name()}, "
        #print(f"{message}\n")
        #myReportFile.write(f"{message}\n")
        
    def count_specific_creds(self, current_semester):
        curr_cred = 0
        for other_course in self.current_courses:
            other_semester = other_course.get_term()
            #if 
            result = compare(current_semester, other_semester)
            if result == 1:
                #curr_cred += other_course.course.get_credits()
                curr_cred += other_course.get_credits()
        app = self.credits_earned
        specific_creds = app + curr_cred
        #print(f"got: {self.credits_earned}, while considered:{specific_creds}")
        return specific_creds
            
            
    def attributes_check(self, courses_taken, prerequisite, req_type, counter_alts, m):
        """
        this function gets one course out of all the courses that satisfy the same prerequisite
        and the list of all the courses that should be looked into to find the requirement
        so, the attrribute that should be passed for prerequisites is the list of courses excluding the current ones
        while the one that should be passed for corequisites is the list of all courses including current
        """
        #self.prerequisite_reason = ""
        #myReportFile = open("reasoning.txt", "w")
        found = False
        #self.single_reason = ""
        
        courses_taken = courses_taken #list of courses that the student has taken
        prerequisite = prerequisite #single alternative for the specific prerequisite
        req_type = req_type #either prerequisites or corequisites
        counter_alts = counter_alts #number of courses that satisfy the same requirement
        current_course = m #the course we are checking the requirements of
        
        single_reason = ""
        requirement_pair = []
        course_name = current_course.course.get_code() #letter part of code whose prerequisites we are checking
        course_num = current_course.course.get_number() #number part of code whose prerequisites we are checking
        current_semester = current_course.get_term() #the semester in which the student is taking the class we are checking the prerequisites of

        prereq_code  = prerequisite["code"]
        prereq_grade = prerequisite["grade"]
        
        #goes through all courses done
        for c_taken in courses_taken[:]:
            #specific for each course to mantain the structure
            #appoggio = {"course": [], "reason": []}
            
            taken_code = c_taken.course.get_code() #letter part of code the student has taken
            taken_num = c_taken.course.get_number() #number part of code the student has taken
            taken_grade = c_taken.get_grade()    
            
            prereq_code = prerequisite["code"]
            prereq_grade = prerequisite["grade"]
            
            #if prereq_grade is float:
                #prereq_grade = "D-"
                    
            lower_bound = prerequisite["lower bound"]
            upper_bound = prerequisite["upper bound"]
            
            taken_semester = c_taken.get_term() #the semester in which the student has taken the course that satisfies the requirement
            
            if found == False: #and taken_semester != "TR":
                #se il prerequisito è lo standing
                if prereq_code == "S":
                    creds = self.count_specific_creds(current_semester)
                    if creds>=lower_bound:
                        found = True
                        break
                    else:
                        single_reason = f"Missing ({creds} credits)"
                        found = False
                            #break
                    
                #elif course_name==taken_code or course_num==taken_num:
                    #print(f"{self.get_name()} same course")
                #to exclude the same course
                #elif course_name!=taken_code or course_num!=taken_num: #
                    #se il prerequisito è un qualunque corso o range di corsi
                #elif course_name==taken_code and course_num==taken_num 
                else:
                    if (int(lower_bound)==int(upper_bound) and int(taken_num)==int(lower_bound) and taken_code == prereq_code) or (int(lower_bound)!=int(upper_bound) and (taken_code.startswith(prereq_code) or taken_code.endswith(prereq_code)) and ((int(taken_num)>int(lower_bound) and int(taken_num)<int(upper_bound)) or int(taken_num)==int(lower_bound) or int(taken_num)==int(upper_bound))):
                    #if taken_code == prereq_code and ((int(taken_num)>int(lower_bound) and int(taken_num)<int(upper_bound)) or (int(taken_num)==int(lower_bound) and int(taken_num)==int(upper_bound)) or (int(taken_num)==int(lower_bound) or int(taken_num)==int(upper_bound))):
                         #print("entered 1") 
                         #print(counter_alts)
                         #prerequisiti 
                         if req_type == "prerequisite":
                             #taken_semester = c_taken.get_term() #the semester in which the student has taken the course that satisfies the requirement
                             result = 0
                             if taken_semester != "TR":
                                 result = compare(current_semester, taken_semester) 
                             else:
                                 result = 1
                                 
                             if taken_grade>=letter_to_number.get(prereq_grade) or taken_grade==letter_to_number.get("P"):
                                 found = True
                                 #myReportFile.write(f"\nokay {current_course.course.get_name()}: found {prerequisite} because {c_taken.course.get_name()} with {number_to_letter.get(taken_grade)}")
                                 #break
                             
                             elif taken_grade==letter_to_number.get("current") and result==1: #and result==1:
                                 found = True
                                 #myReportFile.write(f"\nfound: {prerequisite} because {c_taken.course.get_name()} is current")
                                 #break
                             else:
                                 #if taken_grade==letter_to_number.get("current"):
                                 if (course_name=="AS" and course_num==304) or (course_name=="AS" and course_num==306) or (course_name=="AS" and course_num==330) or (course_name=="AS" and course_num==332) or (course_name=="AS" and course_num==342) or (course_name=="AS" and course_num==345) or (course_name=="AS" and course_num==349) or (course_name=="IT" and course_num==349) or (course_name=="IT" and course_num==399):
                                    if single_reason == "":
                                        single_reason = "Missing"
                                    else:
                                        single_reason += ", missing"
                                    #myReportFile.write("\nstrange")
                                 
                                 elif taken_grade==letter_to_number.get("NP") or taken_grade==letter_to_number.get("W"):
                                     #myReportFile.write("\nfailed")
                                     if counter_alts == 1:
                                         if single_reason == "":
                                             single_reason = f"Failed in {taken_semester}"  
                                         else:
                                             single_reason += f", failed in {taken_semester}"

                                     else:
                                         if single_reason == "":
                                             single_reason = f"{taken_code} {taken_num} failed in {taken_semester}"  
                                         else:
                                            single_reason += f", {taken_code} {taken_num} failed in {taken_semester}"
                                        
                                 elif taken_grade==letter_to_number.get("INC"):
                                     #myReportFile.write("\nincomplete")
                                     if counter_alts == 1:
                                         if single_reason == "":
                                             single_reason = f"Incomplete in {taken_semester}"
                                         else: 
                                             single_reason += f", incomplete in {taken_semester}"
                                         #self.prerequisite_reason.append(single_reason)
                                     else:
                                         if single_reason == "":
                                             single_reason = f"{taken_code} {taken_num} incomplete in {taken_semester}"
                                         else:
                                             single_reason += f", {taken_code} {taken_num} incomplete in {taken_semester}"
                                         #self.prerequisite_reason.append(single_reason)
                                
                                 elif taken_grade==letter_to_number.get("F"):
                                     #myReportFile.write("\nfailed")
                                     if counter_alts == 1:
                                         if single_reason == "":
                                             single_reason = f"Failed in {taken_semester}"
                                         else:
                                             single_reason += f", failed in {taken_semester}"
                                         #self.prerequisite_reason.append(single_reason)
                                         #print("append 1")
                                     else:
                                        if single_reason == "":
                                            single_reason = f"{taken_code} {taken_num} failed in {taken_semester}"
                                        else:
                                            single_reason += f", {taken_code} {taken_num} failed in {taken_semester}"                                         
                                         #self.prerequisite_reason.append(single_reason)
                                         #print("append 2")
                                         
                                 elif taken_grade<letter_to_number.get(prereq_grade):
                                    #myReportFile.write("\ngrade requirement is insufficient")
                                    #print("Grade requirement entered")
                                    if counter_alts == 1:
                                        grade = number_to_letter.get(taken_grade)
                                        if taken_grade == 0.4:
                                            if single_reason == "":
                                                single_reason = f"Grade req ({grade} in {taken_semester})"
                                            else:
                                                single_reason += f", grade req ({grade} in {taken_semester})"
                                        else:
                                            if single_reason == "":
                                                single_reason = f"Grade req ({grade} in {taken_semester})"
                                            else:
                                                single_reason += f", grade req ({grade} in {taken_semester})"
                                        #self.prerequisite_reason.append(single_reason)
                                    else:
                                        grade = number_to_letter.get(taken_grade)
                                        if taken_grade == 0.4:
                                            if single_reason == "":
                                                single_reason = f"Grade req ({grade} in {taken_code} {taken_num} in {taken_semester})"
                                            else:
                                                single_reason += f", grade req ({grade} in {taken_code} {taken_num} in {taken_semester})"
                                        else:
                                            if single_reason == "":
                                                single_reason = f"Grade req ({grade} in {taken_code} {taken_num})"
                                            else:
                                                single_reason += f", grade req ({grade} in {taken_code} {taken_num})"
                                        #self.prerequisite_reason.append(single_reason)
                                     
                                 else:
                                    #myReportFile.write("\nmissing")
                                    if counter_alts == 1:
                                        if single_reason == "":
                                            single_reason = f"Missing in {taken_semester}" 
                                        else:
                                            single_reason += f", missing in {taken_semester}"
                                       #self.prerequisite_reason.append(single_reason)
                                       #print("append 1")
                                    else:
                                        if single_reason == "":
                                            single_reason = f"{taken_code} {taken_num} missing in {taken_semester}"
                                        else:
                                            single_reason += f", {taken_code} {taken_num} missing in {taken_semester}"
                                       #self.prerequisite_reason.append(single_reason)
                                       #print("append 2")   

                             #if found == False:
                                 #myReportFile.write(f"\nNOT FOUND {prerequisite}")
                        
                         #corequisiti dovrebbero avere anche current ammissibile come voto
                         elif req_type == "corequisite":
                            taken_semester = c_taken.get_term() #the semester in which the student has taken the course that satisfies the requirement
                            if taken_semester != "TR":
                                 result = compare(current_semester, taken_semester) 
                            else:
                                 result = 1 
                            if taken_grade>=letter_to_number.get(prereq_grade) or taken_grade==letter_to_number.get("P"):
                                found = True
                                #myReportFile.write(f"\nfound corequisite: {prerequisite} because {c_taken.course.get_name()} with {number_to_letter.get(taken_grade)}")
                            
                            elif taken_grade == letter_to_number.get("current") and (result==1 or result==0):
                                found = True
                                #myReportFile.write(f"\nfound corequisite: {prerequisite} because {c_taken.course.get_name()} is current")
                            
                            else:
                                 if counter_alts == 1:
                                    grade = number_to_letter.get(taken_grade)
                                    single_reason = f"Grade req ({grade})"
                                    #myReportFile.write("\ncorequisite grade insufficient")
                                 else:
                                    grade = number_to_letter.get(taken_grade)
                                    single_reason = f"Grade req ({grade} in {taken_code} {taken_num})"            
                                    #myReportFile.write("\ncorequisite grade insufficient")

                            #if found == False:
                                 #myReportFile.write(f"\ncorequisite NOT FOUND {prerequisite}")

        requirement_pair.append(found)
        requirement_pair.append(single_reason)    
            
        return requirement_pair
                    
    
    def check_requirements(self):
        """
        this function extrapolates the alternatives for each prerequisites, calls the function that checks them
        against the courses that the student has taken, and once received the pair reason and found
        creates the list of missing prerequisites with the necessary reasons       
        """
        #myReportFile.write(f"\n\n{self.get_name()}\n")
        
        #for loop sui current course:
        info_list = [] #will contain the current courses that do not satisfy the requirements in addition to the missing requirements
        self.print_current()

        for m in self.current_courses[:]: 
            info = []
            missing_req = {"prerequisite" : [], "corequisite" : []} #will contain the missing requirement, will be different for each of the courses
            
            #di ogni corso prende prerequisites e corequisites e li mette in req_list:
            current_requirements = m.course.get_requirements_dictionary() # current_prerequisites1 = {"prerequisite" : [[{}, {}]], "corequisite": [[{}], [{}]]}
            req_list = ["prerequisite", "corequisite"]

            reasons = []
            if m.return_honor() == 1:
                if self.gpa < 3.50:
                    req_reason = f"Missing GPA ({self.gpa})"
                    reasons.append(req_reason)
                    
                    requirement = [{"code": "Honors", "lower bound": 0, "upper bound": 0, "grade": ""}]
                    missing_req["prerequisite"].append([requirement, reasons]) #REQUIREMENT = UN PREREQUISITO
                    
            #for loop su req_list:
            for i in req_list[:]: #first checks prereq then coreq
                requirements = current_requirements[i] #either prerequisites or corequisites [[{}, {}], [{}], [{}]]
                found = False
                self.iteration = len(requirements)
                
                round_curr = 0
                #print(f"\n{m.course.get_name()} there are {len(requirements)} requirements")
                for requirement in requirements[:]: #[{}, {}, {}] # a single requirement, which is a list of the possible alternatives that satisfy it

                    found = False    

                    reasons = []
                    counter_alts = len(requirement)
                    self.prerequisite_reason.clear()
                    #prerequisite_reason = []
                    
                    for alternative in requirement[:]: #one of the list of courses that satisfy the same requirement
                        req_reason = ""  
                        if found != True:
                            
                            if i == "prerequisite":
                                requirement_pair = self.attributes_check(self.reduced_courses_list, alternative, i, counter_alts, m)
                            elif i == "corequisite":
                                requirement_pair = self.attributes_check(self.reduced_courses_list, alternative, i, counter_alts, m)

                            found = requirement_pair[0]
                            req_reason = requirement_pair[1]

                            if req_reason == "":
                                  req_reason = "Missing"  
                            reasons.append(req_reason) 

                    round_curr += 1
                    if found != True: #il requirement non è stato soddisfatto 
                        missing_req[i].append([requirement, reasons])
                        #myReportFile.write(f"{m.course.get_name()} not found\n")

                    #elif found == True:
                        #myReportFile.write(f"{m.course.get_name()} found\n")
 
                    found = False
            
            #se al corso non mancano requirements da soddisfare lo ignora 
            #if len(missing_req["prerequisite"]) == 0 and len(missing_req["corequisite"]) == 0:
                #print("no missing prerequisites or corequisites")
                
            if len(missing_req["prerequisite"])!=0 or len(missing_req["corequisite"])!=0:
                info.append(m)
                info.append(missing_req)
                info_list.append(info)

        return info_list
            
            
    def create_prereq_message(self):
        return "nope"
      
        
    #def check_minor1(self):
    
    #def check_minor2
    #"English Composition and Literature", "Math Proficiency", "Math, Science, Computer Science", "Foreign Language", "Social Sciences", "Humanities", "Fine Arts", "Additional Requirements", "Core Courses", "Major Electives", "Major 1", "Major 2"    
    

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Uses the data retrived from the json file to create the list of students
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""   
def create_student_list(students_list):
    #with open('students_file.json', 'r') as myfile:
    #with open('students_list.json', 'r') as myfile:
       #students_list = json.load(myfile)
    students_list = students_list  
    student_obj = []
   
    for i in range(0, len(students_list)): 
        curr_student = students_list[i]
         #print(curr_student)
        student = Student(curr_student[0], curr_student[1], curr_student[2], curr_student[3], curr_student[4], curr_student[5])
        courses_t = curr_student[6]
        for course in courses_t:
            #print(course)
            student.add_course(course)
        #print(student.courses_done)
        student_obj.append(student)
        
    return student_obj

'''
def close_file():
    #myReportFile.close()
    Report2.close()
    '''
