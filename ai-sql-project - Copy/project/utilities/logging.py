from termcolor import colored

def styled_log(header: str, message: str, color: str):
    print(f"{colored(f'{header}:', color, attrs=['bold'])}\n{colored(message, color)}")

def log_tool_call(tool_name: str, message: str):
    styled_log(f' {tool_name}', message, 'magenta')

def log_error(message: str):
    
    styled_log("Confluence Error", message, "red")