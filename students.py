# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 16:15:21 2022

@author: ilda1
"""

#from majors import Major
#from courses import Course, Course_taken
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
    
    def add_course(self, course):
        self.courses_done.append(course)
    
    def change_major(self, majorobj):
        self.major = majorobj
        print(self.major)
        
    def change_courses(self, courses_taken_obj):
        self.courses_done = courses_taken_obj

    #def cumpute_gpa(self):
        #do they compure it on the semester and then they do the total or it's
        #the average of the courses' grades?
    
    #def compute_cur_credits(self):
        
    #def compute_cur_standing(self):
        
    #def compute_nx_credits(self):
        
    #def compute_nx_standing(self):
    
    #def compute_missing_credits(self):
        
def create_student_list():
    with open('students_list.json', 'r') as myfile:
       students_list = json.load(myfile)
      
    student_obj = []
   
    for i in range(0, len(students_list)): 
        curr_student = students_list[i]
        student = Student(curr_student[0], curr_student[1], curr_student[2], curr_student[3], curr_student[4], curr_student[5])
        courses_t = curr_student[6]
        for course in courses_t:
            student.add_course(course)
        cc = student.get_coursesTaken()
        print(cc)
        student_obj.append(student)
        i = i+1
        return student_obj