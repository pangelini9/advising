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


"""""""""""""""""""""""""""""""""
OPEN AND FORMAT THE EXCEL FILE
"""""""""""""""""""""""""""""""""
workbook = prerequisites_formats.workbook
worksheet = prerequisites_formats.worksheet

prerequisites_formats.set_borders()
prerequisites_formats.set_column_width()
prerequisites_formats.set_contour_border()

#p_format = prerequisites_formats.border_left
normal_border = prerequisites_formats.normal_border
normal_noborder = prerequisites_formats.normal_noborder

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

#prerequisites_formats.print_fields_names()

"""    
course structure = [[courses, {'prerequisite': [[[{'code': 'EN', 'lower bound': 103.0, 'upper bound': 103.0, 'grade': 'C'}, 
                                                  {'code': 'EN', 'lower bound': 105.0, 'upper bound': 105.0, 'grade': 'C'}], 
                                                 'Missing']], 
                               'corequisite': []}], 
                    [courses, {'prerequisite': [[[{'code': 'FIN', 'lower bound': 301.0, 'upper bound': 301.0, 'grade': 'D-'}], 
                                                 'Grade']], 
                               'corequisite': []}]]
"""    

prev_row_lenght = 1 #counter so that stuff does  not override eachoter   
'il loop dello studente deve partire sotto questa variabile o i dati vengono sovrascritti'
#worksheet.write(row, column, "stuff to print", format)


missing_num = 0 #counter to print the right number of field names 

