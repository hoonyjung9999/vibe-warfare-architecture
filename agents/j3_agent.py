import ollama
import json
import yaml
import time

def load_prompt():
    with open("prompts/agent_prompts.yaml", "r") as f:
        return yaml.safe_load(f)["j3_agent"]

def run(scenario: dict, j2_output: dict) -> dict:
    prompt = load_prompt()
    context = scenario["context"]
    
    user_message = f"""
Mission: {scenario['vibe']}
Location: {context['location']}
Time Pressure: {context['time_pressure']}
Available Assets: {', '.join(context['available_assets'])}

J2 Intelligence Assessment:
- Threat Confidence: {j2_output.get('threat_confidence', 'N/A')}
- Enemy Presence: {j2_output.get('enemy_presence', 'N/A')}
- ISR Quality: {j2_output.get('isr_quality', 'N/A')}

Develop your recommended Course of Action.
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
    
    result["agent"] = "J3"
    result["elapsed_seconds"] = round(elapsed, 2)
    return result
