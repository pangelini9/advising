# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 08:26:28 2023

@author: ilda1
"""
"""
[{'major name' : "Economics and Finance",
'math requirement' : 1,
'additional requirements' : [[71,0], [56,0], [57,0], [58,0], [36,0], [37,0], [6,0], [7,0]],
'core courses' : [[59, 0], [40, 0], [10,0], [11,0], [14,0], [23,0], [22,1], [0,1], [50,0], [30,0]],
'major electives' : [[3, 300, ["EC", "FIN"]], [3, 200, ["EC", "FIN", "BUS", "LAW", "MA", "MGT", "MKT", "PL", "PS"]]],
'electives description' : "Six courses to be chosen from 200-level of higher BUS, EC, FIN, LAW, MA, MGT, MKT, PL or PS courses. At least three course must be 300-level EC or FIN courses.", 
'major key' : 0},

{'major name' : "Business Administration",
'math requirement' : 1,
'additional requirements' : [[71, 0], [57, 0], [58, 0]],
'core courses' : [[86, 0], [6, 0], [7, 0], [36, 0], [37, 0], [40, 0], [111, 0], [138, 0], [139, 0], [140, 0], [141, 0], [144, 0]],
'major electives' : [],
'electives description' : "Four courses at the 300-level or higher to be chosen from: BUS, EC, FIN, LAW, MGT, MKT courses, MA209, MA299 and 400-level MA courses", 
'major key' : 1},

{'major name' : "International Business",
'math requirement' : 1,
'additional requirements' : [[71, 0], [6, 0], [7, 0], [57, 0], [58, 0]],
'core courses' : [[86, 1], [104, 1], [36, 0], [37, 0], [40, 0], [115, 0], [138, 0], [139, 0], [140, 0], [141, 0], [91, 0], [142, 1], [143, 1], [100, 0]],
'major electives' : [4, 300, ["BUS", "EC", "FIN", "LAW", "MGT", "MKT"]],
'electives description' : "Four courses at the 300-level or higher to be chosen from: BUS, EC, FIN, LAW, MGT, MKT courses", 
'major key' : 2}]
"""


import json

majors_dict = {'Economics and Finance' : {'math requirement' : 1, 'additional requirements' : [[71,0], [56,0], [57,0], [58,0], [36,0], [37,0], [6,0], [7,0]], 'core courses' : [[59, 0], [40, 0], [10,0], [11,0], [14,0], [23,0], [22,1], [0,1], [50,0], [30,0]], 'major electives' : [[3, 300, ["EC", "FIN"]], [3, 200, ["EC", "FIN", "BUS", "LAW", "MA", "MGT", "MKT", "PL", "PS"]]], 'electives description' : "Six courses to be chosen from 200-level of higher BUS, EC, FIN, LAW, MA, MGT, MKT, PL or PS courses. At least three course must be 300-level EC or FIN courses.", 'major key' : 0}, 'Business Administration' : {'math requirement' : 1, 'additional requirements' : [[71, 0], [57, 0], [58, 0]], 'core courses' : [[86, 0], [6, 0], [7, 0], [36, 0], [37, 0], [40, 0], [111, 0], [138, 0], [139, 0], [140, 0], [141, 0], [144, 0]], 'major electives' : [], 'electives description' : "Four courses at the 300-level or higher to be chosen from: BUS, EC, FIN, LAW, MGT, MKT courses, MA209, MA299 and 400-level MA courses", 'major key' : 1}, 'International Business' : {'math requirement' : 1, 'additional requirements' : [[71, 0], [6, 0], [7, 0], [57, 0], [58, 0]], 'core courses' : [[86, 1], [104, 1], [36, 0], [37, 0], [40, 0], [115, 0], [138, 0], [139, 0], [140, 0], [141, 0], [91, 0], [142, 1], [143, 1], [100, 0]], 'major electives' : [4, 300, ["BUS", "EC", "FIN", "LAW", "MGT", "MKT"]], 'electives description' : "Four courses at the 300-level or higher to be chosen from: BUS, EC, FIN, LAW, MGT, MKT courses", 'major key' : 2}}

with open('majors_dictionaries.json', 'w') as outfile:
    json.dump(majors_dict, outfile)
    