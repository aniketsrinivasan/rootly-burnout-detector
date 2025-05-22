from smolagents import Tool


class BiometricsTool(Tool):
    IS_DISABLED = True
    name: str = "biometrics_tool"
    description: str = "A tool for getting the user's biometrics (such as sleep, stress, heart rate, and activity levels)"
    inputs: dict = {
        "email_id": {
            "type": "string",
            "description": "The email ID of the user to get the biometrics for."
        },
        "start_date": {
            "type": "string",
            "description": "The start date of the biometrics to get."
        },
        "end_date": {
            "type": "string",
            "description": "The end date of the biometrics to get."
        },
    }
    output_type: str = "object"

    def forward(self, email_id: str, start_date: str, end_date: str):
        """
        A tool for getting the user's biometrics (such as sleep, stress, heart rate, and activity levels).
        """
        if self.IS_DISABLED:
            return f"The {self.name} tool is currently disabled."
        # Make the API call here, and return the response. 
        return f"Hello, {email_id}!"
