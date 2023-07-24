# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 16:22:06 2023

@author: elettra.scianetti
"""

import json
import xlsxwriter

#When you'll have the program that functions as interface
from execution_files.courses import Course, Course_taken
from execution_files.students import Student, create_student_list #, close_file
from execution_files.majors import Major, create_major_list
from execution_files.create_courses_list import create_course_obj, create_coursetaken_obj, create_remaining_list
from execution_files.planner_structures import additional_courses, core_courses, core_tracks, electives_tracks
from execution_files.banners import banner_list


import execution_files.planner_formats as planner_formats


letter_to_number = {
    "A" : 4,
    "A-" : 3.67,
    "B+" : 3.33,
    "B" : 3,
    "B-" : 2.67,
    "C+" : 2.33,
    "C" : 2,
    "C-" : 1.67,
    "D+" : 1.33,
    "D" : 1,
    "D-" : 0.67, 
    "F" : 0,
    "INC" : 0.1,
    "P" : 5,
    "NP" : 0.2,
    "W" : 0.3,
    "current" : 0.4,
    "TR" : 0.5, # PA: added this entry, for Transfer credits,
    "AU" : 0.01}

number_to_letter = {
    4 : "A",
    3.67 :"A-",
    3.33 :"B+",
    3 : "B",
    2.67 : "B-",
    2.33 : "C+",
    2 : "C",
    1.67 : "C-",
    1.33 : "D+",
    1 : "D",
    0.67: "D-", 
    0 : "F",
    0.1 : "INC", #incomplete
    5 : "P",
    0.2 : "NP",
    0.3 : "W",
    0.4 : "current",
    0.5 : "TR", # PA: added this entry, for Transfer credits
    0.01 : "AU"}


def create_dplanners():   
    """
    IMPORT THE PLANNER PARTS
    """
    with open('execution_files\planner_parts.json', 'r') as myfile:
      planner_elements = json.load(myfile)

    """
    IMPORT THE LIST OF ALL COURSES THE UNIVERSITY OFFERS
    """
    courses_list = create_course_obj()

    """"""""""""""""""""""
    IMPORT THE MAJORS
    """""""""""""""""""""
    majors_list = create_major_list()

    """"""""""""""""""""""
    IMPORT THE STUDENT
    """""""""""""""""""""
    new_list = []
    students = []
    
    with open('execution_files\students_list.json', 'r') as myfile:
       students = json.load(myfile)
       #print(len(students))
       
    for index in range(0, len(students)):
        #print(f"iteration {index}")
        stud = students[index]
        new_list.append(stud)
       
    students_list = create_student_list(new_list)
           
    for index in range(0, len(students_list)):
        curr_student = students_list[index]
        
        """
        Create majors       
        """
        #changes the element major present in the student object as the major key into the major object
        for j in range(0, len(majors_list)):
            curr_major = majors_list[j]
            if curr_student.get_major() == curr_major.get_major_key():
                print(curr_major.get_name())
                curr_student.change_major(curr_major)
                break
        
        courses_taken_list = curr_student.get_coursesTaken()
        courses_taken_obj = create_coursetaken_obj(curr_student, courses_taken_list, courses_list)
        curr_student.change_courses(courses_taken_obj)
        curr_student.remove_retake() #toglie retake
                
        #curr_student.compute_transfer_credits() #counts how many credits the student has not done in residency
        #curr_student.change_credits_total() #sets the total amounts of credis equal to 150 id the student has a double degree
        #curr_student.add_transfer_credits() #if the student has done more than 60 credits out of residency, then it add them to the total amount of credits
        
        curr_student.cumpute_gpa()
        curr_student.compute_credits_earned()
        curr_student.compute_credits_nxsem()
        curr_student.compute_credits_missing()
        curr_student.compute_cur_standing()
        curr_student.compute_nx_standing()
    
        curr_major = curr_student.get_major()
        
        '''FOR EXCEPTIONS
        curr_core = curr_major.get_core_courses()
        curr_courses =  curr_student.get_coursesReduced()   
        print(curr_core) #[[1, [['COM', 101, 101]]], [1, [['exception', 1, 1]]], [1, [['COM', 470, 470]]], [1, [['COM', 480, 480]]]]
        
        for i in curr_core:
            for element in i[1]:
                if element[0] == "exception":
                    if element[1]==1:
                        new_reduced = curr_major.exception_one(curr_courses)
                        curr_student.change_reduced(new_reduced)
                        
                    elif element[1]==2:
                        new_reduced = curr_major.exception_two(curr_courses)
                        curr_student.change_reduced(new_reduced)

                    elif element[1]==3:
                        new_reduced = curr_major.exception_three(curr_courses)
                        curr_student.change_reduced(new_reduced)

                    elif element[1]==3:
                        new_reduced = curr_major.exception_four(curr_courses) 
                        curr_student.change_reduced(new_reduced)

                else:
                    print("checking a course")
                    '''
        stud_name = curr_student.get_name()
        major_name = curr_major.get_name()
        
        planner_name = stud_name + major_name
        #print(planner_name)
                            
        major_structure = curr_major.get_planner_structure()

        if major_structure == 1:
            banner = banner_list["structure_one"]
            legend_keys = ["Math Proficiency", "Math, Science, Computer Science", "Foreign Language", "Social Sciences", "Humanities", "Fine Arts", "Additional Requirements", "Core Courses", "Major Electives", "Minor 1", "Minor 2"]   
            additional_courses(planner_name, curr_student, courses_list, banner, legend_keys)
            
        elif major_structure == 2:
            banner = banner_list["structure_two"]
            legend_keys = ["Math Proficiency", "Math, Science, Computer Science", "Foreign Language", "Social Sciences", "Humanities", "Fine Arts", "Core Courses", "Major Electives", "Minor 1", "Minor 2"]   
            core_courses(planner_name, curr_student, courses_list, banner, legend_keys)
            
        elif major_structure == 3:  
            banner = banner_list["structure_three"]
            legend_keys = ["Math Proficiency", "Math, Science, Computer Science", "Foreign Language", "Social Sciences", "Humanities", "Fine Arts", "Core Courses", "Concentration", "Major Electives", "Minor 1", "Minor 2"]   
            core_tracks(planner_name, curr_student, courses_list, banner, legend_keys)
            
        elif major_structure == 4:
            banner = banner_list["structure_two"]
            legend_keys = ["Math Proficiency", "Math, Science, Computer Science", "Foreign Language", "Social Sciences", "Humanities", "Fine Arts", "Core Courses", "Major Electives", "Minor 1", "Minor 2"]   
            electives_tracks(planner_name, curr_student, courses_list, banner, legend_keys)

    
    
    
    
    
    
    
    
#workbook.close()        