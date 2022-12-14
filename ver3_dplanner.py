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
    0.1 : "INC",
    5 : "P",
    0.2 : "NP",
    0.3 : "W",
    0.4 : "current",
    0.5 : "TR", # PA: added this entry, for Transfer credits
    }


workbook = formats.workbook
worksheet = formats.worksheet
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

"""
IMPORT THE MAJORS
"""
majors_list = create_major_list()

"""
IMPORT THE STUDENT
"""
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

#change the list of courses taken by the student with a list of objects courses taken    
#for i in range(0, len(students_list)):
    #curr_student = students_list[i]
courses_taken_list = curr_student.get_coursesTaken()
courses_taken_obj = create_coursetaken_obj(curr_student, courses_taken_list, courses_list)
curr_student.change_courses(courses_taken_obj)
    #print(curr_student.get_coursesTaken())

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
PRINT MA REQUIREMENT
"""""""""""""""""""""""""""""""""""""""
row =  13
banner_list = banner["math"] 
formats.short_merge_sx(row, banner_list[0], 1)
formats.short_merge_sx(row+1, banner_list[1], 0) #print math proficiency banner
ma_requirement = curr_student.check_ma_req()
formats.course_det_left(row+1)
   
m_list = ma_requirement.get("courses done")
ma_course = m_list[0][0]
ma_format = formats.border_left
if m_list[0] [1] == 0:
    grade_format = formats.color_cell3
elif m_list[0] [1] == 1:
    grade_format = formats.border_center
row = 15
worksheet.write(row, 0, ma_course.course.get_name(), ma_format) #col A=0
worksheet.write(row, 1, ma_course.course.get_code(), ma_format)
worksheet.write(row, 2, ma_course.course.get_number(), ma_format)
worksheet.write(row, 3, ma_course.get_term(), ma_format)
worksheet.write(row, 4, number_to_letter.get(ma_course.get_grade()), grade_format)
worksheet.write(row, 5, ma_course.course.get_credits(), ma_format)

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
    fl_format = formats.border_left
#different format depending on the stile
    if fl_list[i] [1] == 0: 
        grade_format = formats.color_cell3
    elif fl_list[i] [1] == 1:
        grade_format = formats.border_center
    row = 24+i
    worksheet.write(row, 0, fl_course.course.get_name(), fl_format) #col A=0
    worksheet.write(row, 1, fl_course.course.get_code(), fl_format)
    worksheet.write(row, 2, fl_course.course.get_number(), fl_format)
    worksheet.write(row, 3, fl_course.get_term(), fl_format)
    worksheet.write(row, 4, number_to_letter.get(fl_course.get_grade()), grade_format)
    worksheet.write(row, 5, fl_course.course.get_credits(), fl_format)


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
sosc_format = formats.border_left
if sosc_list[0] [1] == 0:
    grade_format = formats.color_cell3
elif sosc_list[0] [1] == 1:
    grade_format = formats.border_center
sosc_course = sosc_list[0][0]
row = 7
worksheet.write(row, 7, sosc_course.course.get_name(), sosc_format) #col H=7
worksheet.write(row, 8, sosc_course.course.get_code(), sosc_format)
worksheet.write(row, 9, sosc_course.course.get_number(), sosc_format)
worksheet.write(row, 10, sosc_course.get_term(), sosc_format)
worksheet.write(row, 11, number_to_letter.get(sosc_course.get_grade()), grade_format)
worksheet.write(row, 12, sosc_course.course.get_credits(), sosc_format)

"""""""""""""""""""""""""""""""""""""""
PRINT HUMANIETIES REQUIREMENT
"""""""""""""""""""""""""""""""""""""""
row = 10
banner_list = banner["hum"] 
formats.short_merge_dx(row, banner_list[0], 1)
formats.short_merge_dx(row+1, banner_list[1], 0) #print humanities banner
hum_req = curr_student.check_hum(curr_student) 
formats.course_det_right(row+1)

hum_list = hum_req.get("courses done")
hum_format = formats.border_left
if hum_list[0] [1] == 0:
    grade_format = formats.color_cell3
elif hum_list[0] [1] == 1:
    grade_format = formats.border_center
hum_course = hum_list[0][0]

row = 12
worksheet.write(row, 7, hum_course.course.get_name(), hum_format) #col H=7
worksheet.write(row, 8, hum_course.course.get_code(), hum_format)
worksheet.write(row, 9, hum_course.course.get_number(), hum_format)
worksheet.write(row, 10, hum_course.get_term(), hum_format)
worksheet.write(row, 11, number_to_letter.get(hum_course.get_grade()), grade_format)
worksheet.write(row, 12, hum_course.course.get_credits(), hum_format)

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
fa_format = formats.border_left
if fa_list[0] [1] == 0:
    grade_format = formats.color_cell3
elif fa_list[0] [1] == 1:
    grade_format = formats.border_center
fa_course = fa_list[0][0]

row = 17
worksheet.write(row, 7, fa_course.course.get_name(), fa_format) #col H=7
worksheet.write(row, 8, fa_course.course.get_code(), fa_format)
worksheet.write(row, 9, fa_course.course.get_number(), fa_format)
worksheet.write(row, 10, fa_course.get_term(), fa_format)
worksheet.write(row, 11, number_to_letter.get(fa_course.get_grade()), grade_format)
worksheet.write(row, 12, fa_course.course.get_credits(), fa_format)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
CONSTRUCT THE LEGEND, GENERAL INFO, COURSES MISSING BY SECTION PART
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#legend
row = 4 
banner_list = banner["G"] 
formats.legend_merge(row, banner_list[0])
legend_list = ["Course not taken yet", "No more than two core courses can be passed with D", "Grade requirement not satisfied", "Courses that the student is taking the current semester"]
formats.legend_structure(legend_list, "", row)


legend_format = [formats.color_cell1, formats.color_cell2, formats.color_cell3, formats.color_cell4]
for i in range(0, len(legend_format)):
    position = int(row + i)
    worksheet.write(position, 15, "", legend_format[i])

#general information
row = 10 
banner_list = banner["H"] 
formats.legend_merge(row, banner_list[0])
worksheet.write(row, 15, "Total", formats.bold_left)
worksheet.write(row, 14, "", formats.bold_left)
info_list = ["Cumulative GPA", "Credits (earned)", "Current Standing", "Tentative Credits following semester", "Tentative Standing following semester", "Credits missing"]
data_list = curr_student.create_info_list()
row = 11
formats.legend_structure(info_list, data_list, row)

#courses missing by section
row = 19 
banner_list = banner["I"]
formats.legend_merge(row, banner_list[0])
worksheet.write(row, 15, "Total", formats.bold_left)
worksheet.write(row, 14, "", formats.bold_left)
missing_list = ["English Composition and Literature", "Math Proficiency", "Math, Science, Computer Science", "Foreign Language", "Social Sciences", "Humanities", "Fine Arts", "Additional Requirements", "Core Courses", "Major Electives", "Major 1", "Major 2"]
num_missing = curr_student.return_missing()
row = 20
formats.legend_structure(missing_list, num_missing, row)

workbook.close()