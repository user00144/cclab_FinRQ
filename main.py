import time
import json
from tqdm import tqdm
from utils.qa_utils import *
from config import *
from socratic_node import SocraticNode
from modules.forward import forward_process
from modules.backward import backward_process
from modules.common import direct_response, cot_zeroshot_response, cot_fewshot_response, eedp_response

with open("../test.json", "r") as f :
    test_data = json.load(f)

def init_data(data) :
    pretext_ = list_to_str(data["pre_text"])
    posttext_ = list_to_str(data["post_text"])
    tablemd_ = get_md_table(data["table"])

    context = f"""
Context(pre-text) : {pretext_}
Context(table) : {tablemd_}
Context(post-text) : {posttext_}
"""
    question = data["qa"]["question"]

    return SocraticNode(context, question, 0)

def run(root) :
    
    fstart = time.time()
    forward_process(root)
    fend = time.time()

    bstart = time.time()
    backward_process(root)
    bend = time.time()

    fspend = fend - fstart
    bspend = bend - bstart
    return root, fspend, bspend

def iter_main(iter) :

    i = 0

    save_json_file = f"./out/result_depth{MAX_DEPTH}_mq{MAX_QUESTION}_eedp2_{MODEL_NAME}{iter}.json"
    save_log_file = f"./logs/log_depth{MAX_DEPTH}_mq{MAX_QUESTION}_eedp2_{MODEL_NAME}{iter}.json"
    save_node_file = f"./node/node_log_depth{MAX_DEPTH}_mq{MAX_QUESTION}_eedp2_{MODEL_NAME}{iter}.json"

    result_list = []
    log_list = []
    node_list = []
    for tdata in tqdm(test_data) :
        root_node = init_data(tdata)
        ts_time = time.time()
        direct_result, raw_direct = direct_response(root_node)
        te_time = time.time()
        direct_time = te_time - ts_time

        cot_z_result, raw_z_cot = eedp_response(root_node)
        cot_z_time = 0

        ts_time = time.time()
        cot_f_result, raw_f_cot = cot_fewshot_response(root_node)
        te_time = time.time()
        cot_f_time = te_time - ts_time

        result_node, fspend, bspend = run(root_node)

        node_list_inner = []
        for ch in result_node.childs :
            node = {
                "q_no" : i,
                "main_question" : result_node.question,
                "sub_question" : ch.question,
                "answer" : ch.answer,
                "raw_answer" : ch.raw_answer
            }
            node_list_inner.append(node)
        node_list.append(node_list_inner)
        result = {
            "no" : i,
            "question" : result_node.question,
            "hints" : result_node.hints,
            "answer" : result_node.answer["answer"],
            "confidence" : result_node.answer["confidence"],
            "forward_time" : fspend,
            "backward_time" : bspend,
            "direct_time" : direct_time,
            "cot_zeroshot_time" : cot_z_time,
            "cot_fewshot_time" : cot_f_time,
            "answer_direct" : direct_result,
            "answer_zeroshot_cot" : cot_z_result,
            "answer_fewshot_cot" : cot_f_result,
        }



        log = {
            "no" : i,
            "question" : result_node.question,
            "socratic_answer" : result_node.raw_answer,
            "direct_answer" : raw_direct,
            "cot_zeroshot_answer" : raw_z_cot,
            "cot_fewshot_answer" : raw_f_cot,
        }

        log_list.append(log)
        result_list.append(result)
        with open(save_json_file, 'w') as json_file:
            json.dump(result_list, json_file, indent=4, ensure_ascii=False)
        with open(save_log_file, 'w') as json_file :
            json.dump(log_list, json_file, indent=4, ensure_ascii=False)
        with open(save_node_file, "w") as json_file :
            json.dump(node_list, json_file, indent=4, ensure_ascii=False)

        i += 1



iteration = 3
for it in range(iteration) :
    iter_main(it)

