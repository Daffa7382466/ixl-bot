import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    # Install browser Chromium kalau belum ada
    if not os.path.exists("/usr/bin/chromium"):
        os.system("playwright install chromium")
        os.system("playwright install-deps")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("🔐 Membuka halaman login...")
        await page.goto("https://www.ixl.com/signin/")

        # Pakai environment variable lebih aman!
        username = os.getenv('IXL_USERNAME', 'daffafalahaldika126')  # default value
        password = os.getenv('IXL_PASSWORD', 'ixlnovember17')  # default value
        
        await page.fill('input#username', username)
        await page.fill('input#password', password)
        await page.press('input#password', 'Enter')

        print("✅ Login berhasil, membuka soal...")
        await page.wait_for_timeout(3000)

        await page.goto("https://www.ixl.com/math/grade-5/addition")
        await page.wait_for_timeout(3000)

        soal = await page.inner_text('.question')
        print("📝 Soal:", soal)

        await browser.close()

asyncio.run(main())
