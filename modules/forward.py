from utils.client import request
from utils.qa_utils import *
from config import MAX_QUESTION

def QG_Module(node) :
    max_questions = int(MAX_QUESTION / (node.depth + 1))
    if max_questions < 1 :
        max_questions = 1

    sys_prompt = f"""
    ### System Define
    Imagine you are a thoughtful and logical question-raiser.
    You are given a financial question.
    Your role is to make a question that asks for just one key idea to solve this problem.
    Remember, to understand this question, you need to identify one important question.
    Think of it as a step-by-step process to create a question.

    Note: form of output is  :
    <explanation> 
    Deep Questions :
    1. <Deep Question>
    """
    
    # - Each raised question must be self-contained, meaning it should include context if needed.
    # - Do not use pronouns or indefinite pronoun phrases in the generated questions.
    # - Each question should contain only one argument.

    user_prompt = f"""
Context : {node.context}
Question : {node.question}
"""
    raw_answer = request(sys_prompt, user_prompt)
    return node.make_child(raw_answer)

def forward_process(node) :
    if not node.isLeaf :
        flg = QG_Module(node)
    if node.hasChild() :
        for child in node.childs :
            forward_process(child)