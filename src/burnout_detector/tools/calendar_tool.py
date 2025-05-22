from smolagents import Tool


class CalendarTool(Tool):
    name: str = "calendar_tool"
    description: str = "A tool for getting the user's calendar events."
    inputs: dict = {
        "email_id": {
            "type": "string",
            "description": "The email ID of the user to get the calendar events for."
        },
        "start_date": {
            "type": "string",
            "description": "The start date of the calendar events to get."
        },
        "end_date": {
            "type": "string",
            "description": "The end date of the calendar events to get."
        },
    }
    output_type: str = "object"

    def forward(self, email_id: str, start_date: str, end_date: str):
        """
        A tool for getting the user's calendar events.
        """
        # Make the API call here, and return the response. 
        return f"Hello, {email_id}!"
    
    
    
    