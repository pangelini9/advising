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
from courses import Course, Course_taken

def create_course_obj():
    with open('course_id_list.json', 'r') as myfile:
      general_courses = json.load(myfile)
      
    courses_obj = []

    for i in range(0, len(general_courses)):
        curr_course = general_courses[i]
        course = Course(curr_course[0], curr_course[1], curr_course[2], curr_course[3], curr_course[4], curr_course[5])
        #print(course.name)
        courses_obj.append(course)
        i = i+1
    
    return courses_obj

def create_coursetaken_obj(courses_list, student, courses_taken_list):
    courses_taken_obj = []
    
    for i in range(0, len(courses_taken_list)): #loops over all the courses the student has taken
        curr_course_taken = courses_taken_list[i]
        course_taken_key = curr_course_taken[0]
        for j in range(0, len(courses_list)): #loops over all the courses the universtity offers
            curr_course = courses_list[j]
            course_key = curr_course.get_course_key()
            if course_taken_key == course_key:
                course_taken = Course_taken(curr_course, student, curr_course_taken[1], curr_course_taken[2], curr_course_taken[3], curr_course_taken[4])
                courses_taken_obj.append(course_taken)
                print(curr_course.get_name())
                break
            else:
                j += 1
        i += 1
        
    return courses_taken_obj
    
"""
ADD KEYS TO COURSES
with open('courses_list.json', 'r') as myfile:
    general_courses = json.load(myfile)
    
for i in range(0, len(general_courses)):
    curr_course = general_courses[i] 
    curr_course[5] = i
    i += 1
    
with open('course_id_list.json', 'w') as myFile:
    json.dump(general_courses, myFile)
"""

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