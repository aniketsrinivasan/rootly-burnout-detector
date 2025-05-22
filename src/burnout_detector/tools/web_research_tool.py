from smolagents import Tool


class WebResearchTool(Tool):
    name: str = "web_research_tool"
    description: str = "A tool for searching the public web, particularly for finding information on burnout"
    inputs: dict = {
        "query_terms": {
            "type": "list[string]",
            "description": "The query terms to search the web for."
        },
        "max_results": {
            "type": "int",
            "description": "The maximum number of results to return."
        },
    }
    output_type: str = "object"
    
    def forward(self, query_terms: list[str], max_results: int):
        """
        A tool for searching the public web, particularly for finding information on burnout.
        """
        # Make the API call here, and return the response. 
        return f"Hello, {query_terms}!"
