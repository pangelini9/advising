# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 14:40:01 2023

@author: elettra.scianetti
"""

"Please copy the xml export with the students' data in the repository called 'prerequisites check' "
"and change 'file_name' below to match the name of that file"
file_name = "students.xml"







"IMPORT FUNCTIONS"
from Update_data import create_courses_list, create_student_json #converts the data of students stored in xml format into a json file
from execution_files.main_prerequisite import check_prerequisites #does the check on fullfilled prerequisites


"START THE ANALYSIS"
print("Importing courses' data...")
#create_courses_list()

print("\nConverting students' data...")#
#create_student_json(file_name)

print("\nStarting the check on prerequisites and retakes...")
check_prerequisites()
