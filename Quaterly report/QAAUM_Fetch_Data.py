import requests

Year_Quarter = "April - June 2025"  # or use logic to get this dynamically

r = requests.post(
    "https://www.amfiindia.com/modules/AverageAUMDetails",
    data={
        'AUmType': 'S',
        'AumCatType': 'Categorywise',
        'MF_Id': -1,
        'Year_Id': 0,
        'Year_Quarter': Year_Quarter
    }
)

with open("qaaum_apr_jun_2025.html", "w", encoding="utf-8") as f:
    f.write(r.text)

print("✅ Saved raw HTML file")
