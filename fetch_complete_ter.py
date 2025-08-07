import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import urllib.parse
from io import StringIO
import time

# Mapping SchemeCat_Desc to human-readable names
scheme_category_dict = {
    "1": "Income",
    "2": "Growth",
    "3": "Balanced",
    "5": "Money Market",
    "6": "Gilt",
    "7": "ELSS",
    "8": "Assured Return",
    "10": "Fund of Funds - Domestic",
    "14": "Multi Cap Fund",
    "15": "Large Cap Fund",
    "16": "Large & Mid Cap Fund",
    "17": "Mid Cap Fund",
    "18": "Small Cap Fund",
    "19": "Dividend Yield Fund",
    "20": "Value Fund",
    "21": "Contra Fund",
    "22": "Focussed Fund",
    "23": "Sectoral/ Thematic",
    "24": "ELSS",
    "25": "Overnight Fund",
    "26": "Liquid Fund",
    "27": "Ultra Short Duration Fund",
    "28": "Low Duration Fund",
    "29": "Money Market Fund",
    "30": "Short Duration Fund",
    "31": "Medium Duration Fund",
    "32": "Medium to Long Duration Fund",
    "33": "Long Duration Fund",
    "34": "Dynamic Bond",
    "35": "Corporate Bond Fund",
    "36": "Credit Risk Fund",
    "37": "Banking and PSU Fund",
    "38": "Gilt Fund",
    "39": "Gilt Fund with 10 year constant duration",
    "40": "Floater Fund",
    "41": "Conservative Hybrid Fund",
    "42": "Balanced Hybrid Fund",
    "43": "Aggressive Hybrid Fund",
    "44": "Dynamic Asset Allocation or Balanced Advantage",
    "45": "Multi Asset Allocation",
    "46": "Arbitrage Fund",
    "47": "Equity Savings",
    "48": "Retirement Fund",
    "49": "Children's Fund",
    "50": "Index Funds",
    "51": "Gold ETF",
    "52": "Other ETFs",
    "53": "FoF Overseas",
    "54": "FoF Domestic",
    "55": "Flexi Cap Fund"
}

ter_scheme_type_dict = {
    "1": "Open Ended",
    "2": "Close Ended",
    "3": "Interval Fund"
}

ter_scheme_type_and_category_dict = {
    "1": ["14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55"],
    "2": ["1", "2", "3", "5", "6", "7", "8", "10"],
    "3": ["1", "2"]
}

amc_names_dict = {
    'ICICI Prudential Mutual Fund': ['ICICI Prudential Mutual Fund', 'ICICI Prudential', 'ICICI'],
    'LIC Mutual Fund': ['LIC Mutual Fund', 'LIC MF'],
    'Union Mutual Fund': ['Union Mutual Fund', 'Union'],
    'Aditya Birla Sun Life Mutual Fund': ['Aditya Birla Sun Life Mutual Fund', 'Aditya Birla', 'ABSL'],
    'Tata Mutual Fund': ['Tata Mutual Fund', 'Tata'],
    'PPFAS Mutual Fund': ['PPFAS Mutual Fund', 'PPFAS', 'Parag Parikh'],
    'Sundaram Mutual Fund': ['Sundaram Mutual Fund', 'Sundaram'],
    'Quant Mutual Fund': ['Quant Mutual Fund', 'Quant'],
    'Canara Robeco Mutual Fund': ['Canara Robeco Mutual Fund', 'Canara Robeco', 'Canara'],
    'Motilal Oswal Mutual Fund': ['Motilal Oswal Mutual Fund', 'Motilal Oswal', 'Motilal'],
    'Nippon India Mutual Fund': ['Nippon India Mutual Fund', 'Nippon India', 'CPSE', 'Nippon'],
    'Shriram Mutual Fund': ['Shriram Mutual Fund', 'Shriram'],
    'Taurus Mutual Fund': ['Taurus Mutual Fund', 'Taurus'],
    'Mirae Asset Mutual Fund': ['Mirae Asset Mutual Fund', 'Mirae Asset', 'Mirae'],
    'Principal Mutual Fund': ['Principal Mutual Fund', 'Principal'],
    'PGIM India Mutual Fund': ['PGIM India Mutual Fund', 'PGIM India', 'PGIM'],
    'UTI Mutual Fund': ['UTI Mutual Fund', 'UTI'],
    'Mahindra Manulife Mutual Fund': ['Mahindra Manulife Mutual Fund', 'Mahindra Manulife'],
    'IDBI Mutual Fund': ['IDBI Mutual Fund', 'IDBI'],
    'DSP Mutual Fund': ['DSP Mutual Fund', 'DSP'],
    'Bandhan Mutual Fund': ['Bandhan Mutual Fund', 'Bandhan'],
    'Baroda BNP Paribas Mutual Fund': ['Baroda BNP Paribas Mutual Fund', 'Baroda BNP Paribas'],
    '360 ONE Mutual Fund (Formerly Known as IIFL Mutual Fund)': ['360 ONE Mutual Fund (Formerly Known as IIFL Mutual Fund)', '360 ONE', 'IIFL'],
    'IIFCL Mutual Fund (IDF)': ['IIFCL Mutual Fund (IDF)', 'IIFCL'],
    'IL&FS Mutual Fund (IDF)': ['IL&FS Mutual Fund (IDF)', 'IL&FS'],
    'Franklin Templeton Mutual Fund': ['Franklin Templeton Mutual Fund', 'Franklin', 'Templeton'],
    'Invesco Mutual Fund': ['Invesco Mutual Fund', 'Invesco'],
    'Edelweiss Mutual Fund': ['Edelweiss Mutual Fund', 'Edelweiss', 'Bharat'],
    'JM Financial Mutual Fund': ['JM Financial Mutual Fund', 'JM ', 'JM Financial'],
    'Kotak Mahindra Mutual Fund': ['Kotak Mahindra Mutual Fund', 'Kotak'],
    'ITI Mutual Fund': ['ITI '],
    'HSBC Mutual Fund': ['HSBC Mutual Fund', 'HSBC'],
    'HDFC Mutual Fund': ['HDFC Mutual Fund', 'HDFC'],
    'Quantum Mutual Fund': ['Quantum Mutual Fund', 'Quantum'],
    'Navi Mutual Fund': ['Navi Mutual Fund', 'Navi'],
    'SBI Mutual Fund': ['SBI Mutual Fund', 'SBI'],
    'Axis Mutual Fund': ['Axis Mutual Fund', 'Axis'],
    'Bank of India Mutual Fund': ['Bank of India Mutual Fund', 'Bank of India', 'BOI'],
    'NJ Mutual Fund': ['NJ '],
    'Samco Mutual Fund': ['Samco'],
    'WhiteOak Capital Mutual Fund': ['WhiteOak'],
    'Trust Mutual Fund': ['Trust Mutual Fund', 'Trust'],
    'Quant Mutual Fund': ['Quant '],
    'Groww Mutual Fund': ['Indiabulls', 'Groww'],
    'Helios Mutual Fund': ['Helios'],
    'Old Bridge Mutual Fund': ['Old Bridge'],
    'Zerodha Mutual Fund': ['Zerodah'],
    'Bajaj Finserv Mutual Fund': ['Bajaj']
}

