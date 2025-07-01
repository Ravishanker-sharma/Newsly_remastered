from langgraph.graph import StateGraph, END, add_messages
from typing import Annotated, TypedDict
from langgraph.prebuilt import tools_condition, ToolNode
from StoreNews.genralscraper import get_data
from Database.vectordatabase import query_base
from langchain.agents import Tool
from langgraph.checkpoint.memory import MemorySaver
from config import llm
from IPython.display import display, Image

memory = MemorySaver()

class Agent_state(TypedDict):
    messages: Annotated[list, add_messages]

tools = [
    Tool(
        name="GetData",
        func=get_data,
        description="Performs a websearch on basis of input and return data."
    ),
    Tool(
        name="Search_vectorbase",
        func=query_base,
        description="Search for the relevent data from the Vector database and return data , accepts a List as a query"
    )
]

llm_with_tools = llm.bind_tools(tools)

def chat_bot(state: Agent_state):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph = StateGraph(Agent_state)
graph.add_node("bot", chat_bot)
graph.add_node("tools", ToolNode(tools))

graph.set_entry_point("bot")
graph.add_conditional_edges("bot", tools_condition)
graph.add_edge("tools", "bot")

app = graph.compile(checkpointer=memory)

display(Image(app.get_graph().draw_mermaid_png()))

def news_chat(message,thread_id):
    config1 = {"configurable": {"thread_id": thread_id}}
    output = app.invoke({"messages": [{"role": "user", "content": message}]}, config=config1)
    print("user:",message)
    print("bot",output['messages'][-1].content)

news_chat("my fav is red","1")
news_chat("what is my fav","1")
