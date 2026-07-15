from  langgraph.graph import StateGraph, START, END
from state import FlowState
from workflow_nodes import retrieve_docs, threshold_check, call_llm, human_review, check_human_review
from checkpoint import get_checkpointer 
from dotenv import load_dotenv 

load_dotenv(override= True)

graph = StateGraph(FlowState) 
checkpoint_context, checkpointer = get_checkpointer()

graph.add_node("retrieve_docs", retrieve_docs)
graph.add_node("generate_answer", call_llm)
graph.add_node("human_review", human_review)


graph.add_edge(START, "retrieve_docs") 
graph.add_conditional_edges("retrieve_docs", threshold_check , {"generate" : "generate_answer" , "review" : "human_review"}) 

graph.add_edge("generate_answer" , END) 

graph.add_conditional_edges("human_review" , check_human_review, {"approved" : "generate_answer" , "rejected" : END})
graph.add_edge("generate_answer" , END) 

workflow = graph.compile(checkpointer = checkpointer)

