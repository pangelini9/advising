# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 18:14:26 2022

@author: ilda1
"""


import json
from execution_files.courses import Course, Course_taken 
#import execution_files.planner_formats as planner_formats

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
    "TR" : 4.5, # PA: added this entry, for Transfer credits,
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


class Communications(Major):
    
    def __init__(self, namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, planner_type, major_key):
        super().__init__(namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, planner_type, major_key)
        
        self.passing_list = []
            
    def return_passing(self) :
        return self.passing_list

    #prints "One 300-level CMS course:"
    def exception_one(self, i, curr_student, reduced_courses_list):
        #print("exception one")
        message = "One 300-level CMS course:"
        
        iteration_counter = 0
        
        #tries to take a CMS course with a grade ==current or above C-
        for taken_course in curr_student.reduced_courses_list:
            iteration_counter += 1
            if len(self.passing_list)==0 and taken_course.used_flag<2 and (taken_course.course.get_code().startswith("CMS") or taken_course.course.get_code().endswith("CMS")):
                 
                if taken_course.get_grade() >= letter_to_number.get("current"):
                    curr_student.m_core["courses done"].append([taken_course,2,message])
                    taken_course.used_flag=2
                    
                elif taken_course.get_grade() >= letter_to_number.get("C-"):
                    curr_student.m_core["courses done"].append([taken_course,1,message])
                    taken_course.used_flag=2
            
        if len(self.passing_list)==0:
            fake_course = Course(message, "", "", "", [], "", "", "", -1)
            fcourse_taken =  Course_taken(fake_course, curr_student, "", "", "", "", 2)
            curr_student.m_core["courses done"].append([fcourse_taken,1,message])

                            
    #needed to handle major electives
    def exception_two(self, i, curr_student, reduced_courses_list):  
        #print("exception two")
        curr_student.m_majorelectives["num_remaining"] = 7
        #se il voto è minore di D- non considerarli, ma sono da lasciare nei General electives
        cms_conc = []
        cms_counter = 0 
        
        dma_conc = []
        dma_counter = 0
        
        djrn_conc = []
        djrn_counter = 0
                
        for taken_course in curr_student.reduced_courses_list:
            curr_grade = taken_course.get_grade()
            format_num = 0
            message = "Course from concentration"
                        
            if (taken_course.course.get_code().startswith("CMS") or taken_course.course.get_code().endswith("CMS")) and cms_counter<3:
                #decide the grade format
                if curr_grade==letter_to_number.get("current"):
                    format_num = 2                    
                    cms_counter += 1    
                    cms_conc.append([taken_course, format_num, message])
                    
                elif curr_grade>=letter_to_number.get("D-"):
                    format_num = 1
                    cms_counter += 1    
                    cms_conc.append([taken_course, format_num, message])
                
            elif taken_course.course.get_code().startswith("DMA") or taken_course.course.get_code().endswith("DMA") and dma_counter<3:
                #decide the grade format
                if curr_grade==letter_to_number.get("current"):
                    format_num = 2
                    dma_counter += 1
                    dma_conc.append([taken_course, format_num, message])
                    
                elif curr_grade>=letter_to_number.get("D-"):
                    format_num = 1
                    dma_counter += 1
                    dma_conc.append([taken_course, format_num, message])
        
            elif taken_course.course.get_code().startswith("DJRN") or taken_course.course.get_code().endswith("DJRN") and djrn_counter<3:
                #decide the grade format
                if curr_grade==letter_to_number.get("current"):
                    format_num = 2
                    djrn_counter += 1
                    djrn_conc.append([taken_course, format_num, message])
                    
                elif curr_grade>=letter_to_number.get("D-"):
                    format_num = 1
                    djrn_counter += 1
                    djrn_conc.append([taken_course, format_num, message])
                    
               
        
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
                self.passing_list.append(["", 1, message])
        
        for element in self.passing_list:
            if element[0]!="":
                for taken_course in curr_student.reduced_courses_list:
                    if taken_course.course.get_code()==element[0].course.get_code() and taken_course.course.get_number()==element[0].course.get_number():
                        curr_student.m_majorelectives["courses done"].append([taken_course, format_num, message])
                        taken_course.used_flag=2   
                        curr_student.m_majorelectives["courses missing"] -= 1
                        curr_student.m_majorelectives["num_remaining"] -= 1
                        curr_student.m_majorelectives["next_num"] += 1
                        
            else:
                fake_course = Course(message, "", "", "", [], "", "", "", -1)
                fcourse_taken =  Course_taken(fake_course, curr_student, "", "", "", "", 2)
                curr_student.m_majorelectives["courses done"].append([fcourse_taken,1,message])
                curr_student.m_majorelectives["num_remaining"] -= 1
                curr_student.m_majorelectives["next_num"] += 1


        
    def major_electives_banner(self, row_number, worksheet, merge_format1, merge_format2):
        row = row_number
        #position = (("A" + str(row)) + (":") + ("M" + str(row)))
        
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

        new_row = row+3
        #print(f"{new_row} vs {row}")
        return new_row


class Psychology(Major):
    
    def __init__(self, namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, planner_type, major_key):
        super().__init__(namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, planner_type, major_key)
        
        self.passing_list = []
        

    def exception_one(self, i, curr_student, reduced_courses_list):
        #print("not_working")

        curr_student.m_core["courses missing"] += i[0]
        
        message = "Two 300 level courses to be chosen from 2 different areas:"   
        curr_student.m_core["courses done"].append(["", 1, message])
        
        possible_courses = {
            "Cognitive Area": [],
            "Developmental Area" : [],
            "Sociocultural Area" : [],
            "Psychobiology Area" : []            
            }
        
        areas_list = ["Cognitive Area", "Developmental Area", "Sociocultural Area", "Psychobiology Area"]
        
        recall_course = []
        
        #to stop the loop at the second course
        counter = 0
        
        #to know how many were directly placed
        placed = 0
        
            
        #loops over the courses that the student has done
        for tcourse in curr_student.reduced_courses_list:
            concentrations_list = tcourse.course.get_course_concentrations()
            if tcourse.course.code =="PS":
                print(f"\nanalyzing {tcourse.course.get_name()} with {concentrations_list}")
            
            #if the course was not previously used in II part of planner, less than two courses were found, and the course can saisfy at least one concentration
            if tcourse.used_flag<2 and counter<2 and len(concentrations_list)!=0 and tcourse.course.get_code() == "PS" and (concentrations_list[0] in possible_courses.keys()):
                print("course with concentrations")
                if len(possible_courses[concentrations_list[0]]) == 0:
                    possible_courses[concentrations_list[0]].append(tcourse)
                    counter += 1
                    tcourse.used_flag = 2
                    
                elif len(concentrations_list)>1 and len(possible_courses[concentrations_list[1]]) == 0:
                    possible_courses[concentrations_list[1]].append(tcourse)
                    counter += 1
                    tcourse.used_flag = 2                    
                    
                elif len(concentrations_list)==1:
                    prev_concentrations =  possible_courses[concentrations_list[0]][0].course.course_concentrations
                    if len(prev_concentrations)>1:
                        old_area_name = prev_concentrations[0]
                        new_area_name = prev_concentrations[1]
                        placed_course = possible_courses[concentrations_list[0]][0]
                        
                        possible_courses[old_area_name].remove(placed_course)
                        possible_courses[old_area_name].append(tcourse)
                        
                        possible_courses[new_area_name].append(placed_course)
                        
                        counter += 1    
                        tcourse.used_flag = 2
                        
                        
        for area_name in possible_courses.keys():
            if len(possible_courses[area_name]) == 0:
                message = " -  " + area_name
                curr_student.m_core["courses done"].append(["", 1, message])
                
            elif len(possible_courses[area_name]) == 1:
                curr_course = possible_courses[area_name][0]
                
                if curr_course.get_grade() == letter_to_number.get("current"):
                    message = " -  " + area_name
                    curr_student.m_core["courses done"].append([curr_course,2,message])
                    curr_student.m_core["courses missing"] -= 1
                    
                elif curr_course.get_grade() >= letter_to_number.get("C-"):
                    message = " -  " + area_name
                    curr_student.m_core["courses done"].append([curr_course,1,message])
                    curr_student.m_core["courses missing"] -= 1
                    
                    
                elif tcourse.get_grade() >= letter_to_number.get("D-"):
                    message = " -  " + area_name
                    curr_student.m_majorelectives["courses done"].append([tcourse,3,message])
                    curr_student.m_core["courses missing"] -= 1
                    
                else:
                    message = " -  " + area_name
                    curr_student.m_majorelectives["courses done"].append([tcourse,0,message])
                    curr_student.m_core["courses missing"] -= 1


class IntAffairs_asfa22(Major):
    
    def __init__(self, namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, planner_type, major_key):
        super().__init__(namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, planner_type, major_key)

        self.counter_low = 2
        self.counter_substitutes = 2

    def course_found(self, curr_student, tcourse, counter):
        if tcourse.used_flag <2:     
            if tcourse.get_grade() == letter_to_number.get("current"):
                message = tcourse.course.get_name()
                curr_student.m_majorelectives["courses done"].append([tcourse,2,message])
                tcourse.used_flag = 2
                counter -= 1
                curr_student.m_majorelectives["courses missing"] -= 1
                
                if tcourse.course.get_number()>199 and tcourse.course.get_number()<300:
                    self.counter_low -= 1
                
                if tcourse.course.get_code()=="EC" or tcourse.course.get_code()=="HS":
                    self.counter_substitutes -= 1
                
            elif tcourse.get_grade() >= letter_to_number.get("D-"):
                message = tcourse.course.get_name()
                curr_student.m_majorelectives["courses done"].append([tcourse,1,message])
                tcourse.used_flag = 2
                counter -= 1
                curr_student.m_majorelectives["courses missing"] -= 1
                
                if tcourse.course.get_number()>199 and tcourse.course.get_number()<300:
                    self.counter_low -= 1
                
                if tcourse.course.get_code()=="EC" or tcourse.course.get_code()=="HS":
                    self.counter_substitutes -= 1

        return counter


    def exception_one(self, i, curr_student, reduced_courses_list):
        counter = i[0]
        curr_student.m_majorelectives["courses missing"] = i[0]
        
        codes_priority=["LAW", "PL"]
        codes_other=["EC", "HS"]
        
        self.counter_substitutes = 2
        self.counter_low = 2
        
        #loop over the list of courses that the student has done
        for tcourse in curr_student.reduced_courses_list:
            
            #we still need to find courses
            if counter>0:
            
                #first look for 300+
                if tcourse.used_flag <2 and (tcourse.course.get_number()>=300 and tcourse.course.get_number()<=1000):
                   
                    #first look for "safe codes"
                    for code in codes_priority:
                        if (tcourse.course.get_code().startswith(code) or tcourse.course.get_code().endswith(code)) and tcourse.used_flag <2:
                            #course was found
                            counter = self.course_found(curr_student, tcourse, counter)
        
        
        #loop over the list of courses that the student has done
        for tcourse in curr_student.reduced_courses_list:        
            #we still need to find courses
            if counter>0:
            
                #first look for 300+
                if tcourse.used_flag <2 and (tcourse.course.get_number()>=300 and tcourse.course.get_number()<=1000) and self.counter_substitutes>0:
                   
                    #first look for "EC" and "HS"
                    for code in codes_other:
                        if (tcourse.course.get_code().startswith(code) or tcourse.course.get_code().endswith(code)) and tcourse.used_flag <2:
                            #course was found
                            counter = self.course_found(curr_student, tcourse, counter)

                #then look for 200+
                if tcourse.used_flag <2 and (tcourse.course.get_number()>=200 and tcourse.course.get_number()<300) and self.counter_low>0:
                    if (tcourse.course.get_code()=="MA" and tcourse.course.get_number()==209) :
                        counter = self.course_found(curr_student, tcourse, counter)
                    
                    #first look for "safe codes"
                    for code in codes_priority:
                        if (tcourse.course.get_code().startswith(code) or tcourse.course.get_code().endswith(code)) and tcourse.used_flag <2:
                            #course was found
                            counter = self.course_found(curr_student, tcourse, counter)
        
        
        #loop over the list of courses that the student has done
        for tcourse in curr_student.reduced_courses_list:        
            #we still need to find courses
            if counter>0:    
                
                #then look for 200+
                if tcourse.used_flag <2 and (tcourse.course.get_number()>=200 and tcourse.course.get_number()<300) and self.counter_low>0 and self.counter_substitutes>0:
                    #looks for "EC" and "HS"
                    for code in codes_other:
                        if (tcourse.course.get_code().startswith(code) or tcourse.course.get_code().endswith(code)) and tcourse.used_flag <2:
                            #course was found
                            counter = self.course_found(curr_student, tcourse, counter)
        
        
class IntAffairs_priorfa22(Major):
    
    def __init__(self, namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, planner_type, major_key):
        super().__init__(namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, planner_type, major_key)

        self.counter_low = 2
        self.counter_substitutes = 2

    def course_found(self, curr_student, tcourse, counter):
        #print(f"found course {tcourse.course.get_name()}")
        if tcourse.get_grade() == letter_to_number.get("current"):
            message = tcourse.course.get_name()
            curr_student.m_majorelectives["courses done"].append([tcourse,2,message])
            tcourse.used_flag = 2
            counter -= 1
            curr_student.m_majorelectives["courses missing"] -= 1
            
            if tcourse.course.get_number()>199 and tcourse.course.get_number()<300:
                self.counter_low -= 1
            
            if tcourse.course.get_code()=="EC" or tcourse.course.get_code()=="HS":
                self.counter_substitutes -= 1
            
        elif tcourse.get_grade() >= letter_to_number.get("D-"):
            message = tcourse.course.get_name()
            curr_student.m_majorelectives["courses done"].append([tcourse,1,message])
            tcourse.used_flag = 2
            counter -= 1
            curr_student.m_majorelectives["courses missing"] -= 1
            
            if tcourse.course.get_number()>199 and tcourse.course.get_number()<300:
                self.counter_low -= 1
            
            if tcourse.course.get_code()=="EC" or tcourse.course.get_code()=="HS":
                self.counter_substitutes -= 1

        return counter


    def exception_one(self, i, curr_student, reduced_courses_list):
        #print("entered exception intl affairs")
        counter = i[0]
        #print(f"courses missing number {i[0]}")
        curr_student.m_majorelectives["courses missing"] = i[0]
        
        codes_priority=["LAW", "PL"]
        codes_other=["EC", "HS"]
        
        self.counter_substitutes = 2
        self.counter_low = 2
        
        #loop over the list of courses that the student has done
        for tcourse in curr_student.reduced_courses_list:
            
            #we still need to find courses
            if counter>0:
            
                #first look for 300+
                if tcourse.used_flag <2 and (tcourse.course.get_number()>=300 and tcourse.course.get_number()<=1000):
                   
                    #first look for "safe codes"
                    for code in codes_priority:
                        if (tcourse.course.get_code().startswith(code) or tcourse.course.get_code().endswith(code)) and tcourse.used_flag <2:
                            #course was found
                            counter = self.course_found(curr_student, tcourse, counter)
        
        
        #loop over the list of courses that the student has done
        for tcourse in curr_student.reduced_courses_list:        
            #we still need to find courses
            if counter>0:
            
                #first look for 300+
                if tcourse.used_flag <2 and (tcourse.course.get_number()>=300 and tcourse.course.get_number()<=1000) and self.counter_substitutes>0:
                   
                    #first look for "EC" and "HS"
                    for code in codes_other:
                        if (tcourse.course.get_code().startswith(code) or tcourse.course.get_code().endswith(code)) and tcourse.used_flag <2:
                            #course was found
                            counter = self.course_found(curr_student, tcourse, counter)

                #then look for 200+
                if tcourse.used_flag <2 and (tcourse.course.get_number()>=200 and tcourse.course.get_number()<300) and self.counter_low>0:                    
                    #first look for "safe codes"
                    for code in codes_priority:
                        if (tcourse.course.get_code().startswith(code) or tcourse.course.get_code().endswith(code)) and tcourse.used_flag <2:
                            #course was found
                            counter = self.course_found(curr_student, tcourse, counter)
        
        
        #loop over the list of courses that the student has done
        for tcourse in curr_student.reduced_courses_list:        
            #we still need to find courses
            if counter>0:    
                
                #then look for 200+
                if tcourse.used_flag <2 and (tcourse.course.get_number()>=200 and tcourse.course.get_number()<300) and self.counter_low>0 and self.counter_substitutes>0:
                    #looks for "EC" and "HS"
                    for code in codes_other:
                        if (tcourse.course.get_code().startswith(code) or tcourse.course.get_code().endswith(code)) and tcourse.used_flag <2:
                            #course was found
                            counter = self.course_found(curr_student, tcourse, counter)        
        
            
class PolScience_asfa22(Major):     
    
    def __init__(self, namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, planner_type, major_key):
        super().__init__(namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, planner_type, major_key)

        self.counter_low = 2
        self.counter_HS = 2
        self.counter_SOSC = 1

    def course_found(self, curr_student, tcourse, counter):
        #print(f"found course {tcourse.course.get_name()}")
        if tcourse.get_grade() == letter_to_number.get("current"):
            message = tcourse.course.get_name()
            curr_student.m_majorelectives["courses done"].append([tcourse,2,message])
            tcourse.used_flag = 2
            counter -= 1
            curr_student.m_majorelectives["courses missing"] -= 1
            curr_student.m_majorelectives["next_num"] += 1
            
            if tcourse.course.get_number()>199 and tcourse.course.get_number()<300:
                self.counter_low -= 1
            
            if tcourse.course.get_code()=="HS":
                self.counter_HS -= 1
                
            if tcourse.course.get_code()=="SOSC":
                self.counter_SOSC -= 1
                
            
        elif tcourse.get_grade() >= letter_to_number.get("D-"):
            message = tcourse.course.get_name()
            curr_student.m_majorelectives["courses done"].append([tcourse,1,message])
            tcourse.used_flag = 2
            counter -= 1
            curr_student.m_majorelectives["courses missing"] -= 1
            curr_student.m_majorelectives["next_num"] += 1
            
            if tcourse.course.get_number()>199 and tcourse.course.get_number()<300:
                self.counter_low -= 1
            
            if tcourse.course.get_code()=="HS":
                self.counter_HS -= 1
                
            if tcourse.course.get_code()=="SOSC":
                self.counter_SOSC -= 1

        return counter


    def exception_one(self, i, curr_student, reduced_courses_list):
        print("entered exception political sciences")
        counter = i[0]
        #print(f"courses missing number {i[0]}")
        curr_student.m_majorelectives["courses missing"] = i[0]
        
        codes_priority=["LAW", "PL"]
        #codes_other=["HS", "SOSC"]
        
        self.counter_low = 2
        self.counter_HS = 2
        self.counter_SOSC = 1
        
        #loop over the list of courses that the student has done
        for tcourse in curr_student.reduced_courses_list:
            
            #we still need to find courses
            if counter>0:
            
                #first look for 300+
                if tcourse.used_flag <2 and (tcourse.course.get_number()>=300 and tcourse.course.get_number()<=1000):
                   
                    #first look for "safe codes"
                    for code in codes_priority:
                        if (tcourse.course.get_code().startswith(code) or tcourse.course.get_code().endswith(code)) and tcourse.used_flag <2:
                            #course was found
                            counter = self.course_found(curr_student, tcourse, counter)
        
        
        #loop over the list of courses that the student has done
        for tcourse in curr_student.reduced_courses_list:        
            #we still need to find courses
            if counter>0:
            
                #first look for 300+
                if tcourse.used_flag <2 and (tcourse.course.get_number()>=300 and tcourse.course.get_number()<=1000): #and self.counter_substitutes>0:
                   #look for HS and SOSC separed because a student can take courses with either
                    if self.counter_HS>0:
                       if (tcourse.course.get_code().startswith("HS") or tcourse.course.get_code().endswith("HS")) and tcourse.used_flag <2:
                           #course was found
                           counter = self.course_found(curr_student, tcourse, counter)

                    if self.counter_SOSC>0:                  
                       if (tcourse.course.get_code().startswith("SOSC") or tcourse.course.get_code().endswith("SOSC")) and tcourse.used_flag <2:                            
                           #course was found
                           counter = self.course_found(curr_student, tcourse, counter)
                           

                #then look for 200+
                if tcourse.used_flag <2 and (tcourse.course.get_number()>=200 and tcourse.course.get_number()<300) and self.counter_low>0:                    
                    #first look for "safe codes"
                    for code in codes_priority:
                        if (tcourse.course.get_code().startswith(code) or tcourse.course.get_code().endswith(code)) and tcourse.used_flag <2:
                            #course was found
                            counter = self.course_found(curr_student, tcourse, counter)
        
        
        #loop over the list of courses that the student has done
        for tcourse in curr_student.reduced_courses_list:        
            #we still need to find courses
            if counter>0:    
                
                #then look for 200+
                if tcourse.used_flag <2 and (tcourse.course.get_number()>=200 and tcourse.course.get_number()<300): #and self.counter_low>0 and self.counter_substitutes>0:
                    if self.counter_HS>0:
                       if (tcourse.course.get_code().startswith("HS") or tcourse.course.get_code().endswith("HS")) and tcourse.used_flag <2:
                           #course was found
                           counter = self.course_found(curr_student, tcourse, counter)

                    if self.counter_SOSC>0:                  
                       if (tcourse.course.get_code().startswith("SOSC") or tcourse.course.get_code().endswith("SOSC")) and tcourse.used_flag <2:                            
                           #course was found
                           counter = self.course_found(curr_student, tcourse, counter)



class ClassicalStudies_asfa20(Major):     
    
    def __init__(self, namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, planner_type, major_key):
        super().__init__(namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, planner_type, major_key)

        self.latin = ""
        self.greek = ""

    """
    def course_found(self, curr_student, tcourse, counter):
        #print(f"found course {tcourse.course.get_name()}")
        if tcourse.get_grade() == letter_to_number.get("current"):
            #message = tcourse.course.get_name()
            curr_student.concentrations["courses done"].append([tcourse,2,message])
            tcourse.used_flag = 2
            counter -= 1
            curr_student.concentrations["courses missing"] -= 1
            #curr_student.concentrations["next_num"] += 1
            
            if tcourse.course.get_number()>199 and tcourse.course.get_number()<300:
                self.counter_low -= 1
            
            if tcourse.course.get_code()=="HS":
                self.counter_HS -= 1
                
            if tcourse.course.get_code()=="SOSC":
                self.counter_SOSC -= 1
                
            
        elif tcourse.get_grade() >= letter_to_number.get("D-"):
            message = tcourse.course.get_name()
            curr_student.m_majorelectives["courses done"].append([tcourse,1,message])
            tcourse.used_flag = 2
            counter -= 1
            curr_student.m_majorelectives["courses missing"] -= 1
            curr_student.m_majorelectives["next_num"] += 1
            
            if tcourse.course.get_number()>199 and tcourse.course.get_number()<300:
                self.counter_low -= 1
            
            if tcourse.course.get_code()=="HS":
                self.counter_HS -= 1
                
            if tcourse.course.get_code()=="SOSC":
                self.counter_SOSC -= 1

        return counter
    """
    
    def construct_languages(self, curr_student, tcourse):
        if tcourse.get_grade() == letter_to_number.get("current"):
            curr_student.concentrations["courses done"].append([tcourse,2,message])

    #two ancient language but must be in the same language
    def exception_one(self, i, curr_student, reduced_courses_list):
        print("language")  
        
        message = "Two Language (LAT/GRK) course (both in the same language)"
        curr_student.concentrations["courses done"].append(["", 1, message])
        
        
        message = "First Language course"
        for tcourse in curr_student.reduced_courses_list:
            
        
        
        message = "Second Language course"
        
        
        
    #concentrations
    def exception_two(self, i, curr_student, reduced_courses_list):
        print("concentrations")



"""        
def History(Major):
    
    def __init__(self, namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, planner_type, major_key):
        super().__init__(namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible, planner_type, major_key)

    
    def exception_one(self, i, curr_student, reduced_courses_list):
        
        possible_courses = {
            "Cognitive Area": [],
            "Developmental Area" : [],
            "Sociocultural Area" : [],
            "Psychobiology Area" : []            
            }
        message = "ONE 200/300-level HS from each area:"
        curr_student.m_core["courses done"].append(["", 1, message])
        
        ["Ancient History (before c. 500 C.E.)", "Medieval History (c. 500-1500 C.E.)", "Early Modern History (c. 1500-1800 C.E.)", "Modern History (c. 1800-2000 C.E.)"]

