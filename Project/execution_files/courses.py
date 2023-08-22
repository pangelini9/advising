# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 09:39:11 2022

@author: ilda1
"""
#from students import Student

from execution_files.Utilities import letter_to_number

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
        
        self.used_flag = 0
        """
        0 = is in general electives
        1 = used in A (general distribution requirements)
        2 = used in major not A (additional, core, ...)
        3 = minor 1
        4 = minor 2
        5 = overlap major and minor1
        6 = overlap major and minor2
        7 = overlap major, minor1 and minor2
        8 = overlap minor1 and minor2
        """
        
        
        
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
        