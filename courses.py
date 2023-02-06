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
    "TR" : 0.5, # PA: added this entry, for Transfer credits
    }


class Course:
    
    def __init__(self, namecourse, code, number, credits_num, req_list, course_key):
        self.name = namecourse
        self.code = code
        self.number = number
        self.credits = credits_num
        self.requirements_list = req_list
        self.course_key = course_key
        
    def get_name(self): #full name
        return self.name
    
    def get_code(self): #prefix letter
        return self.code
    
    def get_number(self): #number
        return self.number
    
    def get_credits(self):
        return self.credits
    
    def get_requirements_list(self):
        return self.requirements_list
    
    def get_course_key(self):
        return self.course_key

"""
NB:
course = Course(...)
student = Student(...)
"""
class Course_taken:
    
    def __init__(self, course, student, course_section, grade, term, c_type):
        self.course = course
        self.student = student
        self.section = course_section
        self.grade = letter_to_number.get(grade)
        self.term = term
        self.c_type = c_type
        
    def get_course(self):
        return self.course
        
    def get_credits(self):
        creds = self.course.credits
        if self.c_type == 1:
           creds += 1
        return creds
    
    def get_section(self):
        return self.section
    
    def get_grade(self):
        return self.grade
    
    def get_term(self):
        return self.term
    
    def get_course_type(self):
        if self.c_type == 1:
            return " - Honor"
        else:
            return ""
    