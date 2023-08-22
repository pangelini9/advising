letter_to_number = {
    "P" : 5,
    "TR" : 4.5,
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
    "current" : 0.4,
    "W" : 0.3,
    "NP" : 0.2,
    "INC" : 0.1,
    "AU" : 0.01,
    "F" : 0,
    } 

number_to_letter = {
    5 : "P",
    4.5 : "TR",
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
    0.4 : "current",
    0.3 : "W",
    0.2 : "NP",
    0.1 : "INC", #incomplete
    0.01 : "AU",
    0 : "F",
    }


def compare(f, s):
    #current_semester, taken_semester
    """
    Input f and s: strings
    returns 1 if term f is after s, 2 if s is after, and 0 if they are the same
    """
    
    terms = {"Spring" : 1,
             "Sum I" : 2,
             "Sum i" : 2,
             "Sum II" : 3,
             "Sum ii" : 3,
             "Fall" : 4}
    
    larger = 0
    
    f_list = f.split()
    s_list = s.split()
    
    if int(f_list[-1]) > int(s_list[-1]):
        larger = 1
    elif int(f_list[-1]) < int(s_list[-1]):
        larger = 2
    else:
        f_term = f_list[0]
        if len(f_list) == 3:
            f_term = f_list[0] + " " + f_list[1]
        s_term = s_list[0]
        if len(s_list) == 3:
            s_term = s_list[0] + " " + s_list[1]
        
        if terms[f_term] > terms[s_term]:
            larger = 1
        elif terms[f_term] < terms[s_term]:
            larger = 2
        elif terms[f_term] == terms[s_term]:
            larger = 0
    #print(larger)        
    return larger
    
def check_code(courseCode, prefixes):
    """
    Input: 
        courseCode - str - code of the course, may be cross-listed
        prefixes - list(str) - list of prefixes
    
    Output: True iff the courseCode satisfies one of the prefixes
    """

    found = False
    
    for prefix in prefixes:
        if courseCode == prefix:
            
            found = True
        
        elif courseCode.startswith(prefix) and not courseCode[len(prefix)].isalpha():
            
            found = True
            
        elif courseCode.endswith(prefix) and not courseCode[-len(prefix)-1].isalpha():
            
            found = True
        
    return found
            
    
    