import os
import asyncio
from playwright.async_api import async_playwright


async def run():
    # Get the custom Chromium path from the TEST_BROWSER_PATH environment variable
    browser_path = os.getenv('TEST_BROWSER_PATH')

    if not browser_path:
        raise Exception("TEST_BROWSER_PATH environment variable is not set")

    async with async_playwright() as p:
        # Launch the browser using the custom Chromium binary
        browser = await p.chromium.launch(executable_path=browser_path, headless=False)
        page = await browser.new_page()

        # Intercept WebSocket connections
        def message_handler(ws, message):
            print("REQUEST")
            ws.send("response")

        def route_handler(ws):
            print("Route intercepted")
            ws.send("TEST")
            ws.on_message(
                lambda message: message_handler(ws, message)
            )

        await page.route_web_socket("ws://localhost:8080", route_handler)

        # Set up the page to open the WebSocket client (HTML + JS)
        await page.goto("http://localhost:8000")  # URL of the HTML page served by the HTTP server

        # Wait for interaction or timeout
        await page.wait_for_timeout(10000)  # Wait for 10 seconds

        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
