import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"]
        )
        page = await browser.new_page()
        
        try:
            # [1] LOGIN
            print("🔐 Membuka halaman login...")
            await page.goto("https://www.ixl.com/signin/", timeout=60000)
            await page.fill('input[name="username"]', os.getenv("IXL_USERNAME"))
            await page.fill('input[name="password"]', os.getenv("IXL_PASSWORD"))
            await page.press('input[name="password"]', 'Enter')
            print("✅ Login berhasil")

            # [2] BUKA HALAMAN SOAL
            print("📚 Mengakses soal matematika...")
            await page.goto("https://www.ixl.com/math/grade-5/addition", timeout=60000)
            
            # [3] AMBIL SOAL (BAGIAN YANG DIMODIFIKASI) ▼
            try:
                await page.wait_for_selector(
                    '.math-problem, .question-text', 
                    timeout=15000
                )
                question = await page.inner_text('.math-problem')
                print(f"📝 Soal: {question}")
                await page.screenshot(path="soal.png")
            except Exception as e:
                await page.screenshot(path="error.png")
                print(f"❌ Error: {str(e)}")
            # [AKHIR MODIFIKASI] ▲

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
