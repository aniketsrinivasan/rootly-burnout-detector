# Rootly Burnout Detector

## Overview

The Rootly Burnout Detector is an experimental project aimed at building an AI agent capable of identifying potential burnout risks in on-call Site Reliability Engineers (SREs). It leverages data from the Rootly API and potentially other sources to gather signals related to workload, incident response, and communication patterns.

## Current Functionality

The system currently consists of a set of Python tools designed to interact with specific Rootly API endpoints. These tools are built using the `smolagents` framework, where each tool inherits from a base `Tool` class.

The primary implemented tools fetch data related to:
*   **Schedules**: Information about on-call schedules.
*   **Incidents**: Data on incidents, which can be filtered by user involvement and timeframes.
*   **Users**: Details about users within the Rootly system.

## How it Works (High-Level)

1.  **Data Collection Tools**: Python classes (`ShiftsTool`, `IncidentsTool`, `UsersTool`) are defined to encapsulate the logic for querying specific Rootly API endpoints.
2.  **Authentication**: Tools that interact with the Rootly API expect a `ROOTLY_API_KEY` environment variable to be set for Bearer token authentication.
3.  **Agent Orchestration (Future)**: These tools are designed to be used by an AI agent (from the `smolagents` framework or similar). The agent would invoke these tools, gather the necessary data, and then use its logic to analyze the data for burnout indicators. (The agent logic itself is not yet implemented in this phase).

## Setup Instructions

1.  **Clone the Repository**:
    ```bash
    git clone <your-repository-url>
    cd rootly-burnout-detector
    ```

2.  **Create and Activate a Virtual Environment** (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Environment Variables**:
    You need to set your Rootly API token as an environment variable.
    ```bash
    export ROOTLY_API_KEY="<your_rootly_api_token>"
    ```
    You can add this line to your shell's configuration file (e.g., `.bashrc`, `.zshrc`) for persistence.

## Available Tools

The following tools are implemented in `src/burnout_detector/tools/rootly_tools/`:

### 1. `ShiftsTool` (`shifts_tool.py`)
*   **Purpose**: Retrieves schedule information from the Rootly API. Note: Despite its name and original intent, this tool currently queries the `/v1/schedules` endpoint for schedule-level data, not individual shifts directly from a shifts-specific endpoint.
*   **Rootly API Endpoint**: `GET https://api.rootly.com/v1/schedules`
*   **Key Input Parameters (API filters)**:
    *   `schedule_name` (optional, string): Filters schedules by exact name match (maps to `filter[name]`).
    *   `starts_after` (optional, string): Filters schedules created on or after this ISO 8601 datetime string (maps to `filter[created_at][gte]`).
    *   `ends_before` (optional, string): Filters schedules created on or before this ISO 8601 datetime string (maps to `filter[created_at][lte]`).
*   **Output**: A list of schedule objects matching the filters.

### 2. `IncidentsTool` (`incidents_tool.py`)
*   **Purpose**: Retrieves a list of incidents from the Rootly API.
*   **Rootly API Endpoint**: `GET https://api.rootly.com/v1/incidents`
*   **Key Input Parameters (API filters)**:
    *   `user_id` (optional, integer): Filters incidents for a specific user ID.
    *   `created_at_gte` (optional, string): Filters incidents created on or after this ISO 8601 datetime.
    *   `created_at_lte` (optional, string): Filters incidents created on or before this ISO 8601 datetime.
    *   (Pagination parameters `page_number` and `page_size` were previously implemented and could be re-added if needed).
*   **Output**: A list of incident objects matching the filters.

### 3. `UsersTool` (`users_tool.py`)
*   **Purpose**: Retrieves a list of users from the Rootly API. This can be used to get user details like email, Slack ID, etc.
*   **Rootly API Endpoint**: `GET https://api.rootly.com/v1/users`
*   **Key Input Parameters (API filters)**:
    *   `search` (optional, string): Filters users by a search string.
    *   `email` (optional, string): Filters users by email address.
*   **Output**: A list of user objects matching the filters.


## Future Work (Examples)

*   Implement more tools to gather diverse burnout signals (e.g., communication platform analysis, VCS activity, calendar data).
*   Develop the core AI agent logic to synthesize data from these tools.
*   Define and train a model (or use a heuristic-based system) for burnout prediction.
*   Implement robust error handling and logging.
*   Add comprehensive unit and integration tests.
