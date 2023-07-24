# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 13:04:30 2023

@author: elettra.scianetti
"""

import xlsxwriter
import os.path
import json


from execution_files.courses import Course, Course_taken
from execution_files.students import Student, create_student_list
from execution_files.majors import Major, create_major_list
from execution_files.create_courses_list import create_course_obj, create_coursetaken_obj, create_remaining_list


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
    0.01 : "AU"}

#1 == additional courses
#2 == only core courses
#3 == concentrations after core
#4 == concentrations nei major electives


"""""""""""""""""""""""""""
DEFINE SOME PRINTING FORMATS
"""""""""""""""""""""""

def set_borders(row_list, cell_list, worksheet, border_left): 
    for j in row_list: #loops over rows
        for i in cell_list: #loops over columns
            cell_selected = i - 1
            worksheet.write(cell_selected, j, "", border_left)

def long_merge(row, arg, c, worksheet, merge_format1, merge_format2):
    position = (("A" + str(row)) + (":") + ("M" + str(row)))
    if c == 1:
        worksheet.merge_range(position, arg, merge_format1) #long blue headline
    else:
        worksheet.merge_range(position, arg, merge_format2) #long white headline
  
def short_merge_sx(row, arg, c, worksheet, merge_format1, merge_format2):
    position = (("A" + str(row)) + (":") + ("F" + str(row)))
    if c == 1:
        worksheet.merge_range(position, arg, merge_format1) #short blue headline on left size
    elif c == 0:
        worksheet.merge_range(position, arg, merge_format2) #short white headline followed by course info on left size
        course_det_left(row)
    elif c == 2:
        worksheet.merge_range(position, arg, merge_format2) #short white headline on left size


def short_merge_dx(row, arg, c, worksheet, merge_format1, merge_format2):
    position = (("H" + str(row)) + (":") + ("M" + str(row))) 
    if c == 1:
        worksheet.merge_range(position, arg, merge_format1) #short blue headline on right size
    elif c == 0:
        worksheet.merge_range(position, arg, merge_format2) #short white headline followed by course info on right size
        course_det_right(row)
    elif c == 2:
        worksheet.merge_range(position, arg, merge_format2) #short white headline on right size

def course_det_left(row, worksheet, bold_left):
    worksheet.write(row, 0, "Name", bold_left)
    worksheet.write(row, 1, "Course", bold_left)
    worksheet.write(row, 2, "Code", bold_left)
    worksheet.write(row, 3, "Term", bold_left)
    worksheet.write(row, 4, "Grade", bold_left)
    worksheet.write(row, 5, "Credits", bold_left)
        
def course_det_right(row, worksheet, bold_left):
    worksheet.write(row, 7, "Name", bold_left) #col H=7
    worksheet.write(row, 8, "Course", bold_left)
    worksheet.write(row, 9, "Code", bold_left)
    worksheet.write(row, 10, "Term", bold_left)
    worksheet.write(row, 11, "Grade", bold_left)
    worksheet.write(row, 12, "Credits", bold_left)

def legend_merge(row, arg, worksheet, merge_format1):
    position = (("O" + str(row)) + (":") + ("P" + str(row)))
    worksheet.merge_range(position, arg, merge_format1)


def legend_structure(legend_keys, num_missing, row, worksheet, border_left):
    if num_missing == "":
        for i in range(0, len(legend_keys)):
            curr_key = legend_keys[i]
            position = int(row + i)
            worksheet.write(position, 14, str(curr_key), border_left)
            worksheet.write(position, 15, "", border_left)
            #i = +1
    else: 

        for i in range(0, len(legend_keys)):
            curr_key = legend_keys[i]
            position = int(row + i)
            worksheet.write(position, 14, str(curr_key), border_left)
            worksheet.write(position, 15, str(num_missing[curr_key]), border_left)
            #i = +1
        

"""""""""""""""""""""""""""
CREATE THE STRUCTURES
"""""""""""""""""""""""

#planner structure #1
def additional_courses(planner_name, curr_student, courses_list, banner_content, legend_keys):
    path = os.path.relpath(f"planners/{planner_name}.xlsx")

    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    
    worksheet.set_column(0, 5, 11)
    worksheet.set_column(7, 12, 11) 
    worksheet.set_column(14, 14, 44)
    
    banner = banner_content
     
    """""""""""""""""""""""""""
    DEFINE FORMATS
    """""""""""""""""""""""
    font_size = workbook.add_format({'font_size': 10})

    bold_center = workbook.add_format({'font_size': 10, 'bold': True, 'border': 1, 'align': 'center'})
    bold_left = workbook.add_format({'font_size': 10, 'bold': True, 'border': 1})

    border_center = workbook.add_format({'font_size': 10, 'border': 1, 'align': 'center',})
    border_left = workbook.add_format({'font_size': 10, 'border': 1})

    #blue banner
    merge_format1 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 1,
        'border': 1,
        'align': 'center',
        'fg_color': '#BDD7EE'
        })

    #white banner
    merge_format2 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'text_wrap': True
        })

    #cell format for "Course not taken yet"
    color_cell1 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'fg_color': '#FFE699'
        })

    #cell format for "No more than two core courses can be passed with D"
    color_cell2 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'fg_color': '#F4B084'
        })

    #cell format for "Grade requirement not satisfied"
    color_cell3 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'fg_color': '#FF0000'
        })

    #cell format for "Courses that the student is taking the current semester"
    color_cell4 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'fg_color': '#C6E0B4'
        })

    course_info_format = border_left

    """""""""""""""""""""""""""""""""""""""
    START THE PRINT
    """""""""""""""""""""""""""""""""""""""
    #print student name, surname, and major
    row = 1
    column = 0
    student_name = curr_student.get_name() + " " + curr_student.get_surname()
    student_major = "Degree Planner for B.A. in " + curr_student.major.get_name()
    long_merge(row, student_major, 1) #major
    long_merge(row+1, student_name, 0)  #name and surname
    banner_list = banner["A"]
    long_merge(row+3, banner_list[0], 1)


    """""""""""""""""""""""""""""""""""""""
    PRINT ENGLISH COMP and LIT REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  5
    banner_list = banner["eng"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print english banner
    course_det_left(row+1, worksheet, bold_left)

    curr_student.generate_en_courses(courses_list)
    curr_student.substitute_courses_done()
    curr_student.check_eng_composition()
    eng_requirement = curr_student.check_eng_literature()
    en_list = eng_requirement.get("output courses")
    #eng_requirement = curr_student.check_eng_requirement()

    for i in range(0, len(en_list)):
        en_course = en_list[i]
        if en_course[1] == 1:
            grade_format = border_center
        elif en_course[1] == 2:
            grade_format = color_cell3
        elif en_course[1] == 3:
            grade_format = color_cell4
        row = 7+i
        worksheet.write(row, 0, en_course[0].course.get_name(), course_info_format) #col A=0
        worksheet.write(row, 1, en_course[0].course.get_code(), course_info_format)
        worksheet.write(row, 2, en_course[0].course.get_number(), course_info_format)
        worksheet.write(row, 3, en_course[0].get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(en_course[0].get_grade()), grade_format)
        worksheet.write(row, 5, en_course[0].course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MA REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  13
    banner_list = banner["math"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print math proficiency banner
    ma_requirement = curr_student.check_ma_req()
    course_det_left(row+1, worksheet, bold_left)
       
    m_list = ma_requirement.get("courses done")
    if len(m_list) != 0:
        ma_course = m_list[0][0]
        if m_list[0] [1] == 0:
            grade_format = color_cell3
        elif m_list[0] [1] == 1:
            grade_format = border_center
        elif m_list[0] [1] == 2:
            grade_format = color_cell4
            
        row = 15
        worksheet.write(row, 0, ma_course.course.get_name(), course_info_format) #col A=0
        worksheet.write(row, 1, ma_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, ma_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, ma_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(ma_course.get_grade()), grade_format)
        worksheet.write(row, 5, ma_course.course.get_credits(), course_info_format)

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    CHECK ADDITIONAL REQUIREMENTS, CORE COURSES, AND GENERAL ELECTIVES
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
    additional_requirements = curr_student.check_additional()
    additional_remaining = curr_student.get_additional_remaining()
    obj_additional_remaining = create_remaining_list(courses_list, additional_remaining)
    #print(obj_additional_remaining)
    
    core_courses = curr_student.check_core()
    core_remaining = curr_student.get_core_remaining()
    obj_core_remaining = create_remaining_list(courses_list, core_remaining)
    #print(obj_core_remaining)
    
    major_electives = curr_student.check_major_electives()
        
    """""""""""""""""""""""""""""""""""""""
    PRINT FOREIGN LANGUAGE REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 22
    banner_list = banner["fl"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print foreign language requirements banner
    fl_requirement = curr_student.check_flanguage(curr_student)
    course_det_left(row+1, worksheet, bold_left)
       
    fl_list = fl_requirement.get("courses done")
    for i in range(0, len(fl_list)):
        fl_course = fl_list[i][0]
        #different format depending on the stile
        if fl_list[i] [1] == 0: 
            grade_format = color_cell3
        elif fl_list[i] [1] == 1:
            grade_format = border_center
        elif fl_list[i] [1] == 2:
            grade_format = color_cell4
        row = 24+i
        worksheet.write(row, 0, fl_course.course.get_name(), course_info_format) #col A=0
        worksheet.write(row, 1, fl_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, fl_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, fl_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(fl_course.get_grade()), grade_format)
        worksheet.write(row, 5, fl_course.course.get_credits(), course_info_format)
        
    lenght_left = row
    print(f"languages end at {lenght_left}")
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT SOCIAL SCIENCES REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  5
    banner_list = banner["sosc"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print social sciences banner
    sosc_req = curr_student.check_sosc(curr_student)
    course_det_right(row+1, worksheet, bold_left)

    sosc_list = sosc_req.get("courses done")
    for i in range(0, len(sosc_list)):
        sosc_course = sosc_list[i][0]
        course_grade = sosc_list[i][1]
        if course_grade == 0: #course failed
            grade_format = color_cell3
        elif course_grade == 1: #course passed
            grade_format = border_center
        elif course_grade == 2: #current course
            grade_format = color_cell4
            
        row = 7+i
        worksheet.write(row, 7, sosc_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 8, sosc_course.course.get_code(), course_info_format)
        worksheet.write(row, 9, sosc_course.course.get_number(), course_info_format)
        worksheet.write(row, 10, sosc_course.get_term(), course_info_format)
        worksheet.write(row, 11, number_to_letter.get(sosc_course.get_grade()), grade_format)
        worksheet.write(row, 12, sosc_course.course.get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT HUMANITIES REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 10
    banner_list = banner["hum"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print humanities banner
    hum_req = curr_student.check_hum(curr_student) 
    course_det_right(row+1, worksheet, bold_left)

    hum_list = hum_req.get("courses done")
    for i in range(0, len(hum_list)):
        hum_course = hum_list[i][0]
        course_grade = hum_list[i][1]
        if course_grade == 0: #course failed
            grade_format = color_cell3
        elif course_grade == 1: #course passed
            grade_format = border_center
        elif course_grade == 2: #current course
            grade_format = color_cell4
            
        row = 12+i
        worksheet.write(row, 7, hum_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 8, hum_course.course.get_code(), course_info_format)
        worksheet.write(row, 9, hum_course.course.get_number(), course_info_format)
        worksheet.write(row, 10, hum_course.get_term(), course_info_format)
        worksheet.write(row, 11, number_to_letter.get(hum_course.get_grade()), grade_format)
        worksheet.write(row, 12, hum_course.course.get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT FINE ARTS REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 15
    banner_list = banner["fa"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print fine arts banner
    fa_req = curr_student.check_arts(curr_student) 
    course_det_right(row+1, worksheet, bold_left)

    fa_list = fa_req.get("courses done")
    for i in range(0, len(fa_list)):
        fa_course = fa_list[i][0]
        course_grade = fa_list[i][1]
        if course_grade == 0: #course failed
            grade_format = color_cell3
        elif course_grade == 1: #course passed
            grade_format = border_center
        elif course_grade == 2: #current course
            grade_format = color_cell4

        row = 17+i
        worksheet.write(row, 7, fa_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 8, fa_course.course.get_code(), course_info_format)
        worksheet.write(row, 9, fa_course.course.get_number(), course_info_format)
        worksheet.write(row, 10, fa_course.get_term(), course_info_format)
        worksheet.write(row, 11, number_to_letter.get(fa_course.get_grade()), grade_format)
        worksheet.write(row, 12, fa_course.course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MA, SCI, COMP SCI REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  17
    banner_list = banner["sci"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print math, sci, comp sci banner
    sci_requirement = curr_student.check_sci(curr_student)
    course_det_left(row+1, worksheet, bold_left)


    #if len(sci_requirement.get("courses missing")) != 2:
    sci_list = sci_requirement.get("courses done")
    for i in range(0, len(sci_list)):
        sci_course = sci_list[i][0]
        course_grade = sci_list[i][1]
        #different format depending on the stile
        if course_grade == 0: #course failed
            grade_format = color_cell3
        elif course_grade == 1: #course passed
            grade_format = border_center
        elif course_grade == 2: #current course
            grade_format = color_cell4

        row = 19+i
        worksheet.write(row, 0, sci_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 1, sci_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, sci_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, sci_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(sci_course.get_grade()), grade_format)
        worksheet.write(row, 5, sci_course.course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT GENERAL ELECTIVES
    """""""""""""""""""""""""""""""""""""""
    row = 19
    banner_list = banner["genel"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print general electives courses
    genel_list = curr_student.check_genelectives()
    course_det_right(row+1, worksheet, bold_left)


    for i in range(0, len(genel_list)):
        genel_course = genel_list[i][0]
        course_grade = genel_list[i][1]
        #different format depending on the stile
        if course_grade == 0: 
            grade_format = color_cell3
        elif course_grade == 1:
            grade_format = border_center
        elif course_grade == 2:
            grade_format = color_cell4
            
        row = 21+i
        worksheet.write(row, 7, genel_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 8, genel_course.course.get_code(), course_info_format)
        worksheet.write(row, 9, genel_course.course.get_number(), course_info_format)
        worksheet.write(row, 10, genel_course.get_term(), course_info_format)
        worksheet.write(row, 11, number_to_letter.get(genel_course.get_grade()), grade_format)
        worksheet.write(row, 12, genel_course.course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    DECIDE WHAT LENGHT TO PRINT
    """""""""""""""""""""""""""""""""""""""
    lengt_first_part = 0
    #if (21+len(genel_list)) >= 26:
    if (21+len(genel_list)) >= (lenght_left+1):        
        lengt_first_part = len(genel_list)
    else:
        lengt_first_part = len(fl_list)+1
    
    """""""""""""""""""""""""""""""""""""""
    PRINT ADDITIONAL REQUIREMENTS
    """""""""""""""""""""""""""""""""""""""
    #row = 24+len(genel_list)
    row = 24+lengt_first_part
    banner_list = banner["B"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    #formats.short_merge_sx(row+1, banner_list[1], 0) #print additional courses
    course_det_left(row, worksheet, bold_left)

    #to print the courses that the student has done in this category
    additional_list = additional_requirements.get("courses done")
    for i in range(0, len(additional_list)):
        if additional_list[i][0] == "":
            row = 25+lengt_first_part+i
            if additional_list[i][0] == "":
                short_merge_sx(row, additional_list[i][2], 0,  worksheet, merge_format1, merge_format2)
            else:
                worksheet.write(row, 0, additional_list[i][2], course_info_format) 
            
        else:
            additional_course = additional_list[i][0]
            #different format depending on the stile
            course_grade = additional_list[i][1]
            if course_grade == 0: #course failed
                grade_format = color_cell3
            elif course_grade == 1: #course passed
                grade_format = border_center
            elif course_grade == 2: #current course
                grade_format = color_cell4
                
            #row = 25+len(genel_list)+i
            row = 25+lengt_first_part+i
            #worksheet.write(row, 0, additional_course.course.get_name(), course_info_format) #col A=0
            worksheet.write(row, 0, additional_list[i][2], course_info_format) #col A=0
            worksheet.write(row, 1, additional_course.course.get_code(), course_info_format)
            worksheet.write(row, 2, additional_course.course.get_number(), course_info_format)
            worksheet.write(row, 3, additional_course.get_term(), course_info_format)
            worksheet.write(row, 4, number_to_letter.get(additional_course.get_grade()), grade_format)
            worksheet.write(row, 5, additional_course.course.get_credits(), course_info_format)


    #to print the courses that the student has not done in this category (yet)
    for i in range(0, len(obj_additional_remaining)):
        additional_course = obj_additional_remaining[i]
        
        #instead of the check on grades I would put here a check on the pre-requisites to color the cell with the course name
        
        #row = 25+len(genel_list)+len(additional_list)+i
        row = 25+lengt_first_part+len(additional_list)+i
        worksheet.write(row, 0, additional_course.get_name(), course_info_format) #col A=0
        worksheet.write(row, 1, additional_course.get_code(), course_info_format)
        worksheet.write(row, 2, additional_course.get_number(), course_info_format)
        worksheet.write(row, 3, "", course_info_format)
        worksheet.write(row, 4, "", course_info_format)
        worksheet.write(row, 5, additional_course.get_credits(), course_info_format)
    
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT CORE COURSES
    """""""""""""""""""""""""""""""""""""""
    #row = 24+len(genel_list)
    row = 24+lengt_first_part
    banner_list = banner["C"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print core courses
    course_det_right(row+1, worksheet, bold_left)
    
    core_list = core_courses.get("courses done")
    for i in range(0, len(core_list)):
        
        if core_list[i][0] == "":
            row = 26+lengt_first_part+i
            if core_list[i][0] == "":
                short_merge_sx(row, core_list[i][2], 0,  worksheet, merge_format1, merge_format2)
            else:
                worksheet.write(row, 0, core_list[i][2], course_info_format) 
        else:
            core_course = core_list[i][0]
            course_grade = core_list[i][1]
            #different format depending on the stile
            if course_grade == 0: #failed
                grade_format = color_cell3
            elif course_grade == 1: #passed
                grade_format = border_center
            elif course_grade == 2: #current
                grade_format = color_cell4
            elif course_grade == 3: #highlights the grades that are not failed, but lower than C-
                grade_format = color_cell2
            
            #row = 26+len(genel_list)+i
            row = 26+lengt_first_part+i
            worksheet.write(row, 7, core_list[i][2], course_info_format) #col H=7
            worksheet.write(row, 8, core_course.course.get_code(), course_info_format)
            worksheet.write(row, 9, core_course.course.get_number(), course_info_format)
            worksheet.write(row, 10, core_course.get_term(), course_info_format)
            worksheet.write(row, 11, number_to_letter.get(core_course.get_grade()), grade_format)
            worksheet.write(row, 12, core_course.course.get_credits(), course_info_format)
        
    #to print the courses that the student has not done in this category 
    for i in range(0,len(obj_core_remaining)):
        core_course = obj_core_remaining[i]
        
        row = 26+lengt_first_part+len(core_list)+i

        worksheet.write(row, 7, core_list[i][2], course_info_format) #col H=7
        worksheet.write(row, 8, core_course.get_code(), course_info_format)
        worksheet.write(row, 9, core_course.get_number(), course_info_format)
        worksheet.write(row, 10, "", course_info_format)
        worksheet.write(row, 11, "", course_info_format)
        worksheet.write(row, 12, core_course.get_credits(), course_info_format)    
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MAJOR ELECTIVES
    """""""""""""""""""""""""""""""""""""""
    #set the row depending on the longest between core and additional requirements
    final_row = 0
    if (len(obj_core_remaining)+len(core_list)) >= (len(obj_additional_remaining)+len(additional_list)):
       final_row = (len(obj_core_remaining)+len(core_list))
    else:
        final_row = (len(obj_additional_remaining)+len(additional_list))
    #row = 30+lengt_first_part+len(core_list)+len(obj_core_remaining)
    
    row = 30 + lengt_first_part + final_row
    
    banner_list = banner["D"] 
    long_merge(row, banner_list[0], 1, worksheet, merge_format1, merge_format2) #prints "Major Electives"
    long_merge(row+1, curr_student.major.get_major_explanation(), 0, worksheet, merge_format1, merge_format2) #prints description
    course_det_left(row+1, worksheet, bold_left)

    electives_list = major_electives.get("courses done")
    for i in range(0, len(electives_list)):
        elective_course = electives_list[i][0]
        course_grade = electives_list[i][1]
        #different format depending on the stile
        if course_grade == 0: #failed
            grade_format = color_cell3
        elif course_grade == 1: #passed
            grade_format = border_center
        elif course_grade == 2: #current
            grade_format = color_cell4
            
        #row = 32+len(genel_list)+len(core_list)+i
        row = 32+lengt_first_part+len(core_list)+i
        worksheet.write(row, 0, elective_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 1, elective_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, elective_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, elective_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(elective_course.get_grade()), grade_format)
        worksheet.write(row, 5, elective_course.course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    CONSTRUCT THE LEGEND, GENERAL INFO, COURSES MISSING BY SECTION PART
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    #legend
    row = 4 
    banner_list = banner["G"] 
    legend_merge(row, banner_list[0], worksheet, merge_format1)
    legend_list = ["No more than two core courses with a grade below C-", "Grade requirement not satisfied", "Courses that the student is taking the current semester"]
    legend_structure(legend_list, "", row, worksheet, border_left)


    legend_format = [color_cell2, color_cell3, color_cell4]
    for i in range(0, len(legend_format)):
        position = int(row + i)
        worksheet.write(position, 15, "", legend_format[i])

    #general information
    row = row + 2 +  len(legend_list)
    banner_list = banner["H"] 
    legend_merge(row, banner_list[0], worksheet, merge_format1)
    worksheet.write(row, 15, "Total", bold_left)
    worksheet.write(row, 14, "", bold_left)
    info_list = ["Cumulative GPA", "Credits (earned)", "Current Standing", "Tentative Credits following semester", "Tentative Standing following semester", "Credits missing"]
    data_list = curr_student.create_info_list()
    row = row + 1
    legend_structure(info_list, data_list, row, worksheet, border_left)

    #courses missing by section
    row = row + len(legend_list) + len(info_list) - 1
    banner_list = banner["I"]
    legend_merge(row, banner_list[0], worksheet, merge_format1)
    worksheet.write(row, 15, "Total", bold_left)
    worksheet.write(row, 14, "", bold_left)
    #missing_list = ["Math Proficiency", "Math, Science, Computer Science", "Foreign Language", "Social Sciences", "Humanities", "Fine Arts", "Additional Requirements", "Core Courses", "Major Electives", "Minor 1", "Minor 2"]
    num_missing = curr_student.return_missing()
    row = row + 1
    legend_structure(legend_keys, num_missing, row, worksheet, border_left)

    #CLOSE THE PLANNER!
    workbook.close() 
    

    
#planner structure #2    
def core_courses(planner_name, curr_student, courses_list, banner_content, legend_keys):
    path = os.path.relpath(f"planners/{planner_name}.xlsx")

    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    
    worksheet.set_column(0, 5, 11)
    worksheet.set_column(7, 12, 11) 
    worksheet.set_column(14, 14, 44)    
    
    banner = banner_content
    
    
    """""""""""""""""""""""""""
    DEFINE FORMATS
    """""""""""""""""""""""
    font_size = workbook.add_format({'font_size': 10})

    bold_center = workbook.add_format({'font_size': 10, 'bold': True, 'border': 1, 'align': 'center'})
    bold_left = workbook.add_format({'font_size': 10, 'bold': True, 'border': 1})

    border_center = workbook.add_format({'font_size': 10, 'border': 1, 'align': 'center',})
    border_left = workbook.add_format({'font_size': 10, 'border': 1})

    #blue banner
    merge_format1 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 1,
        'border': 1,
        'align': 'center',
        'fg_color': '#BDD7EE'
        })

    #white banner
    merge_format2 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'text_wrap': True
        })

    #cell format for "Course not taken yet"
    color_cell1 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'fg_color': '#FFE699'
        })

    #cell format for "No more than two core courses can be passed with D"
    color_cell2 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'fg_color': '#F4B084'
        })

    #cell format for "Grade requirement not satisfied"
    color_cell3 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'fg_color': '#FF0000'
        })

    #cell format for "Courses that the student is taking the current semester"
    color_cell4 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'fg_color': '#C6E0B4'
        })
    
    
    course_info_format = border_left

    """""""""""""""""""""""""""""""""""""""
    START THE PRINT
    """""""""""""""""""""""""""""""""""""""
    #print student name, surname, and major
    row = 1
    column = 0
    student_name = curr_student.get_name() + " " + curr_student.get_surname()
    student_major = "Degree Planner for B.A. in " + curr_student.major.get_name()
    long_merge(row, student_major, 1) #major
    long_merge(row+1, student_name, 0)  #name and surname
    banner_list = banner["A"]
    long_merge(row+3, banner_list[0], 1)


    """""""""""""""""""""""""""""""""""""""
    PRINT ENGLISH COMP and LIT REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  5
    banner_list = banner["eng"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print english banner
    course_det_left(row+1, worksheet, bold_left)

    curr_student.generate_en_courses(courses_list)
    curr_student.substitute_courses_done()
    curr_student.check_eng_composition()
    eng_requirement = curr_student.check_eng_literature()
    en_list = eng_requirement.get("output courses")
    #eng_requirement = curr_student.check_eng_requirement()

    for i in range(0, len(en_list)):
        en_course = en_list[i]
        if en_course[1] == 1:
            grade_format = border_center
        elif en_course[1] == 2:
            grade_format = color_cell3
        elif en_course[1] == 3:
            grade_format = color_cell4
        row = 7+i
        worksheet.write(row, 0, en_course[0].course.get_name(), course_info_format) #col A=0
        worksheet.write(row, 1, en_course[0].course.get_code(), course_info_format)
        worksheet.write(row, 2, en_course[0].course.get_number(), course_info_format)
        worksheet.write(row, 3, en_course[0].get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(en_course[0].get_grade()), grade_format)
        worksheet.write(row, 5, en_course[0].course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MA REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  13
    banner_list = banner["math"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print math proficiency banner
    ma_requirement = curr_student.check_ma_req()
    course_det_left(row+1, worksheet, bold_left)
       
    m_list = ma_requirement.get("courses done")
    if len(m_list) != 0:
        ma_course = m_list[0][0]
        if m_list[0] [1] == 0:
            grade_format = color_cell3
        elif m_list[0] [1] == 1:
            grade_format = border_center
        elif m_list[0] [1] == 2:
            grade_format = color_cell4
            
        row = 15
        worksheet.write(row, 0, ma_course.course.get_name(), course_info_format) #col A=0
        worksheet.write(row, 1, ma_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, ma_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, ma_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(ma_course.get_grade()), grade_format)
        worksheet.write(row, 5, ma_course.course.get_credits(), course_info_format)

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    CHECK CORE COURSES AND GENERAL ELECTIVES
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""    
    core_courses = curr_student.check_core()
    core_remaining = curr_student.get_core_remaining()
    obj_core_remaining = create_remaining_list(courses_list, core_remaining)
    #print(obj_core_remaining)
    
    major_electives = curr_student.check_major_electives()
        
    """""""""""""""""""""""""""""""""""""""
    PRINT FOREIGN LANGUAGE REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 22
    banner_list = banner["fl"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print foreign language requirements banner
    fl_requirement = curr_student.check_flanguage(curr_student)
    course_det_left(row+1, worksheet, bold_left)
       
    fl_list = fl_requirement.get("courses done")
    for i in range(0, len(fl_list)):
        fl_course = fl_list[i][0]
        #different format depending on the stile
        if fl_list[i] [1] == 0: 
            grade_format = color_cell3
        elif fl_list[i] [1] == 1:
            grade_format = border_center
        elif fl_list[i] [1] == 2:
            grade_format = color_cell4
        row = 24+i
        worksheet.write(row, 0, fl_course.course.get_name(), course_info_format) #col A=0
        worksheet.write(row, 1, fl_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, fl_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, fl_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(fl_course.get_grade()), grade_format)
        worksheet.write(row, 5, fl_course.course.get_credits(), course_info_format)
        
    lenght_left = row
    print(f"languages end at {lenght_left}")
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT SOCIAL SCIENCES REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  5
    banner_list = banner["sosc"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print social sciences banner
    sosc_req = curr_student.check_sosc(curr_student)
    course_det_right(row+1, worksheet, bold_left)

    sosc_list = sosc_req.get("courses done")
    for i in range(0, len(sosc_list)):
        sosc_course = sosc_list[i][0]
        course_grade = sosc_list[i][1]
        if course_grade == 0: #course failed
            grade_format = color_cell3
        elif course_grade == 1: #course passed
            grade_format = border_center
        elif course_grade == 2: #current course
            grade_format = color_cell4
            
        row = 7+i
        worksheet.write(row, 7, sosc_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 8, sosc_course.course.get_code(), course_info_format)
        worksheet.write(row, 9, sosc_course.course.get_number(), course_info_format)
        worksheet.write(row, 10, sosc_course.get_term(), course_info_format)
        worksheet.write(row, 11, number_to_letter.get(sosc_course.get_grade()), grade_format)
        worksheet.write(row, 12, sosc_course.course.get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT HUMANITIES REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 10
    banner_list = banner["hum"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print humanities banner
    hum_req = curr_student.check_hum(curr_student) 
    course_det_right(row+1, worksheet, bold_left)

    hum_list = hum_req.get("courses done")
    for i in range(0, len(hum_list)):
        hum_course = hum_list[i][0]
        course_grade = hum_list[i][1]
        if course_grade == 0: #course failed
            grade_format = color_cell3
        elif course_grade == 1: #course passed
            grade_format = border_center
        elif course_grade == 2: #current course
            grade_format = color_cell4
            
        row = 12+i
        worksheet.write(row, 7, hum_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 8, hum_course.course.get_code(), course_info_format)
        worksheet.write(row, 9, hum_course.course.get_number(), course_info_format)
        worksheet.write(row, 10, hum_course.get_term(), course_info_format)
        worksheet.write(row, 11, number_to_letter.get(hum_course.get_grade()), grade_format)
        worksheet.write(row, 12, hum_course.course.get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT FINE ARTS REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 15
    banner_list = banner["fa"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print fine arts banner
    fa_req = curr_student.check_arts(curr_student) 
    course_det_right(row+1, worksheet, bold_left)

    fa_list = fa_req.get("courses done")
    for i in range(0, len(fa_list)):
        fa_course = fa_list[i][0]
        course_grade = fa_list[i][1]
        if course_grade == 0: #course failed
            grade_format = color_cell3
        elif course_grade == 1: #course passed
            grade_format = border_center
        elif course_grade == 2: #current course
            grade_format = color_cell4

        row = 17+i
        worksheet.write(row, 7, fa_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 8, fa_course.course.get_code(), course_info_format)
        worksheet.write(row, 9, fa_course.course.get_number(), course_info_format)
        worksheet.write(row, 10, fa_course.get_term(), course_info_format)
        worksheet.write(row, 11, number_to_letter.get(fa_course.get_grade()), grade_format)
        worksheet.write(row, 12, fa_course.course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MA, SCI, COMP SCI REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  17
    banner_list = banner["sci"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print math, sci, comp sci banner
    sci_requirement = curr_student.check_sci(curr_student)
    course_det_left(row+1, worksheet, bold_left)


    #if len(sci_requirement.get("courses missing")) != 2:
    sci_list = sci_requirement.get("courses done")
    for i in range(0, len(sci_list)):
        sci_course = sci_list[i][0]
        course_grade = sci_list[i][1]
        #different format depending on the stile
        if course_grade == 0: #course failed
            grade_format = color_cell3
        elif course_grade == 1: #course passed
            grade_format = border_center
        elif course_grade == 2: #current course
            grade_format = color_cell4

        row = 19+i
        worksheet.write(row, 0, sci_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 1, sci_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, sci_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, sci_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(sci_course.get_grade()), grade_format)
        worksheet.write(row, 5, sci_course.course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT GENERAL ELECTIVES
    """""""""""""""""""""""""""""""""""""""
    row = 19
    banner_list = banner["genel"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print general electives courses
    genel_list = curr_student.check_genelectives()
    course_det_right(row+1, worksheet, bold_left)


    for i in range(0, len(genel_list)):
        genel_course = genel_list[i][0]
        course_grade = genel_list[i][1]
        #different format depending on the stile
        if course_grade == 0: 
            grade_format = color_cell3
        elif course_grade == 1:
            grade_format = border_center
        elif course_grade == 2:
            grade_format = color_cell4
            
        row = 21+i
        worksheet.write(row, 7, genel_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 8, genel_course.course.get_code(), course_info_format)
        worksheet.write(row, 9, genel_course.course.get_number(), course_info_format)
        worksheet.write(row, 10, genel_course.get_term(), course_info_format)
        worksheet.write(row, 11, number_to_letter.get(genel_course.get_grade()), grade_format)
        worksheet.write(row, 12, genel_course.course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    DECIDE WHAT LENGHT TO PRINT
    """""""""""""""""""""""""""""""""""""""
    lengt_first_part = 0
    #if (21+len(genel_list)) >= 26:
    if (21+len(genel_list)) >= (lenght_left+1):        
        lengt_first_part = len(genel_list)
    else:
        lengt_first_part = len(fl_list)+1 
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT CORE COURSES
    """""""""""""""""""""""""""""""""""""""
    #row = 24+len(genel_list)
    row = 24+lengt_first_part
    banner_list = banner["B"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print core courses
    course_det_right(row+1, worksheet, bold_left)
    
    core_list = core_courses.get("courses done")
    for i in range(0, len(core_list)):
        
        if core_list[i][0] == "":
            row = 26+lengt_first_part+i
            if core_list[i][0] == "":
                short_merge_sx(row, core_list[i][2], 0,  worksheet, merge_format1, merge_format2)
            else:
                worksheet.write(row, 0, core_list[i][2], course_info_format) 
        else:
            core_course = core_list[i][0]
            course_grade = core_list[i][1]
            #different format depending on the stile
            if course_grade == 0: #failed
                grade_format = color_cell3
            elif course_grade == 1: #passed
                grade_format = border_center
            elif course_grade == 2: #current
                grade_format = color_cell4
            elif course_grade == 3: #highlights the grades that are not failed, but lower than C-
                grade_format = color_cell2
            
            #row = 26+len(genel_list)+i
            row = 26+lengt_first_part+i
            worksheet.write(row, 0, core_list[i][2], course_info_format) #col H=7
            worksheet.write(row, 1, core_course.course.get_code(), course_info_format)
            worksheet.write(row, 2, core_course.course.get_number(), course_info_format)
            worksheet.write(row, 3, core_course.get_term(), course_info_format)
            worksheet.write(row, 4, number_to_letter.get(core_course.get_grade()), grade_format)
            worksheet.write(row, 5, core_course.course.get_credits(), course_info_format)
        
    #to print the courses that the student has not done in this category 
    for i in range(0,len(obj_core_remaining)):
        core_course = obj_core_remaining[i]
        
        row = 26+lengt_first_part+len(core_list)+i

        worksheet.write(row, 0, core_list[i][2], course_info_format) #col H=7
        worksheet.write(row, 1, core_course.get_code(), course_info_format)
        worksheet.write(row, 2, core_course.get_number(), course_info_format)
        worksheet.write(row, 3, "", course_info_format)
        worksheet.write(row, 4, "", course_info_format)
        worksheet.write(row, 5, core_course.get_credits(), course_info_format)    
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MAJOR ELECTIVES
    """""""""""""""""""""""""""""""""""""""
    #set the row depending on the longest between core and additional requirements
    
    row = 30 + lengt_first_part + (len(obj_core_remaining)+len(core_list))
    
    banner_list = banner["C"] 
    long_merge(row, banner_list[0], 1, worksheet, merge_format1, merge_format2) #prints "Major Electives"
    long_merge(row+1, curr_student.major.get_major_explanation(), 0, worksheet, merge_format1, merge_format2) #prints description
    course_det_left(row+1, worksheet, bold_left)

    electives_list = major_electives.get("courses done")
    for i in range(0, len(electives_list)):
        elective_course = electives_list[i][0]
        course_grade = electives_list[i][1]
        #different format depending on the stile
        if course_grade == 0: #failed
            grade_format = color_cell3
        elif course_grade == 1: #passed
            grade_format = border_center
        elif course_grade == 2: #current
            grade_format = color_cell4
            
        #row = 32+len(genel_list)+len(core_list)+i
        row = 32+lengt_first_part+len(core_list)+i
        worksheet.write(row, 0, elective_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 1, elective_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, elective_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, elective_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(elective_course.get_grade()), grade_format)
        worksheet.write(row, 5, elective_course.course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    CONSTRUCT THE LEGEND, GENERAL INFO, COURSES MISSING BY SECTION PART
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    #legend
    row = 4 
    banner_list = banner["G"] 
    legend_merge(row, banner_list[0], worksheet, merge_format1)
    legend_list = ["No more than two core courses with a grade below C-", "Grade requirement not satisfied", "Courses that the student is taking the current semester"]
    legend_structure(legend_list, "", row, worksheet, border_left)


    legend_format = [color_cell2, color_cell3, color_cell4]
    for i in range(0, len(legend_format)):
        position = int(row + i)
        worksheet.write(position, 15, "", legend_format[i])

    #general information
    row = row + 2 +  len(legend_list)
    banner_list = banner["H"] 
    legend_merge(row, banner_list[0], worksheet, merge_format1)
    worksheet.write(row, 15, "Total", bold_left)
    worksheet.write(row, 14, "", bold_left)
    info_list = ["Cumulative GPA", "Credits (earned)", "Current Standing", "Tentative Credits following semester", "Tentative Standing following semester", "Credits missing"]
    data_list = curr_student.create_info_list()
    row = row + 1
    legend_structure(info_list, data_list, row, worksheet, border_left)

    #courses missing by section
    row = row + len(legend_list) + len(info_list) - 1
    banner_list = banner["I"]
    legend_merge(row, banner_list[0], worksheet, merge_format1)
    worksheet.write(row, 15, "Total", bold_left)
    worksheet.write(row, 14, "", bold_left)
    #missing_list = ["Math Proficiency", "Math, Science, Computer Science", "Foreign Language", "Social Sciences", "Humanities", "Fine Arts", "Core Courses", "Major Electives", "Minor 1", "Minor 2"]
    num_missing = curr_student.return_missing()
    row = row + 1
    legend_structure(legend_keys, num_missing, row, worksheet, border_left)
    
    #CLOSE THE PLANNER!
    workbook.close() 
    
    
    
#planner structure #3    
def core_tracks(planner_name, curr_student, courses_list, banner_content, legend_keys):
    path = os.path.relpath(f"planners/{planner_name}.xlsx")

    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    
    worksheet.set_column(0, 5, 11)
    worksheet.set_column(7, 12, 11) 
    worksheet.set_column(14, 14, 44)
    
    banner = banner_content
    
    """""""""""""""""""""""""""
    DEFINE FORMATS
    """""""""""""""""""""""
    font_size = workbook.add_format({'font_size': 10})

    bold_center = workbook.add_format({'font_size': 10, 'bold': True, 'border': 1, 'align': 'center'})
    bold_left = workbook.add_format({'font_size': 10, 'bold': True, 'border': 1})

    border_center = workbook.add_format({'font_size': 10, 'border': 1, 'align': 'center',})
    border_left = workbook.add_format({'font_size': 10, 'border': 1})

    #blue banner
    merge_format1 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 1,
        'border': 1,
        'align': 'center',
        'fg_color': '#BDD7EE'
        })

    #white banner
    merge_format2 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'text_wrap': True
        })

    #cell format for "Course not taken yet"
    color_cell1 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'fg_color': '#FFE699'
        })

    #cell format for "No more than two core courses can be passed with D"
    color_cell2 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'fg_color': '#F4B084'
        })

    #cell format for "Grade requirement not satisfied"
    color_cell3 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'fg_color': '#FF0000'
        })

    #cell format for "Courses that the student is taking the current semester"
    color_cell4 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'fg_color': '#C6E0B4'
        })
    
    course_info_format = border_left

    """""""""""""""""""""""""""""""""""""""
    START THE PRINT
    """""""""""""""""""""""""""""""""""""""
    #print student name, surname, and major
    row = 1
    column = 0
    student_name = curr_student.get_name() + " " + curr_student.get_surname()
    student_major = "Degree Planner for B.A. in " + curr_student.major.get_name()
    long_merge(row, student_major, 1) #major
    long_merge(row+1, student_name, 0)  #name and surname
    banner_list = banner["A"]
    long_merge(row+3, banner_list[0], 1)


    """""""""""""""""""""""""""""""""""""""
    PRINT ENGLISH COMP and LIT REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  5
    banner_list = banner["eng"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print english banner
    course_det_left(row+1, worksheet, bold_left)

    curr_student.generate_en_courses(courses_list)
    curr_student.substitute_courses_done()
    curr_student.check_eng_composition()
    eng_requirement = curr_student.check_eng_literature()
    en_list = eng_requirement.get("output courses")
    #eng_requirement = curr_student.check_eng_requirement()

    for i in range(0, len(en_list)):
        en_course = en_list[i]
        if en_course[1] == 1:
            grade_format = border_center
        elif en_course[1] == 2:
            grade_format = color_cell3
        elif en_course[1] == 3:
            grade_format = color_cell4
        row = 7+i
        worksheet.write(row, 0, en_course[0].course.get_name(), course_info_format) #col A=0
        worksheet.write(row, 1, en_course[0].course.get_code(), course_info_format)
        worksheet.write(row, 2, en_course[0].course.get_number(), course_info_format)
        worksheet.write(row, 3, en_course[0].get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(en_course[0].get_grade()), grade_format)
        worksheet.write(row, 5, en_course[0].course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MA REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  13
    banner_list = banner["math"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print math proficiency banner
    ma_requirement = curr_student.check_ma_req()
    course_det_left(row+1, worksheet, bold_left)
       
    m_list = ma_requirement.get("courses done")
    if len(m_list) != 0:
        ma_course = m_list[0][0]
        if m_list[0] [1] == 0:
            grade_format = color_cell3
        elif m_list[0] [1] == 1:
            grade_format = border_center
        elif m_list[0] [1] == 2:
            grade_format = color_cell4
            
        row = 15
        worksheet.write(row, 0, ma_course.course.get_name(), course_info_format) #col A=0
        worksheet.write(row, 1, ma_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, ma_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, ma_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(ma_course.get_grade()), grade_format)
        worksheet.write(row, 5, ma_course.course.get_credits(), course_info_format)

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    CHECK CORE COURSES AND GENERAL ELECTIVES
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""    
    core_courses = curr_student.check_core()
    core_remaining = curr_student.get_core_remaining()
    obj_core_remaining = create_remaining_list(courses_list, core_remaining)
    #print(obj_core_remaining)
    
    major_electives = curr_student.check_major_electives()
        
    """""""""""""""""""""""""""""""""""""""
    PRINT FOREIGN LANGUAGE REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 22
    banner_list = banner["fl"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print foreign language requirements banner
    fl_requirement = curr_student.check_flanguage(curr_student)
    course_det_left(row+1, worksheet, bold_left)
       
    fl_list = fl_requirement.get("courses done")
    for i in range(0, len(fl_list)):
        fl_course = fl_list[i][0]
        #different format depending on the stile
        if fl_list[i] [1] == 0: 
            grade_format = color_cell3
        elif fl_list[i] [1] == 1:
            grade_format = border_center
        elif fl_list[i] [1] == 2:
            grade_format = color_cell4
        row = 24+i
        worksheet.write(row, 0, fl_course.course.get_name(), course_info_format) #col A=0
        worksheet.write(row, 1, fl_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, fl_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, fl_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(fl_course.get_grade()), grade_format)
        worksheet.write(row, 5, fl_course.course.get_credits(), course_info_format)
        
    lenght_left = row
    print(f"languages end at {lenght_left}")
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT SOCIAL SCIENCES REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  5
    banner_list = banner["sosc"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print social sciences banner
    sosc_req = curr_student.check_sosc(curr_student)
    course_det_right(row+1, worksheet, bold_left)

    sosc_list = sosc_req.get("courses done")
    for i in range(0, len(sosc_list)):
        sosc_course = sosc_list[i][0]
        course_grade = sosc_list[i][1]
        if course_grade == 0: #course failed
            grade_format = color_cell3
        elif course_grade == 1: #course passed
            grade_format = border_center
        elif course_grade == 2: #current course
            grade_format = color_cell4
            
        row = 7+i
        worksheet.write(row, 7, sosc_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 8, sosc_course.course.get_code(), course_info_format)
        worksheet.write(row, 9, sosc_course.course.get_number(), course_info_format)
        worksheet.write(row, 10, sosc_course.get_term(), course_info_format)
        worksheet.write(row, 11, number_to_letter.get(sosc_course.get_grade()), grade_format)
        worksheet.write(row, 12, sosc_course.course.get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT HUMANITIES REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 10
    banner_list = banner["hum"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print humanities banner
    hum_req = curr_student.check_hum(curr_student) 
    course_det_right(row+1, worksheet, bold_left)

    hum_list = hum_req.get("courses done")
    for i in range(0, len(hum_list)):
        hum_course = hum_list[i][0]
        course_grade = hum_list[i][1]
        if course_grade == 0: #course failed
            grade_format = color_cell3
        elif course_grade == 1: #course passed
            grade_format = border_center
        elif course_grade == 2: #current course
            grade_format = color_cell4
            
        row = 12+i
        worksheet.write(row, 7, hum_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 8, hum_course.course.get_code(), course_info_format)
        worksheet.write(row, 9, hum_course.course.get_number(), course_info_format)
        worksheet.write(row, 10, hum_course.get_term(), course_info_format)
        worksheet.write(row, 11, number_to_letter.get(hum_course.get_grade()), grade_format)
        worksheet.write(row, 12, hum_course.course.get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT FINE ARTS REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 15
    banner_list = banner["fa"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print fine arts banner
    fa_req = curr_student.check_arts(curr_student) 
    course_det_right(row+1, worksheet, bold_left)

    fa_list = fa_req.get("courses done")
    for i in range(0, len(fa_list)):
        fa_course = fa_list[i][0]
        course_grade = fa_list[i][1]
        if course_grade == 0: #course failed
            grade_format = color_cell3
        elif course_grade == 1: #course passed
            grade_format = border_center
        elif course_grade == 2: #current course
            grade_format = color_cell4

        row = 17+i
        worksheet.write(row, 7, fa_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 8, fa_course.course.get_code(), course_info_format)
        worksheet.write(row, 9, fa_course.course.get_number(), course_info_format)
        worksheet.write(row, 10, fa_course.get_term(), course_info_format)
        worksheet.write(row, 11, number_to_letter.get(fa_course.get_grade()), grade_format)
        worksheet.write(row, 12, fa_course.course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MA, SCI, COMP SCI REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  17
    banner_list = banner["sci"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print math, sci, comp sci banner
    sci_requirement = curr_student.check_sci(curr_student)
    course_det_left(row+1, worksheet, bold_left)


    #if len(sci_requirement.get("courses missing")) != 2:
    sci_list = sci_requirement.get("courses done")
    for i in range(0, len(sci_list)):
        sci_course = sci_list[i][0]
        course_grade = sci_list[i][1]
        #different format depending on the stile
        if course_grade == 0: #course failed
            grade_format = color_cell3
        elif course_grade == 1: #course passed
            grade_format = border_center
        elif course_grade == 2: #current course
            grade_format = color_cell4

        row = 19+i
        worksheet.write(row, 0, sci_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 1, sci_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, sci_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, sci_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(sci_course.get_grade()), grade_format)
        worksheet.write(row, 5, sci_course.course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT GENERAL ELECTIVES
    """""""""""""""""""""""""""""""""""""""
    row = 19
    banner_list = banner["genel"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print general electives courses
    genel_list = curr_student.check_genelectives()
    course_det_right(row+1, worksheet, bold_left)


    for i in range(0, len(genel_list)):
        genel_course = genel_list[i][0]
        course_grade = genel_list[i][1]
        #different format depending on the stile
        if course_grade == 0: 
            grade_format = color_cell3
        elif course_grade == 1:
            grade_format = border_center
        elif course_grade == 2:
            grade_format = color_cell4
            
        row = 21+i
        worksheet.write(row, 7, genel_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 8, genel_course.course.get_code(), course_info_format)
        worksheet.write(row, 9, genel_course.course.get_number(), course_info_format)
        worksheet.write(row, 10, genel_course.get_term(), course_info_format)
        worksheet.write(row, 11, number_to_letter.get(genel_course.get_grade()), grade_format)
        worksheet.write(row, 12, genel_course.course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    DECIDE WHAT LENGHT TO PRINT
    """""""""""""""""""""""""""""""""""""""
    lengt_first_part = 0
    #if (21+len(genel_list)) >= 26:
    if (21+len(genel_list)) >= (lenght_left+1):        
        lengt_first_part = len(genel_list)
    else:
        lengt_first_part = len(fl_list)+1 
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT CORE COURSES
    """""""""""""""""""""""""""""""""""""""
    #row = 24+len(genel_list)
    row = 24+lengt_first_part
    banner_list = banner["B"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print core courses
    course_det_right(row+1, worksheet, bold_left)
    
    core_list = core_courses.get("courses done")
    for i in range(0, len(core_list)):
        
        if core_list[i][0] == "":
            row = 26+lengt_first_part+i
            if core_list[i][0] == "":
                short_merge_sx(row, core_list[i][2], 0,  worksheet, merge_format1, merge_format2)
            else:
                worksheet.write(row, 0, core_list[i][2], course_info_format) 
        else:
            core_course = core_list[i][0]
            course_grade = core_list[i][1]
            #different format depending on the stile
            if course_grade == 0: #failed
                grade_format = color_cell3
            elif course_grade == 1: #passed
                grade_format = border_center
            elif course_grade == 2: #current
                grade_format = color_cell4
            elif course_grade == 3: #highlights the grades that are not failed, but lower than C-
                grade_format = color_cell2
            
            #row = 26+len(genel_list)+i
            row = 26+lengt_first_part+i
            worksheet.write(row, 0, core_list[i][2], course_info_format) #col H=7
            worksheet.write(row, 1, core_course.course.get_code(), course_info_format)
            worksheet.write(row, 2, core_course.course.get_number(), course_info_format)
            worksheet.write(row, 3, core_course.get_term(), course_info_format)
            worksheet.write(row, 4, number_to_letter.get(core_course.get_grade()), grade_format)
            worksheet.write(row, 5, core_course.course.get_credits(), course_info_format)
        
    #to print the courses that the student has not done in this category 
    for i in range(0,len(obj_core_remaining)):
        core_course = obj_core_remaining[i]
        
        row = 26+lengt_first_part+len(core_list)+i

        worksheet.write(row, 0, core_list[i][2], course_info_format) #col H=7
        worksheet.write(row, 1, core_course.get_code(), course_info_format)
        worksheet.write(row, 2, core_course.get_number(), course_info_format)
        worksheet.write(row, 3, "", course_info_format)
        worksheet.write(row, 4, "", course_info_format)
        worksheet.write(row, 5, core_course.get_credits(), course_info_format)    
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MAJOR ELECTIVES
    """""""""""""""""""""""""""""""""""""""
    #set the row depending on the longest between core and additional requirements
    
    row = 30 + lengt_first_part + (len(obj_core_remaining)+len(core_list))
    
    banner_list = banner["C"] 
    long_merge(row, banner_list[0], 1, worksheet, merge_format1, merge_format2) #prints "Major Electives"
    long_merge(row+1, curr_student.major.get_major_explanation(), 0, worksheet, merge_format1, merge_format2) #prints description
    course_det_left(row+1, worksheet, bold_left)

    electives_list = major_electives.get("courses done")
    for i in range(0, len(electives_list)):
        elective_course = electives_list[i][0]
        course_grade = electives_list[i][1]
        #different format depending on the stile
        if course_grade == 0: #failed
            grade_format = color_cell3
        elif course_grade == 1: #passed
            grade_format = border_center
        elif course_grade == 2: #current
            grade_format = color_cell4
            
        #row = 32+len(genel_list)+len(core_list)+i
        row = 32+lengt_first_part+len(core_list)+i
        worksheet.write(row, 0, elective_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 1, elective_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, elective_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, elective_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(elective_course.get_grade()), grade_format)
        worksheet.write(row, 5, elective_course.course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    CONSTRUCT THE LEGEND, GENERAL INFO, COURSES MISSING BY SECTION PART
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    #legend
    row = 4 
    banner_list = banner["G"] 
    legend_merge(row, banner_list[0], worksheet, merge_format1)
    legend_list = ["No more than two core courses with a grade below C-", "Grade requirement not satisfied", "Courses that the student is taking the current semester"]
    legend_structure(legend_list, "", row, worksheet, border_left)


    legend_format = [color_cell2, color_cell3, color_cell4]
    for i in range(0, len(legend_format)):
        position = int(row + i)
        worksheet.write(position, 15, "", legend_format[i])

    #general information
    row = row + 2 +  len(legend_list)
    banner_list = banner["H"] 
    legend_merge(row, banner_list[0], worksheet, merge_format1)
    worksheet.write(row, 15, "Total", bold_left)
    worksheet.write(row, 14, "", bold_left)
    info_list = ["Cumulative GPA", "Credits (earned)", "Current Standing", "Tentative Credits following semester", "Tentative Standing following semester", "Credits missing"]
    data_list = curr_student.create_info_list()
    row = row + 1
    legend_structure(info_list, data_list, row, worksheet, border_left)

    #courses missing by section
    row = row + len(legend_list) + len(info_list) - 1
    banner_list = banner["I"]
    legend_merge(row, banner_list[0], worksheet, merge_format1)
    worksheet.write(row, 15, "Total", bold_left)
    worksheet.write(row, 14, "", bold_left)
    #missing_list = ["Math Proficiency", "Math, Science, Computer Science", "Foreign Language", "Social Sciences", "Humanities", "Fine Arts", "Core Courses", "Major Electives", "Minor 1", "Minor 2"]
    num_missing = curr_student.return_missing()
    row = row + 1
    legend_structure(legend_keys, num_missing, row, worksheet, border_left)
    
    #CLOSE THE PLANNER!
    workbook.close() 


#planner structure #4 
def electives_tracks(planner_name, curr_student, courses_list, banner_content, legend_keys):
    path = os.path.relpath(f"planners/{planner_name}.xlsx")

    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    
    worksheet.set_column(0, 5, 11)
    worksheet.set_column(7, 12, 11) 
    worksheet.set_column(14, 14, 44)
    
    banner = banner_content
    
    """""""""""""""""""""""""""
    DEFINE FORMATS
    """""""""""""""""""""""
    font_size = workbook.add_format({'font_size': 10})

    bold_center = workbook.add_format({'font_size': 10, 'bold': True, 'border': 1, 'align': 'center'})
    bold_left = workbook.add_format({'font_size': 10, 'bold': True, 'border': 1})

    border_center = workbook.add_format({'font_size': 10, 'border': 1, 'align': 'center',})
    border_left = workbook.add_format({'font_size': 10, 'border': 1})

    #blue banner
    merge_format1 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 1,
        'border': 1,
        'align': 'center',
        'fg_color': '#BDD7EE'
        })

    #white banner
    merge_format2 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'text_wrap': True
        })

    #cell format for "Course not taken yet"
    color_cell1 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'fg_color': '#FFE699'
        })

    #cell format for "No more than two core courses can be passed with D"
    color_cell2 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'fg_color': '#F4B084'
        })

    #cell format for "Grade requirement not satisfied"
    color_cell3 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'fg_color': '#FF0000'
        })

    #cell format for "Courses that the student is taking the current semester"
    color_cell4 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'fg_color': '#C6E0B4'
        })
    
    course_info_format = border_left

    """""""""""""""""""""""""""""""""""""""
    START THE PRINT
    """""""""""""""""""""""""""""""""""""""
    #print student name, surname, and major
    row = 1
    column = 0
    student_name = curr_student.get_name() + " " + curr_student.get_surname()
    student_major = "Degree Planner for B.A. in " + curr_student.major.get_name()
    long_merge(row, student_major, 1) #major
    long_merge(row+1, student_name, 0)  #name and surname
    banner_list = banner["A"]
    long_merge(row+3, banner_list[0], 1)


    """""""""""""""""""""""""""""""""""""""
    PRINT ENGLISH COMP and LIT REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  5
    banner_list = banner["eng"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print english banner
    course_det_left(row+1, worksheet, bold_left)

    curr_student.generate_en_courses(courses_list)
    curr_student.substitute_courses_done()
    curr_student.check_eng_composition()
    eng_requirement = curr_student.check_eng_literature()
    en_list = eng_requirement.get("output courses")
    #eng_requirement = curr_student.check_eng_requirement()

    for i in range(0, len(en_list)):
        en_course = en_list[i]
        if en_course[1] == 1:
            grade_format = border_center
        elif en_course[1] == 2:
            grade_format = color_cell3
        elif en_course[1] == 3:
            grade_format = color_cell4
        row = 7+i
        worksheet.write(row, 0, en_course[0].course.get_name(), course_info_format) #col A=0
        worksheet.write(row, 1, en_course[0].course.get_code(), course_info_format)
        worksheet.write(row, 2, en_course[0].course.get_number(), course_info_format)
        worksheet.write(row, 3, en_course[0].get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(en_course[0].get_grade()), grade_format)
        worksheet.write(row, 5, en_course[0].course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MA REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  13
    banner_list = banner["math"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print math proficiency banner
    ma_requirement = curr_student.check_ma_req()
    course_det_left(row+1, worksheet, bold_left)
       
    m_list = ma_requirement.get("courses done")
    if len(m_list) != 0:
        ma_course = m_list[0][0]
        if m_list[0] [1] == 0:
            grade_format = color_cell3
        elif m_list[0] [1] == 1:
            grade_format = border_center
        elif m_list[0] [1] == 2:
            grade_format = color_cell4
            
        row = 15
        worksheet.write(row, 0, ma_course.course.get_name(), course_info_format) #col A=0
        worksheet.write(row, 1, ma_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, ma_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, ma_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(ma_course.get_grade()), grade_format)
        worksheet.write(row, 5, ma_course.course.get_credits(), course_info_format)

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    CHECK CORE COURSES AND GENERAL ELECTIVES
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""    
    core_courses = curr_student.check_core()
    core_remaining = curr_student.get_core_remaining()
    obj_core_remaining = create_remaining_list(courses_list, core_remaining)
    #print(obj_core_remaining)
    
    major_electives = curr_student.check_major_electives()
        
    """""""""""""""""""""""""""""""""""""""
    PRINT FOREIGN LANGUAGE REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 22
    banner_list = banner["fl"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print foreign language requirements banner
    fl_requirement = curr_student.check_flanguage(curr_student)
    course_det_left(row+1, worksheet, bold_left)
       
    fl_list = fl_requirement.get("courses done")
    for i in range(0, len(fl_list)):
        fl_course = fl_list[i][0]
        #different format depending on the stile
        if fl_list[i] [1] == 0: 
            grade_format = color_cell3
        elif fl_list[i] [1] == 1:
            grade_format = border_center
        elif fl_list[i] [1] == 2:
            grade_format = color_cell4
        row = 24+i
        worksheet.write(row, 0, fl_course.course.get_name(), course_info_format) #col A=0
        worksheet.write(row, 1, fl_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, fl_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, fl_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(fl_course.get_grade()), grade_format)
        worksheet.write(row, 5, fl_course.course.get_credits(), course_info_format)
        
    lenght_left = row
    print(f"languages end at {lenght_left}")
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT SOCIAL SCIENCES REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  5
    banner_list = banner["sosc"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print social sciences banner
    sosc_req = curr_student.check_sosc(curr_student)
    course_det_right(row+1, worksheet, bold_left)

    sosc_list = sosc_req.get("courses done")
    for i in range(0, len(sosc_list)):
        sosc_course = sosc_list[i][0]
        course_grade = sosc_list[i][1]
        if course_grade == 0: #course failed
            grade_format = color_cell3
        elif course_grade == 1: #course passed
            grade_format = border_center
        elif course_grade == 2: #current course
            grade_format = color_cell4
            
        row = 7+i
        worksheet.write(row, 7, sosc_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 8, sosc_course.course.get_code(), course_info_format)
        worksheet.write(row, 9, sosc_course.course.get_number(), course_info_format)
        worksheet.write(row, 10, sosc_course.get_term(), course_info_format)
        worksheet.write(row, 11, number_to_letter.get(sosc_course.get_grade()), grade_format)
        worksheet.write(row, 12, sosc_course.course.get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT HUMANITIES REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 10
    banner_list = banner["hum"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print humanities banner
    hum_req = curr_student.check_hum(curr_student) 
    course_det_right(row+1, worksheet, bold_left)

    hum_list = hum_req.get("courses done")
    for i in range(0, len(hum_list)):
        hum_course = hum_list[i][0]
        course_grade = hum_list[i][1]
        if course_grade == 0: #course failed
            grade_format = color_cell3
        elif course_grade == 1: #course passed
            grade_format = border_center
        elif course_grade == 2: #current course
            grade_format = color_cell4
            
        row = 12+i
        worksheet.write(row, 7, hum_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 8, hum_course.course.get_code(), course_info_format)
        worksheet.write(row, 9, hum_course.course.get_number(), course_info_format)
        worksheet.write(row, 10, hum_course.get_term(), course_info_format)
        worksheet.write(row, 11, number_to_letter.get(hum_course.get_grade()), grade_format)
        worksheet.write(row, 12, hum_course.course.get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT FINE ARTS REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 15
    banner_list = banner["fa"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print fine arts banner
    fa_req = curr_student.check_arts(curr_student) 
    course_det_right(row+1, worksheet, bold_left)

    fa_list = fa_req.get("courses done")
    for i in range(0, len(fa_list)):
        fa_course = fa_list[i][0]
        course_grade = fa_list[i][1]
        if course_grade == 0: #course failed
            grade_format = color_cell3
        elif course_grade == 1: #course passed
            grade_format = border_center
        elif course_grade == 2: #current course
            grade_format = color_cell4

        row = 17+i
        worksheet.write(row, 7, fa_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 8, fa_course.course.get_code(), course_info_format)
        worksheet.write(row, 9, fa_course.course.get_number(), course_info_format)
        worksheet.write(row, 10, fa_course.get_term(), course_info_format)
        worksheet.write(row, 11, number_to_letter.get(fa_course.get_grade()), grade_format)
        worksheet.write(row, 12, fa_course.course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MA, SCI, COMP SCI REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  17
    banner_list = banner["sci"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print math, sci, comp sci banner
    sci_requirement = curr_student.check_sci(curr_student)
    course_det_left(row+1, worksheet, bold_left)


    #if len(sci_requirement.get("courses missing")) != 2:
    sci_list = sci_requirement.get("courses done")
    for i in range(0, len(sci_list)):
        sci_course = sci_list[i][0]
        course_grade = sci_list[i][1]
        #different format depending on the stile
        if course_grade == 0: #course failed
            grade_format = color_cell3
        elif course_grade == 1: #course passed
            grade_format = border_center
        elif course_grade == 2: #current course
            grade_format = color_cell4

        row = 19+i
        worksheet.write(row, 0, sci_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 1, sci_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, sci_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, sci_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(sci_course.get_grade()), grade_format)
        worksheet.write(row, 5, sci_course.course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT GENERAL ELECTIVES
    """""""""""""""""""""""""""""""""""""""
    row = 19
    banner_list = banner["genel"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print general electives courses
    genel_list = curr_student.check_genelectives()
    course_det_right(row+1, worksheet, bold_left)


    for i in range(0, len(genel_list)):
        genel_course = genel_list[i][0]
        course_grade = genel_list[i][1]
        #different format depending on the stile
        if course_grade == 0: 
            grade_format = color_cell3
        elif course_grade == 1:
            grade_format = border_center
        elif course_grade == 2:
            grade_format = color_cell4
            
        row = 21+i
        worksheet.write(row, 7, genel_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 8, genel_course.course.get_code(), course_info_format)
        worksheet.write(row, 9, genel_course.course.get_number(), course_info_format)
        worksheet.write(row, 10, genel_course.get_term(), course_info_format)
        worksheet.write(row, 11, number_to_letter.get(genel_course.get_grade()), grade_format)
        worksheet.write(row, 12, genel_course.course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    DECIDE WHAT LENGHT TO PRINT
    """""""""""""""""""""""""""""""""""""""
    lengt_first_part = 0
    #if (21+len(genel_list)) >= 26:
    if (21+len(genel_list)) >= (lenght_left+1):        
        lengt_first_part = len(genel_list)
    else:
        lengt_first_part = len(fl_list)+1 
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT CORE COURSES
    """""""""""""""""""""""""""""""""""""""
    #row = 24+len(genel_list)
    row = 24+lengt_first_part
    banner_list = banner["B"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2) #print core courses
    course_det_right(row+1, worksheet, bold_left)
    
    core_list = core_courses.get("courses done")
    for i in range(0, len(core_list)):
        
        if core_list[i][0] == "":
            row = 26+lengt_first_part+i
            if core_list[i][0] == "":
                short_merge_sx(row, core_list[i][2], 0,  worksheet, merge_format1, merge_format2)
            else:
                worksheet.write(row, 0, core_list[i][2], course_info_format) 
        else:
            core_course = core_list[i][0]
            course_grade = core_list[i][1]
            #different format depending on the stile
            if course_grade == 0: #failed
                grade_format = color_cell3
            elif course_grade == 1: #passed
                grade_format = border_center
            elif course_grade == 2: #current
                grade_format = color_cell4
            elif course_grade == 3: #highlights the grades that are not failed, but lower than C-
                grade_format = color_cell2
            
            #row = 26+len(genel_list)+i
            row = 26+lengt_first_part+i
            worksheet.write(row, 0, core_list[i][2], course_info_format) #col H=7
            worksheet.write(row, 1, core_course.course.get_code(), course_info_format)
            worksheet.write(row, 2, core_course.course.get_number(), course_info_format)
            worksheet.write(row, 3, core_course.get_term(), course_info_format)
            worksheet.write(row, 4, number_to_letter.get(core_course.get_grade()), grade_format)
            worksheet.write(row, 5, core_course.course.get_credits(), course_info_format)
        
    #to print the courses that the student has not done in this category 
    for i in range(0,len(obj_core_remaining)):
        core_course = obj_core_remaining[i]
        
        row = 26+lengt_first_part+len(core_list)+i

        worksheet.write(row, 0, core_list[i][2], course_info_format) #col H=7
        worksheet.write(row, 1, core_course.get_code(), course_info_format)
        worksheet.write(row, 2, core_course.get_number(), course_info_format)
        worksheet.write(row, 3, "", course_info_format)
        worksheet.write(row, 4, "", course_info_format)
        worksheet.write(row, 5, core_course.get_credits(), course_info_format)    
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MAJOR ELECTIVES
    """""""""""""""""""""""""""""""""""""""
    #set the row depending on the longest between core and additional requirements
    
    row = 30 + lengt_first_part + (len(obj_core_remaining)+len(core_list))
    
    banner_list = banner["C"] 
    long_merge(row, banner_list[0], 1, worksheet, merge_format1, merge_format2) #prints "Major Electives"
    long_merge(row+1, curr_student.major.get_major_explanation(), 0, worksheet, merge_format1, merge_format2) #prints description
    course_det_left(row+1, worksheet, bold_left)

    electives_list = major_electives.get("courses done")
    for i in range(0, len(electives_list)):
        elective_course = electives_list[i][0]
        course_grade = electives_list[i][1]
        #different format depending on the stile
        if course_grade == 0: #failed
            grade_format = color_cell3
        elif course_grade == 1: #passed
            grade_format = border_center
        elif course_grade == 2: #current
            grade_format = color_cell4
            
        #row = 32+len(genel_list)+len(core_list)+i
        row = 32+lengt_first_part+len(core_list)+i
        worksheet.write(row, 0, elective_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 1, elective_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, elective_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, elective_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(elective_course.get_grade()), grade_format)
        worksheet.write(row, 5, elective_course.course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    CONSTRUCT THE LEGEND, GENERAL INFO, COURSES MISSING BY SECTION PART
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    #legend
    row = 4 
    banner_list = banner["G"] 
    legend_merge(row, banner_list[0], worksheet, merge_format1)
    legend_list = ["No more than two core courses with a grade below C-", "Grade requirement not satisfied", "Courses that the student is taking the current semester"]
    legend_structure(legend_list, "", row, worksheet, border_left)


    legend_format = [color_cell2, color_cell3, color_cell4]
    for i in range(0, len(legend_format)):
        position = int(row + i)
        worksheet.write(position, 15, "", legend_format[i])

    #general information
    row = row + 2 +  len(legend_list)
    banner_list = banner["H"] 
    legend_merge(row, banner_list[0], worksheet, merge_format1)
    worksheet.write(row, 15, "Total", bold_left)
    worksheet.write(row, 14, "", bold_left)
    info_list = ["Cumulative GPA", "Credits (earned)", "Current Standing", "Tentative Credits following semester", "Tentative Standing following semester", "Credits missing"]
    data_list = curr_student.create_info_list()
    row = row + 1
    legend_structure(info_list, data_list, row, worksheet, border_left)

    #courses missing by section
    row = row + len(legend_list) + len(info_list) - 1
    banner_list = banner["I"]
    legend_merge(row, banner_list[0], worksheet, merge_format1)
    worksheet.write(row, 15, "Total", bold_left)
    worksheet.write(row, 14, "", bold_left)
    #missing_list = ["Math Proficiency", "Math, Science, Computer Science", "Foreign Language", "Social Sciences", "Humanities", "Fine Arts", "Core Courses", "Major Electives", "Minor 1", "Minor 2"]
    num_missing = curr_student.return_missing()
    row = row + 1
    legend_structure(legend_keys, num_missing, row, worksheet, border_left)
    
    #CLOSE THE PLANNER!
    workbook.close() 