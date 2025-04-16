def get_md_table(table_data) :
    header = table_data[0]
    body = table_data[1:]

    h_txt = ""
    for _ in header :
        row = _ + "|"
        h_txt += row
    h_txt += "\n"
    
    b_txt = ""
    for _ in body :
        for __ in _ :
            row = __ + "|"
            b_txt += row
        b_txt += "\n"

    return h_txt + b_txt

def list_to_str(strlist) :
    out = ""
    for s in strlist :
        if not s.isspace() and s != "." :
            out += s + "\n"
    return out

def get_clean_questions(raw_qg) :
    answer = raw_qg
    if "Deep Questions" in answer :
        answer = answer.split("Deep Questions")[1]
    if ": " in answer :
        answer = answer.split(":")[1]

    dQs = answer.split("\n")
    out = []
    for _ in dQs :
        if len(_) > 3 and not _.isspace() :
            out.append(_[3:])
    return out

def get_clean_answer(raw_qa) :
    answer = raw_qa

    while '"' in answer :
        answer = answer.replace('"', '')
    if "The final answer is" in answer :
        answer = answer.split("The final answer is")[-1]
    if "The answer is" in answer :
        answer = answer.split("The answer is")[-1]
    
    confidence = answer

    if "Confidence" in confidence :
        confidence = confidence.split("Confidence")[1]

    if "high" in confidence.lower() :
        confidence = "high"
    elif "middle" in confidence.lower() :
        confidence = "middle"
    else :
        confidence = "low"

    if "Answer" in answer :
        answer = answer.split("Answer")[1]

    if ": " in answer :
        answer = answer.split(": ")[1]

    if ";" in answer :
        answer = answer.split(";")[0]

    return answer, confidence 

def get_clean_hints(raw_qtoh) :
    hint = raw_qtoh

    if "Statement :" in hint :
        hint = hint.split("Statement : ")[-1]

    return hint