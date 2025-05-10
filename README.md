# FinRQ  
___  

## Solving Financial QA in Large Language Models with Recursive Questioning  
> **Mar. 2025 ~ Apr. 2025**

---

## Introduction  

- Financial QA needs domain-specific and multi-step reasoning.  
- Prior methods rely on fine-tuning or external tools.  
- FinRQ introduces a recursive strategy with zero-shot prompting.

---

## FinRQ  

### Recursive Questioning Process
- **Step 1: Question Generation (QG)**  
  → Split main question into sub-questions.  
- **Step 2: Answer Tree of Thoughts (ATOH)**  
  → Answer sub-questions and recursively build reasoning tree.
  
![figs](https://github.com/user-attachments/assets/81723901-ab78-477f-b087-20a59d8f1229)

---

## Evaluation  

### Baseline 
 - Direct inference, Chain of Thought(CoT), EEDP(2024)
 - using gpt-4o-mini

### Result
- FinRQ outperforms Direct, CoT, and EEDP on FinQA:  
  - Direct: 49.90%  
  - CoT: 56.84%  
  - EEDP: 58.79%  
  - **FinRQ: 60.48%**

---

## Outputs  
- Publication domestic conference paper(accepted) in Annual Symposium of KIPS 2025 (May. 2025)
