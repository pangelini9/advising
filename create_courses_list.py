# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 19:23:11 2022

@author: ilda1

create_course_obj():
    The object of this code is to import a list containing all the courses,
    each one being a list with elements
    [course name, course code, course number, course credits, course requirements], 
    and transform it in a list of ojects created by the class Course
    
create_coursetaken_obj():
    The object of this code is to create a list of objects courses_taken starting from the list of 
    information on the courses that the student has taken
    handles both a student object, and a course object

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

def create_coursetaken_obj(curr_student, courses_taken_list, courses_list):
    courses_taken_obj = []
    
    for j in range(0, len(courses_taken_list)):
        curr_course_taken = courses_taken_list[j]
        key_course_taken = curr_course_taken[0]
        for h in range(0, len(courses_list)):
            curr_course = courses_list[h]
            key_curr_course = curr_course.get_course_key()
            if key_course_taken == key_curr_course:
                taken_obj = Course_taken(curr_course, curr_student, curr_course_taken[1], curr_course_taken[2], curr_course_taken[3], curr_course_taken[4])
                courses_taken_obj.append(taken_obj)
                #print(taken_obj.grade)
                break
            else:
                h += 1
        j += 1
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