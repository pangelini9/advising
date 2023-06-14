# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 13:09:38 2023

@author: elettra.scianetti
"""

import json
import xlsxwriter
from prereq_courses import Course, Course_taken
from prereq_students import Student, create_student_list
from prereq_majors import Major, create_major_list
from prereq_create_courses_list import create_course_obj, create_coursetaken_obj, create_remaining_list

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
    }

"""""""""""""""""""""""""""""""""""""""""""""""""""""
IMPORT THE LIST OF ALL COURSES THE UNIVERSITY OFFERS
"""""""""""""""""""""""""""""""""""""""""""""""""""
courses_list = create_course_obj()

""""""""""""""""""""""
IMPORT THE STUDENT
"""""""""""""""""""""
students_list = create_student_list()
curr_student = students_list[0]

courses_taken_list = curr_student.get_coursesTaken()
courses_taken_obj = create_coursetaken_obj(curr_student, courses_taken_list, courses_list)
curr_student.change_courses(courses_taken_obj)
curr_student.remove_retake() #toglie retake
curr_student.compute_transfer_credits() #counts how many credits the student has not done in residency
curr_student.change_credits_total() #sets the total amounts of credis equal to 150 id the student has a double degree
curr_student.add_transfer_credits() #if the student has done more than 60 credits out of residency, then it add them to the total amount of credits

curr_student.cumpute_gpa()
curr_student.compute_credits_earned()
curr_student.compute_credits_nxsem()
curr_student.compute_credits_missing()
curr_student.compute_cur_standing()
curr_student.compute_nx_standing()

"""""""""""""""""""""""""""""""""""""""""""""""""""""
CHECK THE PREREQUISITES
"""""""""""""""""""""""""""""""""""""""""""""""""""

curr_student.create_curr_list()
course = []
course = curr_student.check_requirements()

for i in course:
    print("\n")
    print(f"the student cannot take the course: \n{i[0].course.get_name()}")
    print(f"because they have not fullfilled these prerequisites: \n{i[1]}")
#current_courses=curr_student.return_current()









