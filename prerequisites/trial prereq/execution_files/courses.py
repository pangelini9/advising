# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 09:39:11 2022

@author: ilda1
"""
#from students import Student
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
    "AU" : 0.6}


class Course:
    
    def __init__(self, namecourse, code, number, credits_num, req_list, course_key, course_periods, course_concentrations, course_onsite):
        self.name = namecourse
        self.code = code
        self.number = number
        self.credits = credits_num
        self.requirements_dict = req_list
        self.course_key = course_key
        
        self.course_periods = course_periods
        self.course_concentrations = course_concentrations
        self.on_site = course_onsite
        
    def get_name(self): #full name
        return self.name
    
    def get_code(self): #prefix letter aka letter part of the code
        return self.code
    
    def get_number(self): #numerical part of the 
        return self.number
    
    def get_credits(self):
        return self.credits
    
    def get_requirements_dictionary(self):
        return self.requirements_dict
    
    def get_course_key(self):
        return self.course_key
    
    def get_course_periods(self):
        return self.course_periods
    
    def get_course_concentrations(self):
        return self.course_concentrations

    def get_on_site(self):
        return self.on_site


"""
NB:
course = Course(...)
student = Student(...)
"""
class Course_taken:
    
    def __init__(self, course, student, creds, grade, term, c_type, in_residence):
        self.course = course
        self.student = student
        self.creds = creds
        #self.section = course_section
        self.grade = letter_to_number.get(grade)
        self.term = term
        self.c_type = c_type #se è honor
        self.in_residence = in_residence #=1 se il corso è stato fatto in JCU, =0 se è stato fatto col direct exchange
        
        
    def get_course(self):
        return self.course
        
    #def get_credits(self):
        #creds = self.course.credits
        #if self.c_type == 1:
           #creds += 1
        #return creds
    
    def get_grade(self):
        return self.grade
    
    def get_term(self):
        return self.term
    
    def get_course_type(self):
        if self.c_type == 1:
            return " - Honor"
        else:
            return ""
    
    def get_course_type2(self):
        if self.c_type == 1:
            return " H"
        else:
            return ""        
        
    def return_honor(self):
        return self.c_type
    
    def return_in_residence(self):
        return self.in_residence
     
    #has to be substituted because for credits we will consider the amount granted to the student
    #for each of the courses under consideration
    def get_credits(self):
        return self.creds
        