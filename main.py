import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # 1. Launch Browser
        browser = await p.chromium.launch(
            headless=True,
            args=["--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"]
        )
        page = await browser.new_page()
        
        try:
            # 2. Buka Halaman Login
            print("🔐 Membuka halaman login...")
            await page.goto("https://www.ixl.com/signin/", timeout=60000)
            
            # 3. Ambil Screenshot untuk Debug
            await page.screenshot(path="debug_login.png")
            
            # 4. Isi Username (Versi lebih aman)
            username_field = await page.wait_for_selector('input#username', timeout=60000)
            await username_field.fill(os.getenv("IXL_USERNAME"))
            
            # 5. Isi Password
            await page.fill('input#password', os.getenv("IXL_PASSWORD"))
            await page.press('input#password', 'Enter')
            
            print("✅ Login berhasil!")
            
            # 6. Buka Halaman Soal
            await page.goto("https://www.ixl.com/math/grade-5/addition", timeout=60000)
            await page.screenshot(path="debug_soal.png")
            
            # 7. Ambil Soal
            soal = await page.inner_text('.question', timeout=60000)
            print(f"📝 Soal: {soal}")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            await page.screenshot(path="error.png")
            raise
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
