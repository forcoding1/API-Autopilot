import asyncio
from typing import Dict, Any
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
        graph.set_entry_point("scrape_content")
        graph.add_edge("scrape_content", "code_gen")
        graph.add_edge("code_gen", "file_writer")
        graph.add_edge("file_writer", END)
        return graph.compile()



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

        print(len(api_info.endpoints))
        print(api_info.title)
        return {"api_info": api_info}
    
    def _api_codegen(self, state: ResearchState) -> str:
        messages = [
            SystemMessage(content = self.prompts.API_CODEGEN_SYSTEM),
            HumanMessage(content= self.prompts.api_codegen(state.api_info))
        ]
        code = self.llm.invoke(messages)
        code = code.content.replace("`", "").replace("python", "") 
        print("\n\n---------------------------------------------------------------------\n\n")
        print(code)
        return {"code": code}
    

    def _file_writer(self, state: ResearchState) -> str:
        file_name = f"{state.api_info.title}.py"
        with open(file_name, 'w') as file:
            file.write(state.code)

        print(file_name)
        return {"file_name": file_name}




    async def run(self, query: URLPrompt) -> ResearchState:
        initial_state = ResearchState(query=query)
        final_state = await self.workflow.ainvoke(initial_state)
        return ResearchState(**final_state)