#for loop over the list of courses whose requirements are not satisfied
for row_content in range(0, len(missing_courses)): 
               
    #row_index = row_content + prereq_num + 1
    #row_index = row_content + 1
    row_index = row_content + prev_row_lenght
    
    
    req_type = ["prerequisite", "corequisite"]
    requirements = missing_courses[row_content][1] # {'prerequisite': [[[{'code': 'EN', 'lower bound': 103.0, 'upper bound': 103.0, 'grade': 'C'}, {'code': 'EN', 'lower bound': 105.0, 'upper bound': 105.0, 'grade': 'C'}], 'Missing']], 'corequisite': []}
    current_course = missing_courses[row_content][0]
    #print(f"\n{current_course}: {requirements}")
    
    #first picks prerequisites, then corequisites
    for j in req_type: 
        curr_requirement = requirements[j] #the list of missing requirements:
        #[[[{'code': 'EN', 'lower bound': 103.0, 'upper bound': 103.0, 'grade': 'C'}, {'code': 'EN', 'lower bound': 105.0, 'upper bound': 105.0, 'grade': 'C'}], 'Missing']]
        
        #row_index = prev_row_lenght + 1 #prev_row_lenght should account for the last row the program has written, while 1 accounts for the title line
        
        "INFO STUDENT"
        name = f"{curr_student.get_name()} {curr_student.get_surname()}"
        course_name = current_course.course.get_code()
        course_num = current_course.course.get_number()
        course_info = f"{course_name} {course_num}"
        
        special_requirement = False
        
        "LOOK FOR COURSES WITH UNUSUAL PREREQUSITES"
        #Exeptions: Drawing/Painting
        if (course_name=="AS" and course_num==304) or (course_name=="AS" and course_num==306):
            print("Drawing/Painting")   
            special_requirement = True
            r_code = "Drawing or Painting"
            
        #Exeptions: Graphic Design
        elif (course_name=="AS" and course_num==3330) or (course_name=="AS" and course_num==332):
            print("Graphic Design")
            special_requirement = True
            r_code = "Graphic Design"
            
        #Exeptions: Painting / Printmaking
        elif (course_name=="AS" and course_num==342):
            print("Painting / Printmaking")
            special_requirement = True
            r_code = "Painting or Printmaking"
            
        #Exeptions: 
        elif (course_name=="AS" and course_num==345) or (course_name=="AS" and course_num==349):
            print("Photography")
            special_requirement = True
            r_code = "Photography"

        #Exeptions: Italian literature
        elif (course_name=="IT" and course_num==349) or (course_name=="IT" and course_num==399):
            #print("Italian literature")
            special_requirement = True
            r_code = "Italian literature" 
        
        "SPLIT FOR SPECIAL COURSES"
        if special_requirement == True:
            loop_lenght = 0
            #row index should be okay ??
            
            
            worksheet.write(row_index, 0, name, normal_noborder) #prints student's name
            worksheet.write(row_index, 1, course_info, normal_border) #prints name of the course
            
            worksheet.write(row_index, 2, j, normal_noborder) #prints the type of the unfilled requirements
            
            cell_content = f"One {r_code} course" 
            requirement_reason = curr_requirement[0][1]
            #print(curr_requirement)
            #requirement_reason = "problem"
            print(f"\n{cell_content} in row={row_index} column={3}")

            
            worksheet.write(row_index, 3, cell_content, normal_noborder) #prints requirements one by one
            worksheet.write(row_index, 4, requirement_reason, normal_border) #prints the reasoning
            break
           
        #i corsi che non hanno bisogno di requirement strani    
        else:
        
            #colum lenght because goes over all the missing requirements for the same course
            for index_requirement in range(0,len(curr_requirement)):
                if len(curr_requirement)>= missing_num:
                    missing_num = len(curr_requirement)
                       
                single_requirement = curr_requirement[index_requirement] #the list of alternatives for a single requirement + the problem
                #[[{'code': 'FIN', 'lower bound': 301.0, 'upper bound': 301.0, 'grade': 'D-'}], 'Grade']
                #print(f"\nsingle_requirement: {single_requirement}")
                
               
                alternatives_list = single_requirement[0]
                requirement_reason = single_requirement[1]
    
                r_code = 0
                r_lowerbound = 0
                r_upperbound =  0
    
                #version to concatenate strings
                worksheet.write(row_index, 0, name, normal_noborder) #prints student's name
                worksheet.write(row_index, 1, course_info, normal_border) #prints name of the course
                worksheet.write(row_index, 2 + 3*index_requirement, j, normal_noborder) #prints the type of the unfilled requirements
                

                    
                #goes over all the alternatives for a requirement so control rows
                for list_index in range(0, len(alternatives_list)): 
                    loop_lenght = 0
                    #row_index += list_index
                    #row_index += prev_row_lenght
                    
                    """Version for alternatives on different rows 
                    worksheet.write(row_index, 0, name, p_format) #prints student's name
                    worksheet.write(row_index, 1, course_info, p_format) #prints name of the course
                    
                    
                    if list_index != 0:
                        worksheet.write(row_index, 2 + 3*index_requirement, "or", p_format) #prints "OR"
                    else:
                        worksheet.write(row_index, 2 + 3*index_requirement, j, p_format) #prints the type of the unfilled requirements
                    
                    """
                    r_code = alternatives_list[list_index]["code"]
                    
                    #print diverso per lo standing
                    if r_code == "S":
                        creds = alternatives_list[list_index]["lower bound"]
                        #Freshman  0-29, Sophomore 30-59, Junior    60-89, Senior    90-...
                        
                        """Version for alternatives on different rows 
                        if creds>= 90:
                            cell_content = "Senior Standing"
                        elif creds>= 60:    
                            cell_content = "Junior Standing"
                        elif creds>= 30:    
                            cell_content = "Sophomore Standing"
                        elif creds>= 0:    
                            cell_content = "Freshman Standing"
                        """
                        #version to concatenate strings
                        if creds>=90 and list_index==0:
                            cell_content = "Senior Standing"
                        elif creds>=90 and list_index!=0:
                            cell_content += " or Senior Standing"
                            
                        elif creds>=60 and list_index==0:    
                            cell_content = "Junior Standing"
                        elif creds>=60 and list_index!=0:
                            cell_content += " or Junior Standing"
                            
                        elif creds>=30 and list_index==0:    
                            cell_content = "Sophomore Standing"
                        elif creds>=30 and list_index!=0:
                            cell_content += " or Sophomore Standing"
                            
                        elif creds>=0 and list_index==0:    
                            cell_content = "Freshman Standing"
                        elif creds>=0 and list_index!=0:
                            cell_content += " or Freshman Standing"
                            
                    #se il requirement è un corso o un range
                    else:
                        #r_code = alternatives_list[list_index]["code"]
                        r_lowerbound = alternatives_list[list_index]["lower bound"]
                        r_upperbound =  alternatives_list[list_index]["upper bound"]
                        
                        
                        """Version for alternatives on different rows 
                        if r_lowerbound == r_upperbound:
                            cell_content = f"{r_code} {r_lowerbound}"
                        else: 
                            #if the upper and lower bounds are in place only for the execution
                            if r_lowerbound == 1 and r_upperbound == 1000:
                                cell_content = f"One {r_code} course" 
                                
                            #if the upper bound is in place only for the execution, but the lower bound exists
                            elif r_lowerbound != 1 and r_upperbound == 1000:
                                cell_content = f"One {r_code} course from {r_lowerbound} onwards" 
                            
                            #if the lower bound is in place only for the execution, but the upper bound exists
                            elif r_lowerbound == 1 and r_upperbound != 1000: 
                                cell_content = f"One {r_code} course up to {r_upperbound}"
                                
                            #both lower and upper bounds exist
                            elif r_lowerbound != r_upperbound and r_upperbound != 1000:
                                cell_content = f"One {r_code} course from {r_lowerbound} to {r_upperbound}"
                        """      

                        #version to concatenate strings                          
                        if r_lowerbound==r_upperbound and list_index==0:
                            cell_content = f"{r_code} {r_lowerbound}"
                        elif r_lowerbound==r_upperbound and list_index!=0:
                            cell_content += f" or {r_code} {r_lowerbound}"
                            
                        else: 
                            #if the upper and lower bounds are in place only for the execution
                            if (r_lowerbound == 1 and r_upperbound == 1000) and (list_index==0):
                                cell_content = f"One {r_code} course" 
                            elif (r_lowerbound == 1 and r_upperbound == 1000) and (list_index!=0):
                                cell_content += f" or one {r_code} course"  
                            
                            
                            #if the upper bound is in place only for the execution, but the lower bound exists
                            elif (r_lowerbound != 1 and r_upperbound == 1000) and (list_index==0):
                                cell_content = f"One {r_code} course from {r_lowerbound} onwards" 
                            elif (r_lowerbound != 1 and r_upperbound == 1000) and (list_index!=0):
                                cell_content += f" or one {r_code} course from {r_lowerbound} onwards"                            
                                
                            
                            #if the lower bound is in place only for the execution, but the upper bound exists
                            elif (r_lowerbound == 1 and r_upperbound != 1000) and (list_index==0): 
                                cell_content = f"One {r_code} course up to {r_upperbound}"
                            elif (r_lowerbound == 1 and r_upperbound != 1000) and (list_index!=0):
                                cell_content += f" or one {r_code} course up to {r_upperbound}"                            
                                
                            #both lower and upper bounds exist
                            elif (r_lowerbound != r_upperbound and r_upperbound != 1000) and (list_index==0):
                                cell_content = f"One {r_code} course from {r_lowerbound} to {r_upperbound}"         
                            elif (r_lowerbound != r_upperbound and r_upperbound != 1000) and (list_index!=0):
                                cell_content += f" or one {r_code} course from {r_lowerbound} to {r_upperbound}"                           
                        
                        
                    print(f"\n{cell_content} in row={row_index} column={3 + 3*index_requirement}")
    
                    """Version for alternatives on different rows
                    worksheet.write(row_index, 3 + 3*index_requirement, cell_content, p_format) #prints requirements one by one
                    worksheet.write(row_index, 4 + 3*index_requirement, requirement_reason, p_format) #prints the reasoning
                    
                    #column_index += 1
                    if len(alternatives_list)>loop_lenght:
                        loop_lenght = len(alternatives_list)
                        #print(f"\nloop_lenght= {loop_lenght}")
                        
                    row_index -= list_index  
                    """
                    
                worksheet.write(row_index, 3 + 3*index_requirement, cell_content, normal_noborder) #prints requirements one by one
                worksheet.write(row_index, 4 + 3*index_requirement, requirement_reason, normal_border) #prints the reasoning
                
    #prev_row_lenght += loop_lenght        
    #print(f"\nprev_row_lenght= {prev_row_lenght}")

