#!/usr/bin/env python3
import asyncio
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
# from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
# from langchain_ollama import OllamaLLM
from langchain_anthropic import ChatAnthropic

# MODEL = "llama3.2"
MODEL = "claude-3-5-sonnet-20240610"
load_dotenv()

# llm = OllamaLLM(model=MODEL)
llm = ChatAnthropic(model=MODEL)

stdio_server_params = StdioServerParameters(
    command="python",
    args=["/Users/oshafran/AI/MCP/shellserver/servers/math_server.py"],
)


async def main():
    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("OLGA session initialized")
            tools = await load_mcp_tools(session)
            # print(tools)
            agent = create_react_agent(llm, tools)

            result = await agent.ainvoke(
                {"messages": [HumanMessage(content="What is 54 + 2 * 3?")]}
            )
            print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())