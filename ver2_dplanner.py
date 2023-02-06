# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 22:55:11 2022

@author: ilda1

Currently this progam aims at building an "empty checklist" that should be completed
with the student information on course completion

NB: xlxswriter considers the worksheet starting at 0,0 if you call the columns 
with numbers, BUT at row=1 if columns are called through letters
this is why the same row number is used to write in different rows with diff fucntions 
"""

import xlsxwriter
#from courses import Course, Course_taken
from students import Student
#from majors import Major
#from create_courses_list import return_class_objects

workbook = xlsxwriter.Workbook('planner_template.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column(0, 5, 11)
worksheet.set_column(7, 12, 11) 
worksheet.set_column(14, 14, 44)

"""
DEFINE SOME PRINTING FORMATS
"""
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

"""
DEFINE SOME PRINTING SHORTCUTS
"""
#funtion to print borders only on the cells selected, could be removed once in the implementation
#courses are printed with their own format containing border info
def set_borders(row_list, cell_list): 
    for j in row_list: #loops over rows
        for i in cell_list: #loops over columns
            cell_selected = i - 1
            worksheet.write(cell_selected, j, "", border_left)

def long_merge(row, arg, c):
    position = (("A" + str(row)) + (":") + ("M" + str(row)))
    if c == 1:
        worksheet.merge_range(position, arg, merge_format1) #long blue banner
    else:
        worksheet.merge_range(position, arg, merge_format2) #long white banner
  
def short_merge_sx(row, arg, c):
    position = (("A" + str(row)) + (":") + ("F" + str(row)))
    if c == 1:
        worksheet.merge_range(position, arg, merge_format1) #short blue banner on left size
    elif c == 0:
        worksheet.merge_range(position, arg, merge_format2) #short white banner followed by course info on left size
        course_det_left(row)
    elif c == 2:
        worksheet.merge_range(position, arg, merge_format2) #short white banner on left size


def short_merge_dx(row, arg, c):
    position = (("H" + str(row)) + (":") + ("M" + str(row))) 
    if c == 1:
        worksheet.merge_range(position, arg, merge_format1) #short blue banner on right size
    elif c == 0:
        worksheet.merge_range(position, arg, merge_format2) #short white banner followed by course info on right size
        course_det_right(row)
    elif c == 2:
        worksheet.merge_range(position, arg, merge_format2) #short white banner on right size

def course_det_left(row):
    worksheet.write(row, 0, "Name", bold_left)
    worksheet.write(row, 1, "Course", bold_left)
    worksheet.write(row, 2, "Code", bold_left)
    worksheet.write(row, 3, "Term", bold_left)
    worksheet.write(row, 4, "Grade", bold_left)
    worksheet.write(row, 5, "Credits", bold_left)
        
def course_det_right(row):
    worksheet.write(row, 7, "Name", bold_left) #col H=7
    worksheet.write(row, 8, "Course", bold_left)
    worksheet.write(row, 9, "Code", bold_left)
    worksheet.write(row, 10, "Term", bold_left)
    worksheet.write(row, 11, "Grade", bold_left)
    worksheet.write(row, 12, "Credits", bold_left)

def legend_merge(row, arg):
    position = (("O" + str(row)) + (":") + ("P" + str(row)))
    worksheet.merge_range(position, arg, merge_format1)

def legend_structure(name_list, row):
    for i in range(0, len(name_list)):
        position = int(row + i)
        worksheet.write(position, 14, str(name_list[i]), border_left)
        worksheet.write(position, 15, "", border_left)
        i = +1

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
DEFINE THE STUDENT
"""
student = Student("Elettra", "Scianetti", "Economics and Finance", "Mathematics", "")
major = student.major
student_name = student.name + " " + student.surname


"""
PUT BORDERS ONLY ON CELLS THAT NEED IT
not very efficient
"""
sx_cell_list = [8, 9, 10, 11, 12, 15, 19, 20, 23, 24, 29, 30, 31, 32, 33, 34, 35, 36, 45, 46, 47, 48, 49, 50, 57, 58, 59, 60, 61, 62]
sx_row_list = [0, 1, 2, 3, 4, 5]
dx_cell_list = [8, 9, 13, 14, 18, 22, 23, 24, 25, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 57, 58, 59, 60, 61, 62]
dx_row_list = [7, 8, 9, 10, 11, 12]

set_borders(sx_row_list, sx_cell_list)
set_borders(dx_row_list, dx_cell_list)
    

"""
START THE PRINT
"""
row = 1
column = 0
arg = "Degree Planner for B.A. in " + major
long_merge(row, arg, 1) #print major

row = 2
long_merge(row, student_name, 0) #print student name and surname

row = 4
arg = A
long_merge(row, arg, 1) #print Proficiency and General Distribution Requirements

