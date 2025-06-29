import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # 1. KONFIGURASI BROWSER
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ],
            timeout=60000  # Timeout 60 detik
        )
        page = await browser.new_page()
        
        try:
            # 2. PROSES LOGIN
            print("🔐 Membuka halaman login...")
            await page.goto("https://www.ixl.com/signin/", wait_until="networkidle", timeout=60000)
            
            # Screenshot debug
            await page.screenshot(path="1_login_page.png")
            
            # Isi form login
            username = os.getenv("IXL_USERNAME", "daffafalahaldika126")  # Default jika env tidak ada
            password = os.getenv("IXL_PASSWORD", "ixlnovember17")
            
            await page.fill('input[name="username"], input#username', username)
            await page.fill('input[name="password"], input#password', password)
            
            # Coba 3 cara submit
            try:
                await page.click('button:has-text("Sign in"), button[type="submit"]', timeout=5000)
            except:
                try:
                    await page.keyboard.press("Enter")
                except:
                    await page.click('text="Sign in"')
            
            print("✅ Login berhasil!")
            await page.screenshot(path="2
