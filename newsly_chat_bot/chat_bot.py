from langgraph.graph import StateGraph, END, add_messages
from typing import Annotated, TypedDict
from langgraph.prebuilt import tools_condition, ToolNode
from StoreNews.genralscraper import get_data
from Database.vectordatabase import query_base
from langchain.agents import Tool
from langgraph.checkpoint.memory import MemorySaver
from config import llm


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



intialized_threads = set()

def news_chat(message,thread_id):
    if thread_id not in intialized_threads:
        prompt = '''
        You are a helpful News assistant chatbot, who provides unbiased and accurate news to the user.
        Format of news:
            Headline
                Bullet point 1
                Bullet point 2
                Bullet point 3
                Bullet point 4
                Bullet point N
        Provide clear News do not add your own perspective in the news.
        Be very very Polite.
        '''
        msg = {"messages": [{"role":"system","content":prompt},{"role": "user", "content": message}]}
        intialized_threads.add(thread_id)
    else:
        msg = {"messages": [{"role": "user", "content": message}]}
    config1 = {"configurable": {"thread_id": thread_id}}
    output = app.invoke(msg, config=config1)
    return output['messages'][-1].content

def clear_threads(thread_id):
    global intialized_threads
    if thread_id not in intialized_threads:
        intialized_threads.clear()


def chat(message,thread_id):
    clear_threads(thread_id)
    return news_chat(message,thread_id)

