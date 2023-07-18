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

code_to_area_name = {
    "cognitive_area": "Cognitive Area",
    "developmental_area" : "Developmental Area",
    "psychobiology_area" : "Sociocultural Area",
    "sociocultural_area" : "Psychobiology Area"
    }

area_name_to_code = {
    "Cognitive Area" : "cognitive_area" ,
    "Developmental Area" : "developmental_area",
    "Sociocultural Area" : "psychobiology_area",
    "Psychobiology Area" : "sociocultural_area"
    
    }


class Major:
    
    def __init__(self, namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, major_key):
        self.name = namemajor
        self.ma_req = ma_req #=1 if MA101 required
        self.add_req = additional_requirements_list
        self.core_courses = core_courses_list
        self.major_electives = major_elective_courses
        self.explanation = major_electives_possible
        self.major_key = major_key
                
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

'''
class Psychology(Major):
    
    def __init__(self, namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, major_key):
        super().__init__(namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, major_key)
        
        self.applied_psych = [["PS", 354], ["PS", 353], ["PS", 328], ["PS", 351], ["PS", 340]]
        self.cognitive_area = [["PS", 312], ["PS", 311], ["PS", 314], ["PS", 321], ["PS", 315]]
        self.developmental_area = [["PS", 321], ["PS", 325]]
        self.psychobiology_area = [["PS", 315]] 
        self.sociocultural_area = [["PS", 336], ["PS", 337], ["PS", 335]]
        
    def exception_one(self, counter_core_grades, reduced_courses_list):
        """
        in core courses, take two 300-level courses to be chosen from two different areas
        it is important to consider the grade, if there are more than two C- already,
        then the course should be used in the major electives (that do not have grade restriction)
        """
        core_counter = counter_core_grades #tells how many grades lower than C- the student already has
        taken_classes = reduced_courses_list #the list of all the courses done by the student
        
        courses_num = 2
        max_iterations = len(taken_classes)*2 #iterates twice over the list of courses done by the student
        #max_iterations = len(taken_classes)
        passing_list = [] #you'll need a for loop back in the part of program that called this function
        #so that each part is added to the list!!
        
        initial_row = "Two 300 level courses to be chosen from 2 different areas: "
        #either [coursetaken_obj, grade_format, text_to_write]
        #or     [""             , ""          , text_to_write]
        passing_list.append(["", "", initial_row]) 
        
        possible_courses = {
            "cognitive_area": [],
            "developmental_area" : [],
            "psychobiology_area" : [],
            "sociocultural_area" : []            
            }
        
        remaining_types = ["cognitive_area", "developmental_area", "psychobiology_area", "sociocultural_area"]
        
        for index in range(0,max_iterations): #loop on courses
            #i due corsi sono stati trovati
            if courses_num == 0:
                break
            
            #se non sono stati trovati
            else:
                #first time should only take grades at least equal to C-
                if index <= len(taken_classes):
                    curr_course = taken_classes[index]
                    curr_grade = curr_course.get_grade()

                    #for area in range(0, len(remaining_types)):
                    curr_conc = curr_course.course.get_course_concentrations() # ['Cognitive Area', 'Psychobiology Area']
                    
                    #if len(curr_conc) == 0: #è ammissibile solo se ha almeno una concentration, o il prerequisito non è satisfiable
                        #break
                        
                    #check the grade
                    if curr_grade>=letter_to_number.get("C-") and curr_grade!=letter_to_number.get("current"):
                        #è ammissibile solo se ha almeno una concentration, o il prerequisito non è satisfiable
                        if len(curr_conc) != 0:
                            for single_concentration in curr_conc: #'Cognitive Area'
                                for area in remaining_types[:]:  
                                    print(f"{area_name_to_code.get(single_concentration)} and {area}")
                                    if area_name_to_code.get(single_concentration)==area:
                                        if len(curr_conc) == 1:
                                            initial_row = single_concentration
                                            passing_list.append([curr_course, 0, initial_row]) #add the course you found with the needed info
                                            remaining_types.drop(area) #remove the area of the found course because you need the other coming from another area
                                            courses_num -= 1 #reduce because you have found one of the two necessary courses
                                        else:
                                            initial_row = single_concentration
                                            possible_courses[area].append([curr_course, 0, initial_row])
                                            
                        if index==len(taken_classes) and courses_num!=0: #se il giro con i grade satisfactory è finito e i due corsi non sono stati trovati
                            if courses_num == 1:
                                for area in remaining_types[:]:
                                    if len(possible_courses[area])!=0:
                                        passing_list.append(possible_courses[area][0])
                                        remaining_types.drop(area) #remove the area of the found course because you need the other coming from another area
                                        courses_num -= 1 #reduce because you have found one of the two necessary courses
                                        break
                            elif courses_num == 2:
                                stuff
                                
                            
                #if has looked at all the courses and not found one with a satisfactory grade then takes whathever course to fill the core            
                else: #else=grade is not sufficient or not the best possible scenario (either C-, current, or F/INC/NP)
                    
                            
                    
                
                

           
    area_name_to_code


        """
        it goes over the list twice because the first time it should only take grades at least equal to C-
        whereas the second time it takes whathever course applies
        still if there are more than the two grades below C- it will signal that is not satisfactory
        """
        
        
        
        
        for index in range(0,max_iterations):
            
            #once it has found the two courses it needs it will break the loop
            if courses_num == 0:
                break
            
            #still needs to find the course
            else:
                #firs
                if index<=len(taken_classes):
                    curr_course = taken_classes[index]
                    
                    
                    
                else:
                    actual_index = index - len(taken_classes)
                    curr_course = taken_classes[actual_index]


                #pick the course taken to analyze
                if index<=len(taken_classes):
                    curr_course = taken_classes[index]
                    curr_code = curr_course.course.get_code()
                    curr_num = curr_course.course.get_number()
                    curr_grade = curr_course.get_grade()
                    
                    #you need to check for everyone of the fields and remember the previous course because some are cross listed!!
                    
                    for list_name in possible_courses: #"cognitive_area", "developmental_area", "psychobiology_area", "sociocultural_area"
                        actual_list = self.list_name
                        
                        for element in actual_list: #["PS", 354]
                            if curr_code==element[0] and curr_num==element[1]:
                                if curr_grade>=letter_to_number.get("C-"):
                                    cell_text = code_to_area_name.get(list_name)
                                    possible_courses[list_name].append([curr_course, 1, cell_text]) #il numero è il printing format del grade
                    
                    
                    "1. cognitive_area" 
                    for element in self.cognitive_area :
                        if curr_code==[]
                    
                    "2. developmental_area" 
                    for element in self.developmental_area :
                        
                    "3. psychobiology_area" 
                    for element in self.psychobiology_area :
                        
                    "4. sociocultural_area" 
                    for element in self.sociocultural_area :
                    
                                        
                    
                    
                    
                    
                else:
                    actual_position = index - len(taken_classes)
                    curr_course = taken_classes[actual_position]
                    
'''
                    
