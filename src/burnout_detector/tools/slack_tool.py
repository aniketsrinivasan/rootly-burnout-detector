from smolagents import Tool


class SlackTool(Tool):
    IS_DISABLED = True
    name: str = "slack_tool"
    description: str = "A tool to retrieve messages from a Slack channel."
    inputs: dict = {
        "email_id": {
            "type": "string",
            "description": "The email ID of the user to retrieve messages from."
        },
        "channel_id": {
            "type": "string",
            "description": "The ID of the Slack channel to retrieve messages from."
        },
        "max_results": {
            "type": "int",
            "description": "The maximum number of results to return."
        },
    }
    output_type: str = "object"
    
    def forward(self, email_id: str, channel_id: str, max_results: int):
        """
        A tool to retrieve messages from a Slack channel.
        """
        if self.IS_DISABLED:
            return f"The {self.name} tool is currently disabled."
        # Make the API call here, and return the response. 
        return f"Hello, {email_id}!"
    
    