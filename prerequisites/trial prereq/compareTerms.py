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
            
    return larger
    
#first = "Sum II 2023"
#second = "Sum I 2023"

#print(compare(first, second))
