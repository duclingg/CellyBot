from playwright.async_api import async_playwright

def check_followers(account, username):
    url = f"https://www.tiktok.com/@{account}"
    
    with async_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            page.goto(url, timeout=60000)
            
            # scrolling required to load followers dynamically
            for _ in range(10):
                page.mouse.wheel(0, 5000)
                page.wait_for_timeout(1000)
                
            content = page.content()
            browser.close()
            
            return username.lower() in content.lower()
        except Exception as e:
            print(f"[!] Error: {e}")
            browser.close()
            return False