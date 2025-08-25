import os

def write_output(file_name: str, content: str):
    os.makedirs("./.output", exist_ok=True)

    with open(f"./.output/{file_name}", "w") as f:
        f.write(content)