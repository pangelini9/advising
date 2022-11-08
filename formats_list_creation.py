# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 14:10:45 2022

@author: escianetti


ADD FORMAT STRUCTURE
f_list = ["Format name" , {properties, ...}]
format_list.append(f_list)
"""

import json
format_list = []


f_list = ["font_size", {'font_size': 10}]
format_list.append(f_list)

f_list = ["bold_center", {'font_size': 10, 'bold': True, 'border': 1, 'align': 'center'}]
format_list.append(f_list)

f_list = ["bold_left", {'font_size': 10, 'bold': True, 'border': 1}]
format_list.append(f_list)

f_list = ["border_center", {'font_size': 10, 'border': 1, 'align': 'center'}]
format_list.append(f_list)

f_list = ["border_left", {'font_size': 10, 'border': 1}]
format_list.append(f_list)

#blue banner
f_list = ["merge_format1", { 
    'font_size': 10, 
    'bold': 1,
    'border': 1,
    'align': 'center',
    'fg_color': '#BDD7EE'
    }]
format_list.append(f_list)

#white banner
f_list = ["merge_format2", { 
    'font_size': 10, 
    'bold': 0,
    'border': 1,
    'align': 'center',
    }]
format_list.append(f_list)

#cell format for "Course not taken yet"
f_list = ["color_cell1", { 
    'font_size': 10, 
    'bold': 0,
    'border': 1,
    'align': 'center',
    'fg_color': '#FFE699'
    }]
format_list.append(f_list)

#cell format for "No more than two core courses can be passed with D"
f_list = ["color_cell2", { 
    'font_size': 10, 
    'bold': 0,
    'border': 1,
    'align': 'center',
    'fg_color': '#F4B084'
    }]
format_list.append(f_list)

#cell format for "Grade requirement not satisfied"
f_list = ["color_cell3", { 
    'font_size': 10, 
    'bold': 0,
    'border': 1,
    'align': 'center',
    'fg_color': '#FF0000'
    }]
format_list.append(f_list)

#cell format for "Courses that the student is taking the current semester"
f_list = ["color_cell4", { 
    'font_size': 10, 
    'bold': 0,
    'border': 1,
    'align': 'center',
    'fg_color': '#C6E0B4'
    }]
format_list.append(f_list)

with open('formats_list.json', 'w') as myFile:
    json.dump(format_list, myFile)