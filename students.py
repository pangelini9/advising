# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 16:15:21 2022

@author: ilda1
"""

#from majors import Major
#from courses import Course, Course_taken
#NB: major = Major(...)

class Student:
    
    def __init__(self, namestudent, surname, highschool_credits, major, minor1, minor2, courses_done):
        self.name = namestudent
        self.surname = surname
        self.highschool = highschool_credits #=1 if yes
        self.major = major
        self.minor1 = minor1
        self.minor2 = minor2
        self.courses_done = courses_done
        
    #do I need get major, minor1, minor 2? or is it fine since the values are 
    #obtained from the object itself
        
    def get_name(self):
        return self.name
    
    def get_surname(self):
        return self.surname
    
    def get_highschool(self):
        return self.highschool_credits
    
    #def cumpute_gpa(self):
        #do they compure it on the semester and then they do the total or it's
        #the average of the courses' grades?
    
    #def compute_cur_credits(self):
        
    #def compute_cur_standing(self):
        
    #def compute_nx_credits(self):
        
    #def compute_nx_standing(self):
    
    #def compute_missing_credits(self):