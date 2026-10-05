import ollama
import json
import yaml
import time

def load_prompt():
    with open("prompts/agent_prompts.yaml", "r") as f:
        return yaml.safe_load(f)["j4_agent"]

def run(scenario: dict) -> dict:
    prompt = load_prompt()
    context = scenario["context"]
    
    user_message = f"""
Operation: {scenario['vibe']}
Location: {context['location']}
Available Assets: {', '.join(context['available_assets'])}
Time Pressure: {context['time_pressure']}

Assess logistical support for this operation.
"""
    
    start = time.time()
    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        options={"temperature": 0}
    )
    elapsed = time.time() - start
    
    raw = response["message"]["content"]
    
    try:
        start_idx = raw.find("{")
        end_idx = raw.rfind("}") + 1
        result = json.loads(raw[start_idx:end_idx])
    except:
        result = {"raw_response": raw}
    
    result["agent"] = "J4"
    result["elapsed_seconds"] = round(elapsed, 2)
    return result
