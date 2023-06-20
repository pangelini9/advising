# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 17:06:06 2023

@author: elettra.scianetti
"""

import xlsxwriter
workbook = xlsxwriter.Workbook('prerequisites.xlsx')
worksheet = workbook.add_worksheet()

"""""""""""""""""""""""""""""""""
DEFINE SOME PRINTING FORMATS
"""""""""""""""""""""""""""""""""

font_size = workbook.add_format({'font_size': 11})

bold_left = workbook.add_format({'font_size': 11, 'bold': True, 'border': 1})
border_left = workbook.add_format({'font_size': 11, 'border': 1})

"""""""""""""""""""""""""""""""""
DEFINE SOME PRINTING SHORTCUTS
"""""""""""""""""""""""""""""""""
"""OLD VERSION
fields_names = ["Name", "Course", 
                "Type", "Missing Prerequisite 1", "Reason",
                "Type", "Missing Prerequisite 2", "Reason",
                "Type", "Missing Prerequisite 3", "Reason",
                "Type", "Missing Prerequisite 4", "Reason",
                "Type", "Missing Prerequisite 5", "Reason",
                "Type", "Missing Prerequisite 6", "Reason",
                "Type", "Missing Prerequisite 7", "Reason",
                "Type", "Missing Prerequisite 8", "Reason",
                "Type", "Missing Prerequisite 9", "Reason",
                "Type", "Missing Prerequisite 10", "Reason",
                "Type", "Missing Prerequisite 11", "Reason",
                "Type", "Missing Prerequisite 12", "Reason"
                ]

def print_fields_names():
    #worksheet.write(row, column, "stuff to print", format)
    for index in range(0,len(fields_names)):
        worksheet.write(0, index, fields_names[index], bold_left)
"""

""" OLD VERSION
def print_fields_names(index):
    worksheet.write(0, index, fields_names[index], bold_left)
""" 
   
def print_fields_informations(row, index, information_list):
    worksheet.write(row, index, information_list[index], border_left)

"""OLD VERSION
row = 1
stud_info = ["Elettra Scianetti", "EN 110", 
             "Prerequisite", "EN 103", "Grade must be at least C",
             "Prerequisite", "EN 105", "Grade must be at least C",
             "Prerequisite", "MA 100"]

for i in range(0,len(stud_info)):
    print_fields_names(i)
    print_fields_informations(row, i, stud_info)
"""


def print_fields_names(maxlen):
    worksheet.write(0, 0, "Name", bold_left)
    worksheet.write(0, 1, "Course", bold_left)
    for index in range(0, maxlen):
        requirement_info = f"Missing requirement {index+1}"
        worksheet.write(0, 2 + 3*index, "Type", bold_left)
        worksheet.write(0, 3 + 3*index, requirement_info, bold_left)
        worksheet.write(0, 4 + 3*index, "Reason", bold_left)


#workbook.close()
