# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 09:39:11 2022

@author: ilda1
"""
#from students import Student

class Course:
    
    def __init__(self, namecourse, code, number, credits_num, req_list, course_key):
        self.name = namecourse
        self.code = code
        self.number = number
        self.credits = credits_num
        self.requirements_list = req_list
        self.course_key = course_key
        
    def get_name(self):
        return self.name
    
    def get_code(self):
        return self.code
    
    def get_number(self):
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
        self.grade = grade
        self.term = term
        self.c_type = c_type
        
    def change_credits(self):
        if self.c_type == 1:
            self.course.credits = self.course.credits + 1
    
    #do I need get student/course?
    
    def get_section(self):
        return self.section
    
    def get_grade(self):
        return self.grade
    
    def get_term(self):
        return self.term
    
    def get_course_type(self):
        if self.c_type == 0:
            return ""
        else:
            return " - Honor"