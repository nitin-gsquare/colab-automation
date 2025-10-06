
####### New Approach (Working) ########
import requests
import json

# Parameters for April - June 2025 (based on your provided API responses)
fy_id = 1  # April 2025 - March 2026
period_id = 7305  # April - June 2025
str_type = "Categorywise"
mf_id = 0  # All mutual funds

# Build the API URL
url = "https://www.amfiindia.com/api/average-aum-schemewise"
params = {
    "strType": str_type,
    "fyId": fy_id,
    "periodId": period_id,
    "MF_ID": mf_id
}

# Send GET request (these APIs use GET, not POST)
r = requests.get(url, params=params)

# Check if successful
if r.status_code == 200:
    data = r.json()  # Parse as JSON
    with open("qaaum_apr_jun_2025.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)  # Save pretty-printed JSON
    print("✅ Saved JSON data file")
else:
    print(f"❌ Request failed with status: {r.status_code}")

# Optional: Print a preview of the data
print(json.dumps(data, indent=4)[:500] + "...")  # First 500 chars for preview



######## Initial Attempt (Working FOR json dOWNLOAD) ########

# import requests
# import json

# # Step 1: Get financial years
# fy_response = requests.get("https://www.amfiindia.com/api/average-aum-fundwise").json()

# # Debug print to confirm structure
# # print(json.dumps(fy_response, indent=2))

# # Correct search string
# fy_id = next(
#     fy["id"] for fy in fy_response["data"] 
#     if "April 2025 - March 2026" in fy["financial_year"]
# )

# print("📅 Found Financial Year ID:", fy_id)

# # Step 2: Get available periods for that financial year
# period_response = requests.get(
#     f"https://www.amfiindia.com/api/average-aum-schemewise?fyId={fy_id}&strType=Categorywise&MF_ID=0"
# ).json()

# # Debug print to confirm structure
# # print(json.dumps(period_response, indent=2))

# # Pick "July - September 2025"
# period_id = next(
#     p["id"] for p in period_response["data"]["periods"] 
#     if "July - September 2025" in p["period"]
# )

# print("🗓️ Found Period ID:", period_id)

# # Step 3: Fetch the AUM data
# aum_response = requests.get(
#     f"https://www.amfiindia.com/api/average-aum-schemewise?strType=Categorywise&fyId={fy_id}&periodId={period_id}&MF_ID=0"
# ).json()

# # Step 4: Save raw JSON
# with open("qaaum_jul_sep_2025.json", "w", encoding="utf-8") as f:
#     json.dump(aum_response, f, indent=2)

# print("✅ Saved AUM data for July - September 2025 in JSON format.")





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
