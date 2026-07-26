# Agentic AI:
Agentic Ai is a goal oriented autonomous systems with multiple agents working collaboratively to achieve complex goals. It uses multiple frameworks for its iterative reasoning capabilities such as ReAct( reasoning and acting), Chain-of-Thought  prompting and tree of thoughts which help it to break down complex tasks. The memory persistent system allows it to preserve memory and persist knowledge across task cycles. It includes episodic memory(task-specific memory) semantic memory (long term facts or structure data) and vector based memory for retrieval augmented generation.

<br/>**6 Main Steps in Agentic AI Loop:**
<br/>  1. Construct Prompt
 <br/> 2. Generate Response
 <br/> 3. Parse Response 
 <br/> 4. Execute Action
 <br/> 5. Feedback to string
 <br/> 6. Continue loop
<br/>
<br/>
<h3>Frameworks:</h3>
 LangGraph:<br/>
    A framework within the langchain ecosystem for building multi-agent workflows using a graph based execution model. It allows us to define agents as nodes and their interactions as edges orchestrating collaboration between agents.<br/>
    Langchain,<br/>
   A python framework for building applications around LLMs. It has modular architecture. It supports tool usage and APIs (to simplify building chatbots, virtual assistants) RAG pipelines, memory buffers, chain of reasoning and agent interfaces. It is a building block that helps to combine language models with external data and APIs. Its core component is chain system or directed graph structure.<br/>
RAG workflow example: 1.retrieve relevant document 2.sumerize 3.generate an answer.<br/>
IBM Bee, CrewAi, Autogen etc:<br/>
  These tools allow to simplify the design of multi-agent teams, role assignment and structured task planning. This allow developers to simulate or deploy collaborative agent environment using memory , messaging and dynamic delegation<br/>

<h3>RAG:</h3>
RAG (retrieval augmented generation): It enhances AI to provide context aware response and integrate real time information. For AI agents it is hard to understand causal prompt and can have hallucination and prompt sensitivity where RAG mitigates these problems by expending static LLM knowledge through grounding output into real time data. The shared grounding mechanism across agents allows distributed agents to operate on a unified semantic layer.<br/>
24/07/26 Basic Counter using Langgraph
