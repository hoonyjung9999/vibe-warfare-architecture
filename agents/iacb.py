import json
from datetime import datetime

def evaluate(j2_output: dict, j3_output: dict, j4_output: dict, jag_output: dict) -> dict:
    """
    IACB - Inter-Agent Checks and Balances
    Phase 1: Conflict Detection
    Phase 2: Veto Evaluation (JAG priority)
    Phase 3: Confidence Scoring
    """
    
    timestamp = datetime.utcnow().isoformat()
    audit_log = []
    
    conflicts = []
    
    j2_threat = j2_output.get("threat_confidence", 1.0)
    j3_feasibility = j3_output.get("feasibility", 1.0)
    j4_resources = j4_output.get("resource_availability", 1.0)
    
    if j2_threat < 0.5 and j3_feasibility > 0.8:
        conflicts.append({
            "agents": ["J2", "J3"],
            "type": "Intel vs Operational",
            "detail": "Low threat confidence but high operational feasibility proposed"
        })
    
    if j4_resources < 0.4 and j3_feasibility > 0.7:
        conflicts.append({
            "agents": ["J4", "J3"],
            "type": "Logistics vs Operational", 
            "detail": "Insufficient resources for proposed COA"
        })
    
    audit_log.append({
        "phase": 1,
        "name": "Conflict Detection",
        "timestamp": timestamp,
        "conflicts_found": len(conflicts),
        "conflicts": conflicts
    })
    
    veto_result = {
        "triggered": False,
        "agent": None,
        "reason": None,
        "timestamp": timestamp
    }
    
    if jag_output.get("veto_triggered", False):
        veto_result = {
            "triggered": True,
            "agent": "JAG",
            "reason": jag_output.get("veto_reason", "IHL threshold not met"),
            "distinction_score": jag_output.get("distinction_score"),
            "proportionality_score": jag_output.get("proportionality_score"),
            "necessity_score": jag_output.get("necessity_score"),
            "timestamp": timestamp
        }
    
    audit_log.append({
        "phase": 2,
        "name": "Veto Evaluation",
        "timestamp": timestamp,
        "veto_result": veto_result
    })
    
    if not veto_result["triggered"]:
        confidence_scores = {
            "J2_threat_confidence": j2_threat,
            "J3_feasibility": j3_feasibility,
            "J4_resource_availability": j4_resources,
            "JAG_distinction": jag_output.get("distinction_score", 0),
            "JAG_proportionality": jag_output.get("proportionality_score", 0),
            "JAG_necessity": jag_output.get("necessity_score", 0),
        }
        overall = round(sum(confidence_scores.values()) / len(confidence_scores), 3)
        
        audit_log.append({
            "phase": 3,
            "name": "Confidence Scoring",
            "timestamp": timestamp,
            "scores": confidence_scores,
            "overall_confidence": overall
        })
    
    return {
        "conflicts": conflicts,
        "veto_result": veto_result,
        "audit_log": audit_log,
        "ihl_compliant": not veto_result["triggered"]
    }
