import asyncio, os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            channel="chromium",
            args=["--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"]
        )
        page = await browser.new_page()
        
        try:
            # Login
            await page.goto("https://www.ixl.com/signin/", timeout=60000)
            await page.screenshot(path="login_page.png")
            
            # Gunakan selector alternatif
            username = os.getenv("IXL_USERNAME")
            password = os.getenv("IXL_PASSWORD")
            
            await page.fill('input[name="username"], input#username', username)
            await page.fill('input[name="password"], input#password', password)
            await page.click('button[type="submit"], text="Sign in"')
            
            # Cek login berhasil
            await page.wait_for_selector('.avatar', timeout=10000)
            print("✅ Login sukses")
            
            # Ambil soal
            await page.goto("https://www.ixl.com/math/grade-5/addition")
            soal = await page.text_content('.question')
            print(f"📝 Soal: {soal}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            await page.screenshot(path="error.png")
            raise
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
