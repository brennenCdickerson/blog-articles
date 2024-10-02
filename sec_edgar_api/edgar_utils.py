import requests


headers = {"User-Agent" : "PLACEHOLDER"}


def get_tickers_dict():
    company_tickers = requests.get(
        "https://www.sec.gov/files/company_tickers.json", headers=headers
    ).json()
    return company_tickers


def company_search(tickers):
    searching = True
    while searching:
        company_name = input("Provide a Company Name: ").upper()
        search_results = []
        for company in tickers.values():
            if company_name in company["title"].upper():
                d = {"title": company["title"], "cik": str(company["cik_str"]).zfill(10)}
                if d not in search_results:
                    search_results.append(d)
        if len(search_results) == 1:
            return search_results[0]["cik"]
        elif len(search_results) > 1:
            print(f"Multiple possible matches, re-enter from the following list: {search_results}")
        else:
            print("No matches found.")
            return


def get_submissions(cik):
    company_submissions = requests.get(
        f"https://data.sec.gov/submissions/CIK{cik}.json", headers=headers
    ).json()
    return company_submissions

