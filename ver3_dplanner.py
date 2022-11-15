# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 16:58:52 2022

@author: ilda1
"""
import json
import xlsxwriter
from courses import Course, Course_taken
from students import Student, create_student_list
from majors import Major, create_major_list
from create_courses_list import create_course_obj, create_coursetaken_obj


workbook = xlsxwriter.Workbook('planner.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column(0, 5, 11)
worksheet.set_column(7, 12, 11) 
worksheet.set_column(14, 14, 44)

"""
IMPORT THE FORMATS
...
"""
with open('formats_list.json', 'r') as myfile:
  format_list = json.load(myfile)

for i in range(0, len(format_list)):
    curr_format = format_list[i]
    curr_format[0] = workbook.add_format(curr_format[1])
    i += 1
    

"""
IMPORT THE PLANNER PARTS
"""
with open('planner_parts.json', 'r') as myfile:
  planner_elements = json.load(myfile)
  
"""
IMPORT THE LIST OF ALL COURSES THE UNIVERSITY OFFERS
"""
courses_list = create_course_obj()

"""
IMPORT THE MAJORS
"""
majors_list = create_major_list()

"""
IMPORT THE STUDENT
"""
students_list = create_student_list()

#changes the element major present in the student object as the major key into the major object
for i in range(0, len(students_list)):
    curr_student = students_list[i]
    for j in range(0, len(majors_list)):
        curr_major = majors_list[j]
        if curr_student.get_major() == curr_major.get_major_key():
            curr_student.change_major(curr_major)
            break
        else:
            j +=1
    i += 1

#change the list of courses taken by the student with a list of objects courses taken    
for i in range(0, len(students_list)):
    curr_student = students_list[i]
    courses_taken_list = curr_student.get_coursesTaken()
    courses_taken_obj = create_coursetaken_obj(curr_student, courses_taken_list, courses_list)
    curr_student.change_courses(courses_taken_obj)
    #print(curr_student.get_coursesTaken())
    i += 1


    
        
"""
START THE PRINT
"""
#...