"""








        
def create_major_list():
    #with open('execution_files\majors_dictionaries.json', 'r') as myfile:
    with open('execution_files\json\majors_list.json', 'r') as myfile:   
       majors_dict = json.load(myfile)
      
    major_obj = []
    #print("\nConverting majors:")
    
    keys_list = majors_dict.keys()
    #print(keys_list)
    for i in keys_list:
        curr_major = majors_dict[i]
        #print(f"{i}")
        #print(i)
        
        for j in majors_dict[i]:

            if i == "BA Communications" or i == "BA Communications - Milan Exchange":                              
                major = Communications(i, curr_major['math requirement'], curr_major['additional requirements'], curr_major['core courses'], curr_major['major electives'], curr_major['electives description'], curr_major['planner_type'], curr_major['major key'])
            
            elif i == "BA International Affairs (as of Fall 2022)": 
                major = IntAffairs_asfa22(i, curr_major['math requirement'], curr_major['additional requirements'], curr_major['core courses'], curr_major['major electives'], curr_major['electives description'], curr_major['planner_type'], curr_major['major key'])

                
            elif i == "BA International Affairs (prior to Fall 2022)":
                major = IntAffairs_priorfa22(i, curr_major['math requirement'], curr_major['additional requirements'], curr_major['core courses'], curr_major['major electives'], curr_major['electives description'], curr_major['planner_type'], curr_major['major key'])

            elif i == "BA Political Science (prior to Fall 2022)":
                major = PolScience_asfa22(i, curr_major['math requirement'], curr_major['additional requirements'], curr_major['core courses'], curr_major['major electives'], curr_major['electives description'], curr_major['planner_type'], curr_major['major key'])
                
            elif i == "BA Psychological Science":
                major = Psychology(i, curr_major['math requirement'], curr_major['additional requirements'], curr_major['core courses'], curr_major['major electives'], curr_major['electives description'], curr_major['planner_type'], curr_major['major key'])

            else:
                major = Major(i, curr_major['math requirement'], curr_major['additional requirements'], curr_major['core courses'], curr_major['major electives'], curr_major['electives description'], curr_major['planner_type'], curr_major['major key'])
        #print(major.name)
        #print(major.add_req)
        #print(major.core_courses)
        #print(major.major_electives)
        major_obj.append(major)

    return major_obj     