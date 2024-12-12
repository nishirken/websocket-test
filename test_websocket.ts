import { chromium, Browser, Page } from 'playwright';

async function run() {
    // Launch the custom Chromium browser
    const browser: Browser = await chromium.launch({
        executablePath: process.env.TEST_BROWSER_PATH,  // Use the custom browser path from the environment variable
        headless: false,
    });

    // Open a new page
    const page: Page = await browser.newPage();

    // Intercept WebSocket connections

    await page.routeWebSocket("ws://localhost:8080", (ws) => {
        console.log("Route Intercepted");
        ws.send("TEST");
        ws.onMessage(message => {
            console.log("Message ", message);
        });
    });
    // Set up the page to open the WebSocket client (HTML + JS)
    await page.goto('http://localhost:8000');  // Assuming the HTML client is being served on this URL

    // Wait for the test to run (e.g., for WebSocket traffic to happen)
    await page.waitForTimeout(10000);  // Wait for 10 seconds

    // Close the browser
    await browser.close();
}

run().catch(console.error);
