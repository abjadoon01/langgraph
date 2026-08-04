import json
import os
import getpass
from typing import Dict, List
from pydantic import BaseModel, Field
from langchain_ibm import ChatWatsonx
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_communtiy.tools.tavily_search import TavilySearchResults
from langgraph.graph import MessageGraph, END

llm = ChatWatsonx(
    model_id="ibm/granite-4-h-small",
    url="https://us-south.ml.cloud.ibm.com",
    project_id="skills-network")

def _if_not_idetified(var: str) ->None:
    if os.environ.get(var):
        return
    os.environ[var]= getpass.getpass(var)
_if_not_idetified("TAVILY_API_KEY")


generation_prompt = ChatPromptTemplate.from_messages
(
    [
    (   
        "system",
        """You are Dr. Paul Saladino, "Carnivore MD," advocating for animal-based nutrition and challenging plant-centric dietary dogma. Focus on the superior bioavailability of animal foods and the potential toxicity of plant compounds such as oxalates, lectins, and phytates.

        Your response must follow these steps:
        1. {first_instruction}
        2. Present the evolutionary and biochemical rationale for animal-based nutrition, emphasizing nutrient density, bioavailability, and the absence of plant antinutrients.
        3. Challenge conventional "plants are healthy" narratives with mechanistic evidence about plant defense compounds and their impact on human physiology.
        4. Reflect and critique your answer. Be rigorous about evolutionary consistency and nutrient science.
        5. After the reflection, **list 1-3 search queries separately** for researching antinutrients, bioavailability studies, or evolutionary nutrition. Do not include them inside the reflection.

        Focus on: organ meats as superfoods, the carnivore elimination protocol, and why "fiber is unnecessary" based on human evolutionary biology.
        """
    ),
    MessagesPlaceholder = (variable_name= "messages"),
    (
        "system", 
        "Answer the user's question above using the required format, emphasizing the superiority of animal-based nutrition."
    ),
    ]
)


class Reflection(BaseModel):
    missing : str= Field(description= "What information is missing?")
    superflouus : str= Field(description= "What information is unnessesary?")
class AnswerQuestion(BaseModel):
    answer: str = Field(description="Main response to the question")
    reflection : Reflection = Field(description="Contain all critique")
    quries : str = Field(description= "Quries for additional Research")

question = "Any Idea for healthy breakfast"
first_responder_prompt= generation_prompt.partial(first_instruction= "Provide a detailed ~250 words answer.")
initial_chain = first_responder_prompt|llm.bind_tools(tools=[AnswerQuestion])
response = initial_chain.invoke({"messages": [HumanMessage(content:question)]})
