from utils.client import request
from utils.qa_utils import *
from config import MAX_DEPTH

def QTOH_Module(node) :
    sys_prompt = f"""
### System Define
You are given a question-and-answer pair, con you help me to merge the question and answer into a statement sentence.
If the question or the answer is ambiguous you can just output the token "unknown". If the merged sentence is ambiguous, you can just output the token "unknown".
If you can merge the question-and-answer pair, just output the sentence.

### Input

Question : <Question>
Answer : <Answer>

### Output

Statement : <single statement sentence merged>

"""
    usr_prompt = f"""
    Question : {node.question}
    Answer : {node.answer["answer"]}
"""
    answer = request(sys_prompt, usr_prompt)
    clean_shint = get_clean_hints(answer)

    node.setShint(clean_shint)

def QA_Module(node) :

    if node.depth == 0 :
        important_note = """
<Instruction> 

Please carefully analyze the provided information, perform necessary numerical calculations, and
provide accurate answers to the given question using the provided data. Take into account the pre-text, table, and
post-text when formulating your response.
When performing numerical calculations, ensure you gather the required information and follow a step-by-step
approach.

1. Elicit the most relevant domain fact or knowledge that might be useful for you to extract the right operands and
forming the right approach to the problem.

2. Translate table data and Hints into sentences and identify gold evidence for answering the question.

3. Define a sequence of atomic operations (Add, Subtract, Divide, Multiply, Greater, Min, Max, Exp) which take
into account only two operands at a time. Divide a complex task into a sequence of atomic operations defined
above.

4. Finally, conclude as: explanation + The final answer is [Answer: "<final answer>";].
        """
        #        

    else :
        important_note = """
<Instruction> 

Please carefully analyze the provided information, perform necessary numerical calculations, and
provide accurate answers to the given question using the provided data. Take into account the pre-text, table, and
post-text when formulating your response.
When performing numerical calculations, ensure you gather the required information and follow a step-by-step
approach.

1. Elicit the most relevant domain fact or knowledge that might be useful for you to extract the right operands and
forming the right approach to the problem.

2. Translate table data and Hints into sentences and identify gold evidence for answering the question.

3. Define a sequence of atomic operations (Add, Subtract, Divide, Multiply, Greater, Min, Max, Exp) which take
into account only two operands at a time. Divide a complex task into a sequence of atomic operations defined
above.

4. Finally, conclude as: explanation + The final answer is [Answer: "<final answer>";].

"""

    sys_prompt = f"""
### System Define
Imagine you are an logical student.
You are given a financial question. Please use your best judgment to answer it step by step and provide your confidence level.
If there are hints, indicate which ones you used.

{important_note}


"""
    
# ### Important Note
# This is the final question. 
# Please use your best judgement to answer the question step by step.
# If there are some hints, consider the hints.
# You should provide a final answer as a single float, millions , integer, percentage, or yes/no.
# For example : The final answer is [Answer : "311 millions";] , The final answer is [Answer : "13.38%";] , The final answer is [Answer : "Yes";] ...
# Note: Form of output is: 
# <explanation> + The final answer is [Answer: "<final answer>";].

#     ### Important Note
# This is financial sub question. you should provide answer to question according to context.
# Analyze the question and extract the key evidence from the <Context>. , Specify the exact Context reference.
# You should set the confidence level low when you cannot find any evidence from the context.

# Note: Form of output is: 
# <explanation> + The final answer is [Answer: "<final answer>"; Used hints: "<hints ID or None>"; Confidence: "<low, middle, or high>"].


#     ### Demonstration
# Question : what is the total value of purchased shares during october 2017 , in millions?

# Hints : (1) total number of shares puchased in October 2017 is 10,676. 

# Answer : 
# - According the context, Hints (1) "total number of shares puchased in October 2017 is 10,676" confidence is High.

