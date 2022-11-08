# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 19:23:11 2022

@author: ilda1

The object of this code is to import a list containing all the courses,
each one being a list with elements
[course name, course code, course number, course credits, course requirements], 
and transform it in a list of ojects created by the class Course
import from json file: courses_list
retuns the list of objects
"""

import json
from courses import Course


def return_class_objects():
    with open('courses_list.json', 'r') as myfile:
      general_courses = json.load(myfile)
      
    courses_obj = []

    for i in range(0, len(general_courses)):
        curr_course = general_courses[i]
        course = Course(curr_course[0], curr_course[1], curr_course[2], curr_course[3], curr_course[4])
        print(course.name)
        courses_obj.append(course)
    
    return courses_obj

"""
with open('courses_list.json', 'r') as myfile:
  general_courses = json.load(myfile)
  
courses_obj = []

for i in range(0, len(general_courses)):
    curr_course = general_courses[i]
    course = Course(curr_course[0], curr_course[1], curr_course[2], curr_course[3], curr_course[4])
    print(course.name)
    courses_obj.append(course)
"""