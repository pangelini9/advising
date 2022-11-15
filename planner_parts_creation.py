# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 01:20:49 2022

@author: ilda1

p_list = ["part name" , "name that will be printed on the degree planner", "explanation"]
planner_parts_list.append(p_list)

should out in the same list both the name and the explanation

"""

import json 

planner_parts = {
    "A" : ["A. Proficiency and General Distribution Requirements", ""], 
    "B" : ["B. Additional Requirements", ""],
    "C" : ["C. Core Courses", "No more that two core courses might be passed with a grade equal to D"],
    "D" : ["D. Major Electives Courses", ""],
    "G" : ["Legend", ""],
    "H" : ["General Information", ""],
    "I" : ["Courses Missing by Section", ""],
    "L" : ["Minors", ""],
    "E" : ["E. Minor in", "Total of 6 courses (check the website for specific requirements). No more than 3 courses may apply to both the major and minor"],
    "F" : ["F. Minor in", "Total of 6 courses (check the website for specific requirements). No more than 3 courses may apply to both the major and minor"],
    "eng" : ["English Composition and Literature", "Approved subsititutes for the second EN LIT course are: CL268, CL278, ITS292, ITS/EN 295"],
    "math" : ["Math Proficiency", ""],
    "sci" : ["Math, Science, Computer Science", "2 courses to be chosen from: MA, NS, CS"],
    "fl" : ["Foreign Language", ""],
    "sosc" : ["Social Sciences", "2 courses to be chosen from: COM, CMS, DMA, DJRN, EC, GEOG, PL, PS, SOSC"],
    "hum" : ["Humanities", "2 courses to be chosen from: CL, EN LIT, GRK, HM, HS, ITS, LAT, PH, RL"],
    "fa" : ["Fine Arts", "1 course to be chosen from: AH, ARCH, AS, CW, DR, MUS"], 
    "genel" : ["General Electives", "Sufficient to give a total of 120 credits"]
    }
        
with open('planner_parts.json', 'w') as myFile:
    json.dump(planner_parts, myFile)


"""
planner_parts_list = []

p_list = ["A" , "Proficiency and General Distribution Requirements", ""]
planner_parts_list.append(p_list)

p_list = ["B" , "Additional Requirements", ""]
planner_parts_list.append(p_list)

p_list = ["C" , "Core Courses", "No more that two core courses might be passed with a grade equal to D"]
planner_parts_list.append(p_list)

p_list = ["D" , "Major Electives Courses", ""]
planner_parts_list.append(p_list)

p_list = ["E" , "Legend", ""]
planner_parts_list.append(p_list)

p_list = ["F" , "General Information", ""]
planner_parts_list.append(p_list)

p_list = ["G" , "Courses Missing by Section", ""]
planner_parts_list.append(p_list)

p_list = ["H" , "Minors", ""]
planner_parts_list.append(p_list)

p_list = ["h" , "Minor in", "Total of 6 courses (check the website for specific requirements). No more than 3 courses may apply to both the major and minor"]
planner_parts_list.append(p_list)

p_list = ["eng" , "English Composition and Literature", ""]
planner_parts_list.append(p_list)

#p_list = ["engDF" , "Approved subsititutes for the second EN LIT course are: CL268, CL278, ITS292, ITS/EN 295"]
planner_parts_list.append(p_list)

p_list = ["math" , "Math Proficiency", ""]
planner_parts_list.append(p_list)

p_list = ["sci" , "Math, Science, Computer Science", "2 courses to be chosen from: MA, NS, CS"]
planner_parts_list.append(p_list)

p_list = ["fl" , "Foreign Language", ""]
planner_parts_list.append(p_list)

p_list = ["soc" , "Social Sciences", "2 courses to be chosen from: COM, CMS, DMA, DJRN, EC, GEOG, PL, PS, SOSC"]
planner_parts_list.append(p_list)

p_list = ["hum" , "Humanities", "2 courses to be chosen from: CL, EN LIT, GRK, HM, HS, ITS, LAT, PH, RL"]
planner_parts_list.append(p_list)

p_list = ["fa" , "Fine Arts", "1 course to be chosen from: AH, ARCH, AS, CW, DR, MUS"]
planner_parts_list.append(p_list)

p_list = ["genel" , "General Electives", "Sufficient to give a total of 120 credits"]
planner_parts_list.append(p_list)

with open('planner_parts.json', 'w') as myFile:
    json.dump(planner_parts_list, myFile)
"""