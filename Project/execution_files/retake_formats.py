# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 13:36:06 2023

@author: elettra.scianetti
"""

import xlsxwriter

#excel file for the retaken classes
rworkbook = xlsxwriter.Workbook('retaken_courses.xlsx')
rworksheet = rworkbook.add_worksheet()

"""""""""""""""""""""""""""""""""""
DEFINE FORMATS
"""""""""""""""""""""""""""""""""""
#for the title row
rname_title = rworkbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1, 'bottom': 5})
rcourse_title = rworkbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1, 'right': 5, 'bottom': 5})

rblue_right = rworkbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1, 'right': 5, 'bottom': 5, 'fg_color': '#B9EAF9'})
rblue_left = rworkbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1, 'left': 5, 'bottom': 5, 'fg_color': '#B9EAF9'})

rgreen_right = rworkbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1, 'right': 5, 'bottom': 5, 'fg_color': '#CAF6D4'})
rgreen_left = rworkbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'bold': True, 'border': 1, 'left': 5, 'bottom': 5, 'fg_color': '#CAF6D4'})


#to print the cells that are not field names
rnormal_border = rworkbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'border': 1, 'right': 5})
rnormal_noborder = rworkbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'border': 1})
rno_format = rworkbook.add_format({'font_size': 11, 'font_name': 'calibri light'})

rabove_border = rworkbook.add_format({'font_size': 11, 'font_name': 'calibri light', 'top': 5})

"""""""""""""""""""""""""""""""""
DEFINE SOME PRINTING SHORTCUTS
""""""""""""""""""""""""""""""""" 
def rset_column_width():    
    rworksheet.set_column(0, 0, 30)  
    for index in range(1, 6):
       rworksheet.set_column(index, index, 15)  
    
def rprint_fields_names():
    rworksheet.write(0, 0, "Name", rname_title)
    rworksheet.write(0, 1, "Course", rcourse_title)
    rworksheet.write(0, 2, "Old Semester", rblue_left)
    rworksheet.write(0, 3, "Old Grade", rblue_right)
    rworksheet.write(0, 4, "New Semester", rgreen_left)
    rworksheet.write(0, 5, "New Grade", rgreen_right)


def rclose_border(last_row):
    for col_indx in range(0,6):
        rworksheet.write(last_row, col_indx, "", rabove_border)  
    
