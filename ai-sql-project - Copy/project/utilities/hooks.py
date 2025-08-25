from strands import Agent
from strands.experimental.hooks import BeforeToolInvocationEvent

from utilities.logging import log_tool_call

def intercept_tool(event: BeforeToolInvocationEvent) -> None:
    tool_name = event.selected_tool.tool_name.upper() if event.selected_tool else "UNKNOWN_TOOL"
    log_tool_call(tool_name, str(event.tool_use["input"]))

def register_hook(hooks: Agent):
    hooks.hooks.add_callback(BeforeToolInvocationEvent, intercept_tool)