import sys
import requests
import pandas as pd
import datetime
import time

scheme_category_dict = {
    "1": "Income", "2": "Growth", "3": "Balanced", "5": "Money Market", "6": "Gilt",
    "7": "ELSS", "8": "Assured Return", "10": "Fund of Funds - Domestic", "14": "Multi Cap Fund",
    "15": "Large Cap Fund", "16": "Large & Mid Cap Fund", "17": "Mid Cap Fund",
    "18": "Small Cap Fund", "19": "Dividend Yield Fund", "20": "Value Fund",
    "21": "Contra Fund", "22": "Focussed Fund", "23": "Sectoral/ Thematic", "24": "ELSS",
    "25": "Overnight Fund", "26": "Liquid Fund", "27": "Ultra Short Duration Fund",
    "28": "Low Duration Fund", "29": "Money Market Fund", "30": "Short Duration Fund",
    "31": "Medium Duration Fund", "32": "Medium to Long Duration Fund", "33": "Long Duration Fund",
    "34": "Dynamic Bond", "35": "Corporate Bond Fund", "36": "Credit Risk Fund",
    "37": "Banking and PSU Fund", "38": "Gilt Fund", "39": "Gilt Fund with 10 year constant duration",
    "40": "Floater Fund", "41": "Conservative Hybrid Fund", "42": "Balanced Hybrid Fund",
    "43": "Aggressive Hybrid Fund", "44": "Dynamic Asset Allocation or Balanced Advantage",
    "45": "Multi Asset Allocation", "46": "Arbitrage Fund", "47": "Equity Savings",
    "48": "Retirement Fund", "49": "Children's Fund", "50": "Index Funds", "51": "Gold ETF",
    "52": "Other ETFs", "53": "FoF Overseas", "54": "FoF Domestic", "55": "Flexi Cap Fund"
}

ter_scheme_type_dict = {"1": "Open Ended", "2": "Close Ended", "3": "Interval Fund"}

ter_scheme_type_and_category_dict = {
    "1": ["14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
           "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
           "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55"],
    "2": ["1", "2", "3", "5", "6", "7", "8", "10"],
    "3": ["1", "2"]
}

DATA_URL = "https://www.amfiindia.com/api/populate-te-rdata-revised"

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


def get_standard_amc(scheme_name):
    for amc, aliases in amc_names_dict.items():
        if any(alias.lower() in scheme_name.lower() for alias in aliases):
            return amc
    return "Unknown"


def fetch_ter_data(month, fin_year, scheme_cat_desc, nav_id):
    all_pages = []
    page = 1
    page_size = 500

    while True:
        params = {
            "MF_ID": "All",
            "Month": month,
            "strCat": scheme_cat_desc,
            "strType": nav_id,
            "page": page,
            "pageSize": page_size
        }

        try:
            r = requests.get(DATA_URL, params=params, timeout=30)
            r.raise_for_status()
            data = r.json()

            if "data" not in data or not data["data"]:
                break

            df = pd.DataFrame(data["data"])
            all_pages.append(df)

            meta = data.get("meta", {})
            total_pages = meta.get("pageCount", 1)
            print(f"    ✅ Page {page}/{total_pages} fetched ({len(df)} records)")
            if page >= total_pages:
                break
            page += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ Error fetching NAV_ID {nav_id}, SchemeCat_Desc {scheme_cat_desc}: {e}")
            break

    if not all_pages:
        return pd.DataFrame()

    df = pd.concat(all_pages, ignore_index=True)

    df["SchemeCat_Name"] = scheme_category_dict.get(str(scheme_cat_desc), "Unknown")
    df["Scheme Type (Clean)"] = ter_scheme_type_dict.get(str(nav_id), "Unknown")
    df["AMC_NAME"] = df["Scheme_Name"].apply(get_standard_amc)
    df["TER Date"] = pd.to_datetime(df.get("TER_Date"), errors="coerce").dt.tz_localize(None)
    df["Date"] = datetime.datetime.strptime(month, "%m-%Y").strftime("%Y-%m-01")
    df["MF_ID"] = "-1"
    df["NAV_ID"] = nav_id
    df["SchemeCat_Desc"] = scheme_cat_desc

    # AMFI moved TER disclosure from Regulation 52(6A) to Regulation 66 of the
    # SEBI (Mutual Funds) Regulations, 2026, so the API's field names changed too
    # (R_BaseTER/R_6A_B/R_6A_C/R_GST -> R_BER/R_BrokerageCost/R_TransactionCost/R_StatutoryLevies).
    # This is a best-effort mapping onto the legacy column names for schema
    # continuity, not a verified regulatory equivalence -- see docs/TER_CHANGES.md.
    rename_map = {
        "R_BER": "Regular Base TER",
        "R_BrokerageCost": "Regular 52(6A)(B)",
        "R_TransactionCost": "Regular 52(6A)(C)",
        "R_StatutoryLevies": "Regular GST",
        "R_TER": "Regular Total",

        "D_BER": "Direct Base TER",
        "D_BrokerageCost": "Direct 52(6A)(B)",
        "D_TransactionCost": "Direct 52(6A)(C)",
        "D_StatutoryLevies": "Direct GST",
        "D_TER": "Direct Total",

        "Scheme_Name": "Scheme Name"
    }
    df.rename(columns=rename_map, inplace=True)

    return df


def parse_target_date(argv):
    if len(argv) <= 1:
        return datetime.datetime.today()
    date_str = argv[1]
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m-%Y"):
        try:
            return datetime.datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {date_str!r}. Use YYYY-MM-DD, DD-MM-YYYY, or MM-YYYY.")


def main():
    target_date = parse_target_date(sys.argv)
    month = target_date.strftime("%m-%Y")
    fin_year = f"{target_date.year}-{target_date.year + 1}" if target_date.month >= 4 else f"{target_date.year - 1}-{target_date.year}"

    print(f"📅 Target Month: {month}")
    print(f"📅 Financial Year: {fin_year}")
    print(f"📥 Fetching TER data...\n")

    all_data = []

    for nav_id, categories in ter_scheme_type_and_category_dict.items():
        scheme_type = ter_scheme_type_dict.get(nav_id, "Unknown")
        print(f"➡️ Fetching for Scheme Type: {scheme_type} (NAV_ID: {nav_id})")
        for cat in categories:
            print(f"  ➡️ Fetching: {cat} - {scheme_category_dict.get(cat, 'Unknown')}")
            df = fetch_ter_data(month, fin_year, cat, nav_id)
            if not df.empty:
                all_data.append(df)
            time.sleep(1)

    if not all_data:
        print("❌ No data downloaded.")
        return

    final_df = pd.concat(all_data, ignore_index=True)

    cols = [
        "AMC_NAME", "Scheme Name", "SchemeCat_Name", "SchemeCat_Desc",
        "Scheme Type (Clean)", "SchemeType_Desc",
        "Regular Base TER",
        "Regular 52(6A)(B)",
        "Regular 52(6A)(C)",
        "Regular GST",
        "Regular Total",
        "Direct Base TER",
        "Direct 52(6A)(B)",
        "Direct 52(6A)(C)",
        "Direct GST",
        "Direct Total",
        "TER Date", "Date", "MF_ID", "NAV_ID"
    ]
    final_df = final_df[[c for c in cols if c in final_df.columns]]

    filename = "ter_of_mf_performance.xlsx"
    final_df.to_excel(filename, index=False)
    print(f"\n✅ Saved {len(final_df)} records → {filename}")


if __name__ == "__main__":
    main()
