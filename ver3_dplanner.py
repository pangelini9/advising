# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 16:58:52 2022

@author: ilda1
"""
import json
import xlsxwriter
from courses import Course, Course_taken
from students import Student
from majors import Major
from create_courses_list import return_class_objects

workbook = xlsxwriter.Workbook('planner.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column(0, 5, 11)
worksheet.set_column(7, 12, 11) 
worksheet.set_column(14, 14, 44)

"""
IMPORT THE FORMATS
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
return_class_objects()

"""
IMPORT THE MAJORS
"""
#....

"""
IMPORT THE STUDENT
"""
#....

"""
START THE PRINT
"""
#...