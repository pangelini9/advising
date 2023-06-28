# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 17:06:06 2023

@author: elettra.scianetti
"""

import xlsxwriter
#import asposecells

workbook = xlsxwriter.Workbook('prerequisites.xlsx')
worksheet = workbook.add_worksheet()

"""""""""""""""""""""""""""""""""
DEFINE SOME PRINTING FORMATS
"""""""""""""""""""""""""""""""""

font_size = workbook.add_format({'font_size': 11, 'font_name': 'calibri light'})

bold_left = workbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1})
border_left = workbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'border': 1})

above_border = workbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'top': 5})
'''new formats'''
name_title = workbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1, 'bottom': 5})
course_title = workbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1, 'right': 5, 'bottom': 5})

bold_border = workbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1, 'right': 5})
bold_noborder = workbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1})
bold_leftborder = workbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1, 'left': 5})

#B9EAF9
blue_right = workbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1, 'right': 5, 'bottom': 5, 'fg_color': '#B9EAF9'})
blue_center = workbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1, 'bottom': 5, 'fg_color': '#B9EAF9'})
blue_left = workbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1, 'left': 5, 'bottom': 5, 'fg_color': '#B9EAF9'})


#CAF6D4
green_right = workbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1, 'right': 5, 'bottom': 5, 'fg_color': '#CAF6D4'})
green_center = workbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1, 'bottom': 5, 'fg_color': '#CAF6D4'})
green_left = workbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1, 'left': 5, 'bottom': 5, 'fg_color': '#CAF6D4'})

normal_border = workbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'border': 1, 'right': 5})
normal_noborder = workbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'border': 1})
no_format = workbook.add_format({'font_size': 11, 'font_name': 'calibri light'})

"""""""""""""""""""""""""""""""""
DEFINE SOME PRINTING SHORTCUTS
"""""""""""""""""""""""""""""""""   
def print_fields_informations(row, index, information_list):
    worksheet.write(row, index, information_list[index], border_left)

def set_column_width():
    #columns = []
    for index in range(5, 44, 3):
        worksheet.set_column(index-1, index-1, 20)
        worksheet.set_column(index, index, 20)
        #worksheet.set_column(index+1, index+1, 30)

def set_contour_border():
    for column_index in range(2, 44, 3):
        for row_index in range(0,2000):
            worksheet.write(row_index, column_index, "", bold_border)
            
def set_borders():
    for column_index in range(0,44):
        for row_index in range(0,2000):
            worksheet.write(row_index, column_index, "", normal_noborder)

def print_fields_names(maxlen):
    worksheet.write(0, 0, "Name", name_title)
    worksheet.write(0, 1, "Semester", name_title)
    worksheet.write(0, 2, "Course", course_title)
    for index in range(0, maxlen):
        requirement_type = f"Type {index+1}"
        requirement_info = f"Missing requirement {index+1}"
        requirement_reason = f"Reason {index+1}"
        
        if index%2!=0:
            worksheet.write(0, 3 + 3*index, requirement_type, green_left)
            worksheet.write(0, 4 + 3*index, requirement_info, green_center)
            worksheet.write(0, 5 + 3*index, requirement_reason, green_right)    
        
        else:
            worksheet.write(0, 3 + 3*index, requirement_type, blue_left)
            worksheet.write(0, 4 + 3*index, requirement_info, blue_center)
            worksheet.write(0, 5 + 3*index, requirement_reason, blue_right)
            

"""""""""""""""""""""""""""""""""""
FUNZIONE PER TOGLIERE I FORMATI 
"""""""""""""""""""""""""""""""""""
def remove_borders_rows(row_max_len):
    for column_index in range(0, 46):
        for row_index in range(row_max_len,2000):
            worksheet.write(row_index, column_index, "", no_format)
            
def remove_borders_columns(column_max):
    for column_index in range(3 + 3*column_max, 45):
        for row_index in range(0,2000):
            worksheet.write(row_index, column_index, "", no_format)

def closing_border(row_max_len, column_max):
    endpoint = 3 + 3*column_max
    for column_index in range(0, endpoint):
        worksheet.write(row_max_len, column_index, "", above_border)
#rows 1 to 2000
#workbook.close()
