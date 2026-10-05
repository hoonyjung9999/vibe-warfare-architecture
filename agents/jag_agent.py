import ollama
import json
import yaml
import time

VETO_THRESHOLD = 0.85

def load_prompt():
    with open("prompts/agent_prompts.yaml", "r") as f:
        return yaml.safe_load(f)["jag_agent"]

def run(scenario: dict, j2_output: dict, j3_output: dict) -> dict:
    prompt = load_prompt()
    context = scenario["context"]
    
    user_message = f"""
Proposed Action: {scenario['vibe']}
Location: {context['location']}
Civilian Presence: {context['civilian_presence']}
Time Pressure: {context['time_pressure']}

Intelligence (J2):
- Threat Confidence: {j2_output.get('threat_confidence', 'N/A')}
- Enemy Presence Probability: {j2_output.get('enemy_presence', 'N/A')}

Proposed COA (J3): {j3_output.get('coa', 'N/A')}

Evaluate this action under IHL. Veto threshold is 0.85 for each principle.
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
        result = {"raw_response": raw, "veto_triggered": True, 
                  "veto_reason": "Failed to parse JAG response - mandatory escalation"}
    
    if not result.get("raw_response"):
        scores = [
            result.get("distinction_score", 0),
            result.get("proportionality_score", 0),
            result.get("necessity_score", 0)
        ]
        if any(s < VETO_THRESHOLD for s in scores):
            result["veto_triggered"] = True
    
    result["agent"] = "JAG"
    result["veto_threshold"] = VETO_THRESHOLD
    result["elapsed_seconds"] = round(elapsed, 2)
    return result
