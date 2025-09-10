import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from playwright_m import get_page, extract_text_content
from langchain_google_genai import ChatGoogleGenerativeAI
from models import URLPrompt, APIDescription
from langchain_core.messages import HumanMessage, SystemMessage
from prompts import ApiIntegratorPrompts

from dotenv import load_dotenv
load_dotenv()

async def main():
    prompts = ApiIntegratorPrompts()
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    structured_llm_url = llm.with_structured_output(URLPrompt)
    urlp = "Create a python client access and start timers from this service link: https://www.myintervals.com/api/resource?r=timer"
    op = URLPrompt()
    op.url = " https://www.myintervals.com/api/resource?r=timer"
    op.task = "Create a python client access and start timers"
    # messages1 = [
    #     HumanMessage(content=prompts.url_prompt_separator(urlp))
    # ]
    # op = structured_llm_url.invoke(messages1)
    print(op.url)
    print(op.task)
    structured_llm_func = llm.with_structured_output(APIDescription)
    content = await get_page(op.url)



    clean_text = extract_text_content(content)
    messages2 = [
        HumanMessage(content=prompts.api_functionality_extractor(clean_text, op.task))
    ]
    structured_content = structured_llm_func.invoke(messages2)
    print(structured_content)
    endpoints = structured_content.endpoints

    print(endpoints)

    messages3 = [
        SystemMessage(content = prompts.API_CODEGEN_SYSTEM),
        HumanMessage(content=prompts.api_codegen(structured_content))
    ]
    code = llm.invoke(messages3)
    print("\n\n---------------------------------------------------------------------\n\n")
    print(code.content.replace("`", ""))

if __name__ == "__main__":
    asyncio.run(main())

