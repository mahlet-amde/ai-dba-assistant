
from strands.tools import tool
from utilities.tools import ElevatedTools

class PhoneToolManager(ElevatedTools):
    """Manages phone tools to prevent accidental spam calls."""
    
    @tool
    def call_customer(self, message: str) -> str:
        """
        Calls the customer.

        Args:
            message: The message of the call
        """
        if self.usage_count >= 1: 
            return "You may only make 1 call for a given frontline response."

        self.usage_count += 1
        return f"Email sent successfully with subject: {message}"