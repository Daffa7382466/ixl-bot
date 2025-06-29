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
            await page.screenshot(path="2_after_login.png")

            # 3. AKSES HALAMAN SOAL
            print("📚 Mengarahkan ke soal matematika...")
            try:
                await page.goto(
                    "https://www.ixl.com/math/grade-5/addition",
                    wait_until="domcontentloaded",
                    timeout=15000
                )
            except:
                # Fallback jika URL langsung gagal
                await page.goto("https://www.ixl.com/math/grade-5")
                await page.click('text="Addition"')
            
            await page.screenshot(path="3_math_page.png")

            # 4. PROSES AMBIL SOAL
            print("🔍 Mencari soal...")
            try:
                # Coba klik tombol start jika ada
                await page.click('text="Start practicing"', timeout=5000, delay=1000)
                print("🟢 Tombol 'Start practicing' diklik")
            except:
                print("ℹ️ Tidak menemukan tombol start")

            # Tunggu dan cari soal
            try:
                await page.wait_for_timeout(3000)  # Tunggu rendering
                
                # Evaluasi semua kemungkinan selector
                soal = await page.evaluate('''() => {
                    const selectors = [
                        '.math-problem',
                        '.question-text',
                        '.ProblemView-problem',
                        '[data-testid="math-problem"]',
                        '.skill-tree-problem'
                    ];
                    
                    for (const selector of selectors) {
                        const elem = document.querySelector(selector);
                        if (elem && elem.innerText.trim() !== "") {
                            return elem.innerText.trim();
                        }
                    }
                    return null;
                }''')

                if soal:
                    print(f"📝 SOAL DITEMUKAN:\n{soal}")
                    await page.screenshot(path="4_question.png")
                else:
                    raise Exception("Tidak menemukan elemen soal")
                    
            except Exception as e:
                await page.screenshot(path="error_final.png")
                print(f"❌ GAGAL: {str(e)}")
                
                # Debug tambahan
                html = await page.evaluate('''() => {
                    return document.documentElement.outerHTML;
                }''')
                print("ℹ️ Struktur HTML (500 karakter pertama):", html[:500])
                
        finally:
            await browser.close()
            print("🛑 Browser ditutup")

if __name__ == "__main__":
    print("🚀 Memulai bot IXL...")
    asyncio.run(main())
