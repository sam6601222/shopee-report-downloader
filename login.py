import asyncio
from playwright.async_api import async_playwright
import os

async def save_auth():
    async with async_playwright() as p:
        # 使用帶介面的瀏覽器供使用者手動登入
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        print("請在開啟的瀏覽器中登入蝦皮賣家中心...")
        await page.goto("https://seller.shopee.tw/portal/sale")
        
        # 等待使用者手動登入成功，直到網址包含 portal 或是看到特定的元素
        # 這裡設定 5 分鐘供使用者輸入帳密、驗證碼與 2FA
        try:
            await page.wait_for_url("**/portal/sale**", timeout=300000)
            print("檢測到登入成功！正在儲存登入狀態...")
            
            # 儲存 Storage State (Cookies, LocalStorage)
            await context.storage_state(path="auth.json")
            print("登入狀態已儲存至 auth.json")
        except Exception as e:
            print(f"等待超時或發生錯誤: {e}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(save_auth())
