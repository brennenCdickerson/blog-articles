import requests


headers = {"User-Agent" : "YOUR INFORMATION"}


def get_tickers_dict(headers):
    company_tickers = requests.get(
        "https://www.sec.gov/files/company_tickers.json", headers=headers
    ).json()
    return company_tickers


def company_search():
    searching = True
    while searching:
        company_name = input("Provide a Company Name: ").upper()
        search_results = []
        for company in tickers.values():
            if company_name in company["title"].upper():
                d = {"title": company["title"], "cik": str(company["cik_str"]).zfill(10)}
                if d not in search_results:
                    search_results.append(d)
            else:
                searching = False
                print("No matches found.")
                return
        if len(search_results) > 1:
            print(f"Multiple matches, re-enter from the following list {search_results}")
        else:
            searching = False
            return search_results[0]["cik"]


tickers = get_tickers_dict(headers)
