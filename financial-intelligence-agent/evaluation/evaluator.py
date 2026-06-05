
import json
import re

from gateway.llm_gateway import call_llm

def evaluate_report(question, report):
    evaluation_prompt = f"Evaluate the following investment research report based on the question asked by the user. Provide scores from 1 to 10 for accuracy, relevance, groundedness, conciseness, and an overall score. Also provide a brief feedback comment.\n\nQuestion: {question}\n\nReport:\n{report}"
    
    evaluation_response = call_llm([
        {"role": "system", "content": "You are a financial analyst evaluator. Return ONLY valid JSON with keys: accuracy, relevance, groundedness, conciseness, overall (all 1-10), and feedback (string). No other text."},
        {"role": "user", "content": evaluation_prompt}
    ])
    
    try:
        evaluation = json.loads(evaluation_response)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', evaluation_response, re.DOTALL)
        if match:
            evaluation = json.loads(match.group())
        else:
            evaluation = {"accuracy": 0, "relevance": 0, "groundedness": 0, "conciseness": 0, "overall": 0, "feedback": "Evaluation failed to parse."}
    return evaluation


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    question = "What is Apple's investment risk for 2025?"
    report = "Apple faces moderate risk with a score of 6/10 due to supply chain issues and regulatory pressure."
    
    result = evaluate_report(question, report)
    print(result)