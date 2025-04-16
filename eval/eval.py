import re
import json
import os
from glob import glob
from tqdm import tqdm

# answer

# 1. float
# 2. percentage : x.x% / x%
# 3. int
# 4. yes / no
# 소수점 아래 몇자리까지 있는지 확인(float, percentage 유형의 경우)


# $ 있을경우 -> float or int
# % 있을경우 -> percentage / "answer" > %없애고, split(.) len(pre) / len(post)
# yes/no 있을경우 -> yes / no

# million 있는 경우에는 100만 곱하기(0 6개)

RESULTS = "../out"
LOGS = "../logs"

result_list = glob(os.path.join(RESULTS, "*.json"))

pattern = r"-?\d+(?:\.\d+)?"

def filter_string(s):
    s = s.lower()
    allowed_chars = set("0123456789.-")
    allowed_words = {"yes", "no"}

    result = []
    temp_word = ""

    for char in s:
        if char in allowed_chars:
            result.append(char)
        else:
            temp_word += char
            if temp_word in allowed_words:
                result.append(temp_word)
                temp_word = ""

    return ''.join(result)


class Answer :
    def __init__(self, ans, gt) :
        self.ans = ans
        self.gt = filter_string(gt)
    
    def check_correct(self) :
        if self.gt == "" :
            for a in self.ans :
                if a == "" :
                    return 1
        
        if "yes" in self.gt.lower() :
            for a in self.ans :
                if a.lower() == "yes" :
                    return 1
        
        if "no" in self.gt.lower() :
            for a in self.ans :
                if a.lower() == "no" :
                    return 1

        try :
            if "." in self.gt :
                gt_splited = self.gt.split(".")
                len_gt = len(gt_splited[1])
                if gt_splited[1] in ['0', '00'] :
                    for a in self.ans :
                        if str(int(round(float(a),0))) == str(int(float(self.gt))) :
                            return 1
                for a in self.ans :
                    if str(round(float(a), len_gt)) == self.gt :
                        return 1
            else : 
                for a in self.ans :
                    if str(int(round(float(a), 0))) == self.gt :
                        return 1
        except ValueError :
            return 0
        return 0
    

def process_answer(text) :
    if text and text[-1] == "." :
        text = text[:-2]
    text_clean = filter_string(text)
    answer_out = []
    # all_numbers = re.findall(pattern,text)
    # answer_out += all_numbers

    if not text_clean or text_clean.isspace() :
        answer_out.append("")
        return answer_out


    if "yes" in text.lower() or "no" in text.lower() :
        if "yes" in text.lower() :
            answer_out.append("yes")
        else :
            answer_out.append("no")

        return answer_out
    try :
        if "decrease" in text :
            text_clean = "-" + text_clean
        if "million" in text :
            answer_out.append(text_clean)
            answer_out.append(str(float(text_clean) * 1000000))
            return answer_out
        # case float
        if "." in text_clean :
            answer_out.append(text_clean)
            return answer_out
        else :
            answer_out.append(text_clean)
            return answer_out
    except ValueError :
        answer_out.append("")
        return answer_out


with open("../../test.json", "r") as f :
    gt_data = json.load(f)


