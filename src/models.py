from typing import List, Literal, Optional
from pydantic import BaseModel


class ResearchQuery(BaseModel):
    url: str
    query: str


class URLPrompt(BaseModel):
    url: Optional[str] = None
    task: Optional[str] = None


class FunctionDescription(BaseModel):
    language: Literal["javascript", "typescript", "python", "other"] = "javascript"
    code_snippets: List[str]


class APIEndpoint(BaseModel):
    http_method: str                    # GET, POST, PUT, DELETE
    path: str                           # e.g. /api/v1/users
    description: Optional[str] = None
    parameters: Optional[List[str]] = None
    requires_api_key: bool = False      # true if authentication needed
    request_example: Optional[str] = None
    response_example: Optional[str] = None
    api_key: Optional[str] = None


class APIDescription(BaseModel):
    title: str
    base_url: str
    endpoints: List[APIEndpoint]


class ResearchState(BaseModel):
    query: URLPrompt
    api_info: Optional[APIDescription] = None
    code: str = ""
    file_name: str = ""
    requires_api_key: Literal["api_key", "code_gen"] = "code_gen"
    api_key: Optional[str] = None