amfi_performance_amc_names = {"ALL": "All"}
ter_amc_names = {"-1": "All"}

def fetch_ter_data(month, fin_year, scheme_cat_desc, nav_id):
    url = "https://www.amfiindia.com/modules/LoadTERData"
    payload = {
        "FinTER": fin_year,
        "MonthTER": month,
        "MF_ID": "-1",
        "NAV_ID": nav_id,
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
        print(f"❌ Error for NAV_ID {nav_id}, SchemeCat_Desc {scheme_cat_desc}: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    if not table:
        print(f"❌ No table found for NAV_ID {nav_id}, SchemeCat_Desc {scheme_cat_desc}")
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
        df["NAV_ID"] = nav_id
        df["SchemeCat_Desc"] = scheme_cat_desc
        df["SchemeCat_Name"] = scheme_category_dict.get(scheme_cat_desc, "Unknown")
        df["Scheme Type (Clean)"] = ter_scheme_type_dict.get(nav_id, "Unknown")
        return df
    except Exception as e:
        print(f"❌ Failed to parse table for NAV_ID {nav_id}, SchemeCat_Desc {scheme_cat_desc}: {e}")
        return pd.DataFrame()

def main():
    # month = "07-2025"
    # fin_year = "2025-2026"
    # all_data = []
    
    today = datetime.datetime.today()
    month = today.strftime("%m-%Y")

    # Determine financial year
    if today.month >= 4:
        fin_year = f"{today.year}-{today.year + 1}"
    else:
        fin_year = f"{today.year - 1}-{today.year}"

    all_data = []
    print(f"📅 Current Month: {month}\n")
    print(f"📅 Today Year: {today}\n")
    print(f"📅 Financial Year: {fin_year}\n")
    print(f"📥 Downloading TER for all scheme types and categories in {month} ({fin_year})...\n")

    for nav_id, scheme_categories in ter_scheme_type_and_category_dict.items():
        scheme_type = ter_scheme_type_dict.get(nav_id, "Unknown")
        print(f"➡️ Fetching for Scheme Type: {scheme_type} (NAV_ID: {nav_id})")
        for scheme_cat_desc in scheme_categories:
            print(f"  ➡️ Fetching: {scheme_cat_desc} - {scheme_category_dict.get(scheme_cat_desc, 'Unknown')}")
            df = fetch_ter_data(month, fin_year, scheme_cat_desc, nav_id)
            if not df.empty:
                all_data.append(df)
            time.sleep(1)  # Be gentle with server

    if not all_data:
        print("❌ No data downloaded.")
        return

    final_df = pd.concat(all_data, ignore_index=True)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # filename = f"ter_of_mf_all_categories_{timestamp}.xlsx"
    filename = "ter_of_mf_performance.xlsx"
    
    final_df.to_excel(filename, index=False)
    print(f"\n✅ All categories saved as: {filename}")

if __name__ == "__main__":
    main()