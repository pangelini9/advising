# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 13:09:38 2023

@author: elettra.scianetti
"""

import json
import xlsxwriter
from courses import Course, Course_taken
from v2_students import Student, create_student_list
from majors import Major, create_major_list
from create_courses_list import create_course_obj, create_coursetaken_obj, create_remaining_list
import prerequisites_formats

workbook = prerequisites_formats.workbook
worksheet = prerequisites_formats.worksheet

p_format = prerequisites_formats.border_left

#[[{'code': 'EN', 'lower bound': 103.0, 'upper bound': 103.0, 'grade': 'C'}], [{'code': 'EN', 'lower bound': 105.0, 'upper bound': 105.0, 'grade': 'C'}]]

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
    0.5 : "TR" # PA: added this entry, for Transfer credits
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
#curr_student.compute_transfer_credits() #counts how many credits the student has not done in residency
#curr_student.change_credits_total() #sets the total amounts of credis equal to 150 id the student has a double degree
#curr_student.add_transfer_credits() #if the student has done more than 60 credits out of residency, then it add them to the total amount of credits

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

"""
for i in course:
    print("\n")
    print(f"the student cannot take the course: \n{i[0].course.get_name()}")
    print(f"because they have not fullfilled these prerequisites: \n{i[1]}")
#current_courses=curr_student.return_current()
"""

#print(f"\n{course}")

prerequisites_formats.print_fields_names()

"""    
course structure = [
                        [course_taken, {'prerequisite': [[{'code': 'EN', 'lower bound': 103.0, 'upper bound': 103.0, 'grade': 'C'}], [{'code': 'EN', 'lower bound': 105.0, 'upper bound': 105.0, 'grade': 'C'}]], 'corequisite': []}], 
                                        'corequisite': [[]]}
                         ], 
                        [course_taken, {'prerequisite': [[{'code': 'MA', 'lower bound': 198.0, 'upper bound': 198.0, 'grade': 'D-'}], [{'code': 'MA', 'lower bound': 208.0, 'upper bound': 208.0, 'grade': 'D-'}], 
                                        'corequisite': [[]]}
                         ]
                    ]
"""    

prereq_num = 0 #counter so that stuff does  not override eachoter   

#worksheet.write(row, column, "stuff to print", format)
for row_content in range(0, len(course)): 
               
    #row_index = row_content + prereq_num + 1
    row_index = row_content + 1
    
    req_type = ["prerequisite", "corequisite"]
    requirements = course[row_content][1] # {'prerequisite': [[{'code': 'MA', 'lower bound': 198.0, 'upper bound': 198.0, 'grade': 'D-'}], [{'code': 'MA', 'lower bound': 208.0, 'upper bound': 208.0, 'grade': 'D-'}]]
    
    row_index += prereq_num
    
    for j in req_type:
        
        curr_requirement = requirements[j] #[[{'code': 'MA', 'lower bound': 198.0, 'upper bound': 198.0, 'grade': 'D-'}], [{'code': 'MA', 'lower bound': 208.0, 'upper bound': 208.0, 'grade': 'D-'}]]
        row_index += prereq_num
        
        for index_requirement in range(0,len(curr_requirement)):
            
            worksheet.write(row_index, 0, curr_student.get_name(), p_format) #prints name
            worksheet.write(row_index, 1, curr_student.get_surname(), p_format) #prints surname
            worksheet.write(row_index, 2, course[row_content][0].course.get_name(), p_format) #prints name of the course
            
            prereq_num += 1
            #row_index += 1
            
            single_requirement = curr_requirement[index_requirement]
            for list_index in range(0, len(requirements)):

                #print("\nnext step")
                #print(j)
                
                column_index = list_index + 4
                
                for counter in range(0, len(single_requirement)):

                    worksheet.write(row_index, 3, j, p_format)
                    
                    print_info = single_requirement[counter]
                    #print(print_info)
                    """
                    r_code = print_info["code"]
                    r_lowerbound = print_info["lower bound"]
                    r_upperbound =  print_info["upper bound"]
                    
                    if r_lowerbound == r_upperbound:
                        cell_content = f"{r_code} {r_lowerbound}"
                    else:
                        cell_content = f"A {r_code} course from {r_lowerbound} to {r_upperbound}" #prints requirements one by one
                        
                    worksheet.write(row_index, column_index, cell_content, p_format)
                    """
            row_index += 1
            
        row_index -= len(curr_requirement)

"""             
[[<courses.Course_taken object at 0x000001391D1A0970>, {'prerequisite': [[[{'code': 'EN', 'lower bound': 103.0, 'upper bound': 103.0, 'grade': 'C'}]]], 
                                                        'corequisite': []}], [<courses.Course_taken object at 0x000001391D1A0E20>, {'prerequisite': [[[{'code': 'MA', 'lower bound': 208.0, 'upper bound': 208.0, 'grade': 'D-'}]]], 'corequisite': []}]]
"""


workbook.close()