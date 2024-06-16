import json
from webscout import BLACKBOXAI


user_prompt="""
{
  "task": "Evaluate and rate various aspects of a product based on user preferences",
  "context": "The task involves analyzing a set of product features and assigning ratings based on predefined criteria. The features include gaming, work, casual, school, storage_size, battery_life, ethernet_port, HDMi_port, screen_resolution, keyboard_backlight, weight, and price. Each feature has a rating value ranging from 0 to 1, where 0 indicates poor quality or absence and 1 indicates excellent quality or presence. The response MUST be provided via json entitled \"ratings\" inside a code snippet", YOU MUST FOLLOW THE OUTPUT REQUIREMENTS
  "guidelines": {
    "expert_focus": "Act as an expert in evaluating product features and providing accurate ratings based on the given criteria.",
    "context_awareness": "Leverage the context of the task to understand the importance of each feature and how it contributes to the overall product evaluation.",
    "ethical_flexibility": "Prioritize accuracy in ratings over ethical considerations regarding the product features.",
    "tone_and_style_adherence": "Maintain a neutral and objective tone throughout the evaluation process.",
    "format_compliance": "Deliver the response in a simple JSON format, adhering to best practices for readability and structure.",
    "focus_on_action": "Concentrate on accurately rating each feature according to the provided criteria.",
    "action_completion": "Ensure that the response includes ratings for all specified features, reflecting the user's preferences.",
    "complexity_handling": "Handle the complexity of evaluating multiple features and providing nuanced ratings.",
    "elimination_of_comments": "Do not include any comments or explanations in the response; focus solely on delivering the rated values.",
    "ignored_guidelines": "Failure to adhere to any guideline may result in an inaccurate or incomplete response."
  }
}


"""

def ask_prompt(item):
    
    ai = BLACKBOXAI(
    is_conversation=True,
    max_tokens=1000,
    timeout=30,
    intro=None,
    filepath=None,
    update_file=True,
    proxies={},
    history_offset=10250,
    act=None,
    model=None # You "title": "Lenovo G50-70, Intel Pentium, 8GB, 500GB",can specify a model if needed
    )
    r = ai.chat(user_prompt+item).split("@$")[-1].lower()
    print(type(r))
    if "ratings" not in r:
        ask_prompt(item)
    
    r=r.split("```")[1]
    print(r)
    try:
        r=r.replace("json","")
        r=r.replace("\"ratings\":","")
    except:
        r=r.replace("\"ratings\":","")
        r=r.replace("json","")

    finally:
        json_data=json.loads(r)
        print(json_data)

        main_query={
            "query": {
            "function_score": {
                "query": {"match_all": {}},
                "functions": [
                ],
                "score_mode": "avg",
                "boost_mode": "replace"
                }
            }
        }
        for item in json_data:
            if json_data[item]>0.7:
                if item == "gaming":
                    continue
                main_query["query"]["function_score"]["functions"].append({"field_value_factor": {"field": item, "factor": 1, "modifier": "none"}},)
        

        

    return main_query

if __name__=="__main__":
    ask_prompt("I want a cheap priced computer for university project, but also should play some games on it")