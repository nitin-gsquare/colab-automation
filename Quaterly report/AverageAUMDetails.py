import requests
import json

# --- Confirmed AMFI endpoints for Fundwise AUM ---
quarters = [
    ("April - June 2025", 1, 7397),
    ("July - September 2025", 1, 7559),
]

url = "https://www.amfiindia.com/api/average-aum-fundwise"
combined = []

for qtr_name, fy_id, period_id in quarters:
    params = {
        "fyId": fy_id,
        "periodId": period_id
    }
    print(f"🔄 Fetching {qtr_name} (fyId={fy_id}, periodId={period_id}) ...")
    try:
        r = requests.get(url, params=params, timeout=60)
        if r.status_code == 200:
            data = r.json()
            count = len(data.get("data", []))
            print(f"✅ {qtr_name}: {count} AMC entries")
            combined.append({
                "quarter": qtr_name,
                "fyId": fy_id,
                "periodId": period_id,
                "data": data
            })
        else:
            print(f"❌ Failed {qtr_name} ({r.status_code})")
    except Exception as e:
        print(f"❌ Error fetching {qtr_name}: {e}")

if combined:
    with open("fundwise_qaaum_combined.json", "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=4)
    print("💾 Saved combined file: fundwise_qaaum_combined.json")
else:
    print("⚠️ No data fetched.")




############## Outdated Code - Do Not Use ##############
# import requests
# import json
# import os

# headers = {
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
#     "Accept": "*/*",
#     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#     "X-Requested-With": "XMLHttpRequest",
#     "Accept-Language": "en-US,en;q=0.5"
# }

# session = requests.Session()
# session.headers.update(headers)

# # === 1. Save Year List
# url1 = 'https://www.amfiindia.com/modules/AvergaeAUMYearByMFId'
# data1 = "AUmType=F&MF_Id="
# r1 = session.post(url1, data=data1)
# with open("amfi_years.json", "w", encoding="utf-8") as f:
#     json.dump(r1.json(), f, indent=2)

# # === 2. Save Quarters for a sample/latest Year_Id (adjust as needed)
# url2 = 'https://www.amfiindia.com/modules/AvergaeAUMQuarterByYearId'
# data2 = "AUmType=F&MF_Id=&Year_Id=0"
# r2 = session.post(url2, data=data2)
# with open("amfi_quarters.json", "w", encoding="utf-8") as f:
#     json.dump(r2.json(), f, indent=2)

# # === 3. Save HTML for a sample quarter (change year_id and quarter as needed)
# url3 = 'https://www.amfiindia.com/modules/AverageAUMDetails'
# quarter_str = "April+-+June+2025"
# data3 = f"AUmType=F&AumCatType=&MF_Id=&Year_Id=0&Year_Quarter={quarter_str}"
# r3 = session.post(url3, data=data3)
# with open("amfi_april_-_june_2025.html", "w", encoding="utf-8") as f:
#     f.write(r3.text)

# session.close()

# print("✅ JSONs and HTML saved locally.")
