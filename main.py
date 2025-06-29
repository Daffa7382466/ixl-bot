import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # 1. BUKA BROWSER
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "--no-sandbox"
            ],
            timeout=60000  # Timeout 60 detik
        )
        page = await browser.new_page()
        
        try:
            # 2. LOGIN IXL
            print("🔐 Membuka halaman login...")
            await page.goto("https://www.ixl.com/signin/", timeout=60000)
            
            # Isi username & password (pakai environment variables)
            username = os.getenv("IXL_USERNAME", "daffafalahaldika126")  # Default fallback
            password = os.getenv("IXL_PASSWORD", "ixlnovember17")         # Default fallback
            
            await page.fill('input[name="username"], input#username', username)
            await page.fill('input[name="password"], input#password', password)
            
            # Submit form (coba 3 cara)
            try:
                await page.click('button[type="submit"]', timeout=5000)
            except:
                try:
                    await page.click('text="Sign in"', timeout=5000)
                except:
                    await page.press('input[name="password"]', 'Enter')
            
            print("✅ Login berhasil!")
            await page.wait_for_url("**/dashboard**", timeout=10000)  # Tunggu sampai redirect

            # 3. BUKA HALAMAN SOAL
            print("📚 Menuju ke soal matematika...")
            await page.goto(
                "https://www.ixl.com/math/grade-5/addition",
                wait_until="networkidle",  # Tunggu sampai jaringan idle
                timeout=15000
            )
            
            # 4. AMBIL SOAL
            try:
                # Tunggu sampai soal muncul
                await page.wait_for_selector(
                    '.math-problem, .question, [data-testid="math-problem"]',
                    state="visible",
                    timeout=20000  # Timeout 20 detik
                )
                
                # Ambil teks soal
                soal = await page.evaluate('''() => {
                    const elem = document.querySelector('.math-problem') || 
                                document.querySelector('.question-text');
                    return elem?.innerText.trim() || "Soal tidak ditemukan";
                }''')
                
                print(f"📝 SOAL: {soal}")
                await page.screenshot(path="hasil_soal.png")  # Simpan bukti screenshot
                
            except Exception as e:
                await page.screenshot(path="error_soal.png")
                print(f"❌ GAGAL: {str(e)}")
                print("ℹ️ Cek 'error_soal.png' untuk debug")

        except Exception as e:
            await page.screenshot(path="error_utama.png")
            print(f"💥 ERROR KRITIS: {str(e)}")
            raise

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
