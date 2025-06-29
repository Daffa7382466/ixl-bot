import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    print("🚀 MEMULAI BOT IXL...")
    
    async with async_playwright() as p:
        # ========================
        # 1. SETUP BROWSER
        # ========================
        print("🛠️ Menyiapkan browser...")
        browser = await p.chromium.launch(
            headless=True,  # Run tanpa tampilan GUI
            args=[
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)",  # Fake user agent
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ],
            timeout=60000  # Timeout 60 detik
        )
        page = await browser.new_page()
        
        try:
            # ========================
            # 2. PROSES LOGIN
            # ========================
            print("🔐 Mencoba login ke IXL...")
            await page.goto("https://www.ixl.com/signin/", wait_until="networkidle", timeout=60000)
            
            # Screenshot untuk debug
            await page.screenshot(path="1_login_page.png")
            
            # Isi form login
            username = os.getenv("IXL_USERNAME", "daffafalahaldika126")  # Default jika env kosong
            password = os.getenv("IXL_PASSWORD", "ixlnovember17")
            
            await page.fill('input[name="username"]', username)
            await page.fill('input[name="password"]', password)
            
            # Coba 3 cara submit berbeda
            try:
                await page.click('button[type="submit"]', timeout=5000)
            except:
                try:
                    await page.keyboard.press("Enter")
                except:
                    await page.click('text="Sign in"', timeout=5000)
            
            print("✅ LOGIN BERHASIL!")
            await page.screenshot(path="2_after_login.png")

            # ========================
            # 3. AKSES SOAL MATEMATIKA
            # ========================
            print("📚 Menuju ke soal matematika...")
            
            # Coba 2 metode navigasi:
            try:
                # Metode 1: Buka langsung URL soal
                await page.goto(
                    "https://www.ixl.com/math/grade-5/addition",
                    wait_until="domcontentloaded",
                    timeout=20000
                )
                print("🟢 Berhasil buka URL langsung")
            except Exception as e:
                print(f"⚠️ Gagal buka URL langsung: {str(e)}")
                
                # Metode 2: Buka manual lewat menu
                await page.goto("https://www.ixl.com/math/grade-5", timeout=20000)
                await page.screenshot(path="3_math_menu.png")
                
                # Cari tombol Addition dengan 3 selector berbeda
                addition_btn = await page.query_selector('text="Addition", .skill-addition, [aria-label="Addition"]')
                if addition_btn:
                    await addition_btn.click(delay=1000)  # Delay seperti manusia
                    print("🟢 Berhasil klik tombol Addition")
                else:
                    raise Exception("Tombol Addition tidak ditemukan")

            # ========================
            # 4. MENGAMBIL SOAL
            # ========================
            print("🔍 Mencari soal...")
            await page.wait_for_timeout(3000)  # Tunggu 3 detik
            
            # Coba 5 selector berbeda untuk soal
            soal = await page.evaluate('''() => {
                const selectors = [
                    '.math-problem',
                    '.question-text',
                    '[data-testid="math-problem"]',
                    '.ProblemView-problem',
                    '.skill-tree-problem'
                ];
                
                for (const selector of selectors) {
                    const elem = document.querySelector(selector);
                    if (elem && elem.innerText.trim() !== "") {
                        return elem.innerText.trim();
                    }
                }
                return "Soal tidak ditemukan";
            }''')
            
            print(f"📝 HASIL SOAL:\n{soal}")
            await page.screenshot(path="4_question.png")

        except Exception as e:
            # Tangkap semua error dan simpan screenshot
            await page.screenshot(path="error_final.png")
            print(f"❌ ERROR: {str(e)}")
            
            # Debug tambahan: Cetak 500 karakter pertama HTML
            html = await page.content()
            print("ℹ️ STRUKTUR HTML:\n", html[:500])
            
        finally:
            await browser.close()
            print("🛑 BROWSER DITUTUP")

if __name__ == "__main__":
    asyncio.run(main())
