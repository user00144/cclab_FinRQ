from utils.client import request
from utils.qa_utils import *


def direct_response(node) :
    sys_prompt = f"""
### System Define
You are given a question. Please answer the question directly.
Note: Form of output is: The final answer is [Answer: "final answer";].

"""
    usr_prompt = f"""
Context : {node.context}
Question : {node.question}
    """

    answer = request(sys_prompt, usr_prompt)
    clean_answer, confidence = get_clean_answer(answer)
    

    return clean_answer, answer

def cot_zeroshot_response(node) :
    sys_prompt = f"""
### System Define
You are given a question.
Please answer the question following step-by-step thinking process.

- Extract important evidence from the context.
- Make an executable equation.
- Calculate the equation and provide the final answer.

Note: Form of output is : explanation + The final answer is [Answer: "final answer";].
"""

    usr_prompt = f"""
Context : {node.context}
Question : {node.question}
    """

    answer = request(sys_prompt, usr_prompt)
    clean_answer, confidence = get_clean_answer(answer)

    return clean_answer, answer

def cot_fewshot_response(node) :
    sys_prompt = f"""
### System Define
You are given a financial question. Please answer the question using given context.
Please answer the question following step-by-step thinking process.

- Extract important evidence from the context.
- Make an executable equation.
- Calculate the equation and provide the final answer.

Note: Form of output is: explanation + [Answer: "final answer";].

### Demonstration

Question : what is the total value of purchased shares during october 2017 , in millions?

- From the context, The total number of shares purchased in October 2017 is 10,676.
The average price paid per share in October 2017 is $104.10.

- Make Equation : 10,676 * 104.10

- Caculate Equation : 10,676 * 104.10 = 1,111,431.60.

The final answer is [Answer : "1.111 (million)";].

"""


    usr_prompt = f"""
Context : {node.context}
Question : {node.question}
    """

    answer = request(sys_prompt, usr_prompt)
    clean_answer, confidence = get_clean_answer(answer)

    return clean_answer, answer

def eedp_response(node) :
    sys_prompt = f"""
<Instruction> 

Please carefully analyze the provided information, perform necessary numerical calculations, and
provide accurate answers to the given question using the provided data. Take into account the pre-text, table, and
post-text when formulating your response.
When performing numerical calculations, ensure you gather the required information and follow a step-by-step
approach.

1. Elicit the most relevant domain fact or knowledge that might be useful for you to extract the right operands and
forming the right approach to the problem.

2. Translate table data into sentences and identify gold evidence for answering the question.

3. Define a sequence of atomic operations (Add, Subtract, Divide, Multiply, Greater, Min, Max, Exp) which take
into account only two operands at a time. Divide a complex task into a sequence of atomic operations defined
above.

4. Finally, conclude as: explanation + The final answer is [Answer: "<final answer>";].

Demonstration: 
“Effective Income Tax Rate”: A reconciliation of the United States federal statutory income tax rate
to our effective income tax rate is as follows: In 2019 and 2018 we had pre-tax losses of $19,573 and $25,403,
respectively, which are available for carry forward to offset future taxable income.
| |Year Ended | Year Ended |
| | December 31, 2018 | December 31, 2019 |
| United States federal statutory rate | 21.00% | 21.00% |
| Effective income tax rate | 1.99% | -0.01% |

Question: What was the 2019 percentage change in pre-tax losses?

Response #:

Domain Knowledge: Pre-tax losses, or operating losses, refer to financial losses that a company incurs before
considering the effects of income taxes. To find the 2019 percentage change in pre-tax losses, we need to find the
difference between the new and the old value of the pre-tax losses, then divide the obtained difference by the old value
and multiply this value by 100.

Gold Evidences:
• The pre-tax losses in 2019 are $19,573.
• The pre-tax losses in 2018 are $25,403.
Steps:
1. Subtract 25403 from 19573.
    • Response 1: 19573 - 25403 = -5830
2. Divide #1 by 25403.
    • Response 2: −5830/25403 = −0.2295
3. Multiply #2 by 100.
    • Response 3: −0.2295 × 100 =−22.95

The final answer is [Answer: "-22.95%";].

"""
    usr_prompt = f"""
Context : {node.context}
Question : {node.question}
    """

    answer = request(sys_prompt, usr_prompt)
    clean_answer, confidence = get_clean_answer(answer)

    return clean_answer, answer