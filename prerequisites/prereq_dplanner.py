# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 16:58:52 2022

@author: ilda1
"""
"""old version
import json
import xlsxwriter
from courses import Course, Course_taken
from students import Student, create_student_list
from majors import Major, create_major_list
from create_courses_list import create_course_obj, create_coursetaken_obj, create_remaining_list
import formats
from banners import banner
"""


import json
import xlsxwriter
from prereq_courses import Course, Course_taken
from prereq_students import Student, create_student_list
from prereq_majors import Major, create_major_list
from prereq_create_courses_list import create_course_obj, create_coursetaken_obj, create_remaining_list
import formats
from banners import banner

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


workbook = formats.workbook
worksheet = formats.worksheet
course_info_format = formats.border_left
#workbook = xlsxwriter.Workbook('planner.xlsx')
#worksheet = workbook.add_worksheet()

worksheet.set_column(0, 5, 11)
worksheet.set_column(7, 12, 11) 
worksheet.set_column(14, 14, 44)
    

"""
IMPORT THE PLANNER PARTS
"""
with open('planner_parts.json', 'r') as myfile:
  planner_elements = json.load(myfile)
  
"""
IMPORT THE LIST OF ALL COURSES THE UNIVERSITY OFFERS
"""
courses_list = create_course_obj()

""""""""""""""""""""""
IMPORT THE MAJORS
"""""""""""""""""""""
majors_list = create_major_list()

""""""""""""""""""""""
IMPORT THE STUDENT
"""""""""""""""""""""
students_list = create_student_list()
curr_student = students_list[0]


#changes the element major present in the student object as the major key into the major object
#for i in range(0, len(students_list)):
    #curr_student = students_list[i]
for j in range(0, len(majors_list)):
    curr_major = majors_list[j]
    if curr_student.get_major() == curr_major.get_major_key():
        curr_student.change_major(curr_major)
        break

#OR or

#change the list of courses taken by the student with a list of objects courses taken    
#for i in range(0, len(students_list)):
    #curr_student = students_list[i]
courses_taken_list = curr_student.get_coursesTaken()
courses_taken_obj = create_coursetaken_obj(curr_student, courses_taken_list, courses_list)
curr_student.change_courses(courses_taken_obj)
curr_student.remove_retake() #toglie retake
curr_student.compute_transfer_credits() #counts how many credits the student has not done in residency
curr_student.change_credits_total() #sets the total amounts of credis equal to 150 id the student has a double degree
curr_student.add_transfer_credits() #if the student has done more than 60 credits out of residency, then it add them to the total amount of credits

#compute credits and standing for the student
curr_student.cumpute_gpa()
curr_student.compute_credits_earned()
curr_student.compute_credits_nxsem()
curr_student.compute_credits_missing()
curr_student.compute_cur_standing()
curr_student.compute_nx_standing()

"""""""""""""""""""""""""""""""""""""""
START THE PRINT
"""""""""""""""""""""""""""""""""""""""
#print student name, surname, and major
row = 1
column = 0
student_name = curr_student.get_name() + " " + curr_student.get_surname()
student_major = "Degree Planner for B.A. in " + curr_student.major.get_name()
formats.long_merge(row, student_major, 1) #major
formats.long_merge(row+1, student_name, 0)  #name and surname
banner_list = banner["A"]
formats.long_merge(row+3, banner_list[0], 1)


"""""""""""""""""""""""""""""""""""""""
PRINT ENGLISH COMP and LIT REQUIREMENT
"""""""""""""""""""""""""""""""""""""""
row =  5
banner_list = banner["eng"] 
formats.short_merge_sx(row, banner_list[0], 1)
formats.short_merge_sx(row+1, banner_list[1], 0) #print english banner
formats.course_det_left(row+1)

curr_student.generate_en_courses(courses_list)
curr_student.substitute_courses_done()
curr_student.check_eng_composition()
eng_requirement = curr_student.check_eng_literature()
en_list = eng_requirement.get("output courses")
#eng_requirement = curr_student.check_eng_requirement()

for i in range(0, len(en_list)):
    en_course = en_list[i]
    if en_course[1] == 1:
        grade_format = formats.border_center
    elif en_course[1] == 2:
        grade_format = formats.color_cell3
    elif en_course[1] == 3:
        grade_format = formats.color_cell4
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
formats.short_merge_sx(row, banner_list[0], 1)
formats.short_merge_sx(row+1, banner_list[1], 0) #print math proficiency banner
ma_requirement = curr_student.check_ma_req()
formats.course_det_left(row+1)
   
m_list = ma_requirement.get("courses done")
if len(m_list) != 0:
    ma_course = m_list[0][0]
    if m_list[0] [1] == 0:
        grade_format = formats.color_cell3
    elif m_list[0] [1] == 1:
        grade_format = formats.border_center
    elif m_list[0] [1] == 2:
        grade_format = formats.color_cell4
        
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
#additional_requirements = curr_student.additional_remaining(courses_list)
additional_remaining = curr_student.get_additional_remaining()
obj_additional_remaining = create_remaining_list(courses_list, additional_remaining)
#print(obj_additional_remaining)

core_courses = curr_student.check_core()
#core_courses = curr_student.core_remaining(courses_list)
core_remaining = curr_student.get_core_remaining()
obj_core_remaining = create_remaining_list(courses_list, core_remaining)
#print(obj_core_remaining)

major_electives = curr_student.check_major_electives()


"""""""""""""""""""""""""""""""""""""""
PRINT FOREIGN LANGUAGE REQUIREMENT
"""""""""""""""""""""""""""""""""""""""
row = 22
banner_list = banner["fl"] 
formats.short_merge_sx(row, banner_list[0], 1)
formats.short_merge_sx(row+1, banner_list[1], 0) #print foreign language requirements banner
fl_requirement = curr_student.check_flanguage(curr_student)
formats.course_det_left(row+1)
   
fl_list = fl_requirement.get("courses done")
for i in range(0, len(fl_list)):
    fl_course = fl_list[i][0]
    #different format depending on the stile
    if fl_list[i] [1] == 0: 
        grade_format = formats.color_cell3
    elif fl_list[i] [1] == 1:
        grade_format = formats.border_center
    elif fl_list[i] [1] == 2:
        grade_format = formats.color_cell4
    row = 24+i
    worksheet.write(row, 0, fl_course.course.get_name(), course_info_format) #col A=0
    worksheet.write(row, 1, fl_course.course.get_code(), course_info_format)
    worksheet.write(row, 2, fl_course.course.get_number(), course_info_format)
    worksheet.write(row, 3, fl_course.get_term(), course_info_format)
    worksheet.write(row, 4, number_to_letter.get(fl_course.get_grade()), grade_format)
    worksheet.write(row, 5, fl_course.course.get_credits(), course_info_format)


"""""""""""""""""""""""""""""""""""""""
PRINT SOCIAL SCIENCES REQUIREMENT
"""""""""""""""""""""""""""""""""""""""
row =  5
banner_list = banner["sosc"] 
formats.short_merge_dx(row, banner_list[0], 1)
formats.short_merge_dx(row+1, banner_list[1], 0) #print social sciences banner
sosc_req = curr_student.check_sosc(curr_student)
formats.course_det_right(row+1)

sosc_list = sosc_req.get("courses done")
for i in range(0, len(sosc_list)):
    sosc_course = sosc_list[i][0]
    course_grade = sosc_list[i][1]
    if course_grade == 0: #course failed
        grade_format = formats.color_cell3
    elif course_grade == 1: #course passed
        grade_format = formats.border_center
    elif course_grade == 2: #current course
        grade_format = formats.color_cell4
        
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
formats.short_merge_dx(row, banner_list[0], 1)
formats.short_merge_dx(row+1, banner_list[1], 0) #print humanities banner
hum_req = curr_student.check_hum(curr_student) 
formats.course_det_right(row+1)

hum_list = hum_req.get("courses done")
for i in range(0, len(hum_list)):
    hum_course = hum_list[i][0]
    course_grade = hum_list[i][1]
    if course_grade == 0: #course failed
        grade_format = formats.color_cell3
    elif course_grade == 1: #course passed
        grade_format = formats.border_center
    elif course_grade == 2: #current course
        grade_format = formats.color_cell4
        
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
formats.short_merge_dx(row, banner_list[0], 1)
formats.short_merge_dx(row+1, banner_list[1], 0) #print fine arts banner
fa_req = curr_student.check_arts(curr_student) 
formats.course_det_right(row+1)

fa_list = fa_req.get("courses done")
for i in range(0, len(fa_list)):
    fa_course = fa_list[i][0]
    course_grade = fa_list[i][1]
    if course_grade == 0: #course failed
        grade_format = formats.color_cell3
    elif course_grade == 1: #course passed
        grade_format = formats.border_center
    elif course_grade == 2: #current course
        grade_format = formats.color_cell4

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
formats.short_merge_sx(row, banner_list[0], 1)
formats.short_merge_sx(row+1, banner_list[1], 0) #print math, sci, comp sci banner
sci_requirement = curr_student.check_sci(curr_student)
formats.course_det_left(row+1)


#if len(sci_requirement.get("courses missing")) != 2:
sci_list = sci_requirement.get("courses done")
for i in range(0, len(sci_list)):
    sci_course = sci_list[i][0]
    course_grade = sci_list[i][1]
    #different format depending on the stile
    if course_grade == 0: #course failed
        grade_format = formats.color_cell3
    elif course_grade == 1: #course passed
        grade_format = formats.border_center
    elif course_grade == 2: #current course
        grade_format = formats.color_cell4

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
formats.short_merge_dx(row, banner_list[0], 1)
formats.short_merge_dx(row+1, banner_list[1], 0) #print general electives courses
genel_list = curr_student.check_genelectives()
formats.course_det_right(row+1)


for i in range(0, len(genel_list)):
    genel_course = genel_list[i][0]
    course_grade = genel_list[i][1]
    #different format depending on the stile
    if course_grade == 0: 
        grade_format = formats.color_cell3
    elif course_grade == 1:
        grade_format = formats.border_center
    elif course_grade == 2:
        grade_format = formats.color_cell4
        
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
if (21+len(genel_list)) >= 26:
    lengt_first_part = len(genel_list)
else:
    lengt_first_part = 4
    
"""""""""""""""""""""""""""""""""""""""
PRINT ADDITIONAL REQUIREMENTS
"""""""""""""""""""""""""""""""""""""""
#row = 24+len(genel_list)
row = 24+lengt_first_part
banner_list = banner["B"] 
formats.short_merge_sx(row, banner_list[0], 1)
#formats.short_merge_sx(row+1, banner_list[1], 0) #print core courses
formats.course_det_left(row)

#to print the courses that the student has done in this category
additional_list = additional_requirements.get("courses done")
#print(additional_list)
for i in range(0, len(additional_list)):
    additional_course = additional_list[i][0]
    #different format depending on the stile
    course_grade = additional_list[i][1]
    if course_grade == 0: #course failed
        grade_format = formats.color_cell3
    elif course_grade == 1: #course passed
        grade_format = formats.border_center
    elif course_grade == 2: #current course
        grade_format = formats.color_cell4
        
    #row = 25+len(genel_list)+i
    row = 25+lengt_first_part+i
    worksheet.write(row, 0, additional_course.course.get_name(), course_info_format) #col A=0
    worksheet.write(row, 1, additional_course.course.get_code(), course_info_format)
    worksheet.write(row, 2, additional_course.course.get_number(), course_info_format)
    worksheet.write(row, 3, additional_course.get_term(), course_info_format)
    worksheet.write(row, 4, number_to_letter.get(additional_course.get_grade()), grade_format)
    worksheet.write(row, 5, additional_course.course.get_credits(), course_info_format)

#to print the courses that the student has not done in this category

#additional_remaining = additional_requirements.get("courses remaining")
#print(additional_remaining)

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
formats.short_merge_dx(row, banner_list[0], 1)
formats.short_merge_dx(row+1, banner_list[1], 0) #print core courses
formats.course_det_right(row+1)

core_list = core_courses.get("courses done")
for i in range(0, len(core_list)):
    core_course = core_list[i][0]
    course_grade = core_list[i][1]
    #different format depending on the stile
    if course_grade == 0: #failed
        grade_format = formats.color_cell3
    elif course_grade == 1: #passed
        grade_format = formats.border_center
    elif course_grade == 2: #current
        grade_format = formats.color_cell4
    elif course_grade == 3: #highlights the grades that are not failed, but lower than C-
        grade_format = formats.color_cell2
    
    #row = 26+len(genel_list)+i
    row = 26+lengt_first_part+i
    worksheet.write(row, 7, core_course.course.get_name(), course_info_format) #col H=7
    worksheet.write(row, 8, core_course.course.get_code(), course_info_format)
    worksheet.write(row, 9, core_course.course.get_number(), course_info_format)
    worksheet.write(row, 10, core_course.get_term(), course_info_format)
    worksheet.write(row, 11, number_to_letter.get(core_course.get_grade()), grade_format)
    worksheet.write(row, 12, core_course.course.get_credits(), course_info_format)
    
#to print the courses that the student has not done in this category
#core_remaining = core_courses.get("courses remaining")
#print(core_remaining)

#obj_additional_remaining, obj_core_remaining

for i in range(0,len(obj_core_remaining)):
    core_course = obj_core_remaining[i]
    
    #instead of the check on grades I would put here a check on the pre-requisites to color the cell with the course name
    
    #row = 26+len(genel_list)+len(core_list)+i
    row = 26+lengt_first_part+len(core_list)+i
    #print(core_course.get_name())
    #print(core_course.get_code())
    #print(core_course.get_number())
    #print(core_course.get_credits())

    worksheet.write(row, 7, core_course.get_name(), course_info_format) #col H=7
    worksheet.write(row, 8, core_course.get_code(), course_info_format)
    worksheet.write(row, 9, core_course.get_number(), course_info_format)
    worksheet.write(row, 10, "", course_info_format)
    worksheet.write(row, 11, "", course_info_format)
    worksheet.write(row, 12, core_course.get_credits(), course_info_format)

    
"""""""""""""""""""""""""""""""""""""""
PRINT MAJOR ELECTIVES
"""""""""""""""""""""""""""""""""""""""
#set the row depending on the longest between core and additional requirements
#row = 30+len(genel_list)+len(core_list)
row = 30+lengt_first_part+len(core_list)+len(obj_core_remaining)

banner_list = banner["D"] 
formats.long_merge(row, banner_list[0], 1) #prints "Major Electives"
formats.long_merge(row+1, curr_student.major.get_major_explanation(), 0) #prints description
formats.course_det_left(row+1)

electives_list = major_electives.get("courses done")
for i in range(0, len(electives_list)):
    elective_course = electives_list[i][0]
    course_grade = electives_list[i][1]
    #different format depending on the stile
    if course_grade == 0: #failed
        grade_format = formats.color_cell3
    elif course_grade == 1: #passed
        grade_format = formats.border_center
    elif course_grade == 2: #current
        grade_format = formats.color_cell4
        
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
formats.legend_merge(row, banner_list[0])
legend_list = ["No more than two core courses can be passed with D", "Grade requirement not satisfied", "Courses that the student is taking the current semester"]
formats.legend_structure(legend_list, "", row)


legend_format = [formats.color_cell2, formats.color_cell3, formats.color_cell4]
for i in range(0, len(legend_format)):
    position = int(row + i)
    worksheet.write(position, 15, "", legend_format[i])

#general information
row = row + 2 +  len(legend_list)
banner_list = banner["H"] 
formats.legend_merge(row, banner_list[0])
worksheet.write(row, 15, "Total", formats.bold_left)
worksheet.write(row, 14, "", formats.bold_left)
info_list = ["Cumulative GPA", "Credits (earned)", "Current Standing", "Tentative Credits following semester", "Tentative Standing following semester", "Credits missing"]
data_list = curr_student.create_info_list()
row = row + 1
formats.legend_structure(info_list, data_list, row)

#courses missing by section
row = row + len(legend_list) + len(info_list) - 1
banner_list = banner["I"]
formats.legend_merge(row, banner_list[0])
worksheet.write(row, 15, "Total", formats.bold_left)
worksheet.write(row, 14, "", formats.bold_left)
missing_list = ["Math Proficiency", "Math, Science, Computer Science", "Foreign Language", "Social Sciences", "Humanities", "Fine Arts", "Additional Requirements", "Core Courses", "Major Electives", "Minor 1", "Minor 2"]
num_missing = curr_student.return_missing()
row = row + 1
formats.legend_structure(missing_list, num_missing, row)

#print("CC")
workbook.close()