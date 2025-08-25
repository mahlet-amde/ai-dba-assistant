
from strands.tools import tool
from utilities.tools import ElevatedTools

class VbdaToolManager(ElevatedTools):
    """Manages VBDA tools to prevent accidental spam maintenance windows."""
    
    @tool
    def create_maintaince_window(self, duration: int) -> str:
        """
        Creates a VBDA maintenance window for a specified period of time.

        Args:
            duration: The duration of time in minutes the maintenance window will be active.
        """
        if self.usage_count >= 1: 
            return "You may only create 1 VBDA maintenance window for a given frontline response."

        self.usage_count += 1
        return f"VBDA maintenance window created successfully for {duration} minutes."