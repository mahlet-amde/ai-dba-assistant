from typing import List
from mcp import Tool
from strands.tools.mcp import MCPClient


def filter_mcp_tools(mcp_client: MCPClient, tool_names: List[str]) -> List[Tool]:
    tools: List[Tool] = mcp_client.list_tools_sync()
    filtered_tools = [tool for tool in tools if tool.tool_spec.get('name') in tool_names]
    
    return filtered_tools;