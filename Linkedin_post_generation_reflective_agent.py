from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_ibm import ChatWatsonx
from langgraph.graph import  MessageGraph, END
from typing import List, Annotated, TypedDict, Sequence
from IPython.display import Image, display

llm = ChatWatsonx(model_id="ibm/granite-4-h-small",
    url="https://us-south.ml.cloud.ibm.com",
    project_id="skills-network")
generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a professional LinkedIn content assistant tasked with crafting engaging, insightful, and well-structured LinkedIn posts."
            "Generate the best LinkedIn post possible for the user's request."
            "If the user provides feedback or critique, respond with a refined version of your previous attempts, improving clarity, tone, or engagement as needed.",
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)
generate_chain= generation_prompt | llm
reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a professional LinkedIn content strategist and thought leadership expert. Your task is to critically evaluate the given LinkedIn post and provide a comprehensive critique. Follow these guidelines:

            1. Assess the post’s overall quality, professionalism, and alignment with LinkedIn best practices.
            2. Evaluate the structure, tone, clarity, and readability of the post.
            3. Analyze the post’s potential for engagement (likes, comments, shares) and its effectiveness in building professional credibility.
            4. Consider the post’s relevance to the author’s industry, audience, or current trends.
            5. Examine the use of formatting (e.g., line breaks, bullet points), hashtags, mentions, and media (if any).
            6. Evaluate the effectiveness of any call-to-action or takeaway.

        Provide a detailed critique that includes:
        - A brief explanation of the post’s strengths and weaknesses.
        - Specific areas that could be improved.
        - Actionable suggestions for enhancing clarity, engagement, and professionalism.

        Your critique will be used to improve the post in the next revision step, so ensure your feedback is thoughtful, constructive, and practical.
        """
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)

reflected_chain=  reflection_prompt | llm

class AgentState(TypedDict):
    messages : Annotated[List[HumanMessage|AIMessage|SystemMessage], "add_messages"]
graph = MessageGraph()
def generate_node(state: Sequence[BaseMessage]) -> List[BaseMessage]:
    generate_post = generate_chain.invoke({"messages":state})
    return [AIMessage(content=generate_post.content)]
def reflection_node(message: Sequence[BaseMessage]) -> List[BaseMessage]:
    res = reflected_chain.invoke({"messages":message})
    return [HumanMessage(content=res.content)]
def should_continue(state: Sequence[BaseMessage]):
    print(state)
    print(len(state))
    print("---------------------------------------")
    if len(state) >2:
        return END
    return "generate"
inputs = HumanMessage(content="""Write a linkedin post on getting a software developer job at IBM under 160 characters""")
graph.add_node("generate", generate_node)
graph.add_node("reflect", reflection_node)
graph.set_entry_point("generate")
graph.add_edge("generate", "reflect")
graph.add_conditional_edges("reflect", should_continue)
app = graph.compile()
response = app.invoke(inputs)
response[1].content
response[2].content
response[-1].content
display(Image(app.get_graph().draw_png()))



