class ApiIntegratorPrompts:
    @staticmethod
    def url_prompt_separator(query: str) -> str:
        return f"""Query: {query}

            Task:
            1. Identify the documentation URL.
            2. State clearly what the user’s goal is.

            Return JSON:
            - url: full link to the documentation
            - task: concise user goal
            """

    API_FUNCTIONALITY_SYSTEM = """
        You are an expert API documentation analyst.  
        You specialize in reading API docs and extracting structured, developer-ready metadata.
        """
    
    @staticmethod
    def api_functionality_extractor(page_text: str, task: str) -> str:
        return f"""Documentation content:
            {page_text}

            User goal: {task}

            Your tasks:
            1. Identify all API endpoints relevant to the user’s goal.
            2. For each endpoint, extract:
            - method: HTTP method (GET, POST, PUT, DELETE, etc.)
            - path: the request path (e.g. /api/v1/users)
            - description: short, clear explanation of what the endpoint does
            - parameters: list of parameters (name, type, required/optional)
            - requires_api_key: true/false (whether authentication is needed)
            - request_example: example request if available
            - response_example: example response if available
            3. If the API has a base URL, include it.
            4. Ignore irrelevant details, markdown, or styling.

            Return JSON strictly following this schema:
            - title: API title
            - base_url: base url if given
            - endpoints: list of endpoint objects
            """
    
    API_CODEGEN_SYSTEM = """
            You are an expert software engineer. I will provide you with structured API metadata (title, base_url, endpoints with details such as method, path, description, parameters, authentication requirements, request examples, and response examples).  
            Your task is to generate a complete, ready-to-use API client in Python.  
            Keep the code as conscise and precise as possible as we need only necessary information.
            The code should be in a format which I can directly copy paste into a python file.
            It should include only ascii characters.
            """
    
    @staticmethod
    def api_codegen(structured_api_info: str) -> str:
        return f"""
            Requirements:  
            1. Create a clean, reusable Python module or class named after the API title (camel-cased, safe for Python).  
            2. For each endpoint:  
            - Implement a dedicated function with descriptive names.  
            - Include clear docstrings explaining the purpose, parameters, and return values.  
            - Handle authentication automatically (API key headers or query params as required).  
            - Provide a **working code example** showing how to call the function. 
            3. Make sure to add the base url from the information provided 
            4. Wrap network calls with error handling (HTTP status codes, missing params, etc.).  
            5. Keep code production-ready, with clear parameter type hints while keeping them very short.  
            6. Ensure the response is parsed into Python dictionaries/objects.  
            Input (structured metadata): {structured_api_info} 
            """