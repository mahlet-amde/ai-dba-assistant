from strands import Agent
from utilities.mcp import filter_mcp_tools
from utilities.file import write_output
from tools.fetch_alarms import fetch_last_alarm_messages
from utilities.strands_model import model
from utilities.hooks import register_hook
from utilities.logging import styled_log
from tools.confluence import atlassian_mcp

async def analyze_alarm(alarm_message: str):
    with atlassian_mcp() as mcp_client:
        analysis_agent = Agent(
            name="Analysis Agent",
            description="Supports the **Frontline Response Agent** by analyzing alarms and extracting critical details.",
            callback_handler=None,
            model=model,
            tools=[fetch_last_alarm_messages] + filter_mcp_tools(mcp_client, ['getAccessibleAtlassianResources', 'getConfluencePage']),
        )
        register_hook(analysis_agent)

        prompt = f"""
You are the **Analysis Agent**, supporting the **Frontline Response Agent** by analyzing alarms and extracting critical details.

## Goals
1. Gather any useful information about the alarm message.
2. Find the closest event in the documentation to the alarm message.
a. The documentation can be found on Confluence, page ID 2114420748.
3. Provide a clear event ID and context for the Frontline Response Agent.

## Process
- Step 1: Use your tools to gain understanding on what's happening in the alarm message.
- Step 2: Match the event ID in the documentation to the alarm message. Note that the event ID is almost never mentioned in the alarm message.
- Step 3: Provide frontline response instructions for the Frontline Response Agent, please ignore the DBA response instructions.
- Step 4: Share a link to the email template.

## Objective
Using the documentation, find the event ID and useful information for this alarm message: `{alarm_message}`
        """.strip();

        write_output("analysis_prompt.txt", prompt);
        response = analysis_agent(prompt);

        styled_log(' ANALYSIS_BOT', str(response), 'blue')

        return response;