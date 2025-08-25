
from strands.tools import tool
from utilities.tools import ElevatedTools

class EmailToolManager(ElevatedTools):
    """Manages email tools to prevent accidental spam emails."""
    
    @tool
    def email_customer(self, subject: str, message: str) -> str:
        """
        Sends an email to the customer following an email template provided by the confluence documentation.

        Args:
            subject: The subject of the email
            message: The body of the email
        """
        if self.usage_count >= 1: 
            return "You may only send 1 email for a given frontline response."

        self.usage_count += 1
        return f"Email sent successfully with subject: {subject} - {message}"