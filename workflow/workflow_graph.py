"""
workflow_graph.py
LangGraph-style StateGraph definition for LLM-Wiki Presentation Pipeline.
Demonstrates:
  - TypedDict State
  - Sequential & Looping transitions
  - Quality and Readability Gates (Conditional Edges)
"""

from typing import TypedDict, List, Dict, Any, Optional

class PipelineState(TypedDict):
    raw_docs: List[str]
    synthesized_wiki: Dict[str, str]
    wiki_quality_score: float
    slide_outline: List[Dict[str, Any]]
    readability_score: float
    readability_feedback: str
    slide_contents: List[Dict[str, Any]]
    fact_audit_passed: bool
    hallucination_log: List[str]
    html_output: Optional[str]
    iteration_counts: Dict[str, int]

# --- Nodes ---

def node_data_ingestion(state: PipelineState) -> PipelineState:
    print("[Node 1] Ingesting 5 raw historical markdown documents...")
    state["iteration_counts"]["ingest"] = state["iteration_counts"].get("ingest", 0) + 1
    return state

def node_wiki_synthesizer(state: PipelineState) -> PipelineState:
    print("[Node 2] Synthesizing core timeline, mechanics, and cultural impact...")
    state["iteration_counts"]["synthesize"] = state["iteration_counts"].get("synthesize", 0) + 1
    state["wiki_quality_score"] = 9.5
    return state

def node_slide_outliner(state: PipelineState) -> PipelineState:
    count = state["iteration_counts"].get("outliner", 0) + 1
    state["iteration_counts"]["outliner"] = count
    print(f"[Node 3] Generating slide outline (Iteration #{count})...")
    
    # Simulate first attempt having too much jargon, second attempt being beginner-friendly
    if count == 1:
        state["readability_score"] = 6.8
        state["readability_feedback"] = "Too much undefined gaming jargon. Add beginner intro."
    else:
        state["readability_score"] = 9.4
        state["readability_feedback"] = "Clear concepts, progressive learning curve."
    return state

def node_content_generator(state: PipelineState) -> PipelineState:
    print("[Node 4] Writing detailed slide content referencing Wiki citations...")
    state["iteration_counts"]["content"] = state["iteration_counts"].get("content", 0) + 1
    state["fact_audit_passed"] = True
    return state

def node_deck_renderer(state: PipelineState) -> PipelineState:
    print("[Node 5] Compiling interactive HTML presentation with #1 hash navigation...")
    state["iteration_counts"]["render"] = state["iteration_counts"].get("render", 0) + 1
    state["html_output"] = "slides/index.html compiled successfully."
    return state

# --- Conditional Edges / Gates ---

def gate_wiki_quality(state: PipelineState) -> str:
    if state["wiki_quality_score"] >= 8.5:
        return "pass_to_outliner"
    return "retry_synthesizer"

def gate_beginner_readability(state: PipelineState) -> str:
    if state["readability_score"] >= 8.5:
        return "pass_to_content"
    print(f"  [Gate 2 Triggered Retry] {state['readability_feedback']}")
    return "retry_outliner"

def gate_fact_auditor(state: PipelineState) -> str:
    if state["fact_audit_passed"]:
        return "pass_to_renderer"
    return "retry_content"

if __name__ == "__main__":
    # Test state graph flow
    initial_state: PipelineState = {
        "raw_docs": ["01_origins", "02_mechanics", "03_esports", "04_culture", "05_universe"],
        "synthesized_wiki": {},
        "wiki_quality_score": 0.0,
        "slide_outline": [],
        "readability_score": 0.0,
        "readability_feedback": "",
        "slide_contents": [],
        "fact_audit_passed": False,
        "hallucination_log": [],
        "html_output": None,
        "iteration_counts": {}
    }

    state = node_data_ingestion(initial_state)
    state = node_wiki_synthesizer(state)
    assert gate_wiki_quality(state) == "pass_to_outliner"

    # Outliner Loop test
    while True:
        state = node_slide_outliner(state)
        decision = gate_beginner_readability(state)
        if decision == "pass_to_content":
            break

    state = node_content_generator(state)
    assert gate_fact_auditor(state) == "pass_to_renderer"
    state = node_deck_renderer(state)
    print("\nWorkflow Execution Finished Successfully!")
    print(f"Total Outliner Iterations: {state['iteration_counts']['outliner']}")
