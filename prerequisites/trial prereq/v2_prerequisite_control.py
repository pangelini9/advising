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
missing_courses = []
missing_courses = curr_student.check_requirements()

#print(f"\n{missing_courses}")
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
course structure = [[courses, {'prerequisite': [[[{'code': 'EN', 'lower bound': 103.0, 'upper bound': 103.0, 'grade': 'C'}, 
                                                  {'code': 'EN', 'lower bound': 105.0, 'upper bound': 105.0, 'grade': 'C'}], 
                                                 'Missing']], 
                               'corequisite': []}], 
                    [courses, {'prerequisite': [[[{'code': 'FIN', 'lower bound': 301.0, 'upper bound': 301.0, 'grade': 'D-'}], 
                                                 'Grade']], 
                               'corequisite': []}]]
"""    

prev_row_lenght = 0 #counter so that stuff does  not override eachoter   
'il loop dello studente deve partire sotto questa variabile o i dati vengono sovrascritti'
#worksheet.write(row, column, "stuff to print", format)

#for loop over the list of courses whose requirements are not satisfied
for row_content in range(0, len(missing_courses)): 
               
    #row_index = row_content + prereq_num + 1
    row_index = row_content + 1
    
    req_type = ["prerequisite", "corequisite"]
    requirements = missing_courses[row_content][1] # {'prerequisite': [[[{'code': 'EN', 'lower bound': 103.0, 'upper bound': 103.0, 'grade': 'C'}, {'code': 'EN', 'lower bound': 105.0, 'upper bound': 105.0, 'grade': 'C'}], 'Missing']], 'corequisite': []}
    current_course = missing_courses[row_content][0]
    #print(f"\n{current_course}: {requirements}")
    
    #first picks prerequisites, then corequisites
    for j in req_type: 
        curr_requirement = requirements[j] #the list of missing requirements:
        #[[[{'code': 'EN', 'lower bound': 103.0, 'upper bound': 103.0, 'grade': 'C'}, {'code': 'EN', 'lower bound': 105.0, 'upper bound': 105.0, 'grade': 'C'}], 'Missing']]
        #print(f"\ncurr_requirement: {curr_requirement}")
        
        row_index = prev_row_lenght + 1 #prev_row_lenght should acount for the last row the program has written, while 1 accounts for the title line
        
        #colum lenght because goes over all the missing requirements for the same course
        for index_requirement in range(0,len(curr_requirement)):
            name = f"{curr_student.get_name()} {curr_student.get_surname()}"
            course_name = current_course.course.get_code()
            course_num = current_course.course.get_number()
            course_info = f"{course_name} {course_num}"
            
            #row_index += prev_row_lenght
            
            #worksheet.write(row_index, 0, name, p_format) #prints student's name
            #worksheet.write(row_index, 1, course_info, p_format) #prints name of the course
            
                   
            single_requirement = curr_requirement[index_requirement] #the list of alternatives for a single requirement + the problem
            #[[{'code': 'FIN', 'lower bound': 301.0, 'upper bound': 301.0, 'grade': 'D-'}], 'Grade']
            #print(f"\nsingle_requirement: {single_requirement}")
            
            """
            for list_index in range(0, len(requirements)):

                #print("\nnext step")
                #print(j)
                
                column_index = list_index + 3
                """  
            
            alternatives_list = single_requirement[0]
            requirement_reason = single_requirement[1]
            
            #goes over all the alternatives for a requirement so control rows
            for list_index in range(0, len(alternatives_list)): 
                loop_lenght = 0
                row_index += list_index
                #row_index += prev_row_lenght

                worksheet.write(row_index, 0, name, p_format) #prints student's name
                worksheet.write(row_index, 1, course_info, p_format) #prints name of the course
                
                worksheet.write(row_index, 2 + 3*index_requirement, j, p_format) #prints the course with the unfilled requirements
                
                r_code = alternatives_list[list_index]["code"]
                r_lowerbound = alternatives_list[list_index]["lower bound"]
                r_upperbound =  alternatives_list[list_index]["upper bound"]
                
                if r_lowerbound == r_upperbound:
                    cell_content = f"{r_code} {r_lowerbound}"
                else:
                    cell_content = f"A {r_code} missing_courses from {r_lowerbound} to {r_upperbound}" #prints requirements one by one
                
                #column_index = index_requirement 
                
                print(f"\n{cell_content} in row={row_index} column={3 + 3*index_requirement}")
                
                
                
                worksheet.write(row_index, 3 + 3*index_requirement, cell_content, p_format) #prints requirements one by one
                worksheet.write(row_index, 4 + 3*index_requirement, requirement_reason, p_format) #prints the reasoning
                
                #column_index += 1
                if len(alternatives_list)>loop_lenght:
                    loop_lenght = len(alternatives_list)
                    #print(f"\nloop_lenght= {loop_lenght}")
            #prev_row_lenght += loop_lenght        
            #print(f"\nprev_row_lenght= {prev_row_lenght}")
            #print(f"prev_row_lenght: {prev_row_lenght}")
            #row_index += 1
            
        #prev_row_lenght += len(alternatives_list)

        row_index -= len(curr_requirement)
    prev_row_lenght += loop_lenght        
    #print(f"\nprev_row_lenght= {prev_row_lenght}")



workbook.close()