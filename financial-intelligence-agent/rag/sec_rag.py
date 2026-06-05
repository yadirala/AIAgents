import requests
import os
from gateway.llm_gateway import call_llm
import json
from edgar import Company
import re
from bs4 import BeautifulSoup

def fetch_sec_filing(cik):
    headers = {"User-Agent": "yashwanthadirala@gmail.com"}
    
    # get filing metadata
    url = f"https://data.sec.gov/submissions/CIK{str(cik).zfill(10)}.json"
    data = requests.get(url, headers=headers).json()
    
    filings = data["filings"]["recent"]
    for i, form in enumerate(filings["form"]):
        if form == "10-K":
            accession = filings["accessionNumber"][i].replace("-", "")
            primary = filings["primaryDocument"][i]
            # correct URL format
            filing_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{primary}"
            response = requests.get(filing_url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            return soup.get_text()[:8000]
    
    raise ValueError(f"No 10-K found")

def get_cik(ticker):
    """Get the CIK for a given ticker symbol."""
    headers = {"User-Agent": "yashwanthadirala@gmail.com"}
    url = f"https://www.sec.gov/files/company_tickers.json"
    response = requests.get(url, headers=headers)
    data = response.json()

    for item in data.values():
        if item["ticker"] == ticker.upper():
            return item["cik_str"]

    raise ValueError(f"CIK not found for ticker: {ticker}")

def build_index(filing_content, ticker):
    if os.path.exists(f"{ticker}_index.json"):
        with open(f"{ticker}_index.json", "r") as f:
            return json.load(f)
    
    response = call_llm([
        {"role": "system", "content": "You are a financial analyst. Return ONLY valid JSON, no other text. Build a JSON index with sections like Business Overview, Risk Factors, Financial Data, Management Discussion with brief summaries."},
        {"role": "user", "content": filing_content[:8000]}
    ])
    
    try:
        index = json.loads(response)
    except json.JSONDecodeError:
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            index = json.loads(json_match.group())
        else:
            index = {"raw_summary": response}
    
    with open(f"{ticker}_index.json", "w") as f:
        json.dump(index, f)
    
    return index
    
    
    