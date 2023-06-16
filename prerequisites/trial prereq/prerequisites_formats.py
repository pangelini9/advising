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
fields_names = ["Name", "Surname", "Course", "Requirement Type",
                "Missing Prerequisite 1", "Reason",
                "Missing Prerequisite 2", "Reason",
                "Missing Prerequisite 3", "Reason",
                "Missing Prerequisite 4", "Reason",
                "Missing Prerequisite 5", "Reason",
                "Missing Prerequisite 6", "Reason",
                "Missing Prerequisite 7", "Reason",
                "Missing Prerequisite 8", "Reason",
                "Missing Prerequisite 9", "Reason",
                "Missing Prerequisite 10", "Reason",
                "Missing Prerequisite 11", "Reason",
                "Missing Prerequisite 12", "Reason"
                ]

def print_fields_names():
    #worksheet.write(row, column, "stuff to print", format)
    for index in range(0,len(fields_names)):
        worksheet.write(0, index, fields_names[index], bold_left)

def print_fields_informations(row, index, information_list):
    worksheet.write(row, index, information_list[index], border_left)

"""            
row = 0
for i in range(0,len(fields_names)):
    print_fields_names(fields_names, i)


row = 1
stud_info = ["Elettra", "Scianetti", "EN 110", "Prerequisite",
             "EN 103 or EN 105", "Grade must be at least C",
             "MA 208"]
for i in range(0,len(stud_info)):
    print_fields_informations(row, i, stud_info)

#workbook.close()
"""