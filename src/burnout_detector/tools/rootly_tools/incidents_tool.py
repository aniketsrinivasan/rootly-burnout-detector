import os
import requests
from smolagents import Tool

# The requests library must be installed in the environment where this tool is run.

class IncidentsTool(Tool):
    name: str = "incidents_tool"
    description: str = """
        Retrieves a list of incidents from the Rootly API, with options for filtering
        by user ID and creation date range, and supports pagination.
        This tool can be used to get an overview of incidents a user might be involved in
        or affected by, which can be an indicator of workload and potential stress.
    """
    inputs: dict = {
        "user_id": {
            "type": "integer",
            "description": "Optional: Filter incidents for a specific user ID.",
            "required": False,
            "nullable": True
        },
        "created_at_gte": {
            "type": "string",
            "description": "Optional: Filter incidents created on or after this ISO 8601 datetime string (e.g., '2025-05-22T00:00:00Z'). Inclusive.",
            "required": False,
            "nullable": True
        },
        "created_at_lte": {
            "type": "string",
            "description": "Optional: Filter incidents created on or before this ISO 8601 datetime string (e.g., '2025-05-23T23:59:59Z'). Inclusive.",
            "required": False,
            "nullable": True
        }
    }
    output_type: str = "object" 

    def forward(self, user_id: int = None, created_at_gte: str = None, created_at_lte: str = None):
        """
        Retrieves incidents from the Rootly API based on specified filters and pagination.

        Args:
            user_id: Optional user ID to filter incidents by.
            created_at_gte: Optional ISO 8601 string for the start of the creation date range.
            created_at_lte: Optional ISO 8601 string for the end of the creation date range.

        Returns:
            A list of dictionaries, each containing processed incident details,
            or an error string if the API call fails or the response is malformed.
        """
        api_key = os.getenv('ROOTLY_API_KEY')
        if not api_key:
            return "Error: ROOTLY_API_KEY environment variable is not set."

        base_url = "https://api.rootly.com/v1/incidents"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        
        params = {}
        if user_id is not None:
            params["filter[user_id]"] = user_id
        if created_at_gte:
            params["filter[created_at][gte]"] = created_at_gte
        if created_at_lte:
            params["filter[created_at][lte]"] = created_at_lte

        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status() 
            raw_data = response.json()
        except requests.exceptions.RequestException as e:
            return f"Error calling Rootly Incidents API: {str(e)}"
        except ValueError as e:  
            return f"Error decoding Rootly Incidents API response: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred during API call for incidents: {str(e)}"

        processed_incidents = []
        if raw_data and "data" in raw_data:
            for incident_data in raw_data["data"]:
                try:
                    attributes = incident_data.get("attributes", {})
                    if not attributes:
                        print(f"Warning: Incident data {incident_data.get('id')} missing attributes.")
                        continue

                    severity_data = attributes.get("severity", {}).get("data", {})
                    severity_attributes = severity_data.get("attributes", {}) if severity_data else {}

                    environments = [
                        env.get("attributes", {}).get("name") 
                        for env_item in attributes.get("environments", []) 
                        if (env := env_item.get("data")) and env.get("attributes")
                    ]
                    services = [
                        srv.get("attributes", {}).get("name") 
                        for srv_item in attributes.get("services", []) 
                        if (srv := srv_item.get("data")) and srv.get("attributes")
                    ]

                    processed_incidents.append({
                        "incident_id": incident_data.get("id"),
                        "title": attributes.get("title"),
                        "status": attributes.get("status"),
                        "kind": attributes.get("kind"),
                        "severity_name": severity_attributes.get("name"),
                        "severity_level": severity_attributes.get("severity"),
                        "summary": attributes.get("summary"),
                        "created_at": attributes.get("created_at"),
                        "updated_at": attributes.get("updated_at"),
                        "started_at": attributes.get("started_at"), 
                        "resolved_at": attributes.get("resolved_at"),
                        "environments": environments,
                        "services": services
                    })
                except Exception as e:
                    print(f"Error processing individual incident data: {incident_data.get('id')}, Error: {str(e)}")
                    continue
        
        return processed_incidents
