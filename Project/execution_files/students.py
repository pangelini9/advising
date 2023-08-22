# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 16:15:21 2022

@author: ilda1
"""
#KEYWORDS
#get_credits compute_transfer_credits, create_remaining_list, print, create_remaining_list_special


#from majors import Major
from execution_files.courses import Course, Course_taken
from execution_files.Utilities import compare, check_code, letter_to_number, number_to_letter

#NB: major = Major(...)
#    def __init__(self, name, surname, highschool_credits, major, minor1, minor2, courses_done):

#myReportFile = open("reasoning.txt", "w")
#Report2 = open("removeretake.txt", "w")
#removeretake
 
import json
import math
import numpy as np
import pandas as pd

class Student:
     
    def __init__(self, name, surname, language_waived, major, minor1, minor2, double_degree, gpaFile):
        self.name = name
        self.surname = surname
        self.language_waived = language_waived #=1 if yes
        
        
        #attributes for the type of degrees the student is taking
        self.major = major
        self.minor1 = minor1
        self.minor2 = minor2
        self.degrees = double_degree #=1 if double major, =0 if only one major, =2 if double degree
        
        #attributes for the courses that the student has done
        self.courses_done = []
        self.reduced_courses_list = [] #created with the actual list gets reduced as requirements are checked
        self.general_distr_list = []
        self.course_lift_minor = []
        
        #attributesfor credits and standings
        self.credits_to_grad = 120 #120 if single degree/ double major; 150 i fdouble degree
        if self.degrees == 1:
            self.credits_to_grad = 150

        self.credits_earned = 0
        self.credits_in_residence = 0
        self.credits_nxsem = 0
        self.credits_residence_nxsem = 0
        self.credits_missing = self.credits_to_grad # to account for double major
        self.credits_missing_tentative = self.credits_to_grad
        self.credits_missing_actual = self.credits_to_grad
        self.gpa = 0
        self.gpaFile = gpaFile
        self.curr_standing = ""
        self.nx_standing = ""
        
        
        #attributes for the degree planner
        self.m_en = {"courses remaining" : [["EN", 103],["EN", 105],["EN", 110]], "courses prov" : [], "output courses":[]}
        self.m_ma = {"courses missing" : 1, "courses done" : [], "courses remaining" : []}
        self.m_sci = {"courses missing" : 2, "courses done" : [], "courses remaining" : []}
        self.m_flang = {"courses missing" : 2, "courses done" : [], "courses remaining" : []}
        self.m_sosc = {"courses missing" : 2, "courses done" : [], "courses remaining" : []}
        self.m_hum = {"courses missing" : 2, "courses done" : [], "courses remaining" : []}
        self.m_fa = {"courses missing" : 1, "courses done" : [], "courses remaining" : []}
        self.m_additional = {"courses missing" : 0, "courses done" : [], "courses remaining" : []}
        self.m_core = {"courses missing" : 0, "courses done" : [], "courses remaining" : []}
        self.m_majorelectives = {"courses missing" : 0, "courses done" : [], "num_remaining" : 0, "next_num" : 1}
        self.m_minor1_list = {"courses missing" : 0, "courses done" : [], "num_remaining" : 0, "next_num" : 1}
        self.m_minor2_list = {"courses missing" : 0, "courses done" : [], "num_remaining" : 0, "next_num" : 1}
        self.concentrations = {"courses missing" : 0, "courses done" : []}
        self.m_genelectives = []
        
        #this counter accounts for the number of courses in the core section that the student has passed with grade below C- 
        self.counter_core_grades = 0 
        
        #attributes for the prerequisites check
        self.current_courses = []
        self.noncurrent_courses = []
        self.req_satisfied = []
        self.req_not_satisfied = []
        self.iteration = 0
        self.single_reason = ""
        self.prerequisite_reason = []
        
        
        #attributes for the check retake
        self.retaken_classes =  []
        self.text = ""
    
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

    def return_creds_in_residence(self):
        return self.credits_in_residence
    
    def return_courses_information(self):
        message = f"\nthe student has taken {len(self.courses_done)} in total, not retaken {len(self.reduced_courses_list)}, and is taking {len(self.current_courses)} currently."
        return message
    
    def return_retakes(self):
        return self.retaken_classes
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Action Functions
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        
    def change_reduced(self, new_reduced):
        self.reduced_courses_list = new_reduced
    
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
            if letter_to_number.get("D-") <= grade <= letter_to_number.get("A") or grade == letter_to_number.get("F"):
                course_credit = i.get_credits()
                creds += course_credit
                weighted_total += course_credit*grade
        if creds != 0:
            self.gpa = round(weighted_total / creds, 2) # rounding to 2 decimal digits
        else:
            self.gpa = 0
        
        if self.gpaFile == "":
            self.gpaFile = 0
        
        if float(self.gpa) == float(self.gpaFile):
            # print("SAME GPA")
            None
        else:
            # print(f"Different GPA: {self.gpa} and {self.gpaFile}")
            report_name = "information_not_found.txt"
            with open(report_name, "a") as myReportFile:
                myReportFile.write(f"Different GPA for {self.name}: {self.gpa} computed and {self.gpaFile} in xml\n")

        # making sure that the gpa printed in the planner is the one from the xml
        self.gpa = self.gpaFile
    
    def compute_credits_earned(self):
        self.credits_earned = 0
        self.credits_in_residence = 0
        for i in self.reduced_courses_list:
            grade = i.get_grade()
            if pd.isnull(grade) != True:
                if i.get_grade()<letter_to_number.get("AU") or i.get_grade()>letter_to_number.get("current"):
                #if i.get_grade()>= letter_to_number.get("D-") and i.get_grade()==letter_to_number.get("TR"):
                #if grade != "": # PA: this should also be updated to use the dictionary values
                    course_credits = i.get_credits()
                    self.credits_earned += course_credits
                    if i.return_in_residence() == 1:
                        self.credits_in_residence += course_credits
            
    def compute_credits_nxsem(self):
        self.credits_nxsem = 0
        self.credits_residence_nxsem = 0
        for i in self.reduced_courses_list:
            if i.get_grade()<letter_to_number.get("AU") or i.get_grade() == letter_to_number.get("INC") or i.get_grade()>=letter_to_number.get("current"):
 
                # TODO if i.used_flag<14 - What was this? Check
                course_credits = i.get_credits()
                self.credits_nxsem += course_credits
                if i.return_in_residence() == 1:
                    self.credits_residence_nxsem += course_credits

    
    def compute_credits_missing(self):
        #self.credits_missing = 120 - self.credits_nxsem 
        
        self.credits_missing_tentative = self.credits_to_grad - self.credits_nxsem 
        if self.credits_missing_tentative < 0 :
            self.credits_missing_tentative = 0
            
        self.credits_missing_actual = self.credits_to_grad - self.credits_earned 
        if self.credits_missing_actual < 0 :
            self.credits_missing_actual = 0
    
    
    def compute_cur_standing(self):
        if self.credits_earned >= 90:
            self.curr_standing = "Senior"
        elif self.credits_earned >= 60:
            self.curr_standing = "Junior"
        elif self.credits_earned >= 30:
            self.curr_standing = "Sophomore"
        else:
            self.curr_standing = "Freshman"

    def compute_nx_standing(self):
        if self.credits_nxsem >= 90:
            self.nx_standing = "Senior"
        elif self.credits_nxsem >= 60:
            self.nx_standing = "Junior"
        elif self.credits_nxsem >= 30:
            self.nx_standing = "Sophomore"
        else:
            self.nx_standing = "Freshman"
    
            
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Action Functions
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""    
    
    """
    def compute_creds_in_residence(self):
        for tcourse in self.reduced_courses_list:
            if tcourse.in_residence == 1: #the couse has been done at JCU
           """     
                
    
    def major_info_list(self):
        #self.degrees = double_degree #=1 if double major, =0 if only one major, =2 if double degree
        double_degree = "No"
        double_major = "No"
        

        #if self.degrees == 0 the student is doing only one degree
        
        if self.degrees == 1:
            self.credits_to_grad = 150
            double_degree = "Yes"
            
        elif self.degrees == 2:
            double_major = "Yes"

        
        major_list = {
            1 : ["Double Degree" , double_degree],
            2 : ["Double Major", double_major],
            3 : ["Credits Required to Graduate", self.credits_to_grad],
            }
        
        #self.degrees = double_degree #=1 if double major, =0 if only one major, =2 if double degree

        return major_list
    
    def create_info_list(self):
        """"
        Returns a list of informations to be printed in the additional information        
        part of the degree planner
        """
        #["GPA", "Credits(earned)", "Current Standing", "Credits following semester", "Standing following semester", "Credits missing"]
        #info_list = [self.gpa, self.credits_earned, self.curr_standing, self.credits_nxsem, self.nx_standing, self.credits_missing]
        #["Cumulative GPA", "Credits (earned)", "Current Standing", "Tentative Credits following semester", "Tentative Standing following semester", "Credits missing"]
        '''OLD VERSION
        info_list = {
            "Cumulative GPA" : self.gpa,
            "Credits (earned)" : self.credits_earned,
            "Standing (earned)" : self.curr_standing,
            "Credits missing (earned)"  : self.credits_missing_actual,
            
            
            "Credits (tentative)" : self.credits_nxsem,
            "Standing (tentative)" : self.nx_standing, 
            "Credits missing (tentative)" : self.credits_missing_tentative,
            }'''
        
        
        info_list = {
            
            "A": ["Cumulative GPA",  self.gpa],
            "B" : ["Credits earned", self.credits_earned], #Credits (earned)
            "C" : ["Credits earned in residence", self.credits_in_residence],
            "D" : ["Standing", self.curr_standing] , #Standing based on credits earned
            "E" : ["Credits missing", self.credits_missing_actual] , #Credits missing only cosidering the courses that are not current or incomplete
            
            
            "F" : ["Credits", self.credits_nxsem] , #Credits (tentative)
            "G" : ["Credits in residence", self.credits_residence_nxsem], # Credits in residence (tentative)
            "H" : ["Standing", self.nx_standing] , #Standing (tentative)
            "I" : ["Credits missing", self.credits_missing_tentative]  #Credits missing based on the courses has taken considering current
            }
        
        return info_list
    
    #NEEDED TO CREATE THE COUNTER'S PART OF THE PLANNER
    def return_missing(self):
        #["Math Proficiency", "Math, Science, Computer Science", "Foreign Language", "Social Sciences", "Humanities", "Fine Arts", "Additional Requirements", "Core Courses", "Major Electives", "Minor 1", "Minor 2"]
        #missing_numcourses = [self.m_ma["courses missing"], self.m_sci["courses missing"], self.m_flang["courses missing"], self.m_sosc["courses missing"], self.m_hum["courses missing"], self.m_fa["courses missing"], self.m_additional["courses missing"], self.m_core["courses missing"], self.m_majorelectives["courses missing"], "NA", "NA"]
        minor1 = self.minor1
        if minor1 == "":
            minor1 = "None"
        minor2 = self.minor2
        if minor2 == "":
            minor2 = "None"
        
        missing_numcourses = {
            "Math Proficiency" : self.m_ma["courses missing"],
            "Math, Science, Computer Science" : self.m_sci["courses missing"],
            "Foreign Language" : self.m_flang["courses missing"],
            "Social Sciences" : self.m_sosc["courses missing"],
            "Humanities" : self.m_hum["courses missing"],
            "Fine Arts" : self.m_fa["courses missing"],
            "Additional Requirements" : self.m_additional["courses missing"],
            "Core Courses" : self.m_core["courses missing"],
            "Concentration" : "NA",
            "Major Electives" : self.m_majorelectives["courses missing"],
            "Minor 1" : minor1,
            "Minor 2" : minor2            
            }
        
        return missing_numcourses
    
    #adds to the lit of courses the list for each course done by the student
    def add_course(self, course):
        self.courses_done.append(course)
    

    def change_major(self, majorobj):
        """changes the major key (passed by the json file of the student into the major object"""
        self.major = majorobj
        

    def change_courses(self, courses_taken_obj):
        """change list of courses into the list of objects of the class Courses_taken"""
        self.courses_done = courses_taken_obj
        
   #IS IT REALLY NECESSARY? 
    def remove_withdraw(self):
        list_name = [self.reduced_courses_list, self.general_distr_list, self.course_lift_minor]
        for curr_list in list_name:
            for course in curr_list:
                if course.get_grade()==letter_to_number.get("W") or course.get_grade()==letter_to_number.get("AU"):
                    curr_list.remove(course)
    
    
    def change_withdraw_creds(self):
        "Changes the credits of the courses taken that the student has withdrawn from to 0 so that it prints it on the planner"
        for course_taken in self.reduced_courses_list:
            if course_taken.get_grade() == letter_to_number.get("W"):
                course_taken.creds = 0
    
    ''' 
    def check_for_unofficial_retake(self):
        in_residence = 0
        
        special_courses = [0, 281, 299, 381, 399, 499]
        self.text = ""
        for i in range(len(self.courses_done)-1, -1, -1):
            current_course = self.courses_done[i] #first time around
            to_insert = True #è da inserire in reduced
            
            for h in self.reduced_courses_list[:]: #second time around
                in_residence = h.return_in_residence()
                
                #we can ignore AU and null because remove_retake is called before 
                
                #finds the same course in the list                
                elif current_course.course.get_number() == h.course.get_number() and current_course.course.get_code() == h.course.get_code() and (current_course.course.get_number()!=388 and current_course.course.get_code()!="RAS") and (current_course.course.get_number()!=383 and current_course.course.get_code()!="AH") and (current_course.course.get_number()!=373 and current_course.course.get_code()!="AH") and (current_course.course.get_number()!=372 and current_course.course.get_code()!="AH") and (current_course.course.get_number()!=367 and current_course.course.get_code()!="AH") and (current_course.course.get_number()!=283 and current_course.course.get_code()!="AH") and (current_course.course.get_number()!=272 and current_course.course.get_code()!="AH") and (current_course.course.get_number()!=267 and current_course.course.get_code()!="AH") and (current_course.course.get_number()!=315 and current_course.course.get_code()!="EN") and (current_course.course.get_number()!=315 and current_course.course.get_code()!="EN/HS") and (current_course.course.get_number()!=346 and current_course.course.get_code()!="EN") and (current_course.course.get_number()!=306 and current_course.course.get_code()!="EN") and ((current_course.course.get_number() not in special_courses) or (current_course.course.get_number()==299 and current_course.course.get_code()=="MA")):

       '''         
        
    
    def remove_retake(self):
        """
        Removes from the list of courses that the student has done (that the program uses
        for the check) the courses that the student has taken more than once
        Removes the first instance of the class whenever the second grade is not AU, W, INC, or current
        """
        in_residence = 0
        #found_retake = False
        #non deve togliere i duplicates dei corsi fatti non in residence
        special_courses = [0, 281, 299, 381, 399, 499]
        self.text = ""
        # read the list of courses starting from the most recent
        for i in range(len(self.courses_done)-1, -1, -1):
            current_course = self.courses_done[i]
            
            # variable to control whether this course has to be inserted in the reduced list or not
            to_insert = True
            
            # If the grade in the transcript already has an R, the course does not have to be inserted
            if pd.isnull(current_course.get_grade()) == True:
                to_insert = False
            
            # otherwise, I compare the course against the courses that have been already inserted
            else:
                for h in self.reduced_courses_list[:]:
                    
                    # If the same course is already in the list: h is more recent than current!                
                    if current_course.course.get_number() == h.course.get_number() and current_course.course.get_code() == h.course.get_code():
                        
                        # if it is one of the courses that can be repeated, it should be inserted
                        if current_course.course.get_code()=="RAS" or (current_course.course.get_number()==383 and current_course.course.get_code()=="AH") or (current_course.course.get_number()==373 and current_course.course.get_code()=="AH") or (current_course.course.get_number()==372 and current_course.course.get_code()=="AH") or (current_course.course.get_number()==367 and current_course.course.get_code()=="AH") or (current_course.course.get_number()==283 and current_course.course.get_code()=="AH") or (current_course.course.get_number()==272 and current_course.course.get_code()=="AH") or (current_course.course.get_number()==267 and current_course.course.get_code()=="AH") or (current_course.course.get_number()==315 and current_course.course.get_code()=="EN") or (current_course.course.get_number()==315 and current_course.course.get_code()=="EN/HS") or (current_course.course.get_number()==346 and current_course.course.get_code()=="EN") or (current_course.course.get_number()==306 and current_course.course.get_code()=="EN") or (current_course.course.get_number() in special_courses and not (current_course.course.get_number()==299 and current_course.course.get_code()=="MA")):
                            to_insert = True # not needed, just to fill the gap
                        
                        # else, if the new course does not have a grade yet, the old is inserted, but should be ignored for requirements
                        elif h.get_grade()==letter_to_number.get("INC") or h.get_grade()==letter_to_number.get("current"):
                            #print(f"not dropped because second time {h.get_grade()}")
                            current_course.used_flag = 15 # TODO: update the rest of the code to use this (IF NEEDED!)
                            to_insert = True # not needed, just for completeness
                            
                            # Also, if the old course had a valid grade, it should be reported as a retake
                            if current_course.get_grade()!=letter_to_number.get("W") and current_course.get_grade()!=letter_to_number.get("P") and current_course.get_grade()!=letter_to_number.get("NP")  and current_course.get_grade()!=letter_to_number.get("AU"):
                                """
                                Out of all the courses that a student has repeated, only the ones in which the student has
                                not taken W, P, NP, AU must be reported
                                This is a check on the grade of the course taken the first time, not the second
                                """
                                retaken_pair = {"old_course" : current_course,
                                                "new_course" : h
                                                }
                                self.retaken_classes.append(retaken_pair)
                                #self.retaken_classes.append(current_course)
                                self.text += f"{current_course.course.get_name()} done in {current_course.get_term()} ({number_to_letter.get(current_course.get_grade())}, {current_course.get_credits()} creds) and again in {h.get_term()} ({number_to_letter.get(h.get_grade())}, {h.get_credits()} creds)"
                            
                        # else, if the new course is a Withdraw or Audit, the old is inserted, while the new is not inserted
                        elif h.get_grade()==letter_to_number.get("W") or h.get_grade()==letter_to_number.get("AU"):
                            #print(f"not dropped because second time {h.get_grade()}")
                            self.reduced_courses_list.remove(h)
                            to_insert = True # not needed, just for completeness
    
                        # else, if the new course has NOT been taken at JCU, the old is inserted, but should be ignored for requirements
                        elif h.return_in_residence() == 0:
                            #print(f"not dropped because second time not in residence")
                            current_course.used_flag = 15 # TODO: update the rest of the code to use this (IF NEEDED!)
                            to_insert = True # not needed, just for completeness
    
                        else: # the new course has an actual grade and has been taken at JCU, so we do not need to insert
    
                            to_insert = False

            if to_insert:
                self.reduced_courses_list.insert(0, current_course)
                self.general_distr_list.insert(0, current_course)
                self.course_lift_minor.insert(0, current_course)

        #print(f"{self.get_name()} is retaking {len(self.retaken_classes)}\n {self.retaken_classes}\n\n")     
        #self.print_retake()
                

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Functions that are neede to mantain the planner structure
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
    #next two functions are specific for english compositiona and literature
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
            en_taken_prov = Course_taken(curr_course, self, "", "", "", "", 2)
            self.m_en["output courses"].append([en_taken_prov,1])
    
    
    def set_the_grid(self, missing_number, next_num, attribute_name):
        """
        Creates fake courses so that the planner will contain the number of the missing 
        course instead of an empty cell
        
        Example:                                Instead of
            Two English Literature Courses   -->   Two English Literature Courses
            First Course                     -->
            Second Course                    -->
        """
        corresponding_number = {
            1 : "First",
            2 : "Second",
            3 : "Third",
            4 : "Fourth",
            5 : "Fifth", 
            6 : "Sixth",
            7 : "Seventh",
            8 : "Eighth",
            9 : "Ninth",
            10 : "Tenth"
            }
        
        for i in range(0, missing_number):
            
            course_name = f"{corresponding_number.get(next_num)} course"
            fake_course = Course(course_name, "", "", "", [], "", "", "", -1)
            course_taken =  Course_taken(fake_course, self, "", "", "", "", 2)
            
            if attribute_name == self.m_en:
                attribute_name["output courses"].append([course_taken, 10])
            else:
                attribute_name["courses done"].append([course_taken, 10])
                
            next_num += 1
    
    def return_or_courses(self, i, attribute_name, courses_list):
        """
        This function is needed to report in the planner the courses that are in or
        with respect with the course that has been found by the program
        namely that the student has done        
        
        before this function one has to remove the course found from the list of alternatives
        AND add the course found to the ["courses done"] list of the dictionary
        then this function will create elements that have the 
        """
        #i sarebbe la lista di possibili corsi in alternativa a quello che è stato trovato 
        #and from which the course found was removed
            #i[0] = counter
            #i[1] = lista di corsi --> [['MA', 208, 208, ''], ['MA', 209, 209, '']]
                #i[1][0] = codice corso, or "", or exception 
                #i[1][1] = lower bound or ""
                #i[1][2] = upper bound or ""
                #i[1][3] = description
                
        report_name = "information_not_found.txt"
        myReportFile = open(report_name, "a")
        
        if len(i[1])!=0:
            for element in i[1]:
                found = False
                for z in courses_list: #z is an object course
                
                    if element[1] > element[2]  or element[1] < element[2]:
                        #print("found range")
                        message = element[3]
                        if message == "":
                            message  = "exception"
                        new_Course = Course(message, "", "", "", [], -3, "", "", "")
                        new_tcourse = Course_taken(new_Course, self, "", "", "", "", 2)
                        appoggio = [new_tcourse, "", message]
                        attribute_name["courses done"].append(appoggio)
                        found = True
                        break
                    
                    else:
                        if element[0]==z.get_code() and element[1]==z.get_number():
                            #print(f"Found {z.get_name()} {z.get_code()} {z.get_number()}")
                            old_name = z.get_name()
                            new_name = "OR " + old_name #str(old_name)
                            new_Course = Course(new_name, z.get_code(), z.get_number(), z.get_credits(), z.get_requirements_dictionary(), -3, "", "", "")
                            new_tcourse = Course_taken(new_Course, self, "", "", "", "", 2)
                            message = element[3]
                            if message == "":
                                message = new_Course.get_name()
                            appoggio = [new_tcourse, "", message]
                            attribute_name["courses done"].append(appoggio)
                            found = True
       
                if found == False:
                    myReportFile.write(f"\nCourse not existing: {element[0]} {element[1]} range({element[1]} to {element[2]}) in major {self.major.name} ")
        
        #for i in options_list:
            
    def exception_raiser(self, i, curr_student, reduced_courses_list):
        #print(i)
        #political science, communications, international affairs, 
        majors_implemented = [2, 5, 6, 12, 27, 22, 23, 7, 15]
        if self.major.get_major_key() in majors_implemented: 
            if i[1][0][1]==1:
                self.major.exception_one(i, curr_student, reduced_courses_list)
                
                #curr_student.change_reduced(new_reduced)
                
            elif i[1][0][1]==2:
                self.major.exception_two(i, curr_student, reduced_courses_list)
                #curr_student.change_reduced(new_reduced)
    
            elif i[1][0][1]==3:
                self.major.exception_three(i, curr_student, reduced_courses_list)
                #curr_student.change_reduced(new_reduced)
    
            elif i[1][0][1]==4:
                self.major.exception_four(i, curr_student, reduced_courses_list) 
                #curr_student.change_reduced(new_reduced)
                
            elif i[1][0][1]==5:
                self.major.exception_five(i, curr_student, reduced_courses_list) 
            
            elif i[1][0][1]==6:
                self.major.exception_six(i, curr_student, reduced_courses_list) 
            
            elif i[1][0][1]==7:
                self.major.exception_seven(i, curr_student, reduced_courses_list) 
                
            elif i[1][0][1]==8:
                self.major.exception_eight(i, curr_student, reduced_courses_list) 
       
            else:
                print("this exeption was not implemented")
       #else:
            
           # print("not implemented")
    #def report_or(self, i): 
        #for course in i:
            #if 
        
        
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Degree Planner Checks Functions
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""    
    def check_additional(self, courses_list):
        additional_courses = self.major.get_additional_requirements()
        message = ""
        for i in additional_courses[:]:
            counter = i[0] 
            self.m_additional["courses missing"] += i[0]
            
            #LIST LEVELS
            #i[0] = counter
            #i[1] = lista di corsi --> [['MA', 208, 208, ''], ['MA', 209, 209, '']]
                #i[1][0] = codice corso, or "", or exception 
                #i[1][1] = lower bound or ""
                #i[1][2] = upper bound or ""
                #i[1][3] = description
            
            
            if i[1][0][0] == "exception":
                self.exception_raiser(i, self, self.reduced_courses_list)
                additional_courses.remove(i)
                #print("not implemented")
                
            #se c'è una description allora il blocco deve apparire tutto insieme    
            elif i[1][0][0] == "":
                message = i[1][0][3]

                #se il counter == 1 allora i[2] è la description del corso
                if i[0] == 1:
                    found = False
                    for index in range(1, len(i[1])):
                        m = i[1][index]
                        if found == False:
                            for j in self.reduced_courses_list:
                                
                                #print(f"Additional (''), current code:{j.course.get_code()} vs prereq code:{i[1][0][0]} or m={i[1][index]}")

                                if found == False and j.used_flag < 2:
                                    if counter!=0 and j.course.get_number() >= m[1] and j.course.get_number() <= m[2] and check_code(j.course.get_code(), [m[0]]):
                                        
                                        if j.get_grade() == letter_to_number.get("current") or j.get_grade() == letter_to_number.get("INC"):
                                            self.m_additional["courses done"].append([j,2,message])
                                            j.used_flag = 2
                                            additional_courses.remove(i)
                                            counter -= 1
                                            self.m_additional["courses missing"] -= 1
                                            found = True
                
                                        elif j.get_grade() >= letter_to_number.get("D-"):
                                            self.m_additional["courses done"].append([j,1,message])
                                            j.used_flag = 2
                                            additional_courses.remove(i)
                                            counter -= 1
                                            self.m_additional["courses missing"] -= 1
                                            found = True
                
                                        else:
                                            self.m_additional["courses done"].append([j,0,message])
                                            j.used_flag = 2
                                            additional_courses.remove(i)
                                            counter -= 1
                                            self.m_additional["courses missing"] -= 1
                                            found = True

                    if found == False:
                        # TODO: shouldn't this be i, rather than ""?
                        self.m_additional["courses done"].append(["",10,message])
                        additional_courses.remove(i)

                    
                #se il counter > 1 allora il messaggio è da scrivere nella riga superiore
                elif i[0]>1:
                    message = i[0][3]
                    self.m_additional["courses done"].append(["","",message])
                    message = ""
                    course_num = 1
                    #additional_courses.remove(i)
                    found = False
                    for index in range(1, len(i[1])):    
                        m = i[1][index]
                        for j in self.reduced_courses_list:
                            
                            #print(f"Additional (''2): current code:{j.course.get_code()} vs prereq code:{i[1][0][0]}")
                            if j.used_flag < 2:
                                if counter!=0 and j.course.get_number() >= m[1] and j.course.get_number() <= m[2] and check_code(j.course.get_code(), [m[0]]):
                                    
                                    if j.get_grade() == letter_to_number.get("current") or j.get_grade() == letter_to_number.get("INC"):
                                        message = m[3]
                                        if message == "":
                                            message = f"{course_num} course"
                                        course_num += 1
                                        self.m_additional["courses done"].append([j,2,message])
                                        j.used_flag = 2
                                        i[1].remove(m)
                                        counter -= 1
                                        self.m_additional["courses missing"] -= 1
                                        found = True
            
                                    elif j.get_grade() >= letter_to_number.get("D-"):
                                        message = m[3]
                                        if message == "":
                                            message = f"{course_num} course"
                                        course_num += 1
                                        self.m_additional["courses done"].append([j,1,message])
                                        j.used_flag = 2
                                        i[1].remove(m)
                                        counter -= 1
                                        self.m_additional["courses missing"] -= 1
                                        found = True
            
                                    else:
                                        message = m[3]
                                        if message == "":
                                            message = f"{course_num} course"
                                        course_num += 1
                                        self.m_additional["courses done"].append([j,0,message])
                                        j.used_flag = 2
                                        i[1].remove(m)
                                        counter -= 1
                                        self.m_additional["courses missing"] -= 1
                                        found = True
                                            
                    if counter != 0:
                        for index in range(0, counter):
                            message = f"{course_num} course"
                            self.m_additional["courses done"].append(["",10,message]) 
                            course_num += 1                                                               
                    additional_courses.remove(i)                
                    
                    
                
            #se il prerequisito è normale
            else:
                #print("additional in else")
                #print(i)
                for j in self.reduced_courses_list:
                    message = i[1][0][3]
                    
                    for m in i[1][:]:
                        if j.used_flag < 2:
                            if counter!=0 and j.course.get_number() >= m[1] and j.course.get_number() <= m[2] and check_code(j.course.get_code(), [m[0]]):
                                #print(f"add recognized -- : current code:{j.course.get_code()} vs prereq code:{i[1][0][0]}")
                                
                                if j.get_grade() == letter_to_number.get("current") or j.get_grade() == letter_to_number.get("INC"):
                                    message = m[3]
                                    if message == "":
                                        message = j.course.get_name()
                                    self.m_additional["courses done"].append([j,2,message])
                                    j.used_flag = 2
                                    additional_courses.remove(i)
                                    counter -= 1
                                    self.m_additional["courses missing"] -= 1
                                
                                elif j.get_grade() >= letter_to_number.get("D-"):
                                    message = m[3]
                                    if message == "":
                                        message = j.course.get_name()
                                    self.m_additional["courses done"].append([j,1,message])
                                    j.used_flag = 2
                                    additional_courses.remove(i)
                                    counter -= 1
                                    self.m_additional["courses missing"] -= 1
                                
                                else:
                                    message = m[3]
                                    if message == "":
                                        message = j.course.get_name()
                                    self.m_additional["courses done"].append([j,0,message])
                                    j.used_flag = 2
                                    additional_courses.remove(i)
                                    counter -= 1
                                    self.m_additional["courses missing"] -= 1
                                
        self.m_additional["courses remaining"] = additional_courses
        return self.m_additional 

    
    def check_core(self, courses_list):

        core_courses = self.major.get_core_courses()
        self.counter_core_grades = 0

        for i in core_courses[:]: #[1, [['MA', 209, 209, '']]]

            counter = i[0] #1
            self.m_core["courses missing"] += i[0]

            #i[0] = counter
            #i[1] = lista di corsi --> [['MA', 208, 208, ''], ['MA', 209, 209, '']]
                #i[1][0] = codice corso, or "", or exception 
                #i[1][1] = lower bound or ""
                #i[1][2] = upper bound or ""
                #i[1][3] = description

            if i[1][0][0] == "exception": #[['MA', 209, 209, '']]
                self.exception_raiser(i, self, self.reduced_courses_list)
                core_courses.remove(i)
            #se c'è una description allora il blocco deve apparire tutto insieme    
            elif i[1][0][0] == "": #se non c'è il codice corso allora quella lista ha una description
                message = i[1][0][3]
            
                #se il counter == 1 allora i[2] è la description del corso
                if i[0] == 1:
                    found = False
                    for index in range(1, len(i[1])):
                        m = i[1][index] # each course that satisfies this requirement
                        if found == False:
                            for j in self.reduced_courses_list:
                                #print(f"Core (''1), current code:{j.course.get_code()} vs prereq code:{i[1][0][0]} or m={i[1][index]}")
                                if found == False and j.used_flag < 2:
                                    if counter > 0 and j.course.get_number() >= m[1] and j.course.get_number() <= m[2] and check_code(j.course.get_code(), [m[0]]):
                                        
                                        if j.get_grade() == letter_to_number.get("current") or j.get_grade() == letter_to_number.get("INC"):
                                            self.m_core["courses done"].append([j,2,message])
                                            j.used_flag = 2
                                            core_courses.remove(i)
                                            counter -= 1
                                            self.m_core["courses missing"] -= 1
                                            found = True
                
                                        elif j.get_grade() >= letter_to_number.get("C-"):
                                            self.m_core["courses done"].append([j,1,message])
                                            j.used_flag = 2
                                            core_courses.remove(i)
                                            counter -= 1
                                            self.m_core["courses missing"] -= 1
                                            found = True
                                            
                                        elif j.get_grade() >= letter_to_number.get("D-"):
                                            self.m_core["courses done"].append([j,3,message])
                                            j.used_flag = 2
                                            core_courses.remove(i)
                                            counter -= 1
                                            self.m_core["courses missing"] -= 1
                                            found = True
                                            
                                        else:
                                            self.m_core["courses done"].append([j,0,message])
                                            j.used_flag = 2
                                            core_courses.remove(i)
                                            counter -= 1
                                            self.m_core["courses missing"] -= 1
                                            found = True
    
                    if found == False:
                        fake_course = Course(message, "", "", "", [], "", "", "", -1)
                        fcourse_taken =  Course_taken(fake_course, self, "", "", "", "", 2)
                        self.m_core["courses done"].append([fcourse_taken,10,message])
                        # core_courses.remove(i)
            
                #se invce il counter è maggiore di uno la descrizione precede un tot di righe
                elif i[0]>1:
                   #counter = 3
                   message = i[1][0][3]
                   self.m_core["courses done"].append(["","",message])
                   message = ""
                   course_num = 1
                   requ_copy = i[1][:]

                   for index in range(1, len(requ_copy)): 
                       
                       m = requ_copy[index]

                       for j in self.reduced_courses_list:

                           if j.used_flag < 2:
                               if counter!=0 and j.course.get_number() >= m[1] and j.course.get_number() <= m[2] and check_code(j.course.get_code(), [m[0]]):
                                   
                                   if j.get_grade() == letter_to_number.get("current") or j.get_grade() == letter_to_number.get("INC"):
                                       message = m[3]
                                       if message == "":
                                           message = f"{course_num} course"
                                       course_num += 1
                                       self.m_core["courses done"].append([j,2,message])
                                       j.used_flag = 2
                                       counter -= 1
                                       self.m_core["courses missing"] -= 1
                                       i[1].remove(m)
           
                                   elif j.get_grade() >= letter_to_number.get("C-"):
                                       message = m[3]
                                       if message == "":
                                           message = f"{course_num} course"
                                       course_num += 1
                                       self.m_core["courses done"].append([j,1,message])
                                       j.used_flag = 2
                                       #i[1].remove(m)
                                       counter -= 1
                                       self.m_core["courses missing"] -= 1
                                       i[1].remove(m)
                                       
                                   elif j.get_grade() >= letter_to_number.get("D-"):
                                       message = m[3]
                                       if message == "":
                                            message = f"{course_num} course"
                                       course_num += 1
                                       self.m_core["courses done"].append([j,3,message])
                                       j.used_flag = 2
                                       counter -= 1     
                                       self.m_core["courses missing"] -= 1
                                       i[1].remove(m)
           
                                   else:
                                       message = m[3]
                                       if message == "":
                                           message = f"{course_num} course"
                                       course_num += 1
                                       self.m_core["courses done"].append([j,0,message])
                                       j.used_flag = 2
                                       counter -= 1
                                       self.m_core["courses missing"] -= 1
                                       i[1].remove(m)
                                           
                   if counter != 0:
                       for index in range(0, counter):
                           message = f"{course_num} course"
                           self.m_core["courses done"].append(["",10,message]) 
                           course_num += 1                                                               
                   core_courses.remove(i) 
                   #break
                
                
                #altrimenti il requirement è un corso normale
            else:
                found = False
                #print("core in else")
                for j in self.reduced_courses_list:

                    if len(i[1])!=0:
                        message = i[1][0][3]
    
                        for m in i[1][:]:

                            if found == True:
                                break
                            
                            if j.used_flag < 2 and counter!=0 and j.course.get_number() >= m[1] and j.course.get_number() <= m[2] and check_code(j.course.get_code(), [m[0]]):
                                if not (m[0]=="IT" and len(j.course.get_code())>2 and j.course.get_code()[2]=="S") and not (m[0]=="AS" and len(j.course.get_code())>2 and j.course.get_code()[-3]=="R"):
                                    
                                        if j.get_grade() == letter_to_number.get("current") or j.get_grade() == letter_to_number.get("INC"):
                                            #print("found as current")
                                            message = m[3]
                                            if message == "":
                                                message = j.course.get_name()
                                            self.m_core["courses done"].append([j,2,message])
                                            j.used_flag = 2
                                            
                                            i[1].remove(m)
                                            self.return_or_courses(i, self.m_core, courses_list)
                                            core_courses.remove(i)
                                            
                                            counter -= 1
                                            self.m_core["courses missing"] -= 1
                                            found = True
                                            break
                                        
                                        elif j.get_grade() >= letter_to_number.get("C-"):
                                            #print("found as sufficient")
                                            message = m[3]
                                            if message == "":
                                                message = j.course.get_name()
                                            self.m_core["courses done"].append([j,1,message])
                                            j.used_flag = 2
                                            
                                            i[1].remove(m)
                                            self.return_or_courses(i, self.m_core, courses_list)
                                            core_courses.remove(i)
                                            
                                            counter -= 1
                                            self.m_core["courses missing"] -= 1
                                            found = True
                                            break
                                        
                                        elif j.get_grade() < letter_to_number.get("C-") and j.get_grade() > letter_to_number.get("W"):
                                            #print("found as risky")
                                            message = m[3]
                                            if message == "":
                                                message = j.course.get_name()
                                            self.counter_core_grades += 1
                                            self.m_core["courses done"].append([j,3,message])
                                            j.used_flag = 2
                                            
                                            i[1].remove(m)
                                            self.return_or_courses(i, self.m_core, courses_list)
                                            core_courses.remove(i)
                                            
                                            counter -= 1
                                            self.m_core["courses missing"] -= 1
                                            found = True
                                            break
                                        
                                        else:         
                                            #print("found as failed")
                                            message = m[3]
                                            if message == "":
                                                message = j.course.get_name()
                                            self.m_core["courses done"].append([j,0,message])
                                            j.used_flag = 2
                                            
                                            i[1].remove(m)
                                            self.return_or_courses(i, self.m_core, courses_list)
                                            core_courses.remove(i)
                                            
                                            counter -= 1
                                            self.m_core["courses missing"] -= 1
                                            found = True
                                            break
                                
        self.m_core["courses remaining"] = core_courses
        return self.m_core    
    
    
    #MAJOR ELECTIVES
    def check_major_electives(self):
        """
        STRUCTURE:
            "major electives": [[3, [["EC", 300, 1000], ["FIN", 300, 1000]]], [3, [["EC", 200, 1000], ["FIN", 200, 1000], ["BUS", 200, 1000], ["LAW", 200, 1000], ["MA", 200, 1000], ["MGT", 200, 1000], ["MKT", 200, 1000], ["PL", 200, 1000], ["PS", 200, 1000]]]]
            [cap courses, [list of possible electives indicated with code and interval of valid numbers]]
        """
        melective_list = self.major.get_major_electives()
        #curr_student.m_majorelectives["next_num"] = 1
        
        #if self.major.get_name != "Business Administration" : 
        for i in melective_list:
            counter = i[0] 
            self.m_majorelectives["courses missing"] += i[0]
            #print(i)
            
            if i[1][0][0] == "exception":
                #print("foud exception in electives")
                self.exception_raiser(i, self, self.reduced_courses_list)
                #print("not implemented")
            else: 
                for j in self.reduced_courses_list:
                    for m in i[1]:
                        if j.used_flag < 2:
                            if counter!=0 and j.course.get_number() >= m[1] and j.course.get_number() <= m[2] and check_code(j.course.get_code(), [m[0]]):
                                if j.get_grade() == letter_to_number.get("current") or j.get_grade() == letter_to_number.get("INC"):
                                    self.m_majorelectives["courses done"].append([j,2])
                                    j.used_flag = 2
                                    counter -= 1
                                    self.m_majorelectives["courses missing"] -= 1
                                    self.m_majorelectives["num_remaining"] -= 1
                                    self.m_majorelectives["next_num"] += 1
                                    break
                                    
                                elif j.get_grade() >= letter_to_number.get("D-"):
                                    self.m_majorelectives["courses done"].append([j,1])
                                    j.used_flag = 2
                                    counter -= 1
                                    self.m_majorelectives["courses missing"] -= 1
                                    self.m_majorelectives["num_remaining"] -= 1
                                    self.m_majorelectives["next_num"] += 1
                                    break
                                
                                """Failed courses cannot be accepted as major electives
                                else:
                                    self.m_majorelectives["courses done"].append([j,0])
                                    self.reduced_courses_list.remove(j)
                                    counter -= 1
                                    self.m_majorelectives["courses missing"] -= 1
                                    """
               
        if self.major.get_major_key()==12 or self.major.get_major_key()==27: #BA Communications has a different banner
            missing_number = self.m_majorelectives["num_remaining"]
        else:
            missing_number = self.m_majorelectives["courses missing"]
            
        if self.m_majorelectives["courses missing"] != 0:
            self.set_the_grid(missing_number, self.m_majorelectives["next_num"], self.m_majorelectives)                     
              
        return self.m_majorelectives

        
    # First Minor
    def check_minor1(self):
        """
        STRUCTURE:
            "major electives": [[3, [["EC", 300, 1000], ["FIN", 300, 1000]]], [3, [["EC", 200, 1000], ["FIN", 200, 1000], ["BUS", 200, 1000], ["LAW", 200, 1000], ["MA", 200, 1000], ["MGT", 200, 1000], ["MKT", 200, 1000], ["PL", 200, 1000], ["PS", 200, 1000]]]]
            [cap courses, [list of possible electives indicated with code and interval of valid numbers]]
        """
        #melective_list = self.major.get_major_electives()
        #curr_student.m_majorelectives["next_num"] = 1
        
        self.m_minor1_list["courses missing"] = 6
        
        # Here, we should get the list of courses required for the specific minor, check which have been done, and decrease "missing"
        missing_number = self.m_minor1_list["courses missing"]

        if self.m_minor1_list["courses missing"] != 0:
            self.set_the_grid(missing_number, self.m_minor1_list["next_num"], self.m_minor1_list)                     
              
        return self.m_minor1_list

    # Second Minor
    def check_minor2(self):
        """
        STRUCTURE:
            "major electives": [[3, [["EC", 300, 1000], ["FIN", 300, 1000]]], [3, [["EC", 200, 1000], ["FIN", 200, 1000], ["BUS", 200, 1000], ["LAW", 200, 1000], ["MA", 200, 1000], ["MGT", 200, 1000], ["MKT", 200, 1000], ["PL", 200, 1000], ["PS", 200, 1000]]]]
            [cap courses, [list of possible electives indicated with code and interval of valid numbers]]
        """
        #melective_list = self.major.get_major_electives()
        #curr_student.m_majorelectives["next_num"] = 1
        
        self.m_minor2_list["courses missing"] = 6
        
        # Here, we should get the list of courses required for the specific minor, check which have been done, and decrease "missing"
        missing_number = self.m_minor2_list["courses missing"]

        if self.m_minor2_list["courses missing"] != 0:
            self.set_the_grid(missing_number, self.m_minor2_list["next_num"], self.m_minor2_list)                     
              
        return self.m_minor2_list
    
    #GENERAL ELECTIVES
    def check_genelectives(self):
        for i in self.reduced_courses_list:
            if i.used_flag < 1 or i.used_flag > 14:
                if i.get_grade() == letter_to_number.get("current") or i.get_grade() == letter_to_number.get("INC"):
                    i.used_flag = 1
                    self.m_genelectives.append([i,2])
                elif i.get_grade() >= letter_to_number.get("D-"):
                    i.used_flag = 1
                    self.m_genelectives.append([i,1])
                else:
                    i.used_flag = 1
                    self.m_genelectives.append([i,0])

        return self.m_genelectives

    
    #ENGLISH COMPOSITION (Proficiency and General Distribution Requirements)    
    def check_eng_composition(self):
        """
        when passing the course to the list
        0 = Failed (below D-)
        1 = Grade requirement satifsfied (above C)
        2 = Grade requirement not satifsfied (between D- and C-)
        3 = current
        self.m_en = {"courses remaining": [["EN", 103],["EN", 105],["EN", 110]],"courses prov" : [],  "output courses":[]}
        """
        #one has to loop over the actual list not the copy    
        for i in self.reduced_courses_list:
            #might be needed if one checks other planner parts before
            #if i.used_flag < 1:
            if check_code(i.course.get_code(), ["EN"]):
                if i.course.get_number() == 103:
                    if i.get_grade() >= letter_to_number.get("C"):
                        self.m_en["output courses"][0] = [i,1]
                    elif i.get_grade() >= letter_to_number.get("D-"):
                        self.m_en["output courses"][0] = [i,3]
                    elif i.get_grade() == letter_to_number.get("current") or i.get_grade() == letter_to_number.get("INC"):
                        self.m_en["output courses"][0] = [i,2]
                    else:
                        self.m_en["output courses"][0] = [i,0]
                    i.used_flag = 1
                    #self.reduced_courses_list.remove(i) #to be removed
                    
                elif i.course.get_number() == 105 :
                    if i.get_grade() >= letter_to_number.get("C"):
                        self.m_en["output courses"][1] = [i,1] 
                    elif i.get_grade() == letter_to_number.get("current") or i.get_grade() == letter_to_number.get("INC"):
                        self.m_en["output courses"][1] = [i,2]
                    else:
                        self.m_en["output courses"][1] = [i,0]
                    i.used_flag = 1
                    #self.reduced_courses_list.remove(i)
                    
                elif i.course.get_number() == 110:
                    if i.get_grade() >= letter_to_number.get("C"):
                        self.m_en["output courses"][2] = [i,1] 
                    elif i.get_grade() == letter_to_number.get("current") or i.get_grade() == letter_to_number.get("INC"):
                        self.m_en["output courses"][2] = [i,2]
                    else:
                        self.m_en["output courses"][2] = [i,0]
                    i.used_flag = 1
                    #self.reduced_courses_list.remove(i)
                    

    #ENGLISH LITERATURE (Proficiency and General Distribution Requirements)                    
    def check_eng_literature(self):
        """
        when passing the course to the list
        0 = Failed (below D-)
        1 = Grade requirement satifsfied (above C)
        3 = Grade requirement not satifsfied (between D- and C-)
        2 = current
        """
            
        lit_counter = 0 #since "first course" is printed if next number is 1, etc, we need to pass this +1
        missing_num = 2
        
        approved_substitute = False #for the approved substitute for en
        #for i in self.general_distr_list[:]:
        for i in self.reduced_courses_list:
            
            #might be needed if one checks other planner parts before
            #if i.used_flag < 1:
                
            if check_code(i.course.get_code(), ["EN"]):
                if i.course.get_number() >= 200 and lit_counter<2:
                    if i.get_grade() >= letter_to_number.get("D-"):
                        self.m_en["output courses"].append([i,1])
                    elif i.get_grade() == letter_to_number.get("current") or i.get_grade() == letter_to_number.get("INC"):
                        self.m_en["output courses"].append([i,2])
                    #else:
                        #self.m_en["output courses"].append([i,0])
                    i.used_flag = 1
                    #self.general_distr_list.remove(i)
                    
                    lit_counter += 1
                    missing_num -= 1
                    
            # TODO: Put approved subs in a list
                
            elif  i.course.get_code()== "CL" and approved_substitute==False and lit_counter<2:
                if i.course.get_number()== 268 or i.course.get_number()== 278:
                    if i.get_grade() >= letter_to_number.get("D-"):
                        self.m_en["output courses"].append([i,1])
                    elif i.get_grade() == letter_to_number.get("current"):
                        self.m_en["output courses"].append([i,2])
                    #else:
                        #self.m_en["output courses"].append([i,0])
                    #self.general_distr_list.remove(i)
                    i.used_flag = 1
                    
                    approved_substitute = True
                    lit_counter += 1
                    missing_num -= 1
                    
            elif i.course.get_code()== "ITS" and i.course.get_number()==292 and approved_substitute==False and lit_counter<2:
                if i.get_grade() >= letter_to_number.get("D-"):
                    self.m_en["output courses"].append([i,1])
                elif i.get_grade() == letter_to_number.get("current"):
                    self.m_en["output courses"].append([i,2])
                #else:
                    #self.m_en["output courses"].append([i,0])
                #self.general_distr_list.remove(i)
                i.used_flag = 1
                approved_substitute = True
                lit_counter += 1
                missing_num -= 1
        
        if missing_num != 0:
            self.set_the_grid(missing_num, lit_counter+1, self.m_en)  

        return self.m_en    


    #MATHEMATICS REQUIREMENT (Proficiency and General Distribution Requirements)
    def check_ma_req(self):
        math_req = self.major.get_math_requirement()
        next_num = 1
        
        if self.major.get_major_key() == 27:
            course_name = "MA100 or MA101"
            fake_course = Course(course_name, "----", "----", "----", [], "", "", "", -1)
            course_taken =  Course_taken(fake_course, self, "", "", "waived", "", 2)
            self.m_ma["courses done"].append([course_taken, 1])
            
        else:
            
            course_key = [54]            
            if math_req != 1:
                course_key.insert(0, 53)

            for i in self.reduced_courses_list:
                #might be needed if one checks other planner parts before
                #if i.used_flag < 1:
                if i.course.get_course_key() in course_key:
                    #print("recognized")
                    if i.get_grade() == letter_to_number.get("current") or i.get_grade() == letter_to_number.get("INC"):
                        self.m_ma["courses missing"] -= 1
                        self.m_ma["courses done"].append([i, 2]) 
                        i.used_flag = 1
                        #self.general_distr_list.remove(i) 
                    elif i.get_grade() >= letter_to_number.get("C-"):
                        self.m_ma["courses missing"] -= 1
                        self.m_ma["courses done"].append([i, 1]) 
                        i.used_flag = 1
                        #self.general_distr_list.remove(i)
                    else:
                        # TODO: we could check if there is the other course 100/101
                        self.m_ma["courses done"].append([i, 0]) 
                        i.used_flag = 1
                        #self.general_distr_list.remove(i) 
                    break
    
        missing_number = self.m_ma["courses missing"]
        
        if len(self.m_ma["courses done"]) == 0:
            course_name = "First course"
            fake_course = Course(course_name, "", "", "", [], "", "", "", -1)
            course_taken =  Course_taken(fake_course, self, "", "", "", "", 2)

            self.m_ma["courses done"].append([course_taken, 10])
            # TODO: uncomment!
            # self.set_the_grid(missing_number, next_num, self.m_ma)
        
        return self.m_ma

    
    #MATHEMATICS, SCIENCE, COMPUTER SCIENCE ((Proficiency and General Distribution Requirements))
    def check_sci(self):
        """
        course structure
        #Course(namecourse, code, number, credits_num, req_list, course_key)
        #Course_taken(course, student, course_section, grade, term, c_type)
        
        when passing the course to the list
        0 = Failed (below D-)
        1 = Grade requirement satifsfied (above C)
        2 = current
        """
        counter = len(self.reduced_courses_list)
        next_num = 1
        
        while counter>0 and self.m_sci["courses missing"]>0:
            course_codes = ["MA", "NS", "SCI", "CS"]
            for i in self.reduced_courses_list:
                #if self.m_sci["courses missing"] == 0:
                    #break
                #else:
                # TODO: use the list course_codes directly in the check_code function, without loop
                for j in course_codes:
                    if self.m_sci["courses missing"] <= 0:
                        break
                    
                    # TODO: Is this correct? It should be fine to use one from the Core and alike (but not MA 100/101)
                    if i.used_flag < 1:
                        if check_code(i.course.get_code(), [j]):
                            c_creds = i.get_credits()
                        
                            if i.get_grade() == letter_to_number.get("current"):
                                self.m_sci["courses done"].append([i,2])
                                i.used_flag = 1
                                #self.general_distr_list.remove(i)
                                if c_creds==3 or c_creds==4 or c_creds==5:                               #check on credits
                                    self.m_sci["courses missing"] -= 1
                                    next_num += 1
                                elif c_creds == 6:
                                    if self.m_sci["courses missing"] == 1:
                                        self.m_sci["courses missing"] -= 1
                                    else:
                                        self.m_sci["courses missing"] -= 2
                                    next_num += 2
                                    
                                break
                            
                            elif i.get_grade() >= letter_to_number.get("D-"): #check on grades
                                self.m_sci["courses done"].append([i,1]) 
                                i.used_flag = 1
                                #self.general_distr_list.remove(i)
                                if c_creds==3 or c_creds==4 or c_creds==5:                               #check on credits
                                    self.m_sci["courses missing"] -= 1
                                    next_num += 1
                                elif c_creds == 6:
                                    if self.m_sci["courses missing"] == 1:
                                        self.m_sci["courses missing"] -= 1
                                    else:
                                        self.m_sci["courses missing"] -= 2
                                    next_num += 2
                                    
                                break
                            
                            #else:
                             #   self.m_sci["courses done"].append([i,0]) 
                              #  self.general_distr_list.remove(i)    
                                                        
                                
                counter -= 1 
        
        missing_number = self.m_sci["courses missing"]
        if  missing_number > 0:
            self.set_the_grid(missing_number, next_num, self.m_sci)
                
        return self.m_sci


    #SOCIAL SCIENCES ((Proficiency and General Distribution Requirements))
    def check_sosc(self):
        """
        course structure
        #Course(namecourse, code, number, credits_num, req_list, course_key)
        #Course_taken(course, student, course_section, grade, term, c_type)
        
        when passing the course to the list
        0 = Failed (below D-)
        1 = Grade requirement satifsfied (above C)
        2 = current
        """
        counter = len(self.reduced_courses_list)
        next_num = 1
        
        while counter>0 and self.m_sosc["courses missing"]!=0:
            course_codes = ["COM", "CMS", "DMA", "DJRN", "EC", "GEOG", "PL", "PS", "SOSC"]
            for i in self.reduced_courses_list:
                if self.m_sosc["courses missing"] == 0:
                    break
                else:
                    for j in course_codes:
                        if i.used_flag < 1:
                            
                            if check_code(i.course.get_code(), [j]):
                                c_creds = i.get_credits()
                                
                                if i.get_grade() == letter_to_number.get("current"):
                                    self.m_sosc["courses done"].append([i,2])
                                    i.used_flag = 1
                                    #self.general_distr_list.remove(i)
                                    if c_creds==3 or c_creds==4 or c_creds==5:                               #check on credits
                                        self.m_sosc["courses missing"] -= 1
                                        next_num += 1
                                    elif c_creds == 6:
                                        if self.m_sosc["courses missing"] == 1:
                                            self.m_sosc["courses missing"] -= 1
                                        else:
                                            self.m_sosc["courses missing"] -= 2
                                        next_num += 2                                    
                                        
                                    break
                                
                                elif i.get_grade() >= letter_to_number.get("D-"): #check on grades
                                    self.m_sosc["courses done"].append([i,1]) 
                                    i.used_flag = 1
                                    #self.general_distr_list.remove(i)
                                    if c_creds==3 or c_creds==4 or c_creds==5:                               #check on credits
                                        self.m_sosc["courses missing"] -= 1
                                        next_num += 1
                                    elif c_creds == 6:
                                        if self.m_sosc["courses missing"] == 1:
                                            self.m_sosc["courses missing"] -= 1
                                        else:
                                            self.m_sosc["courses missing"] -= 2
                                        next_num += 2 
                                    break
                                #else:
                                 #   self.m_sosc["courses done"].append([i,0]) 
                                  #  self.general_distr_list.remove(i)     

                counter -= 1 
                
        missing_number = self.m_sosc["courses missing"]
        if  missing_number!= 0:
            self.set_the_grid(missing_number, next_num, self.m_sosc)
        
        return self.m_sosc
        
  
    #HUMANITIES ((Proficiency and General Distribution Requirements))
    def check_hum(self):
        """
        course structure
        #Course(namecourse, code, number, credits_num, req_list, course_key)
        #Course_taken(course, student, course_section, grade, term, c_type)
        
        when passing the course to the list
        0 = Failed (below D-)
        1 = Grade requirement satifsfied (above C)
        2 = current
        """
        counter = len(self.reduced_courses_list)
        next_num = 1
        
        while counter>0 and self.m_hum["courses missing"]!=0:
            course_codes = ["CL", "GRK", "HM", "HS", "ITS", "LAT", "PH", "RL"]
            for i in self.reduced_courses_list:
                if self.m_hum["courses missing"] == 0:
                    break
                else:
                    for j in course_codes:
                        if check_code(i.course.get_code(), [j]) or (check_code(i.course.get_code(), ["EN"]) and i.course.get_number()>=200 and i.used_flag != 1):
                            c_creds = i.get_credits()
                            
                            if i.get_grade() == letter_to_number.get("current"):
                                self.m_hum["courses done"].append([i,2]) 
                                i.used_flag = 1
                                #self.general_distr_list.remove(i)
                                if c_creds==3 or c_creds==4 or c_creds==5:                               #check on credits
                                    self.m_hum["courses missing"] -= 1
                                    next_num += 1
                                elif c_creds == 6:
                                    if self.m_hum["courses missing"] == 1:
                                        self.m_hum["courses missing"] -= 1
                                    else:
                                        self.m_hum["courses missing"] -= 2
                                    next_num += 2 
                                break
                                
                            elif i.get_grade() >= letter_to_number.get("D-"): #check on grades
                                self.m_hum["courses done"].append([i,1]) 
                                i.used_flag = 1
                                #self.general_distr_list.remove(i)
                                if c_creds==3 or c_creds==4 or c_creds==5:                               #check on credits
                                    self.m_hum["courses missing"] -= 1
                                    next_num += 1
                                elif c_creds == 6:
                                    if self.m_hum["courses missing"] == 1:
                                        self.m_hum["courses missing"] -= 1
                                    else:
                                        self.m_hum["courses missing"] -= 2
                                    next_num += 2 
                                break
                           # else:
                                #self.m_hum["courses done"].append([i,0]) 
                                #self.general_distr_list.remove(i)    
                                #break   
                counter -= 1    
                
        missing_number = self.m_hum["courses missing"]
        if  missing_number!= 0:
            self.set_the_grid(missing_number, next_num, self.m_hum)
            
        return self.m_hum
        
    
    #FINE ARTS ((Proficiency and General Distribution Requirements))
    def check_arts(self):
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
        next_num = 1
        
        while counter>0 and self.m_fa["courses missing"]!=0:
            course_codes = ["FA","AH", "ARCH", "AS", "CW", "DR", "MUS"]
            for i in self.reduced_courses_list:
                if self.m_fa["courses missing"] == 0:
                    break
                else:
                    if i.used_flag < 1:
                        for j in course_codes:
                            if check_code(i.course.get_code(), [j]):
                                
                                if i.get_grade() == letter_to_number.get("current"):
                                    self.m_fa["courses done"].append([i,2]) 
                                    i.used_flag = 1
                                    #self.general_distr_list.remove(i)
                                    self.m_fa["courses missing"] -= 1
                                    next_num -= 1
                                    
                                elif i.get_grade() >= letter_to_number.get("D-"): #check on grades
                                    #print("added course")
                                    self.m_fa["courses done"].append([i,1]) 
                                    i.used_flag = 1
                                    #self.general_distr_list.remove(i)
                                    self.m_fa["courses missing"] -= 1
                                    next_num -= 1
                                    
                                #else:
                                 #   self.m_fa["courses done"].append([i,0]) 
                                  #  self.general_distr_list.remove(i)      
                                
                                break                                
                                
                counter -= 1
                
        missing_number = self.m_fa["courses missing"]
        if  missing_number!= 0:
            self.set_the_grid(missing_number, next_num, self.m_fa)
                            
        return self.m_fa
        
    
    #FOREIGN LANGUAGE ((Proficiency and General Distribution Requirements))            
    def check_flanguage(self): 
        """
        course structure
        #Course(namecourse, code, number, credits_num, req_list, course_key)
        #Course_taken(course, student, course_section, grade, term, c_type)
        
        when passing the course to the list
        0 = Failed (below D-)
        1 = Grade requirement satifsfied (above C)
        3 = Grade requirement not satifsfied (between D- and C-)
        2 = current or INC
        """
        counter = len(self.reduced_courses_list)
        next_num = 1
        
        #6=BA Political Science (as of Fall 2022) // 22=BA International Affairs (prior to Fall 2022) // 23=BA International Affairs (as of Fall 2022)
        if self.major.get_major_key()==6 or self.major.get_major_key()==22 or self.major.get_major_key()==23:
            #print(f"recognized {self.major.get_name()}, four languages placed")
            self.m_flang["courses missing"] = 4
        
        while counter>0 and self.m_flang["courses missing"]!=0:
            if self.language_waived==1:
                #should this only do a merge and print waived?
                number_list = ["First Required Course", "Second Required Course", "Third Required Course", "Fourth Required Course"]
                language_cap = self.m_flang["courses missing"]
                for i in range(0,language_cap):
                    course = Course(number_list[i], "----", "----", "----", [], "", "", "", "")
                    cc = Course_taken(course, self, 0, "P", "waived", 0, 0)
                    self.m_flang["courses missing"] -= 1
                    self.m_flang["courses done"].append([cc,1])

            else:
                # TODO: Also GER?
                course_codes = ["FR", "IT", "SPAN"]
                for i in self.reduced_courses_list:
                #for i in self.general_distr_list[:]:
                    if self.m_flang["courses missing"] == 0:
                        break
                    for j in course_codes:
                        #if j == i.course.get_code():
                        if i.used_flag < 1:
                            if check_code(i.course.get_code(), [j]):
                                c_creds = i.get_credits()
                                
                                if i.get_grade() == letter_to_number.get("current"): #check on grades
                                    self.m_flang["courses done"].append([i,2]) 
                                    i.used_flag = 1
                                    #self.general_distr_list.remove(i)
                                    if c_creds==3 or c_creds==4 or c_creds==5:                               #check on credits
                                        self.m_flang["courses missing"] -= 1
                                        next_num += 1
                                    elif c_creds == 6:
                                        if self.m_flang["courses missing"] == 1:
                                            self.m_flang["courses missing"] -= 1
                                        else:
                                            self.m_flang["courses missing"] -= 2
                                        next_num += 2 
                                    break    
                                
                                elif i.get_grade() >= letter_to_number.get("D-"): #check on grades
                                    self.m_flang["courses done"].append([i,1]) 
                                    i.used_flag = 1
                                    #self.general_distr_list.remove(i)
                                    if c_creds==3 or c_creds==4 or c_creds==5:                               #check on credits
                                        self.m_flang["courses missing"] -= 1
                                        next_num += 1
                                    elif c_creds == 6:
                                        if self.m_flang["courses missing"] == 1:
                                            self.m_flang["courses missing"] -= 1
                                        else:
                                            self.m_flang["courses missing"] -= 2
                                        next_num += 2
                                    break
                                        
                                #else:
                                 #   self.m_flang["courses done"].append([i,0]) 
                                  #  self.general_distr_list.remove(i)                                
                    counter -=1
                    
        missing_number = self.m_flang["courses missing"]
        if  missing_number!= 0:
            self.set_the_grid(missing_number, next_num, self.m_flang)
                                                        
        return self.m_flang
    
    

    
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
            
            if i.get_grade() == letter_to_number["current"]:
                #print(f"adding {i.course.get_name()}")
                self.current_courses.append(i)
                
                #self.noncurrent_courses.remove(i)
                      
                
    def return_current(self):
        #print(self.current_courses)
        return self.current_courses
    
    def print_current(self):
        message  = ""
        for i in self.current_courses:
            message += f"{i.course.get_name()}, "
        #print(f"{message}\n")
        #myReportFile.write(f"{message}\n")
        
    def count_specific_creds_v1(self, current_semester, course_name, course_num):
        """
        Only considers if the current course is done in the semester before the course that we are checking the prerequisite of
        However if the current is a course that the student is taking again it gives the student the double amount of credits
        """
        #other course is one of the courses taken
        curr_cred = 0
                
        for other_course in self.current_courses:            
            other_semester = other_course.get_term()
            
            result = compare(current_semester, other_semester)
            
            if result == 1: 
                curr_cred += other_course.get_credits()
                
        app = self.credits_earned
        specific_creds = app + curr_cred
        #print(f"got: {self.credits_earned}, while considered:{specific_creds}")
        return specific_creds
            
    def count_specific_creds(self, current_semester, course_name, course_num):
        """
        This function establishes the potential standing of the person, if the student has not received some grades
        of courses taken the semester before the semester in which is taking the class we are checking the prerequisite
        then those credits are taken in consideration. Yet once the grades are received, theyu will either be added to
        the total amount of credit done, or they will be taken out.
        This version considers if the student is retaking a class and only adds the credits once
        """
        curr_name = course_name #the letter part of the code of the current course
        curr_num = course_num #the number part of the code of the current course
        curr_cred = 0
        
        for other_course in self.reduced_courses_list:
            taken_code = other_course.course.get_code() #letter part of code the student has taken
            taken_num = other_course.course.get_number() #number part of code the student has taken
            other_semester = other_course.get_term()
            taken_grade = other_course.get_grade()
            result = 0
            if other_semester=="TR":
                result == 1
            else: 
                result = compare(current_semester, other_semester)
            
            if taken_grade==letter_to_number.get("current") and result == 1 and not (curr_name==taken_code and curr_num==taken_num):
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
            
            if c_taken.used_flag == 15: # this course has been superseded by another course (current or not in residence)
                print(f"Not using: {c_taken.course.get_code()} {c_taken.course.get_number()} from {c_taken.get_term()}")
                
            else:
            
                #specific for each course to mantain the structure
                #appoggio = {"course": [], "reason": []}
                
                taken_code = c_taken.course.get_code() #letter part of code the student has taken
                taken_num = c_taken.course.get_number() #number part of code the student has taken
                taken_grade = c_taken.get_grade()    
                
                prereq_code = prerequisite["code"]
                prereq_grade = prerequisite["grade"]
                            
                if prereq_grade is None or prereq_grade == "":
                    prereq_grade = "D-"
                        
                lower_bound = prerequisite["lower bound"]
                upper_bound = prerequisite["upper bound"]
                
                taken_semester = c_taken.get_term() #the semester in which the student has taken the course that satisfies the requirement
                
                if found == False: #and taken_semester != "TR":
                    #se il prerequisito è lo standing
                    if prereq_code == "S":
                        creds = self.count_specific_creds(current_semester, course_name, course_num)
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
                        if (int(lower_bound)==int(upper_bound) and int(taken_num)==int(lower_bound) and taken_code == prereq_code) or (int(lower_bound)!=int(upper_bound) and check_code(taken_code, [prereq_code]) and ((int(taken_num)>int(lower_bound) and int(taken_num)<int(upper_bound)) or int(taken_num)==int(lower_bound) or int(taken_num)==int(upper_bound))):
     
                             if req_type == "prerequisite":
                                 #taken_semester = c_taken.get_term() #the semester in which the student has taken the course that satisfies the requirement
                                 result = 0
                                 if taken_semester != "TR":
                                     result = compare(current_semester, taken_semester) 
                                 else:
                                     result = 1
                                     
                                 #se il grade requirement è satisfied    
                                 if taken_grade>=letter_to_number.get(prereq_grade) or taken_grade==letter_to_number.get("P"):
                                     found = True
                                     #myReportFile.write(f"\nokay {current_course.course.get_name()}: found {prerequisite} because {c_taken.course.get_name()} with {number_to_letter.get(taken_grade)}")
                                     #break
                                 
                                #se il corso è senza voto ma preso un semestre prima
                                 elif taken_grade==letter_to_number.get("current") and result==1: #and result==1:
                                     found = True
                                     #myReportFile.write(f"\nfound: {prerequisite} because {c_taken.course.get_name()} is current")
                                     #break
                                 else:
                                     #se il corso ha un prerequisito strano
                                     if (course_name=="AS" and course_num==304) or (course_name=="AS" and course_num==306) or (course_name=="AS" and course_num==330) or (course_name=="AS" and course_num==332) or (course_name=="AS" and course_num==342) or (course_name=="AS" and course_num==345) or (course_name=="AS" and course_num==349) or (course_name=="IT" and course_num==349) or (course_name=="IT" and course_num==399):
                                        if single_reason == "":
                                            single_reason = "Missing"
                                        else:
                                            single_reason += ", missing"
                                        #myReportFile.write("\nstrange")
                                     
                                     elif taken_grade==letter_to_number.get("W"):   
                                         if counter_alts == 1:
                                             if single_reason == "":
                                                 single_reason = f"Withdrawn in {taken_semester}"  
                                             else:
                                                 single_reason += f", withdrawn in {taken_semester}"
    
                                         else:
                                             if single_reason == "":
                                                 single_reason = f"Withdrawn from {taken_code} {taken_num} in {taken_semester}"  
                                             else:
                                                single_reason += f", withdrawn from {taken_code} {taken_num} in {taken_semester}"
                                                                         #se il corso è stato proprio fallito   
                                     elif taken_grade==letter_to_number.get("NP") or taken_grade==letter_to_number.get("F"):
                                         if counter_alts == 1:
                                             if single_reason == "":
                                                 single_reason = f"Withdrawn from in {taken_semester}"  
                                             else:
                                                 single_reason += f", failed in {taken_semester}"
    
                                         else:
                                             if single_reason == "":
                                                 single_reason = f"Failed {taken_code} {taken_num} in {taken_semester}"  
                                             else:
                                                single_reason += f", failed {taken_code} {taken_num} in {taken_semester}"
                                     
                                     #se il corso è incomplete    
                                     elif taken_grade==letter_to_number.get("INC"):
                                         if counter_alts == 1:
                                             if single_reason == "":
                                                 single_reason = f"Incomplete in {taken_semester}"
                                             else: 
                                                 single_reason += f", incomplete in {taken_semester}"
                                             #self.prerequisite_reason.append(single_reason)
                                         else:
                                             if single_reason == "":
                                                 single_reason = f"Incomplete in {taken_code} {taken_num} in {taken_semester}"
                                             else:
                                                 single_reason += f", incomplete in {taken_code} {taken_num} in {taken_semester}"
                                             #self.prerequisite_reason.append(single_reason)
                    
                                    #rimosso failed, aggiunto prima
                                             
                                     elif taken_grade<letter_to_number.get(prereq_grade):
    
                                        if counter_alts == 1:
                                            grade = number_to_letter.get(taken_grade)
                                            if taken_grade == letter_to_number.get("current"):
                                                if not (taken_code==course_name and taken_num==course_num):
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
                                            if taken_grade == letter_to_number.get("current"):
                                                if not (taken_code==course_name and taken_num==course_num):
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
                                                single_reason = "Missing" 
                                            else:
                                                single_reason += ", missing"
                                           #self.prerequisite_reason.append(single_reason)
                                           #print("append 1")
                                        else:
                                            if single_reason == "":
                                                single_reason = f"Missing {taken_code} {taken_num} "
                                            else:
                                                single_reason += f", missing {taken_code} {taken_num}"
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
                if float(self.gpa) < 3.50:
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
    
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Remove Retake
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def print_retake(self):
        text = f"{self.get_name()} is retaking {len(self.retaken_classes)} courses: "
        #for i in  self.retaken_classes:
            #text += f"{i.course.get_name()}, "
        if len(self.retaken_classes) != 0:
            final_text = f"{text} {self.text}\n\n"
    
    
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
        #                       name,            surname,   language_waived,      major,            minor1,          minor2     double_degree/major..
        student = Student(curr_student[0], curr_student[1], curr_student[2], curr_student[3], curr_student[4], curr_student[5], curr_student[7], curr_student[8]) 
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
#json