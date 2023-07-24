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
from execution_files.courses import Course, Course_taken
#from execution_files import courses

#creates objects for each of the courses
def create_course_obj():
    with open('execution_files\courses.json', 'r') as myfile:
      general_courses = json.load(myfile)
      
    courses_obj = []

    for i in range(0, len(general_courses)):
        curr_course = general_courses[i]
        
        #                namecourse,         code,          number,      credits_num,     req_list,       course_key,      period,      concentration,     on site
        course = Course(curr_course[0], curr_course[1], curr_course[2], curr_course[3], curr_course[4], curr_course[5], curr_course[6], curr_course[7], curr_course[8])
        
        courses_obj.append(course)
        i = i+1
    
    return courses_obj

#takes the objects of the general courses and modifies for the student
def create_coursetaken_obj(curr_student, courses_taken_list, courses_list):
    courses_taken_obj = []
    
    for j in range(0, len(courses_taken_list)):
        curr_course_taken = courses_taken_list[j]
        key_course_taken = curr_course_taken[0]
        for h in range(0, len(courses_list)):
            curr_course = courses_list[h]
            key_curr_course = curr_course.get_course_key()
            if key_course_taken == key_curr_course:
                #structure of the course taken:
                #                          course,        student,       creds,                   grade,               term,                c_type,              in_residence
                taken_obj = Course_taken(curr_course, curr_student, curr_course_taken[1], curr_course_taken[2], curr_course_taken[3], curr_course_taken[4], curr_course_taken[5])
                courses_taken_obj.append(taken_obj)
                #print(taken_obj.grade)
                break
            #elif key_course_taken != courses_list[-1]:
                #taken_obj = Course_taken(curr_course, curr_student, curr_course_taken[1], curr_course_taken[2], curr_course_taken[3], curr_course_taken[4])
                #courses_taken_obj.append(taken_obj)
                #print(f"key_course_taken : this course is not in list")
            else:
                h += 1
        j += 1
    return courses_taken_obj

#needed for the excel print of the degree planner: creates fake courses objects starting from the majors' requirements that the student has not fullfilled
def create_remaining_list(courses_list, remaining_list):
    obj_remaining_list =  []
    #for m in courses_list: #m is an object course
        #counter +=1
    for i in range(0, len(remaining_list)):
        counter = 0
        curr_info = remaining_list[i] #the list with info about remaing requirement [1, [["EN", 102, 102], ["FIN", 300, 300]]]
        #print(curr_info)
        rem_courses_list = curr_info[1]
        #print(rem_courses_list)
        prevname = ""
        for n in rem_courses_list: #each of the individual courses that can be alternatives
            #counter = 0
            #print(n)
            for m in courses_list: #m is an object course
                if counter==0 and n[0]==m.get_code() and n[1]==m.get_number():
                    obj_remaining_list.append(m)
                    counter += 1
                    prevname = m.get_name()
                elif counter!=0 and n[0]==m.get_code() and n[1]==m.get_number() and prevname!=m.get_name():
                    old_name = m.get_name()
                    new_name = "OR " + old_name #str(old_name)
                    new_Course = Course(new_name, m.get_code(), m.get_number(), m.get_credits(), m.get_requirements_list(), m.get_course_key())
                    obj_remaining_list.append(new_Course)
                    counter += 1

 
        """
        #for i in remaining_list:
            rem_courses_list = curr_info[1]
            for n in rem_courses_list:
                if counter==0 and n[0]==m.get_code() and n[1]==m.get_number():
                    obj_remaining_list.append(m)
                    counter += 1
                elif counter!=0 and n[0]==m.get_code() and n[1]==m.get_number():
                    new_name = "OR " + m.get_name
                    new_Course = Course(new_name, m.get_code, m.get_number , m.get_credits , m.get_requirements_list, m.get_course_key)
                    obj_remaining_list.append(new_Course)
                    counter += 1
        """                
    #print(counter) 
    return obj_remaining_list                    
                    
    
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