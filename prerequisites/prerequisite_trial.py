# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 09:14:19 2023

@author: elettra.scianetti
"""

"""
Freshman  0-29
Sophomore 30-59
Junior    60-89
Senior    90-...
"""

#general structure expanded
prerequisites = {"specific course" : [{"id" : 0,
                                       "code": "", 
                                       "number": 0, 
                                       "grade": "", 
                                       "alternative" : 0, #should signal if there are more than one course that can be used to satisfy the requirement
                                       "placement": 0}],  #if the placement test can be used to waive the requirement
                 
                "course in category" : [{"code": "", 
                                         "number": 0, #this is the minimum number that the course code must have to satisfy the requirement
                                         "grade": "", 
                                         "alternative" : 0}], 
                
                "standing" : 0, #Freshman  0-29, Sophomore 30-59, Junior    60-89, Senior    90-...
                
                "corequisite" : [{"code": "", 
                                  "number": 0, 
                                  "grade": "", 
                                  "alternative" : 0,}],
                "placement" : 0, #some courses require a placement test to be put in that specific course i.e. en103, 
                                                  #although this info might not be available, so this field might be ignored
 }

#alternativa per gli "specific courses":
    # [numero di corsi da fare, [lista di dizionari con i corsi che valgono come alternative]]

#general structure condensed
prerequisites = {
    "specific course" : [{"id" : 0, "code": "", "num": 0, "grade": "", "alternative" : 0, "placement": 0}],
    "course in category" : [{"code": "", "num": 0, "grade": "", "alternative" : 0}], 
    "standing" : 0,
    "corequisite" : [{"code": "", "num": 0, "grade": ""}],
    "placement" : 1
 }
 

#example EN110
prerequisites = {
    "specific course" : [{"code": "EN", "num": 103, "grade": "C", "alternative" : 1},{"code": "EN", "num": 105, "grade": "C", "alternative" : 1}],
    #OR: "specific course" : [1, [{"code": "EN", "num": 103, "grade": "C", "placement": 1}, {"code": "EN", "num": 105, "grade": "C", "placement": 1}]]
    "placement" : 1
}

#example ETH/BUS 301
prerequisites = {
    "standing" : 60
    }