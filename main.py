import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("🔐 Membuka halaman login...")
        await page.goto("https://www.ixl.com/signin/")

        # Ganti dengan username dan password kamu
        await page.fill('input#username', 'daffafalahaldika126')
        await page.fill('input#password', 'ixlnovember17')
        await page.press('input#password', 'Enter')

        print("✅ Login berhasil, membuka soal...")

        await page.wait_for_timeout(3000)  # tunggu 3 detik

        await page.goto("https://www.ixl.com/math/grade-5/addition")
        await page.wait_for_timeout(3000)

        soal = await page.inner_text('.question')
        print("📝 Soal:", soal)

        await browser.close()

asyncio.run(main())
