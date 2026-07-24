import random
import string
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
class ChainState(TypedDict):
  n :int
  letter : str
intial_state= ChainState(n=0, letter="a")
def add(state:ChainState) -> ChainState:
  add_letter = random.choice(string.ascii_lowercase)
  return {**state, "n":state["n"] +1, "letter":add_letter}
def print_out(state:ChainState) -> ChainState:
  print("current no:", state["n"], "letter:",state["letter"])
  return state
def stop_condition(state:ChainState):
  if state["n"] >= 13:
    return "stop"
  return "add"
workflow = StateGraph(ChainState)
workflow.set_entry_point("add")
workflow.add_node("add",add)
workflow.add_node("print_out",print_out)
workflow.add_edge("add","print_out")
workflow.add_conditional_edges("print_out",stop_condition,{"stop":END,"add":"add"})
app = workflow.compile()
result = app.invoke(intial_state)
print (result)