# 1. To find the total value of purchased shares during October 2017, we need to multiply the total number of shares purchased by the average price paid per share for that period.
# 2. From the hint 1, the total number of shares purchased in October 2017 is 10,676.
# 3. The average price paid per share in October 2017 is $104.10.
# 4. Calculate the total value: 10,676  * 104.10 = 1,111,431.60.
# 5. Convert this value into millions: $1,111,431.60 / 1,000,000 = $1.111 million.

# The final answer is : [Answer: "$1.111 million";, Used hints : "1"; , Confidence: "high";]



# ### Demonstration
# Question : what is the total value of purchased shares during october 2017 , in millions?

# Hints : (1) total number of shares puchased in October 2017 is 10,676. 

# Answer : 
# 1. To find the total value of purchased shares during October 2017, we need to multiply the total number of shares purchased by the average price paid per share for that period.
# 2. From the hint 1, the total number of shares purchased in October 2017 is 10,676.
# 3. The average price paid per share in October 2017 is $104.10.
# 4. Calculate the total value: 10,676  * 104.10 = 1,111,431.60.
# 5. Convert this value into millions: $1,111,431.60 / 1,000,000 = $1.111 million.

# The final answer is : [Answer: "$1.111 million";, Used hints : "1"; , Confidence: "high";]
#Question : What were the specific performance milestones prescribed for the equity awards granted in 2012?

# Hints : 

# Answer : To determine the specific performance milestones prescribed for the equity awards granted in 2012, we need to examine the context provided. 
# The context mentions that performance-based awards were issued to certain executive officers and members of senior management, which would vest upon the achievement of prescribed service milestones by the award recipients and revenue performance milestones by the company. 
# However, the specific details of these performance milestones are not explicitly stated in the context.

# The final answer is : [Answer: "Unknown";, Used hints : "None";, Confidence: "low";]


# Question : How is the equity award compensation expense calculated for equity granted during the year 2012?

# Hints : 

# Answer :
# The equity award compensation expense is calculated based on the fair value of the equity awards at the grant date.
# For the year ended March 31, 2012, the weighted average grant-date fair value for restricted stock and restricted stock units was $18.13 per share.
# The total number of shares granted during the year was 607,000.
# The compensation expense is recognized over the period in which the service and performance conditions are expected to be met.
# The company recorded $3.3 million in stock-based compensation expense for equity awards in which the prescribed performance milestones have been achieved or are probable of being achieved.\n6. The remaining unrecognized compensation expense related to these equity awards at March 31, 2012, is $3.6 million, with a weighted-average period of 2.1 years over which this cost will be recognized.

# The final answer is : [Answer: "The equity award compensation expense for equity granted during the year 2012 is calculated based on the grant-date fair value of $18.13 per share, with a total of $3.3 million recorded for achieved or probable performance milestones, and $3.6 million remaining unrecognized, to be recognized over 2.1 years.";, Used hints : "None"; , Confidence: "high";]\n        
    if node.depth == 0 :
        user_prompt = f"""
    Context : {node.context}
    Hints : {node.get_textHints()}
    Question : {node.question}
    """
    else :
        user_prompt = f"""
    Context : {node.context}
    Hints : {node.get_textHints()}
    Question : {node.question}
    """
    raw_answer = request(sys_prompt, user_prompt)
    clean_answer, confidence = get_clean_answer(raw_answer)

    node.update_answer(clean_answer, confidence)
    node.raw_answer = raw_answer

    QTOH_Module(node)

from collections import defaultdict


def group_by_depth(root):
    depth_map = defaultdict(list)
    stack = [root]

    while stack:
        node = stack.pop()
        depth_map[node.depth].append(node)
        for child in node.childs:
            stack.append(child)

    return depth_map

def backward_process(root) :
    depth_map = group_by_depth(root)
    for i in reversed(range(MAX_DEPTH+1)) :
        nodes = depth_map[i]
        for node in nodes :
            node.update_hint()
            QA_Module(node)
            

