# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 18:14:26 2022

@author: ilda1
"""

"""
dditional_requirements = [["MA", 200, 0], ["FIN", 300, 1], ["FIN", 305, 1]]
...
in the check you will have

for i in range(0, len(additional_requirements)):{
        curr_course = additional_requirements[i]
        if curr_course[3] == 1:
            check for both additional_requirements[i] and additional_requirements[i+1]
            i = i+2
        else:
            check only additional_requirements[i]
            i = i+1
    }
resta da controllare se gli or sono gli ultimi della lista
se ci sono major con più di due alternative si può cambiare il numero in posizione 
curr_course[3] e aggiungere degli elif
"""

class Major:
    
    def __init__(self, namemajor, ma_req, additional_requirements_list, core_courses_list, major_elective_courses, major_electives_possible):
        self.name = namemajor
        self.ma_req = ma_req #=1 if MA101 required
        self.add_req = additional_requirements_list
        self.core_courses = core_courses_list
        self.major_electives = major_elective_courses
        self.explanation = major_electives_possible
                
    def get_name(self):
        return self.name
    
    def get_math_requirement(self):
        return self.ma_req
    
    def get_additional_requirements(self):
        return self.add_req    
    
    def get_core_courses(self):
        return self.core_courses
    
    def get_major_explanation(self):
        return self.explanation