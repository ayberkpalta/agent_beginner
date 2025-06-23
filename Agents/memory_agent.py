"""
1. Use diff type - HumanMessages and AIMessage
2. Maintain full conversation history using both message type
3. Create a sophisticated conversation loop
"""

# main goal : craete a form of memory for Agent

import os
from typing import TypedDict , List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START,END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatOpenAI(model = "gpt-4o")

def process(state:AgentState)->AgentState:
    """This node will solve the request you input"""
    response=llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content=response.content))
    ## AI also adds its response to memory
    print(f"\nAI: {response.content}")
    print("Current State:" , state["messages"]) # not necessary
    return state


graph=StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process",END)

agent=graph.compile()

conversation_history = []

user_input= input("Enter your message: ")
while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))

    result=agent.invoke({"messages":conversation_history})
    conversation_history=result["messages"]

    user_input=input("Enter your message: ")


with open("logging.txt","w") as file:
    file.write("Your Conversation Log:\n")

    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n\n")
    file.write("END of Conversation\n")

print("Conversation saved to logging.txt:")