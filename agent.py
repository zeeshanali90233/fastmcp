from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.tools import StructuredTool
import dotenv
import asyncio
from fastmcp import Client

dotenv.load_dotenv()

MCP_URL = "http://127.0.0.1:8000/mcp"

# Step 3: get the list of tools from the MCP server
async def _list_tools():
    async with Client(MCP_URL) as client:
        return await client.list_tools()

mcp_tools = asyncio.run(_list_tools())

def make_tool(mcp_tool):
    async def _call(**kwargs):
        async with Client(MCP_URL) as client:
            result = await client.call_tool(mcp_tool.name, kwargs)
            if result.data is not None:
                return result.data
            return "\n".join(c.text for c in result.content if hasattr(c, "text"))

    def run_tool(**kwargs):
        return asyncio.run(_call(**kwargs))

    return StructuredTool.from_function(
        func=run_tool,
        name=mcp_tool.name,
        description=mcp_tool.description or mcp_tool.name,
        args_schema=mcp_tool.inputSchema,
    )

tools = [make_tool(t) for t in mcp_tools]

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key="GROQ_API_KEY",
)

memory = InMemorySaver()

helpful_assistant = create_agent(
    model=llm,
    tools=tools,
    checkpointer=memory,
    system_prompt = """
You are a helpful assistant.
"""
)

user_input = "Get the weather for New York"
response = helpful_assistant.ainvoke(
    {"messages": [{"role": "user", "content": user_input}]},
    config={"configurable": {"thread_id": "123"}}
)
response = asyncio.run(response)

print(response["messages"][-1].content if "messages" in response else response)
