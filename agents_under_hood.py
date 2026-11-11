from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage, ToolMessage
from langchain.tools import tool
from langsmith import traceable

load_dotenv()

MAX_INTERATIONS = 10
MODEL = "gpt-5-nano"

@tool
def get_product_price(product:str):
  """look for the price of a given product"""
  print(f"Looking for the price of: {product}")
  prices = {"laptop": 1000, "phone": 100, "tablet": 500, "monitor": 300, "keyboard": 50, "mouse": 30}
  return prices.get(product,"Product not found")

@tool
def apply_discount(price: float, discount_tier: str):
  """apply discount to the price of a given product"""
  print(f"Applying discount to: {price} with tier: {discount_tier}")
  discount_percentages = {"silver": 0.05, "gold": 0.1, "platinum": 0.2}
  discount = discount_percentages.get(discount_tier, 0)
  return round(price * (1 - discount), 2)

@traceable(name="run_agent")
def run_agent(question:str):
  tools= [get_product_price, apply_discount]
  tools_dict = {t.name: t for t in tools}
  llm = init_chat_model(MODEL,temperature=0)
  llm_with_tools = llm.bind_tools(tools)
  print(f"Question: {question} ")
  print("="*60)
  messages = [SystemMessage(content=("You are a helpful shopping assistant.")
              , ]
  pass


if __name__ == "__main__":
  result = run_agent("What is the price of a laptop and apply a gold discount?")
  print(result)