row = 5
arg = eng  
short_merge_sx(row, arg, 1) #print english
arg = soc 
short_merge_dx(row, arg, 1) #print social sciences

row = 6
arg = engdf
short_merge_sx(row, arg, 0) #print english explanation + detail row
arg = socdf
short_merge_dx(row, arg, 0) #print social sciences explanation + detail row

#can also be eliminated is just to have a check
for i in range(7,12):
    worksheet.write(i, 2, "EN", border_left)
    i = i+1

row = 13
arg = math
short_merge_sx(row, arg, 1) #print math proficiency
course_det_left(row)

row = 16
arg = sci 
short_merge_sx(row, arg, 1) #print math, sience, computer science

row = 17
arg = scidf
short_merge_sx(row, arg, 0) #print math, sience, computer science explanation + detail row

row = 21
arg = fl
short_merge_sx(row, arg, 1) #print foreign language
course_det_left(row)

row = 27
arg = B
short_merge_sx(row, arg, 1) #print additional requirements
course_det_left(row)
arg = C
short_merge_dx(row, arg, 1) #print core courses

row = 28
arg = Cdf
short_merge_dx(row, arg, 2) #print core courses explanation
course_det_right(row)

row = 41
arg = D
long_merge(row, arg, 1) #print major electives courses
arg = Ddf_1
row =42
long_merge(row, arg, 0) #print major electives courses explanation 
arg = Ddf_2             #could be changed to an only cell through merging
row =43
long_merge(row, arg, 0)
course_det_left(row)

for i in range(44,47):
    worksheet.write(i, 6, "EC or FIN 300-level course", font_size)
    i = i+1    
    
for i in range(1, 7):
    row2 = row + i
    arg = str(i) + " course"
    worksheet.write(row2, 0, arg, border_left)
    i = i+1


"""
SET MINORS STRUCTURE
"""
row = 52
arg = H
long_merge(row, arg, 1) #print minors banner
#arg = h + stud_minor1
arg = h + " " + student.minor1
short_merge_sx(row+1, arg, 1) #print first minor
#arg = h + stud_minor2
arg = h + " " + student.minor2
short_merge_dx(row+1, arg, 1) #print second minor

#print minor explanation
row = row + 2
arg = hdf_1
short_merge_sx(row, arg, 2) 
short_merge_dx(row, arg, 2)

row = row + 1
arg = hdf_2
short_merge_sx(row, arg, 2) 
short_merge_dx(row, arg, 2)

#print minor structure
course_det_left(row)
course_det_right(row)
                 
for i in range(1, 7):
    row2 = row + i
    arg = str(i) + " course"
    worksheet.write(row2, 0, arg, border_left)
    worksheet.write(row2, 7, arg, border_left)
    i = i+1

"""
RIGHT COLUMN
"""
row = 10
arg = hum 
short_merge_dx(row, arg, 1) #print humanities

row = 11
arg = humdf
short_merge_dx(row, arg, 0) #print humanities explanation + detail row

row = 15
arg = fa 
short_merge_dx(row, arg, 1) #print fine arts

row = 16
arg = fadf
short_merge_dx(row, arg, 0) #print fine arts explanation + detail row

row = 19
arg = genel 
short_merge_dx(row, arg, 1) #print general electives

row = 20
arg = geneldf
short_merge_dx(row, arg, 0) #print general electives explanation + detail row

"""
CONSTRUCT THE LEGEND, GENERAL INFO, COURSES MISSING BY SECTION PART
"""   
row = 4 #build legend
arg = E
legend_merge(row, arg)
legend_list = ["Course not taken yet", "No more than two core courses can be passed with D", "Grade requirement not satisfied", "Courses that the student is taking the current semester"]
legend_structure(legend_list, row)

legend_format = [color_cell1, color_cell2, color_cell3, color_cell4]
for i in range(0, len(legend_format)):
    position = int(row + i)
    worksheet.write(position, 15, "", legend_format[i])
    i = i + 1

row = 10 #build general information
arg = F
legend_merge(row, arg)
worksheet.write(row, 15, "Total", bold_left)
worksheet.write(row, 14, "", bold_left)
info_list = ["Cumulative GPA", "Credits (earned)", "Current Standing", "Tentative Credits following semester", "Tentative Standing following semester", "Credits missing"]
row = 11
legend_structure(info_list, row)


row = 19 #build courses missing by section
arg = G
legend_merge(row, arg)
worksheet.write(row, 15, "Total", bold_left)
worksheet.write(row, 14, "", bold_left)
missing_list = ["English Composition and Literature", "Math Proficiency", "Math, Science, Computer Science", "Foreign Language", "Social Sciences", "Humanities", "Fine Arts", "Additional Requirements", "Core Courses", "Major Electives", "Major 1", "Major 2"]
row = 20
legend_structure(missing_list, row)

workbook.close()

