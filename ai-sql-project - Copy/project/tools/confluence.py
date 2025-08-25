import subprocess
from typing import List
from mcp import StdioServerParameters, Tool
from mcp.client.stdio import stdio_client
from strands.tools.mcp import MCPClient;

def atlassian_mcp():
    """
    A little demo to test the Atlassian MCP client.
    """
    mcp_client = MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command="npx",
            args=["-y", "mcp-remote", "https://mcp.atlassian.com/v1/sse"],
        )
    ))

    return mcp_client;

def authorized_atlassian_mcp():
    subprocess.run(["npx", "-y", "mcp-remote", "https://mcp.atlassian.com/v1/sse"], check=True)