from jinja2 import Environment, FileSystemLoader
import os

def render_analysis_prompt(alarm_message: str, recent_alerts: list[str], confluence_notes: str) -> str:
    template_dir = os.path.join(os.path.dirname(__file__), 'prompts')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("analysis_prompt.j2")
    return template.render(
        alarm_message=alarm_message,
        recent_alerts=recent_alerts,
        confluence_notes=confluence_notes
    )
