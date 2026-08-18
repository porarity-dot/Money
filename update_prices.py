import urllib.request
import json
import os
import re
import sys

# Ensure UTF-8 output on Windows consoles
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

def fetch_yahoo_price(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            meta = data['chart']['result'][0]['meta']
            price = meta.get('regularMarketPrice')
            return float(price) if price is not None else None
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None

def update_portfolio():
    print("[*] กำลังดึงราคาตลาดสดและอัตราแลกเปลี่ยน...")
    
    nvda_price = fetch_yahoo_price("NVDA")
    googl_price = fetch_yahoo_price("GOOGL")
    fx_rate = fetch_yahoo_price("USDTHB=X")
    
    print(f"[OK] NVDA Live Price: ${nvda_price:.2f} USD" if nvda_price else "[!] ดึงราคา NVDA ไม่สำเร็จ")
    print(f"[OK] GOOGL Live Price: ${googl_price:.2f} USD" if googl_price else "[!] ดึงราคา GOOGL ไม่สำเร็จ")
    print(f"[OK] USD/THB Interbank Rate: {fx_rate:.2f} THB" if fx_rate else "[!] ดึงค่าเงินไม่สำเร็จ")
    
    # Update HTML file default prices
    html_path = os.path.join(os.path.dirname(__file__), "portfolio_tracker.html")
    if os.path.exists(html_path) and nvda_price and googl_price:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Update NVDA price
        content = re.sub(r"'NVDA':\s*[\d\.]+", f"'NVDA': {nvda_price:.2f}", content)
        # Update GOOGL price
        content = re.sub(r"'GOOGL':\s*[\d\.]+", f"'GOOGL': {googl_price:.2f}", content)
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("[SUCCESS] อัปเดตราคาล่าสุดลงใน portfolio_tracker.html เรียบร้อยแล้ว!")
        
        # Save a live prices JSON file that portfolio_tracker.html can read
        json_path = os.path.join(os.path.dirname(__file__), "live_prices.json")
        prices_data = {
            "last_updated": "latest",
            "NVDA": round(nvda_price, 2),
            "GOOGL": round(googl_price, 2),
            "market_fx": round(fx_rate, 2) if fx_rate else 33.22
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(prices_data, f, indent=2)
        print("[SUCCESS] บันทึก live_prices.json เรียบร้อยแล้ว!")

if __name__ == "__main__":
    update_portfolio()
