from strands import Agent
from utilities.file import write_output
from tools.email import EmailToolManager;
from tools.phone import PhoneToolManager;
from tools.vdba import VbdaToolManager;
from utilities.strands_model import model
from utilities.hooks import register_hook
from utilities.logging import styled_log

def take_action(alarm_text: str, analysis: str):
    frontline_response_agent = Agent(
        name="Frontline Response Agent",
        description="Retrieves an analysis and takes appropriate actions.",
        callback_handler=None,
        model=model,
        tools=[
            EmailToolManager().email_customer,
            PhoneToolManager().call_customer,
            VbdaToolManager().create_maintaince_window,
        ],
    )
    register_hook(frontline_response_agent)

    prompt = f"""
You are the Frontline Response Agent.

## Notes
- The necessary information should already be available in the analysis.
- You are not allowed to significantly alter email templates.

## Goals
1. Identify the event ID from the analysis below.
  a. If the Analysis Bot didn't provide an event ID, infer it from the analysis and the Confluence documentation (The Page ID 2114420748).
2. Strictly and carefully follow the Frontline response procedure.
  a. If the procedure expects you to send emails to customers, you must lookup the email template from Confluence first. The Page ID is referenced inside the last path segment of the link to the email template. Please copy the email on the email template *verbatim*, make deviations as needed.
  b. Follow the procedures with the help of tools, such as contacting customers, creating a maintenance window, or sending an email.
  c. Follow strict protocol, do not deviate from the documentation.

## Error Message
{alarm_text}

## Analysis Bot
{analysis}
    """.strip();

    write_output("frontline_response_prompt.txt", prompt);
    response = frontline_response_agent(prompt);
    styled_log('FRONTLINE_RESPONSE_BOT', str(response), 'blue')

    return response;