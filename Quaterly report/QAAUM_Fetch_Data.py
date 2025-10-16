
# ####### New Approach (Working) ########

import requests
import json

# --- Quarters and IDs confirmed from AMFI ---
quarters = [
    ("April - June 2025", 1, 7305),
    ("July - September 2025", 1, 7467),
]

# --- Common parameters ---
url = "https://www.amfiindia.com/api/average-aum-schemewise"
str_type = "Categorywise"
mf_id = 0

combined = []

for qtr_name, fy_id, period_id in quarters:
    params = {"strType": str_type, "fyId": fy_id, "periodId": period_id, "MF_ID": mf_id}
    print(f"🔄 Fetching {qtr_name} (fyId={fy_id}, periodId={period_id}) ...")
    try:
        r = requests.get(url, params=params, timeout=60)
        if r.status_code == 200:
            data = r.json()
            count = len(data.get("data", []))
            print(f"✅ {qtr_name}: {count} entries")
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

# --- Save combined JSON ---
if combined:
    with open("qaaum_combined.json", "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=4)
    print("💾 Saved combined file: qaaum_combined.json")
else:
    print("⚠️ No data fetched.")



################# Old Approach (Commented Out) #################


# import requests

# Year_Quarter = "July - September 2025"  # or use logic to get this dynamically

# r = requests.post(
#     "https://www.amfiindia.com/modules/AverageAUMDetails",
#     data={
#         'AUmType': 'S',
#         'AumCatType': 'Categorywise',
#         'MF_Id': -1,
#         'Year_Id': 0,
#         'Year_Quarter': Year_Quarter
#     }
# )

# with open("qaaum_july_sept_2025.html", "w", encoding="utf-8") as f:
#     f.write(r.text)

# print("✅ Saved raw HTML file")
