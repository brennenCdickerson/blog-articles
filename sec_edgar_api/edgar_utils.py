import requests
from datetime import *
import json

headers = {"User-Agent" : "[Your email address here]"}

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


def get_form_list(all_submissions, form_type="10-K"):
    form_list = [accession_num for accession_num, form
                 in zip(all_submissions["filings"]["recent"]["accessionNumber"], all_submissions["filings"]["recent"]["form"])
                 if form == form_type]
    return form_list


def get_concept(cik, tag):
    full_concept = requests.get(
        f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{tag}.json",
        headers=headers
        ).json()
    return full_concept


def get_facts(cik):
    facts = requests.get(
        f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json",
        headers=headers
        ).json()
    return facts


def handle_duplicates(concept, allow_date_duplicates=False):
    processed_concept = []
    for unit in concept["units"]:
        if allow_date_duplicates:
            duplicate_tracker = []
            for fact in concept["units"][unit]:
                temp = {fact["end"], fact["val"]} 
                if temp not in duplicate_tracker:
                    processed_concept.append(fact)
                    duplicate_tracker.append(temp)
        else:
            processed_concept = [fact for fact in concept["units"][unit] if "frame" in fact]
    return processed_concept


# Will only work on income statement concepts, as only income statement concepts have start and end keys.
def find_start_end_diff(data):
    count = 0
    for fact in data:
        period_start = datetime.strptime(fact["start"], "%Y-%m-%d")
        period_end = datetime.strptime(fact["end"], "%Y-%m-%d")
        diff = period_end - period_start
        if diff.days > 121 and diff.days < 335:
            count += 1
    return count

# Another helper for testing.
def count_time_period_dupl(data, type="income"):
    tracker = []
    count = 0
    for fact in data:
        if type == "income":
            temp = {fact["start"], fact["end"]}
        else:
            temp = fact["end"]
        if temp not in tracker:
            tracker.append(temp)
        else:
            count += 1
    return count
