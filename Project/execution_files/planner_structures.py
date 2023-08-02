# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 13:04:30 2023

@author: elettra.scianetti
"""
#create_student_json, core_list, print, json, create_info_list

import xlsxwriter
import os.path
import json


from execution_files.courses import Course, Course_taken
from execution_files.students import Student, create_student_list
from execution_files.majors import Major, create_major_list
from execution_files.create_courses_list import create_course_obj, create_coursetaken_obj, create_remaining_list, create_remaining_list_special


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
    4.5 : "TR", # PA: added this entry, for Transfer credits
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
  
def short_merge_sx(row, arg, c, worksheet, merge_format1, merge_format2, bold_left):
    position = (("A" + str(row)) + (":") + ("F" + str(row)))
    if c == 1:
        worksheet.merge_range(position, arg, merge_format1) #short blue headline on left size
    elif c == 0:
        worksheet.merge_range(position, arg, merge_format2) #short white headline followed by course info on left size
        course_det_left(row, worksheet, bold_left)
    elif c == 2:
        worksheet.merge_range(position, arg, merge_format2) #short white headline on left size


def short_merge_dx(row, arg, c, worksheet, merge_format1, merge_format2, bold_left):
    position = (("H" + str(row)) + (":") + ("M" + str(row))) 
    if c == 1:
        worksheet.merge_range(position, arg, merge_format1) #short blue headline on right size
    elif c == 0:
        worksheet.merge_range(position, arg, merge_format2) #short white headline followed by course info on right size
        course_det_right(row, worksheet, bold_left)
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

    workbook = xlsxwriter.Workbook(path, {'nan_inf_to_errors': True, 'useSharedStrings': True, 'useStyles': True})
    worksheet = workbook.add_worksheet()
    
    worksheet.set_column(0, 5, 11)
    worksheet.set_column(7, 12, 11) 
    worksheet.set_column(14, 14, 44)
    worksheet.set_column(15, 15, 11)
    
    banner = banner_content
     
    """""""""""""""""""""""""""
    DEFINE FORMATS
    """""""""""""""""""""""
    bold_left = workbook.add_format({'font_size': 10, 'bold': True, 'border': 1})

    border_center = workbook.add_format({'font_size': 10, 'border': 1, 'align': 'center',})
    border_left = workbook.add_format({'font_size': 10, 'border': 1})

    #blue banner
    merge_format1 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#BDD7EE'
        })

    #white banner
    merge_format2 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
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
    student_major = "Degree Planner for " + curr_student.major.get_name()
    long_merge(row, student_major, 1, worksheet, merge_format1, merge_format2) #major
    long_merge(row+1, student_name, 0, worksheet, merge_format1, merge_format2)  #name and surname
    banner_list = banner["A"]
    long_merge(row+3, banner_list[0], 1,  worksheet, merge_format1, merge_format2)


    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    CHECK THE VARIOUS PARTS
    
    in the specific sections are only left the parts 
    that call the dictionary needed for the print in excel
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    #ENGLISH COMPOSITION AND LITERATURE
    curr_student.generate_en_courses(courses_list)
    curr_student.substitute_courses_done()
    curr_student.check_eng_composition()
    eng_requirement = curr_student.check_eng_literature()
    
    #MATHEMATICS REQUIREMENT (MA100 OR MA101)
    ma_requirement = curr_student.check_ma_req()
    
    #FOREIGN LANGUAGE
    fl_requirement = curr_student.check_flanguage()
    
    #SOCIAL SCIENCES
    sosc_req = curr_student.check_sosc()
    
    #HUMANITIES
    hum_req = curr_student.check_hum()     
    
    #FINE ARTS
    fa_req = curr_student.check_arts() 
    
    #MATHEMATICS, SCIENCE, AND COMPUTER SCIENCE
    sci_requirement = curr_student.check_sci()
    
    #ADDITIONAL REQUIREMENTS
    additional_requirements = curr_student.check_additional()
    additional_remaining = curr_student.get_additional_remaining()
    obj_additional_remaining = create_remaining_list_special(courses_list, additional_remaining, curr_student.major)    
        
    #CORE COURSES
    core_courses = curr_student.check_core()
    core_remaining = curr_student.get_core_remaining()
    obj_core_remaining = create_remaining_list_special(courses_list, core_remaining, curr_student.major)
    
    #MAJOR ELECTIVES
    major_electives = curr_student.check_major_electives()
    
    #MINOR 1
    #MINOR 2
    
    #GENERAL ELECTIVES
    genel_list = curr_student.check_genelectives()
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT ENGLISH COMP and LIT REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  5
    banner_list = banner["eng"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print english banner
    course_det_left(row+1, worksheet, bold_left)

    en_list = eng_requirement.get("output courses")
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
        worksheet.write(row, 5, en_course[0].get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MA REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  13
    banner_list = banner["math"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print math proficiency banner
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
        worksheet.write(row, 5, ma_course.get_credits(), course_info_format)

        
    """""""""""""""""""""""""""""""""""""""
    PRINT FOREIGN LANGUAGE REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 22
    banner_list = banner["fl"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print foreign language requirements banner
    course_det_left(row+1, worksheet, bold_left)
       
    fl_list = fl_requirement.get("courses done")
    for i in range(0, len(fl_list)):
        fl_course = fl_list[i][0]
        #different format depending on the stile
        if fl_list[i] [1] == 0: 
            grade_format = color_cell3 #failed/grade requirement not met
        elif fl_list[i] [1] == 1:
            grade_format = border_center #normal
        elif fl_list[i] [1] == 2:
            grade_format = color_cell4 #current
        row = 24+i
        worksheet.write(row, 0, fl_course.course.get_name(), course_info_format) #col A=0
        worksheet.write(row, 1, fl_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, fl_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, fl_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(fl_course.get_grade()), grade_format)
        worksheet.write(row, 5, fl_course.get_credits(), course_info_format)
        
    lenght_left = row
    #print(f"languages end at {lenght_left}")
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT SOCIAL SCIENCES REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  5
    banner_list = banner["sosc"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print social sciences banner
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
        worksheet.write(row, 12, sosc_course.get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT HUMANITIES REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 10
    banner_list = banner["hum"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print humanities banner
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
        worksheet.write(row, 12, hum_course.get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT FINE ARTS REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 15
    banner_list = banner["fa"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print fine arts banner
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
        worksheet.write(row, 12, fa_course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MA, SCI, COMP SCI REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  17
    banner_list = banner["sci"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print math, sci, comp sci banner
    course_det_left(row+1, worksheet, bold_left)

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
        worksheet.write(row, 5, sci_course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT GENERAL ELECTIVES
    """""""""""""""""""""""""""""""""""""""
    row = 19
    banner_list = banner["genel"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print general electives courses
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
        worksheet.write(row, 12, genel_course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    DECIDE WHAT LENGHT TO PRINT
    """""""""""""""""""""""""""""""""""""""
    lengt_first_part = 0
    #if (21+len(genel_list)) >= 26:
    if (21+len(genel_list)) >= (lenght_left+1):        
        lengt_first_part = len(genel_list)
    else:
        lengt_first_part = len(fl_list)+3
    
    """""""""""""""""""""""""""""""""""""""
    PRINT ADDITIONAL REQUIREMENTS
    """""""""""""""""""""""""""""""""""""""
    #row = 24+len(genel_list)
    
    add_lenght = 0
    
    row = 24+lengt_first_part
    banner_list = banner["B"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    course_det_left(row, worksheet, bold_left)

    #to print the courses that the student has done in this category
    additional_list = additional_requirements.get("courses done")
    add_lenght += len(additional_list)
    for i in range(0, len(additional_list)):
        if additional_list[i][0] == "":
            row = 25+lengt_first_part+i
            if additional_list[i][0] == "":
                short_merge_sx(row, additional_list[i][2], 0,  worksheet, merge_format1, merge_format2, bold_left)
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
            worksheet.write(row, 5, additional_course.get_credits(), course_info_format)


    #to print the courses that the student has not done in this category (yet)
    add_lenght += len(obj_additional_remaining)
    for i in range(0, len(obj_additional_remaining)):
        additional_course = obj_additional_remaining[i][0]
        
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
    core_lenght = 0 
    row = 24+lengt_first_part
    banner_list = banner["C"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print core courses
    course_det_right(row+1, worksheet, bold_left)
    
    core_list = core_courses.get("courses done")
    core_lenght += len(core_list)
    for i in range(0, len(core_list)):

        if core_list[i][0] == "":
            row = 26+lengt_first_part+i
            if core_list[i][0] == "":
                short_merge_sx(row, core_list[i][2], 0,  worksheet, merge_format1, merge_format2, bold_left)
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
            worksheet.write(row, 12, core_course.get_credits(), course_info_format)
        
    #to print the courses that the student has not done in this category 
    core_lenght += len(obj_core_remaining)
    for i in range(0,len(obj_core_remaining)):
        core_course = obj_core_remaining[i][0]
        
        row = 26+lengt_first_part+len(core_list)+i
        worksheet.write(row, 7, obj_core_remaining[i][2], course_info_format) #col H=7
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
    if core_lenght >= add_lenght:
       final_row = core_lenght
    else:
        final_row = add_lenght
    #row = 30+lengt_first_part+len(core_list)+len(obj_core_remaining)
    
    row = 29 + lengt_first_part + final_row
    

    if curr_student.major.get_major_key()==12 or curr_student.major.get_major_key()==27: #communications has a different major electives banner
        row=curr_student.major.major_electives_banner(row, worksheet, merge_format1, merge_format2)
    else:
        banner_list = banner["D"] 
        long_merge(row, banner_list[0], 1, worksheet, merge_format1, merge_format2) #prints "Major Electives"
        long_merge(row+1, curr_student.major.get_major_explanation(), 0, worksheet, merge_format1, merge_format2) #prints description
        worksheet.set_row(row, 50)
    
    course_det_left(row+1, worksheet, bold_left)
    new_row = row+2
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
            
        
        if curr_student.major.get_major_key()==12 or curr_student.major.get_major_key()==27: #communications has a different major electives banner
            row = new_row + i
        else:
            row = 31 + lengt_first_part + final_row + i
        
        worksheet.write(row, 0, elective_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 1, elective_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, elective_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, elective_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(elective_course.get_grade()), grade_format)
        worksheet.write(row, 5, elective_course.get_credits(), course_info_format)
    
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
    info_list = ["Cumulative GPA", "Credits (earned)", "Current Standing", "Tentative Credits following semester", "Tentative Standing following semester", "Credits missing (tentative)", "Credits missing (actual)"]
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

    workbook = xlsxwriter.Workbook(path, {'nan_inf_to_errors': True})
    worksheet = workbook.add_worksheet()
    
    worksheet.set_column(0, 5, 11)
    worksheet.set_column(7, 12, 11) 
    worksheet.set_column(14, 14, 44)    
    worksheet.set_column(15, 15, 11)
    
    banner = banner_content
    
    
    """""""""""""""""""""""""""
    DEFINE FORMATS
    """""""""""""""""""""""
    bold_left = workbook.add_format({'font_size': 10, 'bold': True, 'border': 1})

    border_center = workbook.add_format({'font_size': 10, 'border': 1, 'align': 'center',})
    border_left = workbook.add_format({'font_size': 10, 'border': 1})

    #blue banner
    merge_format1 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#BDD7EE'
        })

    #white banner
    merge_format2 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
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
    student_major = "Degree Planner for " + curr_student.major.get_name()
    long_merge(row, student_major, 1, worksheet, merge_format1, merge_format2) #major
    long_merge(row+1, student_name, 0, worksheet, merge_format1, merge_format2)  #name and surname
    banner_list = banner["A"]
    long_merge(row+3, banner_list[0], 1, worksheet, merge_format1, merge_format2)


    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    CHECK THE VARIOUS PARTS
    
    in the specific sections are only left the parts 
    that call the dictionary needed for the print in excel
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    #ENGLISH COMPOSITION AND LITERATURE
    curr_student.generate_en_courses(courses_list)
    curr_student.substitute_courses_done()
    curr_student.check_eng_composition()
    eng_requirement = curr_student.check_eng_literature()

    #MATHEMATICS REQUIREMENT (MA100 OR MA101)
    ma_requirement = curr_student.check_ma_req()
    
    #FOREIGN LANGUAGE
    fl_requirement = curr_student.check_flanguage()
    
    #SOCIAL SCIENCES
    sosc_req = curr_student.check_sosc()

    #HUMANITIES
    hum_req = curr_student.check_hum()     
    
    #FINE ARTS
    fa_req = curr_student.check_arts() 
    
    #MATHEMATICS, SCIENCE, AND COMPUTER SCIENCE
    sci_requirement = curr_student.check_sci()


    #CORE COURSES
    core_courses = curr_student.check_core()
    core_remaining = curr_student.get_core_remaining()
    obj_core_remaining = create_remaining_list_special(courses_list, core_remaining, curr_student.major)

    #MAJOR ELECTIVES
    major_electives = curr_student.check_major_electives()

    #MINOR 1
    #MINOR 2
    
    #GENERAL ELECTIVES
    genel_list = curr_student.check_genelectives()
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT ENGLISH COMP and LIT REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  5
    banner_list = banner["eng"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print english banner
    course_det_left(row+1, worksheet, bold_left)

    en_list = eng_requirement.get("output courses")

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
        worksheet.write(row, 5, en_course[0].get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MA REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  13
    banner_list = banner["math"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print math proficiency banner
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
        worksheet.write(row, 5, ma_course.get_credits(), course_info_format)


    """""""""""""""""""""""""""""""""""""""
    PRINT FOREIGN LANGUAGE REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 22
    banner_list = banner["fl"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print foreign language requirements banner
    course_det_left(row+1, worksheet, bold_left)
       
    fl_list = fl_requirement.get("courses done")
    for i in range(0, len(fl_list)):
        fl_course = fl_list[i][0]
        #different format depending on the stile
        if fl_list[i] [1] == 0: 
            grade_format = color_cell3 #failed/grade requirement not met
        elif fl_list[i] [1] == 1:
            grade_format = border_center #normal
        elif fl_list[i] [1] == 2:
            grade_format = color_cell4 #current
            
        row = 24+i
        worksheet.write(row, 0, fl_course.course.get_name(), course_info_format) #col A=0
        worksheet.write(row, 1, fl_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, fl_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, fl_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(fl_course.get_grade()), grade_format)
        worksheet.write(row, 5, fl_course.get_credits(), course_info_format)
        
    lenght_left = row
    
    """""""""""""""""""""""""""""""""""""""
    PRINT SOCIAL SCIENCES REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  5
    banner_list = banner["sosc"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print social sciences banner
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
        worksheet.write(row, 12, sosc_course.get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT HUMANITIES REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 10
    banner_list = banner["hum"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print humanities banner
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
        worksheet.write(row, 12, hum_course.get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT FINE ARTS REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 15
    banner_list = banner["fa"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print fine arts banner
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
        worksheet.write(row, 12, fa_course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MA, SCI, COMP SCI REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  17
    banner_list = banner["sci"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print math, sci, comp sci banner
    course_det_left(row+1, worksheet, bold_left)


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
        worksheet.write(row, 5, sci_course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT GENERAL ELECTIVES
    """""""""""""""""""""""""""""""""""""""
    row = 19
    banner_list = banner["genel"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print general electives courses
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
        worksheet.write(row, 12, genel_course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    DECIDE WHAT LENGHT TO PRINT
    """""""""""""""""""""""""""""""""""""""
    lengt_first_part = 0
    #if (21+len(genel_list)) >= 26:
    if (21+len(genel_list)) >= (lenght_left+1):        
        lengt_first_part = len(genel_list) 
    else:
        lengt_first_part = len(fl_list)+3 
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT CORE COURSES
    """""""""""""""""""""""""""""""""""""""
    #row = 24+len(genel_list)
    row = 24+lengt_first_part
    banner_list = banner["B"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print core courses
    course_det_left(row+1, worksheet, bold_left)
    
    core_list = core_courses.get("courses done")
    for i in range(0, len(core_list)):
        
        if core_list[i][0] == "":
            row = 26+lengt_first_part+i
            #if core_list[i][0] == "":
                #short_merge_sx(row, core_list[i][2], 0,  worksheet, merge_format1, merge_format2, bold_left)
            #else:
            worksheet.write(row, 0, core_list[i][2], course_info_format)
            worksheet.write(row, 1, "", course_info_format)
            worksheet.write(row, 2, "", course_info_format)
            worksheet.write(row, 3, "", course_info_format)
            worksheet.write(row, 4, "", course_info_format)
            worksheet.write(row, 5, "", course_info_format)
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
            worksheet.write(row, 5, core_course.get_credits(), course_info_format)
        
    #to print the courses that the student has not done in this category 
    for i in range(0,len(obj_core_remaining)):
        core_course = obj_core_remaining[i][0]
        #
        row = 26+lengt_first_part+len(core_list)+i

        worksheet.write(row, 0, obj_core_remaining[i][2], course_info_format) #col H=7
        worksheet.write(row, 1, core_course.get_code(), course_info_format)
        worksheet.write(row, 2, core_course.get_number(), course_info_format)
        worksheet.write(row, 3, "", course_info_format)
        worksheet.write(row, 4, "", course_info_format)
        worksheet.write(row, 5, core_course.get_credits(), course_info_format)    
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MAJOR ELECTIVES
    """""""""""""""""""""""""""""""""""""""
    #set the row depending on the longest between core and additional requirements
    core_lenght = len(core_list) + len(obj_core_remaining) 
    row = 29 + lengt_first_part + core_lenght
    
    if curr_student.major.get_major_key()==12 or curr_student.major.get_major_key()==27: #communications has a different major electives banner
        row=curr_student.major.major_electives_banner(row, worksheet, merge_format1, merge_format2)
    else:
        banner_list = banner["C"] 
        long_merge(row, banner_list[0], 1, worksheet, merge_format1, merge_format2) #prints "Major Electives"
        long_merge(row+1, curr_student.major.get_major_explanation(), 0, worksheet, merge_format1, merge_format2) #prints description
        worksheet.set_row(row, 50)
        
    course_det_left(row+1, worksheet, bold_left)
    new_row = row+2
#row, arg, c, worksheet, merge_format1, merge_format2

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
            
        if curr_student.major.get_major_key()==12 or curr_student.major.get_major_key()==27: #communications has a different major electives banner
            row = new_row + i
        else:
            row = 31 + lengt_first_part + core_lenght + i
        
        worksheet.write(row, 0, elective_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 1, elective_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, elective_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, elective_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(elective_course.get_grade()), grade_format)
        worksheet.write(row, 5, elective_course.get_credits(), course_info_format)
    
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
    info_list = ["Cumulative GPA", "Credits (earned)", "Current Standing", "Tentative Credits following semester", "Tentative Standing following semester", "Credits missing (tentative)", "Credits missing (actual)"]
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

    workbook = xlsxwriter.Workbook(path, {'nan_inf_to_errors': True})
    worksheet = workbook.add_worksheet()
    
    worksheet.set_column(0, 5, 11)
    worksheet.set_column(7, 12, 11) 
    worksheet.set_column(14, 14, 44)
    worksheet.set_column(15, 15, 11)
    
    banner = banner_content
    
    """""""""""""""""""""""""""
    DEFINE FORMATS
    """""""""""""""""""""""
    bold_left = workbook.add_format({'font_size': 10, 'bold': True, 'border': 1})

    border_center = workbook.add_format({'font_size': 10, 'border': 1, 'align': 'center',})
    border_left = workbook.add_format({'font_size': 10, 'border': 1})

    #blue banner
    merge_format1 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#BDD7EE'
        })

    #white banner
    merge_format2 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
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
    student_major = "Degree Planner for " + curr_student.major.get_name()
    long_merge(row, student_major, 1, worksheet, merge_format1, merge_format2) #major
    long_merge(row+1, student_name, 0, worksheet, merge_format1, merge_format2)  #name and surname
    banner_list = banner["A"]
    long_merge(row+3, banner_list[0], 1, worksheet, merge_format1, merge_format2)


    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    CHECK THE VARIOUS PARTS
    
    in the specific sections are only left the parts 
    that call the dictionary needed for the print in excel
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    #ENGLISH COMPOSITION AND LITERATURE
    curr_student.generate_en_courses(courses_list)
    curr_student.substitute_courses_done()
    curr_student.check_eng_composition()
    eng_requirement = curr_student.check_eng_literature()
    
    #MATHEMATICS REQUIREMENT (MA100 OR MA101)
    ma_requirement = curr_student.check_ma_req()
    
    #FOREIGN LANGUAGE
    fl_requirement = curr_student.check_flanguage()
    
    #SOCIAL SCIENCES
    sosc_req = curr_student.check_sosc()
    
    #HUMANITIES
    hum_req = curr_student.check_hum()     

    #FINE ARTS
    fa_req = curr_student.check_arts() 
    
    #MATHEMATICS, SCIENCE, AND COMPUTER SCIENCE
    sci_requirement = curr_student.check_sci()
    
    #CORE COURSES
    core_courses = curr_student.check_core()
    core_remaining = curr_student.get_core_remaining()
    obj_core_remaining = create_remaining_list_special(courses_list, core_remaining, curr_student.major)
    
    #TRACKS
    
    
    #MAJOR ELECTIVES
    major_electives = curr_student.check_major_electives()
    
    #MINOR 1
    #MINOR 2
    
    #GENERAL ELECTIVES
    genel_list = curr_student.check_genelectives()


    """""""""""""""""""""""""""""""""""""""
    PRINT ENGLISH COMP and LIT REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  5
    banner_list = banner["eng"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print english banner
    course_det_left(row+1, worksheet, bold_left)

    en_list = eng_requirement.get("output courses")
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
        worksheet.write(row, 5, en_course[0].get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MA REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  13
    banner_list = banner["math"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print math proficiency banner
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
        worksheet.write(row, 5, ma_course.get_credits(), course_info_format)


    """""""""""""""""""""""""""""""""""""""
    PRINT FOREIGN LANGUAGE REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 22
    banner_list = banner["fl"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print foreign language requirements banner
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
        worksheet.write(row, 5, fl_course.get_credits(), course_info_format)
        
    lenght_left = row

    """""""""""""""""""""""""""""""""""""""
    PRINT SOCIAL SCIENCES REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  5
    banner_list = banner["sosc"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print social sciences banner
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
        worksheet.write(row, 12, sosc_course.get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT HUMANITIES REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 10
    banner_list = banner["hum"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print humanities banner
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
        worksheet.write(row, 12, hum_course.get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT FINE ARTS REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 15
    banner_list = banner["fa"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print fine arts banner
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
        worksheet.write(row, 12, fa_course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MA, SCI, COMP SCI REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  17
    banner_list = banner["sci"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print math, sci, comp sci banner
    course_det_left(row+1, worksheet, bold_left)

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
        worksheet.write(row, 5, sci_course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT GENERAL ELECTIVES
    """""""""""""""""""""""""""""""""""""""
    row = 19
    banner_list = banner["genel"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print general electives courses
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
        worksheet.write(row, 12, genel_course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    DECIDE WHAT LENGHT TO PRINT
    """""""""""""""""""""""""""""""""""""""
    lengt_first_part = 0
    #if (21+len(genel_list)) >= 26:
    if (21+len(genel_list)) >= (lenght_left+1):        
        lengt_first_part = len(genel_list)
    else:
        lengt_first_part = len(fl_list)+3
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT CORE COURSES
    """""""""""""""""""""""""""""""""""""""
    #row = 24+len(genel_list)
    row = 24+lengt_first_part
    banner_list = banner["B"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print core courses
    course_det_left(row+1, worksheet, bold_left)
    
    core_list = core_courses.get("courses done")
    for i in range(0, len(core_list)):
        
        if core_list[i][0] == "":
            row = 26+lengt_first_part+i
            if core_list[i][0] == "":
                short_merge_sx(row, core_list[i][2], 0,  worksheet, merge_format1, merge_format2, bold_left)
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
            worksheet.write(row, 5, core_course.get_credits(), course_info_format)
        
    #to print the courses that the student has not done in this category 
    for i in range(0,len(obj_core_remaining)):
        core_course = obj_core_remaining[i][0]
        
        row = 26+lengt_first_part+len(core_list)+i

        worksheet.write(row, 0, obj_core_remaining[i][2], course_info_format) #col H=7
        worksheet.write(row, 1, core_course.get_code(), course_info_format)
        worksheet.write(row, 2, core_course.get_number(), course_info_format)
        worksheet.write(row, 3, "", course_info_format)
        worksheet.write(row, 4, "", course_info_format)
        worksheet.write(row, 5, core_course.get_credits(), course_info_format)    

    """""""""""""""""""""""""""""""""""""""
    PRINT TRACKS
    """""""""""""""""""""""""""""""""""""""
    #set the row depending on the longest between core courses
    core_lenght = len(core_list) + len(obj_core_remaining) 
    row = 29 + lengt_first_part + core_lenght

    banner_list = banner["C"] 
    long_merge(row, banner_list[0], 1, worksheet, merge_format1, merge_format2) #prints "chosen track"
    #long_merge(row+1, curr_student.major.get_major_explanation(), 0, worksheet, merge_format1, merge_format2) #prints description
    #worksheet.set_row(row, 50)
    
    #concentration A
    banner_list = banner["X"]
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print core courses
    #course_det_left(row+2, worksheet, bold_left)
    
    #concentration B
    banner_list = banner["Z"]
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print core courses
    #course_det_right(row+2, worksheet, bold_left)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MAJOR ELECTIVES
    """""""""""""""""""""""""""""""""""""""
    #set the row depending on the longest between core courses
    core_lenght = len(core_list) + len(obj_core_remaining) 
    #row = 29 + lengt_first_part + core_lenght
    row = 35 + lengt_first_part + core_lenght
    
    if curr_student.major.get_major_key()==12 or curr_student.major.get_major_key()==27: #communications has a different major electives banner
        row=curr_student.major.major_electives_banner(row, worksheet, merge_format1, merge_format2)
    else:
        banner_list = banner["D"] 
        long_merge(row, banner_list[0], 1, worksheet, merge_format1, merge_format2) #prints "Major Electives"
        long_merge(row+1, curr_student.major.get_major_explanation(), 0, worksheet, merge_format1, merge_format2) #prints description
        worksheet.set_row(row, 50)
        
    course_det_left(row+1, worksheet, bold_left)
    new_row = row+2
    
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
            
        if curr_student.major.get_major_key()==12 or curr_student.major.get_major_key()==27: #communications has a different major electives banner
            row = new_row + i
        else:
            #row = 31 + lengt_first_part + core_lenght + i
            row = 37 + lengt_first_part + core_lenght + i

        worksheet.write(row, 0, elective_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 1, elective_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, elective_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, elective_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(elective_course.get_grade()), grade_format)
        worksheet.write(row, 5, elective_course.get_credits(), course_info_format)
    
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
    info_list = ["Cumulative GPA", "Credits (earned)", "Current Standing", "Tentative Credits following semester", "Tentative Standing following semester", "Credits missing (tentative)", "Credits missing (actual)"]
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

    workbook = xlsxwriter.Workbook(path, {'nan_inf_to_errors': True})
    worksheet = workbook.add_worksheet()
    
    worksheet.set_column(0, 5, 11)
    worksheet.set_column(7, 12, 11) 
    worksheet.set_column(14, 14, 44)
    worksheet.set_column(15, 15, 11)
    
    banner = banner_content
    
    """""""""""""""""""""""""""
    DEFINE FORMATS
    """""""""""""""""""""""
    bold_left = workbook.add_format({'font_size': 10, 'bold': True, 'border': 1})

    border_center = workbook.add_format({'font_size': 10, 'border': 1, 'align': 'center',})
    border_left = workbook.add_format({'font_size': 10, 'border': 1})

    #blue banner
    merge_format1 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#BDD7EE'
        })

    #white banner
    merge_format2 = workbook.add_format({ 
        'font_size': 10, 
        'bold': 0,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
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
    student_major = "Degree Planner for " + curr_student.major.get_name()
    long_merge(row, student_major, 1, worksheet, merge_format1, merge_format2) #major
    long_merge(row+1, student_name, 0, worksheet, merge_format1, merge_format2)  #name and surname
    banner_list = banner["A"]
    long_merge(row+3, banner_list[0], 1, worksheet, merge_format1, merge_format2)


    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    CHECK THE VARIOUS PARTS
    
    in the specific sections are only left the parts 
    that call the dictionary needed for the print in excel
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    #ENGLISH COMPOSITION AND LITERATURE
    curr_student.generate_en_courses(courses_list)
    curr_student.substitute_courses_done()
    curr_student.check_eng_composition()
    eng_requirement = curr_student.check_eng_literature()
    
    #MATHEMATICS REQUIREMENT (MA100 OR MA101)
    ma_requirement = curr_student.check_ma_req()
    
    #FOREIGN LANGUAGE
    fl_requirement = curr_student.check_flanguage()
    
    #SOCIAL SCIENCES
    sosc_req = curr_student.check_sosc()
    
    #HUMANITIES
    hum_req = curr_student.check_hum()     
    
    #FINE ARTS
    fa_req = curr_student.check_arts() 
    
    #MATHEMATICS, SCIENCE, AND COMPUTER SCIENCE
    sci_requirement = curr_student.check_sci()
    
    #CORE COURSES
    core_courses = curr_student.check_core()
    core_remaining = curr_student.get_core_remaining()
    obj_core_remaining = create_remaining_list_special(courses_list, core_remaining, curr_student.major)
    
    #MAJOR ELECTIVES
    major_electives = curr_student.check_major_electives()
    
    #MINOR 1
    #MINOR 2
    
    #GENERAL ELECTIVES
    genel_list = curr_student.check_genelectives()


    """""""""""""""""""""""""""""""""""""""
    PRINT ENGLISH COMP and LIT REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  5
    banner_list = banner["eng"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print english banner
    course_det_left(row+1, worksheet, bold_left)

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
        worksheet.write(row, 5, en_course[0].get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MA REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  13
    banner_list = banner["math"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print math proficiency banner
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
        worksheet.write(row, 5, ma_course.get_credits(), course_info_format)
        
        
    """""""""""""""""""""""""""""""""""""""
    PRINT FOREIGN LANGUAGE REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 22
    banner_list = banner["fl"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print foreign language requirements banner
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
        worksheet.write(row, 5, fl_course.get_credits(), course_info_format)
        
    lenght_left = row

    
    """""""""""""""""""""""""""""""""""""""
    PRINT SOCIAL SCIENCES REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  5
    banner_list = banner["sosc"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print social sciences banner
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
        worksheet.write(row, 12, sosc_course.get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT HUMANITIES REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 10
    banner_list = banner["hum"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print humanities banner
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
        worksheet.write(row, 12, hum_course.get_credits(), course_info_format)
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT FINE ARTS REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row = 15
    banner_list = banner["fa"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print fine arts banner
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
        worksheet.write(row, 12, fa_course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MA, SCI, COMP SCI REQUIREMENT
    """""""""""""""""""""""""""""""""""""""
    row =  17
    banner_list = banner["sci"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print math, sci, comp sci banner
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
        worksheet.write(row, 5, sci_course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    PRINT GENERAL ELECTIVES
    """""""""""""""""""""""""""""""""""""""
    row = 19
    banner_list = banner["genel"] 
    short_merge_dx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_dx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print general electives courses
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
        worksheet.write(row, 12, genel_course.get_credits(), course_info_format)
    
    """""""""""""""""""""""""""""""""""""""
    DECIDE WHAT LENGHT TO PRINT
    """""""""""""""""""""""""""""""""""""""
    lengt_first_part = 0
    #if (21+len(genel_list)) >= 26:
    if (21+len(genel_list)) >= (lenght_left+1):        
        lengt_first_part = len(genel_list) 
    else:
        lengt_first_part = len(fl_list)+3 
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT CORE COURSES
    """""""""""""""""""""""""""""""""""""""
    #row = 24+len(genel_list)
    row = 24+lengt_first_part
    banner_list = banner["B"] 
    short_merge_sx(row, banner_list[0], 1, worksheet, merge_format1, merge_format2, bold_left)
    short_merge_sx(row+1, banner_list[1], 0, worksheet, merge_format1, merge_format2, bold_left) #print core courses
    course_det_left(row+1, worksheet, bold_left)
    
    core_list = core_courses.get("courses done")
    for i in range(0, len(core_list)):
        
        if core_list[i][0] == "":
            row = 26+lengt_first_part+i
            if core_list[i][0] == "":
                short_merge_sx(row, core_list[i][2], 0,  worksheet, merge_format1, merge_format2, bold_left)
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
            worksheet.write(row, 5, core_course.get_credits(), course_info_format)
        
    #to print the courses that the student has not done in this category 
    for i in range(0,len(obj_core_remaining)):
        core_course = obj_core_remaining[i][0]
                
        row = 26+lengt_first_part+len(core_list)+i

        worksheet.write(row, 0, obj_core_remaining[i][2], course_info_format) #col H=7
        worksheet.write(row, 1, core_course.get_code(), course_info_format)
        worksheet.write(row, 2, core_course.get_number(), course_info_format)
        worksheet.write(row, 3, "", course_info_format)
        worksheet.write(row, 4, "", course_info_format)
        worksheet.write(row, 5, core_course.get_credits(), course_info_format)    
    
    
    """""""""""""""""""""""""""""""""""""""
    PRINT MAJOR ELECTIVES
    """""""""""""""""""""""""""""""""""""""
    #set the row depending on the longest between core and additional requirements
    core_lenght = len(core_list) + len(obj_core_remaining) 
    row = 29 + lengt_first_part + core_lenght
    
    if curr_student.major.get_major_key()==12 or curr_student.major.get_major_key()==27: #communications has a different major electives banner
        row=curr_student.major.major_electives_banner(row, worksheet, merge_format1, merge_format2)
    else:
        banner_list = banner["C"] 
        long_merge(row, banner_list[0], 1, worksheet, merge_format1, merge_format2) #prints "Major Electives"
        long_merge(row+1, curr_student.major.get_major_explanation(), 0, worksheet, merge_format1, merge_format2) #prints description
        worksheet.set_row(row, 50)
        
    course_det_left(row+1, worksheet, bold_left)
    new_row = row+2
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
            
        if curr_student.major.get_major_key()==12 or curr_student.major.get_major_key()==27: #communications has a different major electives banner
            row = new_row + i
        else:
            row = 31 + lengt_first_part + core_lenght + i

        worksheet.write(row, 0, elective_course.course.get_name(), course_info_format) #col H=7
        worksheet.write(row, 1, elective_course.course.get_code(), course_info_format)
        worksheet.write(row, 2, elective_course.course.get_number(), course_info_format)
        worksheet.write(row, 3, elective_course.get_term(), course_info_format)
        worksheet.write(row, 4, number_to_letter.get(elective_course.get_grade()), grade_format)
        worksheet.write(row, 5, elective_course.get_credits(), course_info_format)
    
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
    info_list = ["Cumulative GPA", "Credits (earned)", "Current Standing", "Tentative Credits following semester", "Tentative Standing following semester", "Credits missing (tentative)", "Credits missing (actual)"]
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