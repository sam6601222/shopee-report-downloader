import asyncio
from playwright.async_api import async_playwright
import datetime
import os
import calendar

# 配置區
START_YEAR = 2021
START_MONTH = 4
AUTH_FILE = "auth.json"
DOWNLOAD_DIR = "reports"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def get_month_ranges():
    ranges = []
    current_date = datetime.date(START_YEAR, START_MONTH, 1)
    today = datetime.date.today()
    
    while current_date <= today:
        last_day = calendar.monthrange(current_date.year, current_date.month)[1]
        start_str = current_date.strftime("%Y-%m-%d")
        end_str = current_date.replace(day=last_day).strftime("%Y-%m-%d")
        ranges.append((start_str, end_str))
        
        # 移動到下個月
        if current_date.month == 12:
            current_date = datetime.date(current_date.year + 1, 1, 1)
        else:
            current_date = datetime.date(current_date.year, current_date.month + 1, 1)
    return ranges

async def download_shopee_reports():
    if not os.path.exists(AUTH_FILE):
        print("錯誤: 找不到 auth.json，請先執行 python login.py")
        return

    async with async_playwright() as p:
        # 使用 headless=False 方便觀察進度，若穩定後可改為 True
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=AUTH_FILE)
        page = await context.new_page()
        
        print("正在前往蝦皮賣家中心...")
        await page.goto("https://seller.shopee.tw/portal/sale?type=completed")
        
        # 等待頁面載入
        await page.wait_for_load_state("networkidle")
        
        month_ranges = get_month_ranges()
        print(f"預計下載 {len(month_ranges)} 份報表...")

        for start_date, end_date in month_ranges:
            print(f"正在準備下載: {start_date} 至 {end_date}")
            
            try:
                # 這裡需要根據蝦皮實際的 Selector 進行操作
                # 1. 點擊日期選擇器 (這部分通常是 .shopee-date-picker)
                # 2. 輸入 start_date 與 end_date
                # 3. 點擊匯出按鈕
                
                # 注意: 蝦皮後台 UI 經常更新，以下為示意邏輯，具體 Selector 需依實際狀況微調
                # 點擊日期範圍按鈕
                # await page.click(".date-picker-trigger") 
                
                # 這裡模擬點擊並輸入日期 (開發者需根據當前 DOM 調整)
                # ... 
                
                print(f"已點擊匯出 {start_date}，現在進入 65 秒緩衝時間...")
                await asyncio.sleep(65) # 遵守 1 分鐘下載限制
                
            except Exception as e:
                print(f"下載 {start_date} 時發生錯誤: {e}")
                # 錯誤時可以選擇跳過或停止
                continue

        await browser.close()
        print("所有任務已完成！")

if __name__ == "__main__":
    asyncio.run(download_shopee_reports())
