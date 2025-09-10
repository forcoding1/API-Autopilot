import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def get_page(url: str) -> str:
    async with async_playwright() as p: 
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        content = await page.content()
        await browser.close()
        return content
    
def extract_text_content(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    clean_text = soup.get_text(" ", strip=True)
    return clean_text

# async def main():
#     content = await get_page("https://playwright.dev/docs/writing-tests")
#     clean_text = extract_text_content(content)
#     print(clean_text)


# if __name__ == "__main__":
#     asyncio.run(main())
