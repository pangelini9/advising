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
#curr_student.cumpute_gpa()
curr_student.compute_credits_earned()
curr_student.compute_credits_nxsem()
curr_student.compute_credits_missing()
curr_student.compute_cur_standing()
curr_student.compute_nx_standing()

        
"""
START THE PRINT

"""

"""
DEFINE THE SECTIONS OF THE DEGREE PLANNER
"""
A = "Proficiency and General Distribution Requirements"
B = "Additional Requirements"
C = "Core Courses"
Cdf = "No more that two core courses might be passed with a grade equal to D"
D = "Major Electives Courses"
Ddf_1 = "Six courses to be chosen from 200-level of higher BUS, EC, FIN, LAW, MA, MGT, MKT, PL or PS courses."
Ddf_2 = "At least three course must be 300-level EC or FIN courses."
E = "Legend"
F = "General Information"
G = "Courses Missing by Section"
H = "Minors"
h = "Minor in "
hdf_1 = "Total of 6 courses (check the website for specific requirements)." 
hdf_2 = "No more than 3 courses may apply to both the major and minor"

eng = "English Composition and Literature"
engdf = "Approved subsititutes for the second EN LIT course are: CL268, CL278, ITS292, ITS/EN 295"
math = "Math Proficiency"
sci = "Math, Science, Computer Science"
scidf = "2 courses to be chosen from: MA, NS, CS"
fl = "Foreign Language"

soc = "Social Sciences"
socdf = "2 courses to be chosen from: COM, CMS, DMA, DJRN, EC, GEOG, PL, PS, SOSC"
hum = "Humanities"
humdf = "2 courses to be chosen from: CL, EN LIT, GRK, HM, HS, ITS, LAT, PH, RL"
fa = "Fine Arts"
fadf = "1 course to be chosen from: AH, ARCH, AS, CW, DR, MUS"
genel = "General Electives"
geneldf = "Sufficient to give a total of 120 credits"

"""
CONSTRUCT THE LEGEND, GENERAL INFO, COURSES MISSING BY SECTION PART
"""   
row = 4 #build legend
arg = planner_elements.get("G")
formats.legend_merge(row, arg[0])
legend_list = ["Course not taken yet", "No more than two core courses can be passed with D", "Grade requirement not satisfied", "Courses that the student is taking the current semester"]
formats.legend_structure(legend_list, "", row)


legend_format = [formats.color_cell1, formats.color_cell2, formats.color_cell3, formats.color_cell4]
for i in range(0, len(legend_format)):
    position = int(row + i)
    worksheet.write(position, 15, "", legend_format[i])


row = 10 #build general information
arg = planner_elements.get("H")
formats.legend_merge(row, arg[0])
worksheet.write(row, 15, "Total", formats.bold_left)
worksheet.write(row, 14, "", formats.bold_left)
info_list = ["Cumulative GPA", "Credits (earned)", "Current Standing", "Tentative Credits following semester", "Tentative Standing following semester", "Credits missing"]
data_list = curr_student.create_info_list()
row = 11
formats.legend_structure(info_list, data_list, row)


row = 19 #build courses missing by section
arg = planner_elements.get("I")
formats.legend_merge(row, arg[0])
worksheet.write(row, 15, "Total", formats.bold_left)
worksheet.write(row, 14, "", formats.bold_left)
missing_list = ["English Composition and Literature", "Math Proficiency", "Math, Science, Computer Science", "Foreign Language", "Social Sciences", "Humanities", "Fine Arts", "Additional Requirements", "Core Courses", "Major Electives", "Major 1", "Major 2"]
row = 20
formats.legend_structure(missing_list, "", row)

workbook.close()