#will be needed when we will iterate over the students or the program will override rows
prev_row_lenght += len(missing_courses)

prerequisites_formats.print_fields_names(missing_num)
workbook.close()

"""
#Exeptions: Drawing/Painting
if (course_name=="AS" and course_num==304) or (course_name=="AS" and course_num==306):
    print("Drawing/Painting")   
    special_requirement = True
    r_code = "Drawing or Painting"
    
#Exeptions: Graphic Design
elif (course_name=="AS" and course_num==3330) or (course_name=="AS" and course_num==332):
    print("Graphic Design")
    special_requirement = True
    r_code = "Graphic Design"
    
#Exeptions: Painting / Printmaking
elif (course_name=="AS" and course_num==342):
    print("Painting / Printmaking")
    special_requirement = True
    r_code = "Painting or Printmaking"
    
#Exeptions: 
elif (course_name=="AS" and course_num==345) or (course_name=="AS" and course_num==349):
    print("Photography")
    special_requirement = True
    r_code = "Photography"

#Exeptions: Italian literature
elif (course_name=="IT" and course_num==349) or (course_name=="IT" and course_num==399):
    print("Italian literature")
    special_requirement = True
    r_code = "Italian literature"
    
if special_requirement == True:
    loop_lenght = 0
    #row index should be okay ??
    
    
    worksheet.write(row_index, 0, name, p_format) #prints student's name
    worksheet.write(row_index, 1, course_info, p_format) #prints name of the course
    
    worksheet.write(row_index, 2, j, p_format) #prints the type of the unfilled requirements
    
    cell_content = f"One {r_code} course" 
    requirement_reason =
    
    print(f"\n{cell_content} in row={row_index} column={3 + 3*index_requirement}")

    
    worksheet.write(row_index, 3, cell_content, p_format) #prints requirements one by one
    worksheet.write(row_index, 4, requirement_reason, p_format) #prints the reasoning
    
   
#i corsi che non hanno bisogno di requirement strani    
else:
    print("Tutto il resto da riga 155")
"""