import asyncio
from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, END
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from .playwright_m import get_page, extract_text_content
from langchain_google_genai import ChatGoogleGenerativeAI
from .models import URLPrompt, APIDescription, ResearchState
from langchain_core.messages import HumanMessage, SystemMessage
from .prompts import ApiIntegratorPrompts
import unicodedata



class Workflow:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        self.prompts = ApiIntegratorPrompts()
        self.workflow = self._build_workflow()


    def _build_workflow(self):
        graph = StateGraph(ResearchState)
        graph.add_node("scrape_content", self._scrape_content)
        graph.add_node("code_gen", self._api_codegen)
        graph.add_node("file_writer", self._file_writer)
        graph.add_node("api_key", self._api_input)
        graph.set_entry_point("scrape_content")
        graph.add_edge("scrape_content", "code_gen")
        graph.add_conditional_edges("scrape_content", self._api_key_required)
        graph.add_edge("api_key" ,"code_gen")
        graph.add_edge("code_gen", "file_writer")
        graph.add_edge("file_writer", END)
        return graph.compile()

    def _api_input(self, state:ResearchState) -> str:
        api_key = input("API_KEY: ")
        return {"api_key": api_key}
    
    def _api_key_required(self, state: ResearchState) -> Literal["api_key","code_gen"]:
        for endpoints in state.api_info.endpoints:
            if endpoints.requires_api_key:
                return "api_key"
        return "code_gen"


    async def _scrape_content(self, state: ResearchState) -> APIDescription:
        combined_query = state.query
        structured_llm = self.llm.with_structured_output(APIDescription)
        extracted_content = await get_page(combined_query.url)
        extracted_text = extract_text_content(extracted_content)
        messages = [
            
            SystemMessage(content=self.prompts.API_FUNCTIONALITY_SYSTEM) ,
            HumanMessage(content=self.prompts.api_functionality_extractor(extracted_text, combined_query.task))
            
            ]
        api_info = structured_llm.invoke(messages)
        api_info.title = unicodedata.normalize('NFKD', api_info.title).encode('ascii', 'ignore').decode('utf-8')

        print("Title: " + api_info.title)
        print(f"No of relevant endpoints extracted: {len(api_info.endpoints)}")
        return {"api_info": api_info}
    
    def _api_codegen(self, state: ResearchState) -> str:
        for endpoint in state.api_info.endpoints:
            if state.api_key:
                endpoint.api_key = state.api_key
        messages = [
            SystemMessage(content = self.prompts.API_CODEGEN_SYSTEM),
            HumanMessage(content= self.prompts.api_codegen(state.api_info))
        ]
        code = self.llm.invoke(messages)
        code = code.content.replace("`", "").replace("python", "") 
        print("Code Generated......")
        return {"code": code}
    

    def _file_writer(self, state: ResearchState) -> str:
        file_name = f"{state.api_info.title}.py"
        print("Writing to a file.....")
        with open(file_name, 'w') as file:
            file.write(state.code)
        print("Generated code file: " + file_name)
        return {"file_name": file_name}




    async def run(self, query: URLPrompt) -> ResearchState:
        initial_state = ResearchState(query=query)
        final_state = await self.workflow.ainvoke(initial_state)
        return ResearchState(**final_state)




