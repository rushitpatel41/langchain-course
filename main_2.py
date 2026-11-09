import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import Tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()