# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 13:49:57 2022

@author: ilda1
"""

import xlsxwriter
import os.path

path = os.path.relpath("planners/planner.xlsx")

"""
def create_file(student_name):
    full_path = f"planners/{student_name}"
    path = os.path.relpath("planners/planner.xlsx")
"""

#workbook = xlsxwriter.Workbook('planner.xlsx')
workbook = xlsxwriter.Workbook(path)
worksheet = workbook.add_worksheet()


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

def legend_structure(name_list, data_list, row):
    if data_list == "":
        for i in range(0, len(name_list)):
            position = int(row + i)
            worksheet.write(position, 14, str(name_list[i]), border_left)
            worksheet.write(position, 15, "", border_left)
            i = +1
    else: 
        for i in range(0, len(name_list)):
            position = int(row + i)
            worksheet.write(position, 14, str(name_list[i]), border_left)
            worksheet.write(position, 15, str(data_list[i]), border_left)
            i = +1
        
        