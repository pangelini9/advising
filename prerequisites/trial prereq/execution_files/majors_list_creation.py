import pandas as pd
import json

def create_majors_dict():
    #name of the excel file that contains the data of the courses done by the student
    #filename = "../Majors-pat.xlsx"
    #filename = 'majors list.xlsx'
    filename = 'Majors list.xlsx'
    
    df = pd.read_excel(filename, "Esempi")
    
    print(df.keys())

    names = df["Major Name"] # Major name or type of entry (ADD, COR, ELC)
    reqs_nums = df["Math requirement"] # Math requirement 0/1 or number of courses
    elect_codes = df["Electives Description"] # Elective descriptions or code
    keys_lower = df["Major Key"] # Key of the major or lower bound
    upper = df["Unnamed: 4"] # None or upper bound
    
    majors_dict = {} # the general dictionary with all majors
    major = {} # the dict for each single major
    name = "" # the name of the major, which will be used as key for the general dictionary

    # the three lists that will be used in the dictionary of each major    
    add_reqs = []
    core_courses = []
    electives = []

    # the three current variables to handle the OR
    curr_add = ""
    curr_core = ""
    curr_el = ""
    
    for x in range(0,len(names)):
        print("Analyzing: ", names[x])
        # to skip empty lines
        if type(names[x]) is not float:
            
            split_name = names[x].split()
            print(split_name)
            if split_name[0] != "ADD" and split_name[0] != "COR" and split_name[0] != "ELC":
    
                # in this case, we are starting a new major
                
                # I first store the previous one, if any, into the main dictonary
                if name != "":
                    # add the three lists to the major
                    major["additional requirements"] = add_reqs
                    major["core courses"] = core_courses
                    major["major electives"] = electives
                    
                    # add the major to the dict of majors
                    majors_dict[name] = major

                    # I also need to reset the currents and the lists                    
                    add_reqs = []
                    core_courses = []
                    electives = []
                    curr_add = ""
                    curr_core = ""
                    curr_el = ""
                    
                # store the values into appropriate variables
                name = names[x]
                math = reqs_nums[x]
                description = elect_codes[x]
                key = int(keys_lower[x])
                
                major = {
                    "math requirement" : math,
                    "electives description" : description,
                    "major key" : key
                    }
                                
            else:
                # this is one of the requirements, so we store the values into variables
                
                code = str(elect_codes[x])
                lower_bound = int(keys_lower[x])
                upper_bound = int(upper[x])
                
                if split_name[0] == "ADD":
                    print(f"{curr_add}")          
                    
                    #if a new requirement is starting, we create a new list and remember the current
                    #if len(split_name)<1:
                    if curr_add != split_name[1]:
                        number = int(reqs_nums[x])
                        add_reqs.append([number, []])
                        curr_add = split_name[1]
                        
                    # we now add the current requirement to the list of additional requirements
                    add_reqs[-1][1].append([code, lower_bound, upper_bound])
                        
                elif split_name[0] == "COR":
                
                    # if a new requirement is starting, we create a new list and remember the current
                    if curr_core != split_name[1]:
                        number = int(reqs_nums[x])
                        core_courses.append([number, []])
                        curr_core = split_name[1]
                        
                    # we now add the current requirement to the list of core requirements                
                    core_courses[-1][1].append([code, lower_bound, upper_bound])

                elif split_name[0] == "ELC":
                    
                    # if a new requirement is starting, we create a new list and remember the current
                    if curr_el != split_name[1]:
                        number = int(reqs_nums[x])
                        electives.append([number, []])
                        curr_el = split_name[1]
                        
                    # we now add the current requirement to the list of elective requirements
                    electives[-1][1].append([code, lower_bound, upper_bound])
        
    # add the last major
    if name != "":
        major["additional requirements"] = add_reqs
        major["core courses"] = core_courses
        major["major electives"] = electives
        
        # add the major to the dict of majors
        majors_dict[name] = major
    
    print(majors_dict)
    
    with open("majors-new.json", "w") as myFile:
        json.dump(majors_dict, myFile, indent=2)
        

create_majors_dict()
