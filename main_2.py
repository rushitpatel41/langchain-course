import os
from typing import List

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field
from tavily import TavilyClient

load_dotenv()

class Source(BaseModel):
  """Schema for a source of information"""
  url:str =  Field(description="The URL of the source")


class AgentResponse(BaseModel):
  """Schema for an agent response with answer and sources"""
  content: str = Field(description="The content of the agent's response")
  sources: List[Source] = Field(default_factory=list, description="The sources of information for the agent's response")



tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# @tool
# def search(query: str):
#     """
#     Search for information using Tavily over the Internet

#     Args:
#         query (str): The search query

#     Returns:
#         The search results from Tavily
    
#     """
#     print(f"Searching for: {query}")
#     return tavily.search(query)

llm = ChatOpenAI(model="gpt-5-nano")
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)
response = agent.invoke({"messages":[HumanMessage(content="what is the current stock price of NVDA")]})
print(response.structured_response)