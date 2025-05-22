from smolagents import Tool


class RecentMeetingTool(Tool):
    IS_DISABLED = True
    name: str = "recent_meeting_tool"
    description: str = "A tool for getting the user's recent meeting transcripts/notes."
    inputs: dict = {
        "email_id": {
            "type": "string",
            "description": "The email ID of the user to get the recent meetings for."
        },
        "max_length": {
            "type": "int",
            "description": "The maximum length (in characters) of the meeting transcript/notes to return."
        },
    }
    output_type: str = "object"
    
    def forward(self, email_id: str, max_length: int):
        """
        A tool for getting the user's recent meeting transcripts/notes.
        """
        if self.IS_DISABLED:
            return f"The {self.name} tool is currently disabled."
        # Make the API call here, and return the response. 
        return f"Hello, {email_id}!"
    
    