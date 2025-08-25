from agents.analysis import analyze_alarm
from agents.frontline_response import take_action
from utilities.logging import styled_log
from os import system
import asyncio
from dotenv import load_dotenv
from tools.confluence import authorized_atlassian_mcp

load_dotenv()

async def main():
    system('cls') # Clear the console
    
    authorized_atlassian_mcp()
    alarm_message = input("What is the alarm message you want to look up?\n")

    
    styled_log('ALARM', alarm_message, 'yellow')
    
    analysis_response = await analyze_alarm(alarm_message);

    frontline_response = take_action(alarm_message, str(analysis_response));

if __name__ == "__main__":
    asyncio.run(main())