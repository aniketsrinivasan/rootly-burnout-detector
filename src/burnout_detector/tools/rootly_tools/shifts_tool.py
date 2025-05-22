from smolagents import Tool
import requests  
from datetime import datetime
import os


class ShiftsTool(Tool):
    name: str = "shifts_tool"
    description: str = """
        Retrieves on-call shifts for a specified schedule from the Rootly API. This API call is used to get the 
        on-call schedule for a given schedule_id. It primarily contains information on the user_id associated with the 
        shift, the start and end times of the shift, and whether the shift is an override.
    """
    inputs: dict = {
        "schedule_name": {
            "type": "string",
            "description": "Optional: Filter schedules by exact schedule name match (maps to filter[name]). If unsure of the schedule name, leave blank to return all schedules.",
            "required": False,
            "nullable": True
        },
        "starts_after": {
            "type": "string",
            "description": "Optional: Filter shifts starting after this ISO 8601 datetime string (e.g., '2025-05-22T09:00:00-07:00').",
            "required": False,
            "nullable": True
        },
        "ends_before": {
            "type": "string",
            "description": "Optional: Filter shifts ending before this ISO 8601 datetime string (e.g., '2025-05-23T18:00:00-07:00').",
            "required": False,
            "nullable": True
        }
    }
    output_type: str = "object"

    def forward(self, schedule_name: str = None, starts_after: str = None, ends_before: str = None):
        """
        Retrieves schedules from the Rootly API (/schedules endpoint).
        Filters these schedules based on name and creation date via API parameters.
        Further performs client-side filtering based on the input user_id_filter (matching owner_user_id).

        Args:
            schedule_name: Optional name of the schedule to filter by (exact match).
            starts_after: Optional ISO 8601 string to filter schedules created on or after this time.
            ends_before: Optional ISO 8601 string to filter schedules created on or before this time.

        Returns:
            A list of dictionaries, each representing a filtered schedule, or an error string.
        """
        api_key = os.getenv('ROOTLY_API_KEY')
        if not api_key:
            return "Error: ROOTLY_API_KEY environment variable is not set."

        base_url = "https://api.rootly.com/v1/schedules"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        
        params = {}
        if schedule_name:
            params["filter[name]"] = schedule_name
        if starts_after:
            params["filter[created_at][gte]"] = starts_after
        if ends_before:
            params["filter[created_at][lte]"] = ends_before

        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()  
            raw_data = response.json()
        except requests.exceptions.RequestException as e:
            return f"Error calling Rootly API: {str(e)}"
        except ValueError as e:  
            return f"Error decoding Rootly API response: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred during API call: {str(e)}"

        processed_shifts = []
        if raw_data and "data" in raw_data:
            for schedule_data_item in raw_data["data"]:
                try:
                    current_attributes = schedule_data_item.get("attributes", {})
                    owner_user_id = current_attributes.get("owner_user_id")

                    processed_shifts.append({
                        "id": schedule_data_item.get("id"),
                        "type": schedule_data_item.get("type"),
                        "name": current_attributes.get("name"),
                        "description": current_attributes.get("description"),
                        "all_time_coverage": current_attributes.get("all_time_coverage"),
                        "slack_user_group": current_attributes.get("slack_user_group"),
                        "owner_group_ids": current_attributes.get("owner_group_ids"),
                        "owner_user_id": owner_user_id,
                        "created_at": current_attributes.get("created_at"),
                        "updated_at": current_attributes.get("updated_at")
                    })
                except Exception as e:
                    print(f"Error processing individual schedule data: {schedule_data_item.get('id')}, Error: {str(e)}")
                    continue
        
        return processed_shifts
