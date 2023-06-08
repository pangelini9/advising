# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 09:14:19 2023

@author: elettra.scianetti
"""
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
    }

#Freshman  0-29, Sophomore 30-59, Junior    60-89, Senior    90-...

"""""""""""""""""""""""""""""""""""""""
JSON STRUCTURE OF THE PREREQUISITE LIST
"""""""""""""""""""""""""""""""""""""""
#actual structure
dictionary_structure = {#shows two courses that both fullfuill the same requirement
                        "prerequisite": [ [{"code" : "",
                                            "lower bound" : 0,
                                            "upper bound" : 0,
                                            "grade" : 0.5,
                                            "standing" : 0}, #this is to be set !=0 only if there is a standing that fullfills the same requirement of this course
                                           {"code" : 0,
                                            "lower bound" : 0,
                                            "upper bound" : 0,
                                            "grade" : 0.5,
                                            "standing" : 0}
                                           ]],
                        
                        "standing" : 0, #Freshman  0-29, Sophomore 30-59, Junior    60-89, Senior    90-...
                        
                        #shows two courses that satisfy each a different requirement
                        "corequisite" : [[{"code" : "",
                                            "lower bound" : 0,
                                            "upper bound" : 0,
                                            "grade" : 0.5,
                                            "standing" : 0}], 
                                         
                                         [{"code" : "",
                                           "lower bound" : 0,
                                           "upper bound" : 0,
                                           "grade" : 0.5,
                                           "standing" : 0
                                           }]]
                        }

#condensed structure
dictionary_structure = {"prerequisite" : [[{}, {}]], #shows two courses that both fullfuill the same requirement
                        "standing" : 0,
                        "corequisite": [[{}], [{}]] #shows two courses that satisfy each a different requirement
                        }

#condensed structure
dictionary_structure = {"prerequisite" : [[{"code" : "", "lower bound" : 0, "upper bound" : 0, "grade" : 0.5, "standing" : 0}, {"code" : "", "lower bound" : 0, "upper bound" : 0, "grade" : 0.5, "standing" : 0}]],
                        "standing" : 0,
                        "corequisite": [[{"code" : "", "lower bound" : 0, "upper bound" : 0, "grade" : 0.5, "standing" : 0}], [{"code" : "", "lower bound" : 0, "upper bound" : 0, "grade" : 0.5, "standing" : 0}]]    
                        }



"""OLD VERSION
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
                
                "standing" : 0, 
                
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
"""




"""""""""""""""""""""""""""""""""""""""
JSON STRUCTURE OF THE COURSES LIST
"""""""""""""""""""""""""""""""""""""""
courses_list = [["Full name of the course", 
                "letter part of the code", 
                "number part of the code as integer", 
                "number of credits as integer", 
                "prerequisites written as the dictionary_structure", 
                "id number as integer"
                ],
                
                ["another course as above"]
                ]
#example
courses_list = [["Fine Arts Elective", "FA", 0, 3, [], 900],
                ["Greek Elective", "GRK", 0, 3, [], 901]
                ]

"""""""""""""""""""""""""""""""""""""""
JSON STRUCTURE OF THE STUDENTS LIST
"""""""""""""""""""""""""""""""""""""""



"""""""""""""""""""""""""""""""""""""""
JSON STRUCTURE OF THE MAJORS LIST
"""""""""""""""""""""""""""""""""""""""
majors_list = {"name of the major": {"math requirement" : "=1 if the major has MA101 as requirent, =0 if the major has either MA100 or MA101",
                                     
                                     "additional requirements" :  [["int(number of courses to do in this category", [["course code", "int(lower bound)", "int(upper bound)"]]]],
                                     #it is a list that contains a list for each of the additional requirements.
                                     #the first element of this second list is a number that tells you how many courses you have to pick for the requirement
                                     #after that number, there is a list that contains all courses that fullfill the same requirements
                                     #each of that course is a list as well
                                     #NB: if the course is specific just set lowe bound=upper bound
                                     
                                     "core courses" : ["same structure as additional requirements"],
                                     "major electives" : ["same structure as additional requirements"],
                                     
                                     "electives description" : "",
                                     #to be left empty because is it taken from the major
                                     
                                     "major key": 0
                                     #univocal number that identifies a major
                                    },
               
                }

"""
REQUIREMENTS EXAMPLE: 
    [[1, [["CS", 110, 110]]]] - There is only one requirement CS110
    
    [[3, [["EC", 300, 1000], ["FIN", 300, 1000]]] - The student has to do 3 courses either in Economics or in Finance at a level equal or higher than 300


"""

majors_list = {"Economics and Finance (prior to Fall 2021)": {"math requirement": 1, 
                                                              "additional requirements": [[1, [["CS", 110, 110]]], [1, [["MA", 197, 197]]], [1, [["MA", 198, 198]]], [1, [["MA", 208, 208]]], [1, [["FIN", 201, 201]]], [1, [["FIN", 202, 202]]], [1, [["EC", 201, 201]]], [1, [["EC", 202, 202]]]], 
                                                              "core courses": [[1, [["MA", 209, 209]]], [1, [["FIN", 301, 301]]], [1, [["EC", 301, 301]]], [1, [["EC", 302, 302]]], [1, [["EC", 316, 316]]], [1, [["EC", 360, 360]]], [1, [["EC", 350, 350], ["BUS", 301, 301]]], [1, [["FIN", 372, 372], ["EC", 372, 372]]], [1, [["EC", 480, 480]]]], 
                                                              "major electives": [[3, [["EC", 300, 1000], ["FIN", 300, 1000]]], [3, [["EC", 200, 1000], ["FIN", 200, 1000], ["BUS", 200, 1000], ["LAW", 200, 1000], ["MA", 200, 1000], ["MGT", 200, 1000], ["MKT", 200, 1000], ["PL", 200, 1000], ["PS", 200, 1000]]]], 
                                                              "electives description": "Six courses to be chosen from 200-level of higher BUS, EC, FIN, LAW, MA, MGT, MKT, PL or PS courses. At least three course must be 300-level EC or FIN courses.", 
                                                              "major key": 0
                                                              },
               "Finance" : {}
               }