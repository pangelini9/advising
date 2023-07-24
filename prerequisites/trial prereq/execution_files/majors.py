# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 18:14:26 2022

@author: ilda1
"""

"""
dditional_requirements = [[code, 0], [code, 1], [code, 1]]
...
in the check you will have

for i in range(0, len(additional_requirements)):{
        curr_course = additional_requirements[i]
        if curr_course[2] == 1:
            check for both additional_requirements[i] and additional_requirements[i+1]
            i = i+2
        else:
            check only additional_requirements[i]
            i = i+1
    }
resta da controllare se gli or sono gli ultimi della lista
se ci sono major con più di due alternative si può cambiare il numero in posizione 
curr_course[2] e aggiungere degli elif

INITIAL STRUCTURE

def __init__(self, namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, major_key):
    self.name = namemajor
    self.ma_req = ma_req #=1 if MA101 required
    self.add_req = additional_requirements_list
    self.core_courses = core_courses_list
    self.major_electives = major_elective_courses
    self.explanation = major_electives_possible
    self.major_key = major_key
"""
import json
from execution_files.courses import Course, Course_taken 
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

class Major:
    
    def __init__(self, namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, planner_type, major_key):
        self.name = namemajor
        self.ma_req = ma_req #=1 if MA101 required
        self.add_req = additional_requirements_list
        self.core_courses = core_courses_list
        self.major_electives = major_elective_courses
        self.explanation = major_electives_possible
        self.major_key = major_key
        
        self.planner_structure = planner_type
        #1 == additional courses
        #2 == only core courses
        #3 == concentrations after core
        #4 == concentrations nei major electives
        
        
    def get_name(self):
        return self.name
    
    def get_math_requirement(self):
        return self.ma_req
    
    def get_additional_requirements(self):
        return self.add_req    
    
    def get_core_courses(self):
        return self.core_courses
    
    def get_major_electives(self):
        return self.major_electives
    
    def get_major_explanation(self):
        return self.explanation
    
    def get_major_key(self):
        return self.major_key
    
    def get_planner_structure(self):
        return self.planner_structure
    
    def add_requirement(self, course):
        self.core_courses.append(course)
    
    def add_core(self, course):
        self.core_courses.append(course)
            
    def add_elective(self, course):
        self.major_electives.append(course)        

"""
when dictionaries were in a list
        
def create_major_list():
    with open('majors_list.json', 'r') as myfile:
       majors_list = json.load(myfile)
      
    major_obj = []
    
    for i in range(0, len(majors_list)): 
        curr_major = majors_list[i]
        major = Major(curr_major[0], curr_major[1], curr_major[2], curr_major[3], curr_major[4], curr_major[5], curr_major[6])
        print(major.name)
        cc = major.add_req
        print(cc)
        print(major.core_courses)
        print(major.major_electives)
        major_obj.append(major)
        i = i+1
    
    return major_obj     
"""
        
def create_major_list():
    with open('execution_files\majors_dictionaries.json', 'r') as myfile:
       majors_dict = json.load(myfile)
      
    major_obj = []
    print("\nconverting majors:")
    for i in majors_dict.keys():
        curr_major = majors_dict[i]
        print(f"{i}")
        #print(curr_major)
        
        #for j in majors_dict[i]:
        #if i == "Communications":
            #major = Communications(i, curr_major['math requirement'], curr_major['additional requirements'], curr_major['core courses'], curr_major['major electives'], curr_major['electives description'], curr_major['planner_type'], curr_major['major key'])
        #else:
        major = Major(i, curr_major['math requirement'], curr_major['additional requirements'], curr_major['core courses'], curr_major['major electives'], curr_major['electives description'], curr_major['planner_type'], curr_major['major key'])
        #print(major.name)
        #print(major.add_req)
        #print(major.core_courses)
        #print(major.major_electives)
        major_obj.append(major)

    return major_obj     