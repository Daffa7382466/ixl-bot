import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Launch browser with proper configuration
        browser = await p.chromium.launch(
            headless=True,
            channel="chromium",
            args=[
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ],
            timeout=60000
        )
        page = await browser.new_page()
        
        try:
            # Navigate to login page
            print("🔐 Opening login page...")
            await page.goto("https://www.ixl.com/signin/", timeout=60000)
            await page.screenshot(path="login_page.png")

            # Fill login form (using environment variables)
            username = os.getenv("IXL_USERNAME", "daffafalahaldika126")
            password = os.getenv("IXL_PASSWORD", "ixlnovember17")
            
            # Multiple selector options for robustness
            await page.fill('input[name="username"], input#username', username)
            await page.fill('input[name="password"], input#password', password)
            
            # Try different ways to submit
            try:
                await page.click('button[type="submit"], button:has-text("Sign in")', timeout=10000)
            except:
                print("Using Enter key as fallback")
                await page.press('input[name="password"]', 'Enter')

            # Verify login success
            try:
                await page.wait_for_selector('.avatar', timeout=10000)
                print("✅ Login successful")
            except:
                await page.screenshot(path="login_failed.png")
                raise Exception("Login failed - check login_failed.png")

            # Navigate to questions page
            print("📚 Accessing math problems...")
            await page.goto("https://www.ixl.com/math/grade-5/addition", timeout=60000)
            
            # Get question text with multiple fallbacks
            try:
                question = await page.inner_text('.question', timeout=10000)
                print(f"📝 Question: {question}")
            except:
                await page.screenshot(path="question_page.png")
                question = "Could not extract question - check question_page.png"
                print(question)

            # Additional debugging screenshot
            await page.screenshot(path="final_page.png")

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            await page.screenshot(path="error.png")
            raise

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