def eval(json_file) :
    fname = json_file.split("/")[-1][:-5]
    with open(os.path.join(LOGS, fname.replace("result","log")+".json")) as f :
        log_data = json.load(f)

    with open(os.path.join("../node", "node_"+fname.replace("result", "log")+".json")) as f :
        node_data = json.load(f)

    with open(json_file, "r") as f :
        result_data = json.load(f)

    total_len = len(result_data)
    socratic_answers = 0
    direct_answers = 0
    cot_z_answers = 0
    cot_f_answers = 0

    good_cases = []
    bad_cases = []
    good_log = []
    bad_log = []
    wrong_node = []
    wrong_cases = []

    for i in range(total_len) :
        gt = gt_data[i]["qa"]["answer"]
        socratic_answer = Answer(process_answer(result_data[i]["answer"]), gt)
        direct_answer = Answer(process_answer(result_data[i]["answer_direct"]), gt)
        cot_z_answer = Answer(process_answer(result_data[i]["answer_zeroshot_cot"]), gt)
        cot_f_answer = Answer(process_answer(result_data[i]["answer_fewshot_cot"]), gt)

        socratic_ = socratic_answer.check_correct()
        direct_ = direct_answer.check_correct()
        cotz_ = cot_z_answer.check_correct()
        cotf_ = cot_f_answer.check_correct()

        socratic_answers += socratic_
        direct_answers += direct_
        cot_z_answers += cotz_
        cot_f_answers += cotf_

        if socratic_ == 1 and direct_ == 0 and cotf_ == 0 and cotz_ == 0 :
            str_dict = {
                "question" : result_data[i]["question"],
                "gt" : gt,
                "socratic_answer" : result_data[i]["answer"],
                "cot_zeroshot_answer" : result_data[i]["answer_zeroshot_cot"],
                "cot_fewshot_answer" : result_data[i]["answer_fewshot_cot"],
                "direct_answer" : result_data[i]["answer_direct"],
                "socratic_hints" : result_data[i]["hints"]
            }
            good_log.append(log_data[i])
            good_cases.append(str_dict)
        if socratic_ == 0 and direct_ == 1 and cotf_ == 1 and cotz_ == 1:
            str_dict = {
                "question" : result_data[i]["question"],
                "gt" : gt,
                "socratic_answer" : result_data[i]["answer"],
                "cot_zeroshot_answer" : result_data[i]["answer_zeroshot_cot"],
                "cot_fewshot_answer" : result_data[i]["answer_fewshot_cot"],
                "direct_answer" : result_data[i]["answer_direct"],
                "socratic_hints" : result_data[i]["hints"]
            }
            bad_log.append(log_data[i])
            bad_cases.append(str_dict)
        
        if socratic_ == 0 :
            str_dict = {
                "question" : result_data[i]["question"],
                "gt" : gt,
                "program" : gt_data[i]["qa"]["program"],
                "gold_inds" : gt_data[i]["qa"]["gold_inds"],
                "answer" : result_data[i]["answer"],
                "hints" : result_data[i]["hints"],
                "log" : log_data[i]["socratic_answer"]
            }
            wrong_cases.append(str_dict)
            wrong_node.append(node_data[i])


    dem = 2

    os.makedirs(f"./{fname}", exist_ok=True)

    good_json_file = f"./{fname}/good_cases.json"
    with open(good_json_file, 'w') as json_file:
        json.dump(good_cases, json_file, indent=4, ensure_ascii=False)

    bad_json_file = f"./{fname}/bad_cases.json"
    with open(bad_json_file, 'w') as json_file :
        json.dump(bad_cases, json_file, indent=4, ensure_ascii=False)

    good_log_json_file = f"./{fname}/good_log.json"
    with open(good_log_json_file, 'w') as json_file :
        json.dump(good_log, json_file, indent=4, ensure_ascii=False)

    bad_log_json_file = f"./{fname}/bad_log.json"
    with open(bad_log_json_file, 'w') as json_file :
        json.dump(bad_log, json_file, indent=4, ensure_ascii=False)

    wrong_case_json_file = f"./{fname}/wrong_cases.json"
    with open(wrong_case_json_file, 'w') as json_file :
        json.dump(wrong_cases, json_file, indent=4, ensure_ascii=False)


    wrong_node_json_file = f"./{fname}/wrong_node.json"
    with open(wrong_node_json_file, 'w') as json_file :
        json.dump(wrong_node, json_file, indent=4, ensure_ascii=False)

    acc_socratic = round(socratic_answers/total_len * 100, dem)
    acc_direct = round(direct_answers/total_len * 100, dem)


    print(fname)
    print("====== Accuracy =======")
    print("Ours : ", acc_socratic, "%")
    print("CoT : ", round(cot_f_answers/total_len * 100, dem), "%")
    print("EEDP : ", round(cot_z_answers/total_len * 100, dem), "%")
    print("Direct : ", acc_direct, "%")

for result_json in result_list :
    eval(result_json)
    print("\n\n")