class Communications(Major):
    
    def __init__(self, namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, major_key):
        super().__init__(namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, major_key)
        
        self.passing_list = []
        
        
    def return_passing(self) :
        return self.passing_list

    #prints "One 300-level CMS course:"
    def exception_one(self, reduced_courses_list):
        #core_counter = counter_core_grades #tells how many grades lower than C- the student already has
        taken_classes = reduced_courses_list #the list of all the courses done by the student
   
        current_courses = []   
        risky_course = []
        self.passing_list = []
        initial_row = "One 300-level CMS course:"
        
        for taken_course in reduced_courses_list:
            if len(self.passing_list)==0:
                
                #current course
                if taken_course.get_grade() >= letter_to_number.get("current"):
                    current_courses.append([taken_course, 2, initial_row])
                    
                #passed and grade is fine
                elif taken_course.get_grade() >= letter_to_number.get("C-"):
                    self.passing_list.append([taken_course, 1, initial_row])
                    taken_classes.drop(taken_course)
                    break
                
                #passed but with a "risky" grade
                elif taken_course.get_grade()<letter_to_number.get("C-") and taken_course.get_grade()>letter_to_number.get("W"):
                    risky_course.append([taken_course, 3, initial_row])
            
        if len(self.passing_list)==0:
           #se non si è trovato un corso con il voto giusto prima cerca tra i current
           if len(current_courses)!=0:
               for course in current_courses:
                   if len(self.passing_list)==0:
                       self.passing_list.append(course)
                       #se uso il current allora devo dropparlo dalla lista di corsi fatti
                       for taken_course in taken_classes:
                           if course[0].course.get_code()==taken_course.course.get_code() and course[0].course.get_number()==taken_course.course.get_number():
                               reduced_courses_list.drop(course)
                               break
           
           #poi cerca tra le C- che però possono essere solo 3 nei core courses per questo non vengono considerati prima
           elif len(risky_course)!=0:
               if len(self.passing_list)==0:
                   for course in risky_course:
                       self.passing_list.append(course)
                       #se uso il corso con C- or below allora devo dropparlo dalla lista di corsi fatti
                       for taken_course in taken_classes:
                           if course[0].course.get_code()==taken_course.course.get_code() and course[0].course.get_number()==taken_course.course.get_number():
                               reduced_courses_list.drop(course)
                               break
                           
           #lo studente non ha fatto nesun corso di CMS
           else:
                self.passing_list.append(["", "", initial_row])

        return reduced_courses_list
        #ricorda di chiamare la funzione per avere i corsi fatti e  quella per cambiare la lista di corsi nello studente
                            
    #needed to handle major electives
    def exception_two(self, reduced_courses_list):  
        self.passing_list = []
        courses_done = reduced_courses_list
        #se il voto è minore di D- non considerarli, ma sono da lasciare nei General electives
        cms_conc = []
        cms_counter = 0 
        
        dma_conc = []
        dma_counter = 0
        
        djrn_conc = []
        djrn_counter = 0
                
        for taken_course in courses_done:
            curr_grade = taken_course.get_grade()
            format_num = 0
            initial_row = "Course from concentration"
                        
            if taken_course.course.get_code().startswith("CMS") or taken_course.course.get_code().endswith("CMS") and cms_counter<3:
                #decide the grade format
                if curr_grade==letter_to_number.get("current"):
                    format_num = 2                    
                    cms_counter += 1    
                    cms_conc.append([taken_course, format_num, initial_row])
                    
                elif curr_grade>=letter_to_number.get("D-"):
                    format_num = 1
                    cms_counter += 1    
                    cms_conc.append([taken_course, format_num, initial_row])
                
            elif taken_course.course.get_code().startswith("DMA") or taken_course.course.get_code().endswith("DMA") and dma_counter<3:
                #decide the grade format
                if curr_grade==letter_to_number.get("current"):
                    format_num = 2
                    dma_counter += 1
                    dma_conc.append([taken_course, format_num, initial_row])
                    
                elif curr_grade>=letter_to_number.get("D-"):
                    format_num = 1
                    dma_counter += 1
                    dma_conc.append([taken_course, format_num, initial_row])
        
            elif taken_course.course.get_code().startswith("DJRN") or taken_course.course.get_code().endswith("DJRN") and djrn_counter<3:
                #decide the grade format
                if curr_grade==letter_to_number.get("current"):
                    format_num = 2
                    djrn_counter += 1
                    djrn_conc.append([taken_course, format_num, initial_row])
                    
                elif curr_grade>=letter_to_number.get("D-"):
                    format_num = 1
                    djrn_counter += 1
                    djrn_conc.append([taken_course, format_num, initial_row])
                    
               
        
        concentrations = [[cms_counter,cms_conc], [dma_counter,dma_conc], [djrn_counter,djrn_conc]]
        #concentration = 0

        for index1 in range(0,len(concentrations)-1):
            element1 = concentrations[index1]
            for index2 in range(1,len(concentrations)):
                element2 = concentrations[index2]
                
                if element1[0]>=element2[0]:
                    self.passing_list = element1[1]
                else:
                    self.passing_list = element2[1]
                    
        if len(self.passing_list) != 3:
            for times in range(0, 3-len(self.passing_list)):
                self.passing_list.append(["", 1, initial_row])
        
        for element in self.passing_list:
            if element[0]!="":
                for course in reduced_courses_list:
                    if course.course.get_code()==element[0].course.get_code() and course.course.get_number()==element[0].course.get_number():
                        reduced_courses_list.drop(course)
        
        
        #return recall #either the student has done them or not, it contains 3 elements 
        #(because the first 3 lines of the com electives are dedicated to the concentrations)
        return reduced_courses_list
    
    
    
        
    def major_electives_banner(self, row_number, worksheet):
        row = row_number
        #position = (("A" + str(row)) + (":") + ("M" + str(row)))
        
        merge_format1 = planner_formats.merge_format1
        merge_format2 = planner_formats.merge_format2
        
        position = (("A" + str(row)) + (":") + ("M" + str(row)))
        arg = "C. Major Elective Courses"
        worksheet.merge_range(position, arg, merge_format1)
        
        position = (("A" + str(row+1)) + (":") + ("M" + str(row+1)))
        arg = "Seven courses, not taken in the core, to be chosen from 200-level or higher CMS, COM, DMA, and DJRN, and to be chosen in accordance with the following rules:"
        worksheet.merge_range(position, arg, merge_format2)
        
        position = (("A" + str(row+2)) + (":") + ("M" + str(row+2)))
        arg = "-     Three courses at the 200-level or higher must be chosen from one of these clusters: CMS - DMA - DJRN"
        worksheet.merge_range(position, arg, merge_format2)
        
        position = (("A" + str(row+3)) + (":") + ("M" + str(row+3)))
        arg = "-     Fours courses must be at 300-level or higher (these may also be courses belonging to the cluster)"
        worksheet.merge_range(position, arg, merge_format2)
        
        position = (("A" + str(row+4)) + (":") + ("M" + str(row+4)))
        arg = "-     No more than two courses other than those coded CMS/COM/DMA/DJRN may be used as major electives"
        worksheet.merge_range(position, arg, merge_format2)

        

        
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
        if i == "Communications":
            major = Communications(i, curr_major['math requirement'], curr_major['additional requirements'], curr_major['core courses'], curr_major['major electives'], curr_major['electives description'], curr_major['major key'])
        else:
            major = Major(i, curr_major['math requirement'], curr_major['additional requirements'], curr_major['core courses'], curr_major['major electives'], curr_major['electives description'], curr_major['major key'])
        #print(major.name)
        #print(major.add_req)
        #print(major.core_courses)
        #print(major.major_electives)
        major_obj.append(major)

    return major_obj     