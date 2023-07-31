"""
p_list = ["part name" , "name that will be printed on the degree planner", "explanation"]
planner_parts_list.append(p_list)

should out in the same list both the name and the explanation

"""

banner_list = {
    #additional requirements
    "structure_one": {
        "A" : ["A. Proficiency and General Distribution Requirements", ""], 
        "B" : ["B. Additional Requirements", ""],
        "C" : ["C. Core Courses", "No more that two core courses might be passed with a grade lower than C-"],
        "D" : ["D. Major Electives Courses", ""],
        "G" : ["Legend", ""],
        "H" : ["General Information", ""],
        "I" : ["Courses Missing by Section", ""],
        "L" : ["Minors", ""],
        "E" : ["E. Minor in", "Total of 6 courses (check the website for specific requirements). No more than 3 courses may apply to both the major and minor"],
        "F" : ["F. Minor in", "Total of 6 courses (check the website for specific requirements). No more than 3 courses may apply to both the major and minor"],
        "eng" : ["English Composition and Literature", "Approved subsititutes for the second EN LIT course are: CL268, CL278, ITS292, ITS/EN 295"],
        "math" : ["Math Proficiency", "A grade of C- or higher is required"],
        "sci" : ["Math, Science, Computer Science", "2 courses to be chosen from: MA, NS, CS"],
        "fl" : ["Foreign Language", "A grade of C or higher is required"],
        "sosc" : ["Social Sciences", "2 courses to be chosen from: COM, CMS, DMA, DJRN, EC, GEOG, PL, PS, SOSC"],
        "hum" : ["Humanities", "2 courses to be chosen from: CL, EN LIT, GRK, HM, HS, ITS, LAT, PH, RL"],
        "fa" : ["Fine Arts", "1 course to be chosen from: AH, ARCH, AS, CW, DR, MUS"], 
        "genel" : ["General Electives", "Sufficient to give a total of 120 credits"]
        },
    
    #only core courses, AND concentrations in the major electives
    "structure_two": {
        "A" : ["A. Proficiency and General Distribution Requirements", ""], 
        "B" : ["B. Core Courses", "No more that two core courses might be passed with a grade lower than C-"],
        "C" : ["C. Major Electives Courses", ""],
        "G" : ["Legend", ""],
        "H" : ["General Information", ""],
        "I" : ["Courses Missing by Section", ""],
        "L" : ["Minors", ""],
        "D" : ["D. Minor in", "Total of 6 courses (check the website for specific requirements). No more than 3 courses may apply to both the major and minor"],
        "E" : ["E. Minor in", "Total of 6 courses (check the website for specific requirements). No more than 3 courses may apply to both the major and minor"],
        "eng" : ["English Composition and Literature", "Approved subsititutes for the second EN LIT course are: CL268, CL278, ITS292, ITS/EN 295"],
        "math" : ["Math Proficiency", "A grade of C- or higher is required"],
        "sci" : ["Math, Science, Computer Science", "2 courses to be chosen from: MA, NS, CS"],
        "fl" : ["Foreign Language", "A grade of C or higher is required"],
        "sosc" : ["Social Sciences", "2 courses to be chosen from: COM, CMS, DMA, DJRN, EC, GEOG, PL, PS, SOSC"],
        "hum" : ["Humanities", "2 courses to be chosen from: CL, EN LIT, GRK, HM, HS, ITS, LAT, PH, RL"],
        "fa" : ["Fine Arts", "1 course to be chosen from: AH, ARCH, AS, CW, DR, MUS"], 
        "genel" : ["General Electives", "Sufficient to give a total of 120 credits"]
        },
    
    #concentrations below core
    "structure_three": {
        "A" : ["A. Proficiency and General Distribution Requirements", ""], 
        "B" : ["B. Core Courses", "No more that two core courses might be passed with a grade lower than C-"],
        "C" : ["C. Chosen Track", ""],
        "D" : ["D. Major Electives Courses", ""],
        "G" : ["Legend", ""],
        "H" : ["General Information", ""],
        "I" : ["Courses Missing by Section", ""],
        "L" : ["Minors", ""],
        "E" : ["E. Minor in", "Total of 6 courses (check the website for specific requirements). No more than 3 courses may apply to both the major and minor"],
        "F" : ["F. Minor in", "Total of 6 courses (check the website for specific requirements). No more than 3 courses may apply to both the major and minor"],
        "eng" : ["English Composition and Literature", "Approved subsititutes for the second EN LIT course are: CL268, CL278, ITS292, ITS/EN 295"],
        "math" : ["Math Proficiency", "A grade of C- or higher is required"],
        "sci" : ["Math, Science, Computer Science", "2 courses to be chosen from: MA, NS, CS"],
        "fl" : ["Foreign Language", "A grade of C or higher is required"],
        "sosc" : ["Social Sciences", "2 courses to be chosen from: COM, CMS, DMA, DJRN, EC, GEOG, PL, PS, SOSC"],
        "hum" : ["Humanities", "2 courses to be chosen from: CL, EN LIT, GRK, HM, HS, ITS, LAT, PH, RL"],
        "fa" : ["Fine Arts", "1 course to be chosen from: AH, ARCH, AS, CW, DR, MUS"], 
        "genel" : ["General Electives", "Sufficient to give a total of 120 credits"]
        }
    }