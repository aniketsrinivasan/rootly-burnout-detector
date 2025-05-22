from smolagents import Tool
import os
import requests


class UsersTool(Tool):
    name: str = "users_tool"
    description: str = """
        Retrieves a list of users from the Rootly API. By using this tool, you can retrieve user information
        (such as email addresses, Slack IDs, internal user IDs, etc.) for any user in the Rootly database.
    """
    inputs: dict = {
        "search": {
            "type": "string",
            "description": "Optional: Filter users by exact search string (maps to filter[search]).",
            "required": False,
            "nullable": True
        },
        "email": {
            "type": "string",
            "description": "Optional: Filter users by email address (maps to filter[email]).",
            "required": False,
            "nullable": True
        }
    }
    output_type: str = "object"

    def forward(self, search: str = None, email: str = None):
        """
        Retrieves users from the Rootly API (/users endpoint).
        Filters these users based on search and email via API parameters.
        """
        api_key = os.getenv('ROOTLY_API_KEY')
        if not api_key:
            return "Error: ROOTLY_API_KEY environment variable is not set."

        base_url = "https://api.rootly.com/v1/users"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        
        params = {}
        if search:
            params["filter[search]"] = search
        if email:
            params["filter[email]"] = email

        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()  
            raw_data = response.json()
        except requests.exceptions.RequestException as e:
            return f"Error calling Rootly Users API: {str(e)}"
        except ValueError as e:  
            return f"Error decoding Rootly Users API response: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred during API call for users: {str(e)}"

        processed_users = []
        if raw_data and "data" in raw_data:
            for user_data_item in raw_data["data"]:
                try:
                    attributes = user_data_item.get("attributes", {})
                    if not attributes:
                        print(f"Warning: User data {user_data_item.get('id')} missing attributes.")
                        continue
                    
                    processed_users.append({
                        "id": user_data_item.get("id"),
                        "type": user_data_item.get("type"),
                        "name": attributes.get("name"),
                        "email": attributes.get("email"),
                        "first_name": attributes.get("first_name"),
                        "last_name": attributes.get("last_name"),
                        "full_name": attributes.get("full_name"),
                        "slack_id": attributes.get("slack_id"),
                        "time_zone": attributes.get("time_zone"),
                        "created_at": attributes.get("created_at"),
                        "updated_at": attributes.get("updated_at")
                    })
                except Exception as e:
                    print(f"Error processing individual user data: {user_data_item.get('id')}, Error: {str(e)}")
                    continue
        
        return processed_users
    
    