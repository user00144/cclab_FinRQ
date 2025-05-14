from config import MAX_DEPTH
from utils.qa_utils import *
"""
 This is the code started modification from 
 https://github.com/PLUM-Lab/SOCRATIC-QUESTIONING
"""


class SocraticNode :
    def __init__(self, context, question, depth) :
        self.context = context
        self.question = question
        self.shint = ""
        self.hints = []
        self.answer = None
        self.depth = depth
        self.max_depth = MAX_DEPTH
        self.isLeaf = depth >= self.max_depth
        self.childs = []
        self.raw_answer = ""
        
    def hasHint(self):
        if len(self.hints) == 0:
            return False
        else:
            return True
    
    def getShint(self) :
        return self.shint
    
    def setShint(self, shint) :
        self.shint = shint

    def hasChild(self):
        if self.isLeaf :
            return False
        if len(self.childs) == 0:
            return False
        else :
            return True
        
    def update_hint(self):
        self.hints.clear()
        if self.isLeaf :
            return False
        if len(self.childs) == 0 :
            return False
        else :
            for child in self.childs :
                shint = child.getShint()
                if child.answer["confidence"] == "high" :
                    self.hints.append(shint)

    def get_textHints(self):
        hints = ''
        for i, hint in enumerate(self.hints):
            hints += '(' + str(i+1) + ') ' + hint + '; '   
        if len(hints) > 0:  
            hints = hints[:-2] + '.'
        return hints

    def make_child(self, answer) :
        dQs = get_clean_questions(answer)
        if self.isLeaf :
            return False
        
        self.childs.clear()
        for _ in dQs :
            self.childs.append(SocraticNode(self.context, _, self.depth + 1))
            
        return True

    def update_answer(self, answer, confidence):
        self.answer = {
            'answer': answer,
            'confidence': confidence
        }
    
