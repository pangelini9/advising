# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 14:23:50 2023

@author: elettra.scianetti
"""

for loop sui current course:
    di ogni corso prende prerequisites e corequisites e li mette in req_list:
    control_var1 = 0
    for loop su req_list:
        if control_var1 == 0: #ITERAZIONE 1 == PREREQUISITES
            control_var1 += 1
            for loop sulla lista di prerequisites:
                control_var2 = len(lista di corsi alternativi)
                for loop sui corsi in alternative per ogni prerequisite (=h):
                    prendi caratteristiche di h
                    if control_var2 =! 0 and found == False:
                        control_var2 -= 1
                        for loop sui corsi che lo studente ha fatto nei previous semestri (in noncurrent_courses, =course_done):
                            prendi caratteristiche di course_done
                            if caratteristiche di course_done at least caratteristiche di h:
                                rimuovi prerequisito (=j)
                                found = True                        
                                break
                            
                    elif control_var2 == 0 and found == False:
                        lo studente non ha il prerequisito su cui si sta iterando
                        aggiungi il prereqisito alla lista di missing prereq 
                        break
                        
                    else:
                        break
            

        elif control_var1 == 1: #ITERAZIONE 2 == COREQUISITES
        
        
        
"*********************************************************************************************************"

    def check_requirements(self):
        #for loop sui current course:
        for m in self.current_courses[:]:
            #di ogni corso prende prerequisites e corequisites e li mette in req_list:
                current_prerequisites1 = m.course.get_requirements_dictionary() # current_prerequisites1 = {"prerequisite" : [[{}, {}]], "corequisite": [[{}], [{}]]}
                current_prerequisites = current_prerequisites1["prerequisite"] # current_prerequisites = [[{}, {}], [{}, {}]], all the requirements
                current_corequisite = current_prerequisites1["corequisite"] # current_corequisite = [[{}, {}], [{}, {}]]
                req_list = []
                req_list.append(current_prerequisites)
                req_list.append(current_corequisite)
                
                control_var1 = 0 #so that if ==0 checks prerequisites, and if ==1 checks corequisites even if the lists are empty
                
                #for loop su req_list:
                for req in req_list[:]: #first checks prereq then coreq
                    info_list = [] #will contain the name of the current courses that do not satisfy the requirements in addition to the missing requirements
                    missing_req = {"prerequisites" : [], "corequisite" : []} #will contain the missing requirement, will be different for each of the courses
                    
                    #ITERAZIONE 1 == PREREQUISITES
                    if control_var1 == 0: 
                        control_var1 += 1 #so that next iteration is corequisites
                        found = False #so that we know if one of the alternatives for the requirement has been found
                        #for loop sulla lista di prerequisites:
                        for alternatives_for_req in req[:]: #alternatives_for_req = [{}, {}, {}, {}], all the courses that satisfy a single requirement    
                            control_var2 = len(alternatives_for_req) #aka len(lista di corsi alternativi)
                            
                            #for loop sui corsi in alternative per ogni prerequisite:
                            for alternative in alternatives_for_req[:]: #alternative = one course. 
                                #Further, h = {"code" : "", "lower bound" : 0, "upper bound" : 0, "grade" : 0.5}
                                
                                #extrapolate characteristics of the course that satisfies a requirement
                                prereq_grade = alternative["grade"]
                                lower_bound = alternative["lower bound"]
                                upper_bound = alternative["upper bound"]
                                #modify values to avoid the null problem
                                if math.isnan(prereq_grade):
                                    prereq_grade = "D-"
                                if math.isnan(upper_bound):
                                    upper_bound = 1000
                                
                                #case 1: prereq not found but there are still alternatives to look into
                                if control_var2 =! 0 and found == False:
                                    control_var2 -= 1
                                    
                                    #for loop sui corsi che lo studente ha fatto nei previous semestri (in noncurrent_courses, =course_done):
                                    for course_done in self.noncurrent_courses[:]:
                                        taken_code = course_done.course.get_code()
                                        taken_num = course_done.course.get_number()
                                        taken_grade = course_done.get_grade()    
                                        if taken_code==alternative["code"] and (int(taken_num)>=int(lower_bound) and int(taken_num)<=int(upper_bound)) and taken_grade>=letter_to_number.get(prereq_grade):
                                            #one requirement in the list is fullfilled
                                            current_prerequisites.remove(alternatives_for_req)
                                            found = True
                                            break
                                        
                                #case 2: prereq not found in any of the alternatives     
                                elif control_var2 == 0 and found == False:
                                    #aggiungi il prereqisito alla lista di missing prereq
                                    missing_req["prerequisites"].append(alternatives_for_req)
                                    break
                                
                                #case 3: the student has satisfied the prerequisite
                                else:
                                    break

                    #ITERAZIONE 2 == COREQUISITES
                    elif control_var1 == 1:
                        found = False #so that we know if one of the alternatives for the requirement has been found
                        #for loop sulla lista di prerequisites:
                        for alternatives_for_req in req[:]: #alternatives_for_req = [{}, {}, {}, {}], all the courses that satisfy a single requirement    
                            control_var2 = len(alternatives_for_req) #aka len(lista di corsi alternativi)
                            
                            #for loop sui corsi in alternative per ogni prerequisite:
                            for alternative in alternatives_for_req[:]: #alternative = one course. 
                                #Further, h = {"code" : "", "lower bound" : 0, "upper bound" : 0, "grade" : 0.5}
                                
                                #extrapolate characteristics of the course that satisfies a requirement
                                prereq_grade = alternative["grade"]
                                lower_bound = alternative["lower bound"]
                                upper_bound = alternative["upper bound"]
                                #modify values to avoid the null problem
                                if math.isnan(prereq_grade):
                                    prereq_grade = "D-"
                                if math.isnan(upper_bound):
                                    upper_bound = 1000
                                
                                #case 1: prereq not found but there are still alternatives to look into
                                if control_var2 =! 0 and found == False:
                                    control_var2 -= 1
                                    
                                    #for loop sui corsi che lo studente ha fatto nei previous semestri (in noncurrent_courses, =course_done):
                                    for course_done in self.noncurrent_courses[:]:
                                        taken_code = course_done.course.get_code()
                                        taken_num = course_done.course.get_number()
                                        taken_grade = course_done.get_grade()    
                                        if taken_code==alternative["code"] and (int(taken_num)>=int(lower_bound) and int(taken_num)<=int(upper_bound)) and taken_grade>=letter_to_number.get(prereq_grade):
                                            #one requirement in the list is fullfilled
                                            current_prerequisites.remove(alternatives_for_req)
                                            found = True
                                            break
                                        
                                #case 2: prereq not found in any of the alternatives     
                                elif control_var2 == 0 and found == False:
                                    #aggiungi il prereqisito alla lista di missing prereq
                                    missing_req["corequisites"].append(alternatives_for_req)
                                    break
                                
                                #case 3: the student has satisfied the prerequisite
                                else:
                                    break     
                
                #check if both prereq and coreq are empty, if so, do not add to the missing req list                
                if len(missing_req["prerequisites"]) == 0 and len(missing_req["corequisites"]) == 0:
                    break
                else:
                    info_list.append([m,missing_req])
                    self.req_not_satisfied.append(info_list)






















        