import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import urllib.parse
from io import StringIO
import time

# Mapping SchemeCat_Desc to human-readable names
scheme_category_dict = {
    "14":"Multi Cap Fund", "15":"Large Cap Fund", "16":"Large & Mid Cap Fund",
    "17":"Mid Cap Fund", "18":"Small Cap Fund", "19":"Dividend Yield Fund",
    "20":"Value Fund", "21":"Contra Fund", "22":"Focussed Fund",
    "23":"Sectoral/ Thematic", "24":"ELSS", "25":"Overnight Fund",
    "26":"Liquid Fund", "27":"Ultra Short Duration Fund", "28":"Low Duration Fund",
    "29":"Money Market Fund", "30":"Short Duration Fund", "31":"Medium Duration Fund",
    "32":"Medium to Long Duration Fund", "33":"Long Duration Fund", "34":"Dynamic Bond",
    "35":"Corporate Bond Fund", "36":"Credit Risk Fund", "37":"Banking and PSU Fund",
    "38":"Gilt Fund", "39":"Gilt Fund with 10 year constant duration", "40":"Floater Fund",
    "41":"Conservative Hybrid Fund", "42":"Balanced Hybrid Fund", "43":"Aggressive Hybrid Fund",
    "44":"Dynamic Asset Allocation or Balanced Advantage", "45":"Multi Asset Allocation",
    "46":"Arbitrage Fund", "47":"Equity Savings", "48":"Retirement Fund",
    "49":"Children's Fund", "50":"Index Funds", "51":"Gold ETF", "52":"Other  ETFs",
    "53":"FoF Overseas", "54":"FoF Domestic", "55":"Flexi Cap Fund"
}

def fetch_ter_data(month, fin_year, scheme_cat_desc):
    url = "https://www.amfiindia.com/modules/LoadTERData"
    payload = {
        "FinTER": fin_year,
        "MonthTER": month,
        "MF_ID": "-1",
        "NAV_ID": "1",
        "SchemeCat_Desc": scheme_cat_desc
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.amfiindia.com",
        "Referer": "https://www.amfiindia.com/ter-of-mf-schemes"
    }

    try:
        response = requests.post(url, data=urllib.parse.urlencode(payload), headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Error for category {scheme_cat_desc}: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    if not table:
        print(f"❌ No table found for SchemeCat_Desc = {scheme_cat_desc}")
        return pd.DataFrame()

    try:
        df = pd.read_html(StringIO(str(table)))[0]

        # Rename columns to expected internal names
        df.rename(columns={
            'Regular Plan - Base TER (%)': 'Regular Base TER',
            'Regular Plan - Additional expense as per Regulation 52(6A)(b) (%)': 'Regular 52(6A)(B)',
            'Regular Plan - Additional expense as per Regulation 52(6A)(c) (%)': 'Regular 52(6A)(C)',
            'Regular Plan - GST (%)': 'Regular GST',
            'Regular Plan - Total TER (%)': 'Regular Total',
            'Direct Plan - Base TER (%)': 'Direct Base TER',
            'Direct Plan - Additional expense as per Regulation 52(6A)(b) (%)': 'Direct 52(6A)(B)',
            'Direct Plan - Additional expense as per Regulation 52(6A)(c) (%)': 'Direct 52(6A)(C)',
            'Direct Plan - GST (%)': 'Direct GST',
            'Direct Plan - Total TER (%)': 'Direct Total',
        }, inplace=True)

        df["TER Date"] = pd.to_datetime(df["TER Date"], errors="coerce")
        df["Date"] = datetime.datetime.strptime(month, "%m-%Y").strftime("%Y-%m-01")
        df["MF_ID"] = "-1"
        df["NAV_ID"] = "1"
        df["SchemeCat_Desc"] = scheme_cat_desc
        df["SchemeCat_Name"] = scheme_category_dict.get(scheme_cat_desc, "Unknown")
        df["Scheme Type (Clean)"] = "Open Ended"
        return df
    except Exception as e:
        print(f"❌ Failed to parse table for category {scheme_cat_desc}: {e}")
        return pd.DataFrame()

def main():
    month = "07-2025"
    fin_year = "2025-2026"
    all_data = []

    print(f"📥 Downloading TER for all categories in {month}...\n")

    for scheme_cat_desc in scheme_category_dict.keys():
        print(f"➡️  Fetching: {scheme_cat_desc} - {scheme_category_dict[scheme_cat_desc]}")
        df = fetch_ter_data(month, fin_year, scheme_cat_desc)
        if not df.empty:
            all_data.append(df)
        time.sleep(1)  # Be gentle with server

    if not all_data:
        print("❌ No data downloaded.")
        return

    final_df = pd.concat(all_data, ignore_index=True)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"ter_of_mf_all_categories_{timestamp}.xlsx"
    final_df.to_excel(filename, index=False)
    print(f"\n✅ All categories saved as: {filename}")

if __name__ == "__main__":
    main()
