import json
import time
import threading
from datetime import datetime
from agents import j2_agent, j3_agent, j4_agent, jag_agent, iacb

def run_parallel(scenario: dict) -> dict:
    """VWA-Full: J2 and J4 run concurrently, then J3, then JAG, then IACB."""
    results = {}
    
    start_total = time.time()
    
    j2_result = [None]
    j4_result = [None]
    
    def run_j2():
        j2_result[0] = j2_agent.run(scenario)
    
    def run_j4():
        j4_result[0] = j4_agent.run(scenario)
    
    t1 = threading.Thread(target=run_j2)
    t2 = threading.Thread(target=run_j4)
    t1.start(); t2.start()
    t1.join(); t2.join()
    
    j3_result = [None]
    jag_result = [None]
    
    def run_j3():
        j3_result[0] = j3_agent.run(scenario, j2_result[0])
    
    def run_jag():
        jag_result[0] = jag_agent.run(scenario, j2_result[0], 
                                       j3_result[0] if j3_result[0] else {})
    
    t3 = threading.Thread(target=run_j3)
    t3.start(); t3.join()
    
    t4 = threading.Thread(target=run_jag)
    t4.start(); t4.join()
    
    iacb_result = iacb.evaluate(j2_result[0], j3_result[0], 
                                 j4_result[0], jag_result[0])
    
    total_elapsed = round(time.time() - start_total, 2)
    
    return {
        "mode": "VWA-Full (Parallel)",
        "scenario_id": scenario["id"],
        "total_elapsed_seconds": total_elapsed,
        "j2": j2_result[0],
        "j3": j3_result[0],
        "j4": j4_result[0],
        "jag": jag_result[0],
        "iacb": iacb_result
    }


def run_sequential_baseline(scenario: dict) -> dict:
    """Baseline: J2, then J3; no JAG and no IACB."""
    start_total = time.time()
    
    j2_result = j2_agent.run(scenario)
    j3_result = j3_agent.run(scenario, j2_result)
    
    total_elapsed = round(time.time() - start_total, 2)
    
    return {
        "mode": "Baseline (No JAG/IACB)",
        "scenario_id": scenario["id"],
        "total_elapsed_seconds": total_elapsed,
        "j2": j2_result,
        "j3": j3_result,
        "iacb": {
            "ihl_compliant": True,
            "veto_result": {"triggered": False, "agent": None, "reason": "No JAG agent"},
            "note": "No IHL check performed"
        }
    }


def run_noveto(scenario: dict) -> dict:
    """VWA-NoVeto: all agents run; the veto is forced off."""
    start_total = time.time()
    
    j2_result = j2_agent.run(scenario)
    j4_result = j4_agent.run(scenario)
    j3_result = j3_agent.run(scenario, j2_result)
    jag_result = jag_agent.run(scenario, j2_result, j3_result)
    
    jag_result["veto_triggered"] = False
    jag_result["veto_reason"] = None
    
    iacb_result = iacb.evaluate(j2_result, j3_result, j4_result, jag_result)
    
    total_elapsed = round(time.time() - start_total, 2)
    
    return {
        "mode": "VWA-NoVeto",
        "scenario_id": scenario["id"],
        "total_elapsed_seconds": total_elapsed,
        "j2": j2_result,
        "j3": j3_result,
        "j4": j4_result,
        "jag": jag_result,
        "iacb": iacb_result
    }
